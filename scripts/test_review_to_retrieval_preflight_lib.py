from __future__ import annotations

from pathlib import Path

from review_to_retrieval_preflight_lib import (
    build_mapping_review_seed,
    build_preflight_manifest,
    build_review_decision_seed,
    build_retrieval_input_seed,
    load_json,
)


ROOT = Path(__file__).resolve().parents[1]
REVIEW_SURFACE = (
    ROOT
    / "control"
    / "project_domain"
    / "resources"
    / "manifests"
    / "phase2_caption_four_mode_corpus_review_surface_at2026_03_30.json"
)


def test_build_decision_seed() -> None:
    review_surface = load_json(REVIEW_SURFACE)
    rows = build_review_decision_seed(
        review_surface,
        review_surface_path=str(REVIEW_SURFACE.resolve()),
    )
    assert len(rows) == review_surface["image_count"]
    assert rows[0]["review_priority_label"] == "highest"
    assert rows[0]["review_status"] == "pending"
    assert rows[0]["use_for_retrieval"] is False
    assert rows[0]["selected_caption_arm"] is None
    assert rows[0]["retrieval_block_reason"] == "policy_hold"


def test_build_retrieval_and_mapping_seed() -> None:
    review_surface = load_json(REVIEW_SURFACE)
    retrieval_rows = build_retrieval_input_seed(review_surface)
    mapping_rows = build_mapping_review_seed(review_surface)
    assert len(retrieval_rows) == review_surface["image_count"]
    assert len(mapping_rows) == review_surface["image_count"]
    assert retrieval_rows[0]["retrieval_ready"] is False
    assert mapping_rows[0]["mapping_ready"] is False


def test_build_preflight_manifest() -> None:
    review_surface = load_json(REVIEW_SURFACE)
    preflight = build_preflight_manifest(
        review_surface,
        review_surface_path=str(REVIEW_SURFACE.resolve()),
        decision_seed_path="/tmp/decision.jsonl",
        retrieval_seed_path="/tmp/retrieval.jsonl",
        mapping_seed_path="/tmp/mapping.jsonl",
    )
    assert preflight["machine_truth_mode"] == "manifest"
    assert preflight["machine_truth_manifest_only"] is True
    assert preflight["image_count"] == review_surface["image_count"]
    assert preflight["priority_sorted_image_ids"] == review_surface["priority_sorted_image_ids"]


def main() -> int:
    load_json(REVIEW_SURFACE)
    test_build_decision_seed()
    test_build_retrieval_and_mapping_seed()
    test_build_preflight_manifest()
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
