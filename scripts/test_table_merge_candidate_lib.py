from __future__ import annotations

import json
from pathlib import Path

from table_merge_candidate_lib import (
    build_merged_candidate_from_paths,
    build_single_source_candidate_from_path,
)


ROOT = Path(__file__).resolve().parents[1]
APPLE = (
    ROOT
    / "control"
    / "project_domain"
    / "resources"
    / "manifests"
    / "phase0_apple_document_structure_normalized_at2026_03_28.json"
)
PADDLE = (
    ROOT
    / "control"
    / "project_domain"
    / "resources"
    / "manifests"
    / "phase0_paddleocr_table_parse_normalized_at2026_03_28.json"
)
COMPARISON = (
    ROOT
    / "control"
    / "project_domain"
    / "resources"
    / "manifests"
    / "phase0_table_parser_comparison_at2026_03_28.json"
)


def _cell_lookup(merged: dict) -> dict[tuple[int, int], dict]:
    indexed = {}
    for row in merged["rows"]:
        for cell in row["cells"]:
            indexed[(cell["row_index"], cell["col_index"])] = cell
    return indexed


def test_build_real_phase0_merged_candidate() -> None:
    merged = build_merged_candidate_from_paths(
        apple_normalized_json=APPLE,
        paddle_normalized_json=PADDLE,
        comparison_json=COMPARISON,
    )
    assert merged["status"] == "completed"
    assert merged["policy_name"] == "baseline_v1"
    assert merged["structure_source"] == "apple"
    assert merged["merge_summary"]["total_cells"] == 16
    assert merged["merge_summary"]["auto_accept_candidate_count"] == 6
    assert merged["merge_summary"]["pending_review_count"] == 10
    cells = _cell_lookup(merged)
    assert cells[(0, 0)]["review_status"] == "auto_accept_candidate"
    assert cells[(0, 2)]["recommended_text"] == "65Q"
    assert cells[(0, 2)]["review_status"] == "pending_review"
    assert cells[(1, 2)]["recommended_text"] == "0.815"
    assert cells[(1, 2)]["review_reason"] == "numeric_cell_review_gate"
    assert cells[(2, 2)]["recommended_text"] == "0.670"
    assert cells[(2, 2)]["review_status"] == "pending_review"
    assert cells[(1, 0)]["review_status"] == "auto_accept_candidate"


def test_build_single_source_candidate_from_apple_fixture() -> None:
    merged = build_single_source_candidate_from_path(
        normalized_json=APPLE,
        parser_backend="apple_vision_recognize_documents_request",
    )
    assert merged["status"] == "completed"
    assert merged["policy_name"] == "single_source_fallback_v1"
    assert merged["structure_source"] == "apple_single_source"
    assert merged["merge_summary"]["total_cells"] == 16
    cells = _cell_lookup(merged)
    assert cells[(0, 0)]["recommended_text"] == "Metric"
    assert cells[(0, 0)]["review_status"] == "auto_accept_candidate"
    assert cells[(1, 2)]["recommended_text"] == "0.815"
    assert cells[(1, 2)]["review_status"] == "pending_review"


def main() -> int:
    test_build_real_phase0_merged_candidate()
    test_build_single_source_candidate_from_apple_fixture()
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
