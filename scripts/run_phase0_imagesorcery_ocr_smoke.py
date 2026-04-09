#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import json
import math
import os
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
IMAGESORCERY_DIR = ROOT_DIR / "vendor" / "mcp" / "imagesorcery-mcp"
MACOS_OCR_VENV_PYTHON = ROOT_DIR / "vendor" / "mcp" / "macos-ocr-mcp" / ".venv" / "bin" / "python"
MACOS_OCR_MAIN = ROOT_DIR / "vendor" / "mcp" / "macos-ocr-mcp" / "main.py"
YOLO_CONFIG_DIR = ROOT_DIR / "logs" / "imagesorcery" / "ultralytics"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a bounded phase0 smoke: ImageSorcery find/detect, crop/fill, OCR, and context package build."
    )
    parser.add_argument("--image-path", required=True, help="Absolute path to the source image.")
    parser.add_argument("--label", required=True, help="Case label used for output paths.")
    parser.add_argument("--find-description", required=True, help="Text prompt for ImageSorcery find().")
    parser.add_argument(
        "--output-root",
        default=str(ROOT_DIR / "control" / "project_domain" / "runs" / "object_isolation" / "phase0_smoke"),
        help="Directory where smoke outputs should be written.",
    )
    parser.add_argument(
        "--find-model",
        default="yoloe-11s-seg.pt",
        help="Text-prompt model for find(). Must support segmentation.",
    )
    parser.add_argument(
        "--detect-model",
        default="yoloe-11s-seg-pf.pt",
        help="Segmentation model for detect().",
    )
    parser.add_argument("--confidence", type=float, default=0.25, help="Confidence threshold for detect/find().")
    parser.add_argument(
        "--context-note",
        default="",
        help="Optional note to include in the generated context package.",
    )
    return parser.parse_args()


def _ensure_runtime() -> None:
    if not IMAGESORCERY_DIR.is_dir():
        raise RuntimeError(f"Missing ImageSorcery vendor directory: {IMAGESORCERY_DIR}")
    if not MACOS_OCR_VENV_PYTHON.is_file():
        raise RuntimeError(f"Missing macOS OCR python runtime: {MACOS_OCR_VENV_PYTHON}")
    if not MACOS_OCR_MAIN.is_file():
        raise RuntimeError(f"Missing macOS OCR entrypoint: {MACOS_OCR_MAIN}")

    imagesorcery_site_packages = next((IMAGESORCERY_DIR / ".venv" / "lib").glob("python*/site-packages"), None)
    if imagesorcery_site_packages is None:
        raise RuntimeError("Could not locate ImageSorcery site-packages directory.")

    sys.path.insert(0, str(IMAGESORCERY_DIR / "src"))
    sys.path.insert(0, str(imagesorcery_site_packages))

    YOLO_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    os.environ["YOLO_CONFIG_DIR"] = str(YOLO_CONFIG_DIR)


@contextmanager
def _pushd(path: Path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def _load_existing_caption(image_path: Path) -> dict[str, Any] | None:
    jobs_dir = ROOT_DIR / "control" / "project_agent_ops" / "registry" / "runs" / "image_caption_jobs"
    preferred_prefixes = ("phase1_ppt", "phase1_smoke", "phase1_caption_10w")
    target_path = image_path.resolve()
    for prefix in preferred_prefixes:
        for candidate in sorted(jobs_dir.glob(f"{prefix}*.json")):
            payload = json.loads(candidate.read_text())
            for record in payload.get("records", []):
                record_path_text = record.get("path")
                if not record_path_text:
                    continue
                try:
                    record_path = Path(record_path_text).resolve()
                    same_path = record_path == target_path or record_path.samefile(target_path)
                except Exception:
                    same_path = Path(record_path_text).name == image_path.name
                if same_path:
                    return {
                        "job_file": str(candidate),
                        "caption": record.get("caption"),
                        "alt_text": record.get("alt_text"),
                        "status": record.get("status"),
                        "source_context": record.get("source_context"),
                    }
    return None


def _bbox_to_ints(bbox: list[float], width: int, height: int) -> list[int]:
    x1, y1, x2, y2 = bbox
    return [
        max(0, min(width, math.floor(x1))),
        max(0, min(height, math.floor(y1))),
        max(0, min(width, math.ceil(x2))),
        max(0, min(height, math.ceil(y2))),
    ]


def _tool_result_data(result: Any) -> Any:
    structured = getattr(result, "structured_content", None)
    if structured is not None:
        return structured
    data = getattr(result, "data", None)
    if isinstance(data, list) and len(data) == 1:
        item = data[0]
        text = getattr(item, "text", None)
        if text is not None:
            return text
    return data


def _run_ocr(file_path: Path) -> dict[str, Any]:
    code = (
        "import asyncio, importlib.util, json, sys; "
        "spec = importlib.util.spec_from_file_location('macos_ocr_main', sys.argv[1]); "
        "module = importlib.util.module_from_spec(spec); "
        "spec.loader.exec_module(module); "
        "result = asyncio.run(module.ocr_image(sys.argv[2])); "
        "print(json.dumps(result, ensure_ascii=False))"
    )
    completed = subprocess.run(
        [str(MACOS_OCR_VENV_PYTHON), "-c", code, str(MACOS_OCR_MAIN), str(file_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return {
            "error": f"macOS OCR subprocess failed with exit {completed.returncode}",
            "stderr": completed.stderr.strip(),
        }
    stdout = completed.stdout.strip()
    if not stdout:
        return {"error": "macOS OCR subprocess returned empty stdout."}
    try:
        return json.loads(stdout)
    except json.JSONDecodeError as exc:
        return {
            "error": f"macOS OCR subprocess returned invalid JSON: {exc}",
            "stdout": stdout,
            "stderr": completed.stderr.strip(),
        }


def _select_best_source(ocr_results: dict[str, dict[str, Any]]) -> dict[str, Any]:
    best_name = None
    best_score = -1
    for name, payload in ocr_results.items():
        if payload.get("error"):
            continue
        text = payload.get("full_text") or ""
        score = len(text.strip())
        if score > best_score:
            best_score = score
            best_name = name
    if best_name is None:
        return {"selected_source": None, "selected_text": None}
    return {
        "selected_source": best_name,
        "selected_text": ocr_results[best_name].get("full_text"),
    }


def _bbox_area(bbox: list[float]) -> float:
    x1, y1, x2, y2 = bbox
    return max(0.0, x2 - x1) * max(0.0, y2 - y1)


def _bbox_iou(a: list[float], b: list[float]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)
    inter_area = _bbox_area([inter_x1, inter_y1, inter_x2, inter_y2])
    if inter_area <= 0:
        return 0.0
    union = _bbox_area(a) + _bbox_area(b) - inter_area
    if union <= 0:
        return 0.0
    return inter_area / union


async def _run_smoke(args: argparse.Namespace) -> dict[str, Any]:
    _ensure_runtime()

    from PIL import Image
    from fastmcp import Client
    from imagesorcery_mcp.server import mcp as imagesorcery_server

    image_path = Path(args.image_path).resolve()
    if not image_path.is_file():
        raise FileNotFoundError(f"Input image not found: {image_path}")

    output_root = Path(args.output_root).resolve() / args.label
    output_root.mkdir(parents=True, exist_ok=True)

    crop_path = output_root / f"{args.label}_crop.png"
    isolated_path = output_root / f"{args.label}_isolated.png"
    result_path = output_root / f"{args.label}_result.json"

    with Image.open(image_path) as image:
        image_width, image_height = image.size

    baseline_caption = _load_existing_caption(image_path)

    with _pushd(IMAGESORCERY_DIR):
        async with Client(imagesorcery_server) as client:
            detect_result = await client.call_tool(
                "detect",
                {
                    "input_path": str(image_path),
                    "model_name": args.detect_model,
                    "confidence": args.confidence,
                    "return_geometry": True,
                    "geometry_format": "polygon",
                },
            )
            detect_payload = _tool_result_data(detect_result)

            find_result = await client.call_tool(
                "find",
                {
                    "input_path": str(image_path),
                    "description": args.find_description,
                    "model_name": args.find_model,
                    "confidence": args.confidence,
                    "return_all_matches": True,
                    "return_geometry": False,
                },
            )
            find_payload = _tool_result_data(find_result)

            selection_method = None
            selection = None
            geometry_source = None

            found_objects = find_payload.get("found_objects", []) if isinstance(find_payload, dict) else []
            detections = detect_payload.get("detections", []) if isinstance(detect_payload, dict) else []
            if found_objects:
                selection_method = "find"
                selection = max(found_objects, key=lambda item: item.get("confidence", 0.0))
                if detections:
                    geometry_source = max(
                        detections,
                        key=lambda item: _bbox_iou(item.get("bbox", [0, 0, 0, 0]), selection.get("bbox", [0, 0, 0, 0])),
                    )
            else:
                if detections:
                    selection_method = "detect"
                    selection = max(detections, key=lambda item: item.get("confidence", 0.0))
                    geometry_source = selection

            if selection is None:
                summary = {
                    "label": args.label,
                    "image_path": str(image_path),
                    "find_description": args.find_description,
                    "baseline_caption": baseline_caption,
                    "detect_result": detect_payload,
                    "find_result": find_payload,
                    "status": "no_selection",
                    "notes": [
                        "Neither find() nor detect() produced a usable component candidate.",
                    ],
                }
                result_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
                return summary

            bbox = _bbox_to_ints(selection["bbox"], image_width, image_height)

            crop_result = await client.call_tool(
                "crop",
                {
                    "input_path": str(image_path),
                    "x1": bbox[0],
                    "y1": bbox[1],
                    "x2": bbox[2],
                    "y2": bbox[3],
                    "output_path": str(crop_path),
                },
            )
            crop_payload = _tool_result_data(crop_result)

            area: dict[str, Any]
            if geometry_source and geometry_source.get("polygon"):
                area = {"polygon": geometry_source["polygon"], "color": None}
            elif geometry_source and geometry_source.get("mask_path"):
                area = {"mask_path": geometry_source["mask_path"], "color": None}
            else:
                area = {"x1": bbox[0], "y1": bbox[1], "x2": bbox[2], "y2": bbox[3], "color": None}

            fill_result = await client.call_tool(
                "fill",
                {
                    "input_path": str(image_path),
                    "areas": [area],
                    "invert_areas": True,
                    "output_path": str(isolated_path),
                },
            )
            fill_payload = _tool_result_data(fill_result)

    ocr_results = {
        "full_image": _run_ocr(image_path),
        "crop_image": _run_ocr(crop_path),
        "isolated_image": _run_ocr(isolated_path),
    }

    context_choice = _select_best_source(ocr_results)

    summary = {
        "label": args.label,
        "status": "completed",
        "image_path": str(image_path),
        "find_description": args.find_description,
        "baseline_caption": baseline_caption,
        "detect_result": detect_payload,
        "find_result": find_payload,
        "selection_method": selection_method,
        "selection": selection,
        "geometry_source": geometry_source,
        "bbox_int": bbox,
        "crop_output": crop_payload,
        "isolated_output": fill_payload,
        "ocr_results": ocr_results,
        "context_package": {
            "slides": (baseline_caption or {}).get("source_context", {}).get("slide_numbers"),
            "baseline_caption": (baseline_caption or {}).get("caption"),
            "baseline_alt_text": (baseline_caption or {}).get("alt_text"),
            "selected_ocr_source": context_choice["selected_source"],
            "selected_ocr_text": context_choice["selected_text"],
            "context_note": args.context_note or None,
        },
    }
    result_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


def main() -> None:
    args = _parse_args()
    summary = asyncio.run(_run_smoke(args))
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
