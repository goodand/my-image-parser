from __future__ import annotations

from pathlib import Path

from four_mode_small_batch_auto_eval_lib import build_batch_auto_eval, load_json


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "control" / "project_domain" / "resources" / "manifests" / "phase0_caption_four_mode_eval_bundle_at2026_03_28.json"
AGGREGATE_BUNDLE = (
    ROOT
    / "control"
    / "project_domain"
    / "resources"
    / "manifests"
    / "phase1_caption_four_mode_small_batch_bundle_at2026_03_28.json"
)


def test_build_batch_auto_eval_from_phase0_bundle() -> None:
    auto_eval = build_batch_auto_eval([BUNDLE], semantic_judge_available=False)
    assert auto_eval["image_count"] == 1
    assert auto_eval["semantic_judge_available"] is False
    assert auto_eval["actual_input_mode"] == "per_image_bundle_list"
    assert auto_eval["resolved_per_image_bundle_paths"] == [str(BUNDLE.resolve())]
    assert auto_eval["input_resolution"]["actual_input_mode"] == "per_image_bundle_list"
    assert auto_eval["evaluations"][0]["recommended_current_default"] == "full_image_baseline"
    assert auto_eval["evaluations"][0]["baseline_retained"] is True
    assert auto_eval["evaluations"][0]["qualitative_winner_candidate"] == "reviewed_isolated_component_rerun"
    assert auto_eval["winner_frequency"]["reviewed_isolated_component_rerun"] == 1
    assert auto_eval["baseline_retained"] is True
    assert auto_eval["batch_summary"]["winner_frequency"]["reviewed_isolated_component_rerun"] == 1


def test_build_batch_auto_eval_from_aggregate_bundle() -> None:
    aggregate = load_json(AGGREGATE_BUNDLE)
    auto_eval = build_batch_auto_eval(
        aggregate_bundle_paths=[AGGREGATE_BUNDLE],
        semantic_judge_available=False,
    )
    assert auto_eval["actual_input_mode"] == "aggregate_bundle"
    assert auto_eval["input_resolution"]["actual_input_mode"] == "aggregate_bundle"
    assert auto_eval["expanded_aggregate_bundle_paths"] == [str(AGGREGATE_BUNDLE.resolve())]
    assert auto_eval["requested_aggregate_bundle_paths"] == [str(AGGREGATE_BUNDLE.resolve())]
    assert auto_eval["image_count"] == aggregate["image_count"]
    assert sorted(auto_eval["image_ids"]) == sorted(Path(image["source_image_path"]).stem for image in aggregate["images"])


def main() -> int:
    load_json(BUNDLE)
    load_json(AGGREGATE_BUNDLE)
    test_build_batch_auto_eval_from_phase0_bundle()
    test_build_batch_auto_eval_from_aggregate_bundle()
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
