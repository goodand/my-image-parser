#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class ToolAvailability:
    soffice: bool
    pdftoppm: bool
    xcrun: bool


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text())


def media_record(job_name: str, source_filename: str, item: dict) -> dict:
    metadata = item.get("embedded_metadata", {})
    slide_numbers = [usage["slide"] for usage in item.get("slide_usages", [])]
    return {
        "image_id": f"{job_name}:{item['file']}",
        "source_filename": source_filename,
        "source_pptx": item.get("source_pptx"),
        "extraction_method": "ppt_media_extract",
        "image_path": item["output_path"],
        "source_zip_path": item["source_zip_path"],
        "slide_numbers": slide_numbers,
        "extension": item["extension"],
        "bytes": item["bytes"],
        "sha256": item["sha256"],
        "image_width": metadata.get("ImageWidth"),
        "image_height": metadata.get("ImageHeight"),
        "mime_type": metadata.get("MIMEType"),
    }


def tool_availability() -> ToolAvailability:
    return ToolAvailability(
        soffice=shutil.which("soffice") is not None,
        pdftoppm=shutil.which("pdftoppm") is not None,
        xcrun=shutil.which("xcrun") is not None,
    )


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def write_jsonl(path: Path, rows: List[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def build_dataset(manifest_path: Path, output_root: Path, availability: ToolAvailability) -> Path:
    manifest = load_manifest(manifest_path)
    job_name = manifest_path.parent.name
    source_filename = manifest["source_filename"]
    dataset_dir = output_root / job_name
    openai_dir = dataset_dir / "openai_api"
    screenshot_dir = dataset_dir / "slide_screenshots"
    simctl_screenshot_dir = dataset_dir / "slide_screenshots_simctl"
    media_dataset_path = openai_dir / "media_extract_dataset.jsonl"

    rows = [
        media_record(job_name, source_filename, item)
        | {"source_pptx": manifest["source_pptx"]}
        for item in manifest.get("exported_images", [])
    ]
    write_jsonl(media_dataset_path, rows)

    screenshot_dir.mkdir(parents=True, exist_ok=True)
    simctl_screenshot_dir.mkdir(parents=True, exist_ok=True)
    screenshot_status = "ready" if availability.soffice and availability.pdftoppm else "pending_setup"
    simctl_status = "viewer_surface_required" if availability.xcrun else "pending_setup"
    dataset_manifest = {
        "job_name": job_name,
        "source_pptx": manifest["source_pptx"],
        "source_filename": source_filename,
        "cross_validation_methods": {
            "openai_api_on_media_extract": {
                "status": "ready",
                "dataset_path": str(media_dataset_path.resolve()),
                "image_count": len(rows),
                "notes": "Use these extracted media images as direct OpenAI API caption inputs.",
            },
            "current_local_extract": {
                "status": "ready",
                "manifest_path": str(manifest_path.resolve()),
                "media_dir": str((manifest_path.parent / "media").resolve()),
                "image_count": manifest["summary"]["exported_image_count"],
                "notes": "Local PPTX media extraction plus embedded metadata manifest.",
            },
            "slide_screenshot_then_openai_api": {
                "status": screenshot_status,
                "planned_screenshot_dir": str(screenshot_dir.resolve()),
                "required_commands": ["soffice", "pdftoppm"],
                "available_commands": {
                    "soffice": availability.soffice,
                    "pdftoppm": availability.pdftoppm,
                },
                "notes": "Per-slide screenshot generation is blocked until both conversion tools are installed.",
            },
            "slide_screenshot_then_openai_api_via_simctl": {
                "status": simctl_status,
                "planned_screenshot_dir": str(simctl_screenshot_dir.resolve()),
                "required_commands": ["xcrun", "simctl"],
                "available_commands": {
                    "xcrun": availability.xcrun,
                },
                "notes": "simctl screenshot is available, but a simulator-visible slide viewer surface is still required before capture.",
            },
        },
    }
    dataset_manifest_path = dataset_dir / "cross_validation_manifest.json"
    write_json(dataset_manifest_path, dataset_manifest)
    return dataset_manifest_path


def main() -> int:
    manifest_paths = sorted(Path("control/project_domain/resources/pptx_jobs").glob("*/manifest.json"))
    if not manifest_paths:
        raise SystemExit(
            "No PPTX extraction manifests found in control/project_domain/resources/pptx_jobs."
        )
    availability = tool_availability()
    output_root = Path("control/project_domain/resources/cross_validation")
    written = [build_dataset(path, output_root, availability) for path in manifest_paths]
    index = {
        "jobs": [str(path.resolve()) for path in written],
        "tool_availability": {
            "soffice": availability.soffice,
            "pdftoppm": availability.pdftoppm,
            "xcrun": availability.xcrun,
        },
    }
    write_json(output_root / "index.json", index)
    for path in written:
        print(path.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
