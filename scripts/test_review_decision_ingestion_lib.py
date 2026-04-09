from __future__ import annotations

from pathlib import Path

from review_decision_ingestion_lib import (
    build_ingestion_manifest,
    is_mapping_eligible,
    is_retrieval_eligible,
    load_json,
    load_jsonl,
    validate_machine_prefilled_fields,
)


ROOT = Path(__file__).resolve().parents[1]
DECISION_SEED = (
    ROOT
    / "control"
    / "project_domain"
    / "resources"
    / "manifests"
    / "phase2_caption_review_decision_seed_at2026_03_30.jsonl"
)
REVIEW_SURFACE = (
    ROOT
    / "control"
    / "project_domain"
    / "resources"
    / "manifests"
    / "phase2_caption_four_mode_corpus_review_surface_at2026_03_30.json"
)


def test_pending_seed_is_not_ready() -> None:
    rows = load_jsonl(DECISION_SEED)
    assert len(rows) == 9
    assert all(not is_retrieval_eligible(row) for row in rows)
    assert all(not is_mapping_eligible(row) for row in rows)


def test_completed_row_becomes_ready() -> None:
    row = load_jsonl(DECISION_SEED)[0]
    row["selected_caption_arm"] = "full_image_baseline"
    row["selected_caption_promotion_state"] = "default_ready_anchor"
    row["caption_decision"] = "select_active_default"
    row["caption_edit_required"] = False
    row["approved_caption"] = "Approved caption"
    row["approved_alt_text"] = "Approved alt text"
    row["use_for_retrieval"] = True
    row["mapping_review_required"] = True
    row["review_status"] = "completed"
    row["reviewer_id"] = "tester"
    row["reviewed_at"] = "2026-03-30T23:05:00+09:00"
    row["retrieval_block_reason"] = None
    assert is_retrieval_eligible(row) is True
    assert is_mapping_eligible(row) is True


def test_manifest_counts() -> None:
    rows = load_jsonl(DECISION_SEED)
    manifest = build_ingestion_manifest(
        rows,
        decision_seed_path=str(DECISION_SEED.resolve()),
        retrieval_ready_path="/tmp/retrieval_ready.jsonl",
        mapping_ready_path="/tmp/mapping_ready.jsonl",
    )
    assert manifest["input_row_count"] == 9
    assert manifest["retrieval_ready_count"] == 0
    assert manifest["mapping_ready_count"] == 0
    assert manifest["review_status_counts"]["pending"] == 9


def test_prefilled_fields_match_review_surface() -> None:
    rows = load_jsonl(DECISION_SEED)
    review_surface = load_json(REVIEW_SURFACE)
    validate_machine_prefilled_fields(
        rows,
        review_surface=review_surface,
        review_surface_path=str(REVIEW_SURFACE.resolve()),
    )


def test_prefilled_drift_raises() -> None:
    rows = load_jsonl(DECISION_SEED)
    review_surface = load_json(REVIEW_SURFACE)
    rows[0]["comparison_winner"] = "full_image_baseline"
    try:
        validate_machine_prefilled_fields(
            rows,
            review_surface=review_surface,
            review_surface_path=str(REVIEW_SURFACE.resolve()),
        )
    except ValueError as exc:
        assert "Machine-prefilled field drift detected" in str(exc)
        return
    raise AssertionError("expected machine-prefilled drift validation to fail")


def main() -> int:
    test_pending_seed_is_not_ready()
    test_completed_row_becomes_ready()
    test_manifest_counts()
    test_prefilled_fields_match_review_surface()
    test_prefilled_drift_raises()
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
