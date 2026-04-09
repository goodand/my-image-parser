#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from parser_enriched_context_package_lib import (
    build_parser_enriched_context_package,
    summarize_merged_candidate,
)


ROOT_DIR = Path(__file__).resolve().parents[1]
BASE_CONTEXT_JSON = (
    ROOT_DIR
    / "control"
    / "project_domain"
    / "resources"
    / "context_packages"
    / "full_image_ocr_baseline"
    / "01_full_presentation_2026-03-17"
    / "image11"
    / "CONTEXT_PACKAGE.json"
)
MERGED_CANDIDATE_JSON = (
    ROOT_DIR
    / "control"
    / "project_domain"
    / "resources"
    / "manifests"
    / "phase0_table_merge_candidate_at2026_03_28.json"
)


def test_summarize_merged_candidate_real_fixture() -> None:
    merged = json.loads(MERGED_CANDIDATE_JSON.read_text(encoding="utf-8"))
    summary = summarize_merged_candidate(merged)
    assert summary.document_id == "01_full_presentation_2026-03-17"
    assert summary.table_id == "t1"
    assert summary.row_count == 4
    assert summary.column_count == 4
    assert summary.pending_review_count == 10
    assert summary.review_status == "pending_review"
    assert summary.selected_text_evidence


def test_build_parser_enriched_context_package_real_fixture() -> None:
    base_context = json.loads(BASE_CONTEXT_JSON.read_text(encoding="utf-8"))
    merged = json.loads(MERGED_CANDIDATE_JSON.read_text(encoding="utf-8"))
    package = build_parser_enriched_context_package(
        base_context_package=base_context,
        merged_candidate=merged,
    )
    assert package["context_variant"] == "parser_table_enriched"
    assert package["source_image_path"] == base_context["source_image_path"]
    assert package["review_status"] == "pending_review"
    assert package["structured_parse_context"] == package["parser_structured_context"]
    assert package["parser_structured_context"]["table_summary"] == package["table_summary"]
    assert (
        package["parser_structured_context"]["selected_text_evidence"]
        == package["selected_text_evidence"]
    )
    assert (
        package["parser_structured_context"]["table_structure_info"]["document_id"]
        == "01_full_presentation_2026-03-17"
    )
    assert package["parser_structured_context"]["table_structure_info"]["table_id"] == "t1"
    assert package["parser_structured_context"]["table_structure_info"]["pending_review_count"] == 10
    assert package["parser_enrichment"]["document_id"] == "01_full_presentation_2026-03-17"
    assert package["parser_enrichment"]["table_id"] == "t1"
    assert package["parser_enrichment"]["pending_review_count"] == 10
    assert package["ocr_evidence_context"]["selected_text_evidence"] == package["selected_text_evidence"]
    assert package["selected_text_evidence"]
    assert "Parser-enriched bounded table evidence" in package["ppt_local_summary"]


def main() -> int:
    test_summarize_merged_candidate_real_fixture()
    test_build_parser_enriched_context_package_real_fixture()
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
