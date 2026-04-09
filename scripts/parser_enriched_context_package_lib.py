#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from full_image_ocr_context_package_lib import (
    build_ocr_evidence_context_from_package,
    build_ppt_provenance_context_from_package,
)


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = (
    ROOT_DIR
    / "control"
    / "project_domain"
    / "resources"
    / "context_packages"
    / "parser_enriched_table_baseline"
)


@dataclass(frozen=True)
class ParserTableSummary:
    document_id: str
    page: int | None
    table_id: str
    row_count: int
    column_count: int
    total_cells: int
    pending_review_count: int
    auto_accept_candidate_count: int
    review_status: str
    table_summary: str
    selected_text_evidence: list[str]
    source_manifests: dict[str, str]


def load_json(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {path}")
    return payload


def _sanitize_base_summary(summary: str) -> str:
    cleaned = summary.strip()
    marker = " Existing phase-1 caption:"
    if marker in cleaned:
        cleaned = cleaned.split(marker, 1)[0].strip()
    return cleaned


def _row_to_evidence_text(row: dict[str, Any]) -> str:
    cell_texts: list[str] = []
    for cell in row.get("cells", []):
        text = str(cell.get("recommended_text") or "").strip()
        if text:
            cell_texts.append(text)
    return " | ".join(cell_texts)


def summarize_merged_candidate(merged_candidate: dict[str, Any]) -> ParserTableSummary:
    rows = merged_candidate.get("rows", [])
    row_count = len(rows)
    column_count = max((len(row.get("cells", [])) for row in rows), default=0)
    merge_summary = merged_candidate.get("merge_summary") or {}
    total_cells = int(merge_summary.get("total_cells") or 0)
    pending_review_count = int(merge_summary.get("pending_review_count") or 0)
    auto_accept_candidate_count = int(merge_summary.get("auto_accept_candidate_count") or 0)
    review_status = "pending_review" if pending_review_count > 0 else "accepted"

    selected_text_evidence = [
        row_text
        for row_text in (_row_to_evidence_text(row) for row in rows)
        if row_text
    ]

    header_text = selected_text_evidence[0] if selected_text_evidence else ""
    data_lines = selected_text_evidence[1:4]
    summary_parts = [
        f"Parser-enriched bounded table evidence for table `{merged_candidate.get('table_id')}`",
        f"on page `{merged_candidate.get('page')}`.",
        f"Shape: `{row_count} x {column_count}` with `{total_cells}` total cells.",
    ]
    if header_text:
        summary_parts.append(f"Header: {header_text}.")
    if data_lines:
        summary_parts.append("Rows: " + "; ".join(data_lines) + ".")
    summary_parts.append(
        f"Parser review status: `{review_status}` with `{pending_review_count}` pending-review cell(s)."
    )

    return ParserTableSummary(
        document_id=str(merged_candidate.get("document_id") or ""),
        page=int(merged_candidate["page"]) if merged_candidate.get("page") is not None else None,
        table_id=str(merged_candidate.get("table_id") or ""),
        row_count=row_count,
        column_count=column_count,
        total_cells=total_cells,
        pending_review_count=pending_review_count,
        auto_accept_candidate_count=auto_accept_candidate_count,
        review_status=review_status,
        table_summary=" ".join(summary_parts),
        selected_text_evidence=selected_text_evidence[:4],
        source_manifests={
            key: str(value)
            for key, value in (merged_candidate.get("source_manifests") or {}).items()
            if value
        },
    )


def _merge_review_status(base_review_status: str | None, parser_review_status: str) -> str:
    if base_review_status == "rejected":
        return "rejected"
    if base_review_status == "needs_more_context":
        return "needs_more_context"
    if base_review_status == "pending_review" or parser_review_status == "pending_review":
        return "pending_review"
    return parser_review_status or base_review_status or "pending_review"


def _build_parser_structured_context(
    *,
    summary: ParserTableSummary,
    merged_candidate: dict[str, Any],
) -> dict[str, Any]:
    return {
        "table_summary": summary.table_summary,
        "selected_text_evidence": summary.selected_text_evidence,
        "table_structure_info": {
            "document_id": summary.document_id,
            "page": summary.page,
            "table_id": summary.table_id,
            "row_count": summary.row_count,
            "column_count": summary.column_count,
            "total_cells": summary.total_cells,
            "pending_review_count": summary.pending_review_count,
            "auto_accept_candidate_count": summary.auto_accept_candidate_count,
            "review_status": summary.review_status,
            "source_manifests": summary.source_manifests,
            "merge_candidate_status": merged_candidate.get("status"),
            "comparison_difference_count": merged_candidate.get("comparison_difference_count"),
        },
    }


def build_parser_enriched_context_package(
    *,
    base_context_package: dict[str, Any],
    merged_candidate: dict[str, Any],
) -> dict[str, Any]:
    package = dict(base_context_package)
    summary = summarize_merged_candidate(merged_candidate)
    parser_structured_context = _build_parser_structured_context(
        summary=summary,
        merged_candidate=merged_candidate,
    )
    base_summary = _sanitize_base_summary(str(package.get("ppt_local_summary") or ""))
    combined_summary = (
        f"{base_summary} {summary.table_summary}".strip()
        if base_summary
        else summary.table_summary
    )

    notes = list(package.get("notes") or [])
    notes.append(
        "Parser-enriched bounded adapter attached merged table candidate evidence for caption rerun."
    )

    package["context_variant"] = "parser_table_enriched"
    package["ppt_local_summary"] = combined_summary
    package["review_status"] = _merge_review_status(
        str(package.get("review_status") or ""),
        summary.review_status,
    )
    package["ppt_provenance_context"] = build_ppt_provenance_context_from_package(package)
    package["structured_parse_context"] = parser_structured_context
    package["parser_structured_context"] = parser_structured_context
    package["ocr_evidence_context"] = build_ocr_evidence_context_from_package(
        package,
        selected_text_evidence=summary.selected_text_evidence,
    )
    package["selected_text_evidence"] = summary.selected_text_evidence
    package["table_summary"] = summary.table_summary
    package["notes"] = notes
    # Preserve the legacy field until downstream readers migrate to `parser_structured_context`.
    package["parser_enrichment"] = {
        "document_id": summary.document_id,
        "page": summary.page,
        "table_id": summary.table_id,
        "row_count": summary.row_count,
        "column_count": summary.column_count,
        "total_cells": summary.total_cells,
        "pending_review_count": summary.pending_review_count,
        "auto_accept_candidate_count": summary.auto_accept_candidate_count,
        "review_status": summary.review_status,
        "table_summary": summary.table_summary,
        "selected_text_evidence": summary.selected_text_evidence,
        "source_manifests": summary.source_manifests,
        "merge_candidate_status": merged_candidate.get("status"),
        "comparison_difference_count": merged_candidate.get("comparison_difference_count"),
    }
    return package


def render_parser_enriched_context_markdown(package: dict[str, Any]) -> str:
    parser_structured_context = (
        package.get("structured_parse_context")
        or package.get("parser_structured_context")
        or {}
    )
    parser_enrichment = package.get("parser_enrichment") or {}
    table_structure_info = parser_structured_context.get("table_structure_info") or parser_enrichment
    table_summary = parser_structured_context.get("table_summary") or package.get("table_summary")
    selected_text_evidence = (
        parser_structured_context.get("selected_text_evidence")
        or package.get("selected_text_evidence")
        or []
    )
    notes = package.get("notes") or []
    slides = ", ".join(str(item) for item in package.get("source_slide_numbers") or []) or "n/a"
    lines = [
        "# Parser-Enriched Context Package",
        "",
        "## Source",
        "",
        f"- image_id: `{package.get('image_id')}`",
        f"- source_image_path: `{package.get('source_image_path')}`",
        f"- source_dataset: `{package.get('source_dataset')}`",
        f"- source_pptx: `{package.get('source_pptx') or 'n/a'}`",
        f"- source_slide_numbers: `{slides}`",
        f"- context_variant: `{package.get('context_variant') or 'n/a'}`",
        "",
        "## OCR Evidence",
        "",
        f"- ocr_status: `{package.get('ocr_status')}`",
        f"- ocr_annotation_count: `{package.get('ocr_annotation_count')}`",
        "",
        "### OCR Excerpt",
        "",
        str(package.get("ocr_text_excerpt") or "_empty_"),
        "",
        "## Structured Parse Context",
        "",
        f"- document_id: `{table_structure_info.get('document_id')}`",
        f"- page: `{table_structure_info.get('page')}`",
        f"- table_id: `{table_structure_info.get('table_id')}`",
        f"- row_count: `{table_structure_info.get('row_count')}`",
        f"- column_count: `{table_structure_info.get('column_count')}`",
        f"- total_cells: `{table_structure_info.get('total_cells')}`",
        f"- pending_review_count: `{table_structure_info.get('pending_review_count')}`",
        f"- review_status: `{table_structure_info.get('review_status')}`",
        "",
        "### Table Summary",
        "",
        str(table_summary or "_empty_"),
        "",
        "### Selected Text Evidence",
        "",
    ]
    for item in selected_text_evidence:
        lines.append(f"- {item}")
    if not selected_text_evidence:
        lines.append("- _empty_")
    lines.extend(
        [
            "",
            "## Review",
            "",
            f"- review_status: `{package.get('review_status')}`",
            "",
            "## Notes",
            "",
        ]
    )
    for note in notes:
        lines.append(f"- {note}")
    if not notes:
        lines.append("- _empty_")
    return "\n".join(lines).rstrip() + "\n"


def write_parser_enriched_context_package(
    *,
    package: dict[str, Any],
    output_root: Path,
) -> dict[str, Path]:
    dataset = str(package.get("source_dataset") or "unknown_dataset")
    image_stem = Path(str(package.get("source_image_path") or "image")).stem.replace(" ", "_")
    package_dir = output_root.resolve() / dataset / image_stem
    package_dir.mkdir(parents=True, exist_ok=True)
    context_json = package_dir / "CONTEXT_PACKAGE.json"
    context_md = package_dir / "CONTEXT_PACKAGE.md"
    context_json.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    context_md.write_text(render_parser_enriched_context_markdown(package), encoding="utf-8")
    return {
        "package_dir": package_dir,
        "context_package_json_path": context_json,
        "context_package_markdown_path": context_md,
    }


def update_manifest_json(manifest_json: Path, package: dict[str, Any]) -> None:
    rows: list[dict[str, Any]] = []
    if manifest_json.is_file():
        payload = json.loads(manifest_json.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            rows = [item for item in payload if isinstance(item, dict)]
    key = str(package.get("source_image_path") or "")
    replaced = False
    for idx, existing in enumerate(rows):
        if str(existing.get("source_image_path") or "") == key:
            rows[idx] = package
            replaced = True
            break
    if not replaced:
        rows.append(package)
    manifest_json.parent.mkdir(parents=True, exist_ok=True)
    manifest_json.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
