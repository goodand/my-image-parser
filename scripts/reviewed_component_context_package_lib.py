#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from alpha_component_lib import DEFAULT_ALPHA_THRESHOLD, collect_alpha_components
from full_image_ocr_context_package_lib import (
    build_ocr_text_excerpt,
    build_ppt_provenance_context_from_package,
    determine_ocr_status,
    run_full_image_ocr,
)
from parser_enriched_context_package_lib import load_json, summarize_merged_candidate


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = (
    ROOT_DIR
    / "control"
    / "project_domain"
    / "resources"
    / "context_packages"
    / "reviewed_isolated_component"
)
DEFAULT_COMPONENT_PROXIMITY_PADDING = 48
DEFAULT_ALPHA_COMPONENT_MIN_PIXELS = 64
DEFAULT_MAX_EXTERNAL_COMPONENTS_FOR_RECROP = 24


@dataclass(frozen=True)
class ReviewedComponentCrop:
    source_image_path: str
    component_kind: str
    bbox_int: list[int]
    component_image_path: str
    image_width: int
    image_height: int


@dataclass(frozen=True)
class ReviewedCropCandidate:
    candidate_name: str
    bbox_int: list[int]
    rationale: str
    external_component_count: int
    nearby_component_pixels: int


def _sanitize_base_summary(summary: str) -> str:
    cleaned = summary.strip()
    marker = " Existing phase-1 caption:"
    if marker in cleaned:
        cleaned = cleaned.split(marker, 1)[0].strip()
    return cleaned


def _tokenize_text(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9@.+-]+", text)


def load_text_file(path_value: str | None) -> str:
    if not path_value:
        return ""
    path = Path(path_value)
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def normalized_xywh_bottom_to_bbox_int(
    bbox: list[float] | list[int],
    *,
    image_width: int,
    image_height: int,
) -> list[int]:
    if len(bbox) != 4:
        raise ValueError(f"Expected 4-element bbox, got {bbox!r}")

    x, y, width, height = [float(value) for value in bbox]
    if max(abs(x), abs(y), abs(width), abs(height)) <= 1.5:
        x1 = x * image_width
        x2 = (x + width) * image_width
        y1 = (1.0 - y - height) * image_height
        y2 = (1.0 - y) * image_height
        return [int(round(x1)), int(round(y1)), int(round(x2)), int(round(y2))]

    return [int(round(x)), int(round(y)), int(round(width)), int(round(height))]


def _pad_bbox_int(
    bbox: list[int],
    *,
    image_width: int,
    image_height: int,
    padding: int,
) -> list[int]:
    x1, y1, x2, y2 = bbox
    return [
        max(0, x1 - padding),
        max(0, y1 - padding),
        min(image_width, x2 + padding),
        min(image_height, y2 + padding),
    ]


def _bbox_area(bbox: list[int]) -> int:
    x1, y1, x2, y2 = bbox
    return max(0, x2 - x1) * max(0, y2 - y1)


def _bbox_contains(outer: list[int], inner: list[int]) -> bool:
    return outer[0] <= inner[0] and outer[1] <= inner[1] and outer[2] >= inner[2] and outer[3] >= inner[3]


def _bbox_intersects(left: list[int], right: list[int]) -> bool:
    return not (
        left[2] <= right[0]
        or right[2] <= left[0]
        or left[3] <= right[1]
        or right[3] <= left[1]
    )


def _bbox_union(boxes: list[list[int]]) -> list[int]:
    return [
        min(box[0] for box in boxes),
        min(box[1] for box in boxes),
        max(box[2] for box in boxes),
        max(box[3] for box in boxes),
    ]


def compute_reviewed_table_component_bbox(
    *,
    merged_candidate: dict[str, Any],
    image_width: int,
    image_height: int,
    padding: int = 8,
) -> list[int]:
    xs1: list[int] = []
    ys1: list[int] = []
    xs2: list[int] = []
    ys2: list[int] = []
    for row in merged_candidate.get("rows", []):
        for cell in row.get("cells", []):
            bbox = normalized_xywh_bottom_to_bbox_int(
                cell["bbox"],
                image_width=image_width,
                image_height=image_height,
            )
            xs1.append(bbox[0])
            ys1.append(bbox[1])
            xs2.append(bbox[2])
            ys2.append(bbox[3])
    if not xs1:
        raise ValueError("Merged candidate does not contain any cell bbox values.")
    union_bbox = [min(xs1), min(ys1), max(xs2), max(ys2)]
    return _pad_bbox_int(
        union_bbox,
        image_width=image_width,
        image_height=image_height,
        padding=padding,
    )


def export_reviewed_component_crop(
    *,
    source_image_path: Path,
    output_path: Path,
    bbox_int: list[int],
    component_kind: str = "reviewed_table_component",
) -> ReviewedComponentCrop:
    from PIL import Image

    source_image = source_image_path.resolve()
    output_file = output_path.resolve()
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(source_image) as image:
        image_width, image_height = image.size
        crop = image.crop(tuple(bbox_int)).convert("RGB")
        crop.save(output_file)

    return ReviewedComponentCrop(
        source_image_path=str(source_image),
        component_kind=component_kind,
        bbox_int=[int(value) for value in bbox_int],
        component_image_path=str(output_file),
        image_width=image_width,
        image_height=image_height,
    )


def expected_table_tokens(merged_candidate: dict[str, Any]) -> list[str]:
    summary = summarize_merged_candidate(merged_candidate)
    tokens: list[str] = []
    seen: set[str] = set()
    for row_text in summary.selected_text_evidence:
        for token in _tokenize_text(row_text):
            if token not in seen:
                tokens.append(token)
                seen.add(token)
    return tokens


def analyze_alpha_recrop_candidates(
    *,
    source_image_path: Path,
    seed_bbox_int: list[int],
    image_width: int,
    image_height: int,
    padding: int,
    alpha_threshold: int = DEFAULT_ALPHA_THRESHOLD,
    alpha_min_pixels: int = DEFAULT_ALPHA_COMPONENT_MIN_PIXELS,
    component_proximity_padding: int = DEFAULT_COMPONENT_PROXIMITY_PADDING,
    max_external_components_for_recrop: int = DEFAULT_MAX_EXTERNAL_COMPONENTS_FOR_RECROP,
) -> tuple[list[ReviewedCropCandidate], dict[str, Any]]:
    candidates = [
        ReviewedCropCandidate(
            candidate_name="seed_bbox",
            bbox_int=[int(value) for value in seed_bbox_int],
            rationale="Union bbox from merged table candidate cell geometry.",
            external_component_count=0,
            nearby_component_pixels=0,
        )
    ]
    alpha_summary = collect_alpha_components(
        source_image=source_image_path,
        alpha_threshold=alpha_threshold,
        min_pixels=alpha_min_pixels,
    )
    expanded_seed = _pad_bbox_int(
        seed_bbox_int,
        image_width=image_width,
        image_height=image_height,
        padding=component_proximity_padding,
    )
    external_nearby: list[dict[str, Any]] = []
    for component in alpha_summary["components"]:
        bbox = [int(value) for value in component["bbox"]]
        if _bbox_contains(seed_bbox_int, bbox):
            continue
        if _bbox_intersects(expanded_seed, bbox):
            external_nearby.append(
                {
                    "index": int(component["index"]),
                    "pixel_count": int(component["pixel_count"]),
                    "bbox": bbox,
                }
            )

    analysis = {
        "alpha_component_count": int(alpha_summary["component_count"]),
        "alpha_threshold": int(alpha_threshold),
        "alpha_min_pixels": int(alpha_min_pixels),
        "component_proximity_padding": int(component_proximity_padding),
        "seed_bbox_int": [int(value) for value in seed_bbox_int],
        "seed_bbox_area": _bbox_area(seed_bbox_int),
        "external_nearby_component_count": len(external_nearby),
        "external_nearby_components": external_nearby[:32],
        "max_external_components_for_recrop": int(max_external_components_for_recrop),
        "recrop_candidate_added": False,
        "skip_reason": None,
    }

    if not external_nearby:
        analysis["skip_reason"] = "no_external_components_near_seed_bbox"
        return candidates, analysis

    if len(external_nearby) > max_external_components_for_recrop:
        analysis["skip_reason"] = "too_many_external_components_near_seed_bbox"
        return candidates, analysis

    augmented_union = _bbox_union([seed_bbox_int] + [item["bbox"] for item in external_nearby])
    augmented_bbox = _pad_bbox_int(
        augmented_union,
        image_width=image_width,
        image_height=image_height,
        padding=padding,
    )
    if augmented_bbox == seed_bbox_int:
        analysis["skip_reason"] = "external_components_do_not_expand_seed_bbox"
        return candidates, analysis

    analysis["recrop_candidate_added"] = True
    analysis["augmented_bbox_int"] = [int(value) for value in augmented_bbox]
    analysis["augmented_bbox_area"] = _bbox_area(augmented_bbox)
    candidates.append(
        ReviewedCropCandidate(
            candidate_name="alpha_nearby_union",
            bbox_int=[int(value) for value in augmented_bbox],
            rationale=(
                "Seed bbox expanded to include nearby disconnected alpha components "
                "that likely carry table context such as titles, labels, or adjacent notes."
            ),
            external_component_count=len(external_nearby),
            nearby_component_pixels=sum(item["pixel_count"] for item in external_nearby),
        )
    )
    return candidates, analysis


def selected_text_evidence_from_ocr(ocr_result: dict[str, Any], *, limit: int = 6) -> list[str]:
    values: list[str] = []
    for annotation in ocr_result.get("annotations", []):
        text = str(annotation.get("text") or "").strip()
        if text and text not in values:
            values.append(text)
        if len(values) >= limit:
            break
    if values:
        return values
    full_text = str(ocr_result.get("full_text") or "").strip()
    return [token for token in _tokenize_text(full_text)[:limit]]


def compare_component_ocr_to_full_image(
    *,
    full_image_ocr_text: str,
    reviewed_component_ocr_text: str,
    merged_candidate: dict[str, Any],
) -> dict[str, Any]:
    expected_tokens = expected_table_tokens(merged_candidate)
    expected_token_set = set(expected_tokens)

    full_tokens = _tokenize_text(full_image_ocr_text)
    reviewed_tokens = _tokenize_text(reviewed_component_ocr_text)

    full_hits = [token for token in full_tokens if token in expected_token_set]
    reviewed_hits = [token for token in reviewed_tokens if token in expected_token_set]
    full_extras = [token for token in full_tokens if token not in expected_token_set]
    reviewed_extras = [token for token in reviewed_tokens if token not in expected_token_set]

    reviewed_better = (
        len(set(reviewed_hits)) >= len(set(full_hits))
        and len(reviewed_extras) < len(full_extras)
    )

    rationale = (
        "Reviewed component OCR preserves the same or better table-token coverage "
        "with fewer extraneous tokens than the full-image OCR excerpt."
        if reviewed_better
        else "Reviewed component OCR does not yet improve on the full-image OCR evidence."
    )

    return {
        "expected_tokens": expected_tokens,
        "full_image_hit_count": len(set(full_hits)),
        "full_image_extra_token_count": len(full_extras),
        "full_image_extra_tokens": full_extras[:16],
        "reviewed_component_hit_count": len(set(reviewed_hits)),
        "reviewed_component_extra_token_count": len(reviewed_extras),
        "reviewed_component_extra_tokens": reviewed_extras[:16],
        "reviewed_component_better_for_caption_input": reviewed_better,
        "rationale": rationale,
    }


def _reviewed_candidate_rank_key(evaluation: dict[str, Any]) -> tuple[int, int, int, int, int]:
    comparison = evaluation["comparison"]
    return (
        int(comparison["reviewed_component_hit_count"]),
        -int(comparison["reviewed_component_extra_token_count"]),
        int(bool(comparison["reviewed_component_better_for_caption_input"])),
        -int(evaluation["candidate_area"]),
        1 if evaluation["candidate_name"] == "seed_bbox" else 0,
    )


def evaluate_reviewed_crop_candidates(
    *,
    source_image_path: Path,
    candidate_specs: list[ReviewedCropCandidate],
    candidate_output_dir: Path,
    merged_candidate: dict[str, Any],
    full_image_ocr_text: str,
    ocr_runner: Callable[[Path], dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    candidate_output_dir.mkdir(parents=True, exist_ok=True)
    evaluations: list[dict[str, Any]] = []
    for candidate in candidate_specs:
        candidate_path = candidate_output_dir / f"REVIEWED_COMPONENT_{candidate.candidate_name}.png"
        exported = export_reviewed_component_crop(
            source_image_path=source_image_path,
            output_path=candidate_path,
            bbox_int=candidate.bbox_int,
            component_kind=f"reviewed_table_component::{candidate.candidate_name}",
        )
        ocr_result = ocr_runner(Path(exported.component_image_path))
        comparison = compare_component_ocr_to_full_image(
            full_image_ocr_text=full_image_ocr_text,
            reviewed_component_ocr_text=str(ocr_result.get("full_text") or ""),
            merged_candidate=merged_candidate,
        )
        evaluations.append(
            {
                "candidate_name": candidate.candidate_name,
                "candidate_bbox_int": [int(value) for value in candidate.bbox_int],
                "candidate_area": _bbox_area(candidate.bbox_int),
                "candidate_image_path": exported.component_image_path,
                "candidate_component_kind": exported.component_kind,
                "candidate_rationale": candidate.rationale,
                "external_component_count": int(candidate.external_component_count),
                "nearby_component_pixels": int(candidate.nearby_component_pixels),
                "ocr_status": determine_ocr_status(ocr_result),
                "selected_text_evidence": selected_text_evidence_from_ocr(ocr_result),
                "comparison": comparison,
                "ocr_result": ocr_result,
            }
        )
    selected = max(evaluations, key=_reviewed_candidate_rank_key)
    return selected, evaluations


def build_ocr_evidence_context(
    *,
    package: dict[str, Any],
    ocr_result: dict[str, Any],
    selected_text_evidence: list[str],
    component_evidence: dict[str, Any],
) -> dict[str, Any]:
    return {
        "source_kind": "ocr_evidence",
        "ocr_surface": package.get("ocr_surface"),
        "ocr_status": package.get("ocr_status"),
        "ocr_engine": ocr_result.get("engine"),
        "ocr_annotation_count": int(ocr_result.get("annotation_count") or 0),
        "ocr_text_excerpt": package.get("ocr_text_excerpt"),
        "ocr_text_full_path": package.get("ocr_text_full_path"),
        "ocr_result_json_path": package.get("ocr_result_json_path"),
        "selected_text_evidence": selected_text_evidence,
        "comparison_against_full_image": component_evidence,
    }


def build_reviewed_component_context_package(
    *,
    base_context_package: dict[str, Any],
    merged_candidate: dict[str, Any],
    crop: ReviewedComponentCrop,
    ocr_result: dict[str, Any],
    component_evidence: dict[str, Any],
) -> dict[str, Any]:
    package = dict(base_context_package)
    summary = summarize_merged_candidate(merged_candidate)
    base_summary = _sanitize_base_summary(str(base_context_package.get("ppt_local_summary") or ""))
    component_note = (
        f"Reviewed isolated component crop for table `{summary.table_id}` on page `{summary.page}`. "
        "This crop focuses on the table region only and is intended as the primary visual caption surface "
        "for the isolated-component arm."
    )
    combined_summary = " ".join(
        part for part in [base_summary, component_note, component_evidence["rationale"]] if part
    ).strip()

    package["image_id"] = f"{base_context_package.get('image_id')}::reviewed_table_component"
    package["source_image_path"] = crop.component_image_path
    package["image_surface"] = "reviewed_table_component_crop"
    package["ocr_surface"] = "reviewed_component_standalone_ocr"
    package["ocr_status"] = determine_ocr_status(ocr_result)
    package["ocr_engine"] = ocr_result.get("engine")
    package["ocr_annotation_count"] = int(ocr_result.get("annotation_count") or 0)
    package["ocr_text_excerpt"] = build_ocr_text_excerpt(ocr_result)
    package["ppt_local_summary"] = combined_summary
    package["review_status"] = (
        "reviewed_candidate"
        if component_evidence["reviewed_component_better_for_caption_input"]
        else "pending_review"
    )
    package["context_variant"] = "reviewed_isolated_component"
    package["selected_text_evidence"] = selected_text_evidence_from_ocr(ocr_result)
    package["ppt_provenance_context"] = build_ppt_provenance_context_from_package(package)
    package["ocr_evidence_context"] = build_ocr_evidence_context(
        package=package,
        ocr_result=ocr_result,
        selected_text_evidence=package["selected_text_evidence"],
        component_evidence=component_evidence,
    )
    package["notes"] = list(base_context_package.get("notes") or []) + [
        "Reviewed isolated-component arm uses a bounded table crop rather than a raw alpha component."
    ]
    package["reviewed_component_enrichment"] = {
        "component_kind": crop.component_kind,
        "parent_source_image_path": base_context_package.get("source_image_path"),
        "component_image_path": crop.component_image_path,
        "component_bbox_int": crop.bbox_int,
        "document_id": summary.document_id,
        "page": summary.page,
        "table_id": summary.table_id,
        "source_manifests": summary.source_manifests,
        "evidence_comparison": component_evidence,
    }
    return package


def render_reviewed_component_context_markdown(package: dict[str, Any]) -> str:
    enrichment = package.get("reviewed_component_enrichment") or {}
    comparison = enrichment.get("evidence_comparison") or {}
    candidate_selection = enrichment.get("candidate_selection") or {}
    ocr_evidence_context = package.get("ocr_evidence_context") or {}
    lines = [
        "# Reviewed Isolated Component Context Package",
        "",
        "## Source",
        "",
        f"- image_id: `{package.get('image_id')}`",
        f"- source_image_path: `{package.get('source_image_path')}`",
        f"- source_dataset: `{package.get('source_dataset')}`",
        f"- source_pptx: `{package.get('source_pptx') or 'n/a'}`",
        f"- source_slide_numbers: `{', '.join(str(item) for item in package.get('source_slide_numbers') or []) or 'n/a'}`",
        f"- context_variant: `{package.get('context_variant')}`",
        "",
        "## Reviewed Component",
        "",
        f"- component_kind: `{enrichment.get('component_kind')}`",
        f"- parent_source_image_path: `{enrichment.get('parent_source_image_path')}`",
        f"- component_image_path: `{enrichment.get('component_image_path')}`",
        f"- component_bbox_int: `{enrichment.get('component_bbox_int')}`",
        f"- table_id: `{enrichment.get('table_id')}`",
        f"- page: `{enrichment.get('page')}`",
        f"- selected_candidate_name: `{candidate_selection.get('selected_candidate_name') or 'n/a'}`",
        f"- candidate_count: `{candidate_selection.get('candidate_count') or 0}`",
        "",
        "## OCR Evidence Context",
        "",
        f"- ocr_status: `{ocr_evidence_context.get('ocr_status') or package.get('ocr_status')}`",
        f"- ocr_engine: `{ocr_evidence_context.get('ocr_engine') or package.get('ocr_engine') or 'n/a'}`",
        f"- ocr_annotation_count: `{ocr_evidence_context.get('ocr_annotation_count') or package.get('ocr_annotation_count')}`",
        f"- ocr_text_full_path: `{ocr_evidence_context.get('ocr_text_full_path') or package.get('ocr_text_full_path')}`",
        "",
        "### OCR Excerpt",
        "",
        str(package.get("ocr_text_excerpt") or "_empty_"),
        "",
        "## Comparison Evidence",
        "",
        f"- reviewed_component_better_for_caption_input: `{comparison.get('reviewed_component_better_for_caption_input')}`",
        f"- full_image_hit_count: `{comparison.get('full_image_hit_count')}`",
        f"- reviewed_component_hit_count: `{comparison.get('reviewed_component_hit_count')}`",
        f"- full_image_extra_token_count: `{comparison.get('full_image_extra_token_count')}`",
        f"- reviewed_component_extra_token_count: `{comparison.get('reviewed_component_extra_token_count')}`",
        "",
        str(comparison.get("rationale") or "_empty_"),
        "",
        "## PPT-Local Summary",
        "",
        str(package.get("ppt_local_summary") or "_empty_"),
        "",
        "## Review",
        "",
        f"- review_status: `{package.get('review_status')}`",
        "",
    ]
    candidate_evaluations = candidate_selection.get("candidate_evaluations") or []
    if candidate_evaluations:
        lines.extend(
            [
                "## Candidate Selection",
                "",
                f"- selection_strategy: `{candidate_selection.get('selection_strategy') or 'n/a'}`",
                "",
                "| candidate | bbox | hit_count | extra_token_count | better_vs_full | ocr_status |",
                "| --- | --- | ---: | ---: | --- | --- |",
            ]
        )
        for item in candidate_evaluations:
            comparison_item = item.get("comparison") or {}
            lines.append(
                f"| `{item.get('candidate_name')}` | `{item.get('candidate_bbox_int')}` | "
                f"{comparison_item.get('reviewed_component_hit_count')} | "
                f"{comparison_item.get('reviewed_component_extra_token_count')} | "
                f"{comparison_item.get('reviewed_component_better_for_caption_input')} | "
                f"{item.get('ocr_status')} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_reviewed_component_context_package(
    *,
    package: dict[str, Any],
    ocr_result: dict[str, Any],
    output_root: Path,
) -> dict[str, Path]:
    dataset = str(package.get("source_dataset") or "unknown_dataset")
    image_stem = Path(str(package.get("reviewed_component_enrichment", {}).get("parent_source_image_path") or package.get("source_image_path") or "image")).stem.replace(" ", "_")
    package_dir = output_root.resolve() / dataset / image_stem
    package_dir.mkdir(parents=True, exist_ok=True)
    ocr_result_json_path = package_dir / "OCR_RESULT.json"
    ocr_text_full_path = package_dir / "OCR_FULL_TEXT.txt"
    context_json_path = package_dir / "CONTEXT_PACKAGE.json"
    context_md_path = package_dir / "CONTEXT_PACKAGE.md"
    ocr_result_json_path.write_text(json.dumps(ocr_result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ocr_text_full_path.write_text((ocr_result.get("full_text") or "") + "\n", encoding="utf-8")
    package["ocr_result_json_path"] = str(ocr_result_json_path)
    package["ocr_text_full_path"] = str(ocr_text_full_path)
    package["context_package_json_path"] = str(context_json_path)
    package["context_package_markdown_path"] = str(context_md_path)
    context_json_path.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    context_md_path.write_text(render_reviewed_component_context_markdown(package), encoding="utf-8")
    return {
        "package_dir": package_dir,
        "ocr_result_json_path": ocr_result_json_path,
        "ocr_text_full_path": ocr_text_full_path,
        "context_package_json_path": context_json_path,
        "context_package_markdown_path": context_md_path,
    }


def write_json_manifest(path: Path, rows: list[dict[str, Any]]) -> None:
    existing_rows: list[dict[str, Any]] = []
    if path.is_file():
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            existing_rows = [item for item in payload if isinstance(item, dict)]

    for row in rows:
        key = str(row.get("source_image_path") or "")
        replaced = False
        for index, existing in enumerate(existing_rows):
            if str(existing.get("source_image_path") or "") == key:
                existing_rows[index] = row
                replaced = True
                break
        if not replaced:
            existing_rows.append(row)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(existing_rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_dataset_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    path.write_text(payload, encoding="utf-8")


def build_reviewed_component_bundle(
    *,
    base_context_package: dict[str, Any],
    merged_candidate: dict[str, Any],
    output_root: Path,
    padding: int = 8,
    alpha_threshold: int = DEFAULT_ALPHA_THRESHOLD,
    alpha_min_pixels: int = DEFAULT_ALPHA_COMPONENT_MIN_PIXELS,
    component_proximity_padding: int = DEFAULT_COMPONENT_PROXIMITY_PADDING,
    max_external_components_for_recrop: int = DEFAULT_MAX_EXTERNAL_COMPONENTS_FOR_RECROP,
    ocr_runner: Callable[[Path], dict[str, Any]] = run_full_image_ocr,
) -> tuple[dict[str, Any], dict[str, Path], dict[str, Any], dict[str, Any]]:
    source_image_path = Path(str(base_context_package["source_image_path"])).resolve()
    image_width = int(base_context_package.get("image_width") or 0)
    image_height = int(base_context_package.get("image_height") or 0)
    if image_width <= 0 or image_height <= 0:
        raise ValueError("Base context package does not include valid image dimensions.")

    bbox_int = compute_reviewed_table_component_bbox(
        merged_candidate=merged_candidate,
        image_width=image_width,
        image_height=image_height,
        padding=padding,
    )
    package_root = (
        output_root.resolve()
        / str(base_context_package.get("source_dataset") or "unknown_dataset")
        / source_image_path.stem.replace(" ", "_")
    )
    candidate_specs, alpha_recrop_analysis = analyze_alpha_recrop_candidates(
        source_image_path=source_image_path,
        seed_bbox_int=bbox_int,
        image_width=image_width,
        image_height=image_height,
        padding=padding,
        alpha_threshold=alpha_threshold,
        alpha_min_pixels=alpha_min_pixels,
        component_proximity_padding=component_proximity_padding,
        max_external_components_for_recrop=max_external_components_for_recrop,
    )
    full_image_ocr_text = load_text_file(str(base_context_package.get("ocr_text_full_path") or ""))
    selected_candidate, candidate_evaluations = evaluate_reviewed_crop_candidates(
        source_image_path=source_image_path,
        candidate_specs=candidate_specs,
        candidate_output_dir=package_root / "_candidate_crops",
        merged_candidate=merged_candidate,
        full_image_ocr_text=full_image_ocr_text,
        ocr_runner=ocr_runner,
    )
    crop_output_path = package_root / "REVIEWED_COMPONENT.png"
    crop = export_reviewed_component_crop(
        source_image_path=source_image_path,
        output_path=crop_output_path,
        bbox_int=selected_candidate["candidate_bbox_int"],
        component_kind="reviewed_table_component",
    )
    ocr_result = selected_candidate["ocr_result"]
    component_evidence = selected_candidate["comparison"]
    package = build_reviewed_component_context_package(
        base_context_package=base_context_package,
        merged_candidate=merged_candidate,
        crop=crop,
        ocr_result=ocr_result,
        component_evidence=component_evidence,
    )
    output_paths = write_reviewed_component_context_package(
        package=package,
        ocr_result=ocr_result,
        output_root=output_root,
    )
    package["reviewed_component_enrichment"]["candidate_selection"] = {
        "selection_strategy": "seed_bbox_then_alpha_nearby_union",
        "selected_candidate_name": selected_candidate["candidate_name"],
        "selected_candidate_bbox_int": selected_candidate["candidate_bbox_int"],
        "candidate_count": len(candidate_evaluations),
        "alpha_recrop_analysis": alpha_recrop_analysis,
        "candidate_evaluations": [
            {
                "candidate_name": item["candidate_name"],
                "candidate_bbox_int": item["candidate_bbox_int"],
                "candidate_area": item["candidate_area"],
                "candidate_image_path": item["candidate_image_path"],
                "candidate_component_kind": item["candidate_component_kind"],
                "candidate_rationale": item["candidate_rationale"],
                "external_component_count": item["external_component_count"],
                "nearby_component_pixels": item["nearby_component_pixels"],
                "ocr_status": item["ocr_status"],
                "selected_text_evidence": item["selected_text_evidence"],
                "comparison": item["comparison"],
            }
            for item in candidate_evaluations
        ],
    }
    Path(package["context_package_json_path"]).write_text(
        json.dumps(package, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    Path(package["context_package_markdown_path"]).write_text(
        render_reviewed_component_context_markdown(package),
        encoding="utf-8",
    )
    dataset_row = {
        "image_id": package["image_id"],
        "image_path": crop.component_image_path,
        "source_image_path": base_context_package.get("source_image_path"),
        "source_filename": base_context_package.get("source_filename"),
        "source_pptx": base_context_package.get("source_pptx"),
        "slide_numbers": base_context_package.get("source_slide_numbers") or [],
        "source_zip_path": base_context_package.get("source_zip_path"),
        "surface_type": "reviewed_isolated_component",
        "review_status": package["review_status"],
        "component_kind": crop.component_kind,
        "component_bbox_int": selected_candidate["candidate_bbox_int"],
    }
    manifest_row = {
        "image_id": package["image_id"],
        "source_image_path": base_context_package.get("source_image_path"),
        "reviewed_component_image_path": crop.component_image_path,
        "selected_candidate_name": selected_candidate["candidate_name"],
        "context_package_json_path": package["context_package_json_path"],
        "context_package_markdown_path": package["context_package_markdown_path"],
        "ocr_result_json_path": package["ocr_result_json_path"],
        "ocr_status": package["ocr_status"],
        "review_status": package["review_status"],
        "evidence_comparison": component_evidence,
    }
    return package, output_paths, dataset_row, manifest_row


__all__ = [
    "DEFAULT_ALPHA_COMPONENT_MIN_PIXELS",
    "DEFAULT_COMPONENT_PROXIMITY_PADDING",
    "DEFAULT_MAX_EXTERNAL_COMPONENTS_FOR_RECROP",
    "DEFAULT_OUTPUT_ROOT",
    "analyze_alpha_recrop_candidates",
    "build_reviewed_component_bundle",
    "build_reviewed_component_context_package",
    "compare_component_ocr_to_full_image",
    "compute_reviewed_table_component_bbox",
    "evaluate_reviewed_crop_candidates",
    "expected_table_tokens",
    "export_reviewed_component_crop",
    "load_json",
    "normalized_xywh_bottom_to_bbox_int",
    "render_reviewed_component_context_markdown",
    "selected_text_evidence_from_ocr",
    "write_dataset_jsonl",
    "write_json_manifest",
]
