from __future__ import annotations

from pathlib import Path

from table_parser_comparison_lib import compare_normalized_tables, load_normalized_table


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


def test_compare_real_phase0_tables() -> None:
    apple = load_normalized_table(APPLE)
    paddle = load_normalized_table(PADDLE)
    comparison = compare_normalized_tables(apple, paddle)
    assert comparison["structure_alignment"]["compatible_for_shared_wrapper"] is True
    assert comparison["difference_count"] == 6
    assert comparison["repairable_difference_count"] == 5
    assert comparison["review_required_count"] == 1
    assert comparison["merge_policy"]["structure_source"] == "apple"
    cells = {(d["row_index"], d["col_index"]): d for d in comparison["differences"]}
    assert cells[(0, 2)]["classification"] == "header_character_substitution"
    assert cells[(0, 2)]["recommended_text_source"] == "review"
    assert cells[(2, 2)]["classification"] == "missing_in_paddle"
    assert cells[(2, 2)]["recommended_text_source"] == "apple"
    assert cells[(3, 2)]["classification"] == "decimal_point_drift"
    assert cells[(3, 2)]["recommended_text_source"] == "apple"
    assert cells[(1, 2)]["classification"] == "decimal_point_drift"
    assert cells[(1, 2)]["recommended_text_source"] == "apple"


def main() -> int:
    test_compare_real_phase0_tables()
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
