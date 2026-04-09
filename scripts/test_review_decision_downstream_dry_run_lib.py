from __future__ import annotations

from pathlib import Path

from review_decision_downstream_dry_run_lib import (
    build_mapping_dry_run_manifest,
    build_retrieval_dry_run_manifest,
    load_json,
    load_jsonl,
)


ROOT = Path(__file__).resolve().parents[1]
INGESTION = (
    ROOT
    / "control"
    / "project_domain"
    / "resources"
    / "manifests"
    / "phase2_caption_review_decision_ingestion_at2026_03_30.json"
)
RETRIEVAL_READY = (
    ROOT
    / "control"
    / "project_domain"
    / "resources"
    / "manifests"
    / "phase2_retrieval_ready_rows_at2026_03_30.jsonl"
)
MAPPING_READY = (
    ROOT
    / "control"
    / "project_domain"
    / "resources"
    / "manifests"
    / "phase2_mapping_ready_rows_at2026_03_30.jsonl"
)


def test_zero_ready_dry_run_manifests() -> None:
    ingestion = load_json(INGESTION)
    retrieval_rows = load_jsonl(RETRIEVAL_READY)
    mapping_rows = load_jsonl(MAPPING_READY)
    retrieval_manifest = build_retrieval_dry_run_manifest(
        ingestion,
        retrieval_rows,
        retrieval_ready_rows_path=str(RETRIEVAL_READY.resolve()),
    )
    mapping_manifest = build_mapping_dry_run_manifest(
        ingestion,
        mapping_rows,
        mapping_ready_rows_path=str(MAPPING_READY.resolve()),
    )
    assert retrieval_manifest["retrieval_ready_count"] == 0
    assert retrieval_manifest["ready_to_execute"] is False
    assert retrieval_manifest["blocked_reason"] == "no_completed_review_rows_marked_for_retrieval"
    assert mapping_manifest["mapping_ready_count"] == 0
    assert mapping_manifest["ready_to_execute"] is False
    assert mapping_manifest["blocked_reason"] == "no_completed_review_rows_ready_for_mapping"


def main() -> int:
    test_zero_ready_dry_run_manifests()
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

