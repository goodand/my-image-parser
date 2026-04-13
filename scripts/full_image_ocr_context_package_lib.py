#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
PPTX_JOBS_DIR = ROOT_DIR / "control" / "project_domain" / "resources" / "pptx_jobs"
CAPTION_JOBS_DIR = Path(
    os.environ.get(
        "CAPTION_JOB_ROOT",
        str(ROOT_DIR / "control" / "project_agent_ops" / "registry" / "jobs" / "image_caption_jobs"),
    )
)
MACOS_OCR_DIR = Path(
    os.environ.get("MACOS_OCR_MCP_SERVER_DIR", str(ROOT_DIR / "vendor" / "mcp" / "macos-ocr-mcp"))
)
MACOS_OCR_MAIN = MACOS_OCR_DIR / "main.py"
DEFAULT_OUTPUT_ROOT = ROOT_DIR / "control" / "project_domain" / "resources" / "context_packages" / "full_image_ocr_baseline"
DEFAULT_MANIFEST_JSONL = ROOT_DIR / "control" / "project_domain" / "resources" / "manifests" / "phase0_full_image_ocr_context_package_manifest.jsonl"


@dataclass(frozen=True)
class ManifestRecord:
    dataset: str
    manifest_path: str
    source_pptx: str
    source_filename: str
    image_file: str
    source_zip_path: str | None
    output_path: str
    slide_numbers: list[int]
    sha256: str | None
    image_width: int | None
    image_height: int | None
    mime_type: str | None


@dataclass(frozen=True)
class CaptionRecord:
    job_file: str
    caption: str | None
    alt_text: str | None
    status: str | None
    source_context: dict[str, Any] | None


@dataclass(frozen=True)
class ContextPackage:
    image_id: str
    source_image_path: str
    source_dataset: str
    source_pptx: str | None
    source_slide_numbers: list[int]
    image_surface: str
    ocr_surface: str
    ocr_status: str
    ocr_engine: str | None
    ocr_annotation_count: int
    ocr_text_excerpt: str
    ocr_text_full_path: str
    ppt_local_summary: str
    context_package_markdown_path: str
    context_package_json_path: str
    review_status: str
    notes: list[str]
    source_filename: str | None = None
    source_zip_path: str | None = None
    sha256: str | None = None
    image_width: int | None = None
    image_height: int | None = None
    mime_type: str | None = None
    ocr_result_json_path: str | None = None
    baseline_caption: str | None = None
    baseline_alt_text: str | None = None
    ppt_provenance_context: dict[str, Any] | None = None
    ocr_evidence_context: dict[str, Any] | None = None


def _resolve_samefile(a: Path, b: Path) -> bool:
    try:
        return a.resolve() == b.resolve() or a.samefile(b)
    except Exception:
        return a.name == b.name


def resolve_macos_ocr_python() -> Path:
    override = os.environ.get("MACOS_OCR_PYTHON")
    candidates = []
    if override:
        candidates.append(Path(override))
    candidates.extend(
        [
            MACOS_OCR_DIR / ".venv" / "bin" / "python",
            MACOS_OCR_DIR / "venv" / "bin" / "python",
        ]
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return candidates[0]


def find_manifest_record(image_path: Path) -> ManifestRecord | None:
    target = image_path.resolve()
    direct_manifest = image_path.parent.parent / "manifest.json"
    manifest_paths: list[Path]
    if direct_manifest.is_file():
        manifest_paths = [direct_manifest]
    else:
        manifest_paths = sorted(PPTX_JOBS_DIR.glob("*/manifest.json"))

    for manifest_path in manifest_paths:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        dataset = manifest_path.parent.name
        source_pptx = payload.get("source_pptx")
        source_filename = payload.get("source_filename")
        for item in payload.get("exported_images", []):
            output_path_text = item.get("output_path")
            if not output_path_text:
                continue
            candidate = Path(output_path_text)
            if not _resolve_samefile(candidate, target):
                continue
            embedded = item.get("embedded_metadata", {})
            slide_numbers = [entry.get("slide") for entry in item.get("slide_usages", []) if entry.get("slide") is not None]
            return ManifestRecord(
                dataset=dataset,
                manifest_path=str(manifest_path.resolve()),
                source_pptx=source_pptx,
                source_filename=source_filename,
                image_file=item.get("file", image_path.name),
                source_zip_path=item.get("source_zip_path"),
                output_path=str(candidate.resolve()),
                slide_numbers=slide_numbers,
                sha256=item.get("sha256"),
                image_width=embedded.get("ImageWidth"),
                image_height=embedded.get("ImageHeight"),
                mime_type=embedded.get("MIMEType"),
            )
    return None


def load_caption_record(image_path: Path) -> CaptionRecord | None:
    target = image_path.resolve()
    if not CAPTION_JOBS_DIR.is_dir():
        return None
    for candidate in sorted(CAPTION_JOBS_DIR.glob("*.json")):
        try:
            payload = json.loads(candidate.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        for record in payload.get("records", []):
            record_path_text = record.get("path")
            if not record_path_text:
                continue
            if not _resolve_samefile(Path(record_path_text), target):
                continue
            return CaptionRecord(
                job_file=str(candidate.resolve()),
                caption=record.get("caption"),
                alt_text=record.get("alt_text"),
                status=record.get("status"),
                source_context=record.get("source_context"),
            )
    return None


def run_full_image_ocr(image_path: Path) -> dict[str, Any]:
    macos_ocr_python = resolve_macos_ocr_python()
    if not macos_ocr_python.is_file():
        raise RuntimeError(f"Missing macOS OCR python runtime: {macos_ocr_python}")
    if not MACOS_OCR_MAIN.is_file():
        raise RuntimeError(f"Missing macOS OCR main module: {MACOS_OCR_MAIN}")

    code = (
        "import asyncio, importlib.util, json, sys; "
        "spec = importlib.util.spec_from_file_location('macos_ocr_main', sys.argv[1]); "
        "module = importlib.util.module_from_spec(spec); "
        "spec.loader.exec_module(module); "
        "result = asyncio.run(module.ocr_image(sys.argv[2])); "
        "print(json.dumps(result, ensure_ascii=False))"
    )
    completed = subprocess.run(
        [str(macos_ocr_python), "-c", code, str(MACOS_OCR_MAIN), str(image_path)],
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


def determine_ocr_status(ocr_result: dict[str, Any]) -> str:
    if ocr_result.get("error"):
        return "error"
    full_text = (ocr_result.get("full_text") or "").strip()
    annotation_count = int(ocr_result.get("annotation_count") or 0)
    if not full_text or annotation_count <= 0:
        return "no_text"
    if annotation_count <= 2 or len(full_text) < 16:
        return "weak_text"
    return "usable"


def determine_review_status(ocr_status: str) -> str:
    if ocr_status == "usable":
        return "pending_review"
    if ocr_status in {"weak_text", "no_text"}:
        return "needs_more_context"
    return "rejected"


def build_ocr_text_excerpt(ocr_result: dict[str, Any], max_chars: int = 400) -> str:
    text = " ".join((ocr_result.get("full_text") or "").split())
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "…"


def build_ppt_provenance_context(
    *,
    image_path: Path,
    manifest_record: ManifestRecord | None,
    caption_record: CaptionRecord | None,
) -> dict[str, Any]:
    if manifest_record is None:
        return {
            "source_kind": "ppt_manifest_fallback",
            "source_dataset": image_path.parent.parent.name,
            "source_manifest_path": None,
            "source_pptx": None,
            "source_filename": None,
            "source_slide_numbers": [],
            "source_image_file": image_path.name,
            "source_zip_path": None,
            "sha256": None,
            "image_width": None,
            "image_height": None,
            "mime_type": None,
            "baseline_caption": caption_record.caption if caption_record else None,
            "baseline_alt_text": caption_record.alt_text if caption_record else None,
        }
    return {
        "source_kind": "ppt_export_manifest",
        "source_dataset": manifest_record.dataset,
        "source_manifest_path": manifest_record.manifest_path,
        "source_pptx": manifest_record.source_pptx,
        "source_filename": manifest_record.source_filename,
        "source_slide_numbers": manifest_record.slide_numbers,
        "source_image_file": manifest_record.image_file,
        "source_zip_path": manifest_record.source_zip_path,
        "sha256": manifest_record.sha256,
        "image_width": manifest_record.image_width,
        "image_height": manifest_record.image_height,
        "mime_type": manifest_record.mime_type,
        "baseline_caption": caption_record.caption if caption_record else None,
        "baseline_alt_text": caption_record.alt_text if caption_record else None,
    }


def build_ppt_provenance_context_from_package(package: dict[str, Any]) -> dict[str, Any]:
    existing = package.get("ppt_provenance_context")
    if isinstance(existing, dict) and existing:
        return dict(existing)
    return {
        "source_kind": "ppt_export_manifest" if package.get("source_pptx") else "ppt_manifest_fallback",
        "source_dataset": package.get("source_dataset"),
        "source_manifest_path": package.get("source_manifest_path"),
        "source_pptx": package.get("source_pptx"),
        "source_filename": package.get("source_filename"),
        "source_slide_numbers": list(package.get("source_slide_numbers") or []),
        "source_image_file": Path(str(package.get("source_image_path") or "")).name or None,
        "source_zip_path": package.get("source_zip_path"),
        "sha256": package.get("sha256"),
        "image_width": package.get("image_width"),
        "image_height": package.get("image_height"),
        "mime_type": package.get("mime_type"),
        "baseline_caption": package.get("baseline_caption"),
        "baseline_alt_text": package.get("baseline_alt_text"),
    }


def build_ocr_evidence_context(
    *,
    ocr_result: dict[str, Any],
    ocr_status: str,
    ocr_surface: str,
    ocr_text_excerpt: str,
    ocr_text_full_path: str,
    ocr_result_json_path: str | None,
    selected_text_evidence: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "source_kind": "ocr_evidence",
        "ocr_surface": ocr_surface,
        "ocr_status": ocr_status,
        "ocr_engine": ocr_result.get("engine"),
        "ocr_annotation_count": int(ocr_result.get("annotation_count") or 0),
        "ocr_text_excerpt": ocr_text_excerpt,
        "ocr_text_full_path": ocr_text_full_path,
        "ocr_result_json_path": ocr_result_json_path,
        "selected_text_evidence": list(selected_text_evidence or []),
    }


def build_ocr_evidence_context_from_package(
    package: dict[str, Any],
    *,
    selected_text_evidence: list[str] | None = None,
    comparison_against_full_image: dict[str, Any] | None = None,
) -> dict[str, Any]:
    existing = dict(package.get("ocr_evidence_context") or {})
    existing.update(
        {
            "source_kind": "ocr_evidence",
            "ocr_surface": package.get("ocr_surface"),
            "ocr_status": package.get("ocr_status"),
            "ocr_engine": package.get("ocr_engine"),
            "ocr_annotation_count": int(package.get("ocr_annotation_count") or 0),
            "ocr_text_excerpt": package.get("ocr_text_excerpt"),
            "ocr_text_full_path": package.get("ocr_text_full_path"),
            "ocr_result_json_path": package.get("ocr_result_json_path"),
            "selected_text_evidence": list(
                selected_text_evidence
                if selected_text_evidence is not None
                else package.get("selected_text_evidence") or []
            ),
        }
    )
    if comparison_against_full_image is not None:
        existing["comparison_against_full_image"] = comparison_against_full_image
    return existing


def build_ppt_local_summary(
    image_path: Path,
    manifest_record: ManifestRecord | None,
    caption_record: CaptionRecord | None,
) -> str:
    if manifest_record is None:
        parts = [
            f"Extracted image file `{image_path.name}`.",
            "No matching PPT extraction manifest was found in `resources/pptx_jobs/`.",
        ]
    else:
        slide_text = ", ".join(str(item) for item in manifest_record.slide_numbers) or "unknown"
        parts = [
            f"Source PPT: `{manifest_record.source_filename}`.",
            f"Dataset: `{manifest_record.dataset}`.",
            f"Slides: {slide_text}.",
            f"Extracted media file: `{manifest_record.image_file}` from `{manifest_record.source_zip_path}`."
            if manifest_record.source_zip_path
            else f"Extracted media file: `{manifest_record.image_file}`.",
        ]
    if caption_record and caption_record.caption:
        parts.append(f"Existing phase-1 caption: {caption_record.caption}")
    elif caption_record and caption_record.alt_text:
        parts.append(f"Existing phase-1 alt text: {caption_record.alt_text}")
    return " ".join(parts)


def render_context_package_markdown(package: ContextPackage) -> str:
    notes = package.notes or ["n/a"]
    slides = ", ".join(str(item) for item in package.source_slide_numbers) or "n/a"
    ppt_provenance_context = package.ppt_provenance_context or {}
    ocr_evidence_context = package.ocr_evidence_context or {}
    lines = [
        "# Context Package",
        "",
        "## Source",
        "",
        f"- image_id: `{package.image_id}`",
        f"- source_image_path: `{package.source_image_path}`",
        f"- source_dataset: `{package.source_dataset}`",
        f"- source_pptx: `{package.source_pptx or 'n/a'}`",
        f"- source_slide_numbers: `{slides}`",
        f"- image_surface: `{package.image_surface}`",
        f"- ocr_surface: `{package.ocr_surface}`",
        "",
        "## PPT Provenance Context",
        "",
        f"- source_kind: `{ppt_provenance_context.get('source_kind') or 'n/a'}`",
        f"- source_manifest_path: `{ppt_provenance_context.get('source_manifest_path') or 'n/a'}`",
        f"- source_image_file: `{ppt_provenance_context.get('source_image_file') or 'n/a'}`",
        "",
        "## OCR Evidence Context",
        "",
        f"- ocr_status: `{ocr_evidence_context.get('ocr_status') or package.ocr_status}`",
        f"- ocr_engine: `{ocr_evidence_context.get('ocr_engine') or package.ocr_engine or 'n/a'}`",
        f"- ocr_annotation_count: `{ocr_evidence_context.get('ocr_annotation_count') or package.ocr_annotation_count}`",
        f"- ocr_text_full_path: `{ocr_evidence_context.get('ocr_text_full_path') or package.ocr_text_full_path}`",
        f"- ocr_result_json_path: `{ocr_evidence_context.get('ocr_result_json_path') or package.ocr_result_json_path or 'n/a'}`",
        "",
        "### OCR Excerpt",
        "",
        package.ocr_text_excerpt or "_empty_",
        "",
        "## PPT-Local Summary",
        "",
        package.ppt_local_summary or "_empty_",
        "",
        "## Existing Baseline Caption",
        "",
        package.baseline_caption or "_none_",
        "",
        "## Existing Baseline Alt Text",
        "",
        package.baseline_alt_text or "_none_",
        "",
        "## Review",
        "",
        f"- review_status: `{package.review_status}`",
        "",
        "## Notes",
        "",
    ]
    for note in notes:
        lines.append(f"- {note}")
    return "\n".join(lines).rstrip() + "\n"


def _json_default(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def _write_jsonl_replace(path: Path, row: dict[str, Any], key_field: str) -> None:
    rows: list[dict[str, Any]] = []
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            rows.append(json.loads(stripped))
    replaced = False
    for idx, existing in enumerate(rows):
        if existing.get(key_field) == row.get(key_field):
            rows[idx] = row
            replaced = True
            break
    if not replaced:
        rows.append(row)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(item, ensure_ascii=False, default=_json_default) + "\n" for item in rows),
        encoding="utf-8",
    )


def build_context_package(
    image_path: Path,
    output_root: Path = DEFAULT_OUTPUT_ROOT,
    ocr_result: dict[str, Any] | None = None,
    ppt_local_summary_override: str | None = None,
    extra_notes: list[str] | None = None,
) -> tuple[ContextPackage, dict[str, Path]]:
    image_path = image_path.resolve()
    if not image_path.is_file():
        raise FileNotFoundError(f"Input image not found: {image_path}")

    manifest_record = find_manifest_record(image_path)
    caption_record = load_caption_record(image_path)
    if ocr_result is None:
        ocr_result = run_full_image_ocr(image_path)

    if manifest_record is not None:
        image_id = f"{manifest_record.dataset}:{manifest_record.image_file}"
        dataset = manifest_record.dataset
        source_pptx = manifest_record.source_pptx
        slide_numbers = manifest_record.slide_numbers
        source_filename = manifest_record.source_filename
        source_zip_path = manifest_record.source_zip_path
        sha256 = manifest_record.sha256
        image_width = manifest_record.image_width
        image_height = manifest_record.image_height
        mime_type = manifest_record.mime_type
    else:
        dataset = image_path.parent.parent.name
        image_id = f"{dataset}:{image_path.name}"
        source_pptx = None
        slide_numbers = []
        source_filename = None
        source_zip_path = None
        sha256 = None
        image_width = None
        image_height = None
        mime_type = None

    safe_image_stem = image_path.stem.replace(" ", "_")
    package_dir = output_root.resolve() / dataset / safe_image_stem
    package_dir.mkdir(parents=True, exist_ok=True)
    ocr_result_json_path = package_dir / "OCR_RESULT.json"
    ocr_text_full_path = package_dir / "OCR_FULL_TEXT.txt"
    context_package_json_path = package_dir / "CONTEXT_PACKAGE.json"
    context_package_markdown_path = package_dir / "CONTEXT_PACKAGE.md"

    ocr_status = determine_ocr_status(ocr_result)
    review_status = determine_review_status(ocr_status)
    ppt_local_summary = ppt_local_summary_override or build_ppt_local_summary(image_path, manifest_record, caption_record)
    notes = list(extra_notes or [])
    if manifest_record is None:
        notes.append("No matching PPT extraction manifest was found; package uses fallback dataset inference.")
    if ocr_result.get("error"):
        notes.append(f"OCR error: {ocr_result['error']}")

    baseline_caption = caption_record.caption if caption_record else None
    baseline_alt_text = caption_record.alt_text if caption_record else None
    ocr_text_excerpt = build_ocr_text_excerpt(ocr_result)

    package = ContextPackage(
        image_id=image_id,
        source_image_path=str(image_path),
        source_dataset=dataset,
        source_pptx=source_pptx,
        source_slide_numbers=slide_numbers,
        image_surface="full_image_original",
        ocr_surface="full_image_standalone_ocr",
        ocr_status=ocr_status,
        ocr_engine=ocr_result.get("engine"),
        ocr_annotation_count=int(ocr_result.get("annotation_count") or 0),
        ocr_text_excerpt=ocr_text_excerpt,
        ocr_text_full_path=str(ocr_text_full_path),
        ppt_local_summary=ppt_local_summary,
        context_package_markdown_path=str(context_package_markdown_path),
        context_package_json_path=str(context_package_json_path),
        review_status=review_status,
        notes=notes,
        source_filename=source_filename,
        source_zip_path=source_zip_path,
        sha256=sha256,
        image_width=image_width,
        image_height=image_height,
        mime_type=mime_type,
        ocr_result_json_path=str(ocr_result_json_path),
        baseline_caption=baseline_caption,
        baseline_alt_text=baseline_alt_text,
        ppt_provenance_context=build_ppt_provenance_context(
            image_path=image_path,
            manifest_record=manifest_record,
            caption_record=caption_record,
        ),
        ocr_evidence_context=build_ocr_evidence_context(
            ocr_result=ocr_result,
            ocr_status=ocr_status,
            ocr_surface="full_image_standalone_ocr",
            ocr_text_excerpt=ocr_text_excerpt,
            ocr_text_full_path=str(ocr_text_full_path),
            ocr_result_json_path=str(ocr_result_json_path),
        ),
    )

    ocr_result_json_path.write_text(json.dumps(ocr_result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ocr_text_full_path.write_text((ocr_result.get("full_text") or "") + "\n", encoding="utf-8")
    context_package_json_path.write_text(json.dumps(asdict(package), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    context_package_markdown_path.write_text(render_context_package_markdown(package), encoding="utf-8")

    return package, {
        "package_dir": package_dir,
        "ocr_result_json_path": ocr_result_json_path,
        "ocr_text_full_path": ocr_text_full_path,
        "context_package_json_path": context_package_json_path,
        "context_package_markdown_path": context_package_markdown_path,
    }


def update_context_package_manifest(manifest_jsonl: Path, package: ContextPackage) -> None:
    row = asdict(package)
    _write_jsonl_replace(manifest_jsonl.resolve(), row, key_field="image_id")


def print_json(payload: Any) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
