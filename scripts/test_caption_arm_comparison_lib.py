from __future__ import annotations

from pathlib import Path

from caption_arm_comparison_lib import (
    _normalized_path_key,
    build_eval_bundle_from_comparison,
    build_small_batch_bundle_from_candidates,
    build_small_batch_candidate_selection,
    build_comparison_parity_audit,
    compare_ready_caption_arms,
    compare_caption_modes,
    determine_promotion_gate,
    extract_mode_record,
)
from run_caption_arm_comparison import (
    build_candidate_records,
    infer_ready_arm_report_title,
    parse_candidate_arm_spec,
)


ROOT = Path(__file__).resolve().parents[1]
BASELINE_LEDGER = ROOT / "control" / "project_agent_ops" / "registry" / "jobs" / "image_caption_jobs" / "phase1_ppt1_w1.json"
RERUN_LEDGER = (
    ROOT
    / "control"
    / "project_agent_ops"
    / "registry"
    / "jobs"
    / "image_caption_jobs"
    / "phase0_full_image_context_rerun_image11_at2026_03_28.json"
)
PARSER_RERUN_LEDGER = (
    ROOT
    / "control"
    / "project_agent_ops"
    / "registry"
    / "jobs"
    / "image_caption_jobs"
    / "phase0_parser_enriched_rerun_image11_at2026_03_28.json"
)
REVIEWED_COMPONENT_RERUN_LEDGER = (
    ROOT
    / "control"
    / "project_agent_ops"
    / "registry"
    / "jobs"
    / "image_caption_jobs"
    / "phase0_reviewed_isolated_component_rerun_image11_at2026_03_28.json"
)
SOURCE_IMAGE = (
    ROOT
    / "control"
    / "project_domain"
    / "resources"
    / "pptx_jobs"
    / "01_full_presentation_2026-03-17"
    / "media"
    / "image11.png"
)


def test_compare_real_two_mode_caption_records() -> None:
    baseline = extract_mode_record(
        ledger_path=BASELINE_LEDGER,
        source_image_path=SOURCE_IMAGE,
        execution_arm="full_image_baseline",
        fallback_input_surface="extracted_full_image",
    )
    rerun = extract_mode_record(
        ledger_path=RERUN_LEDGER,
        source_image_path=SOURCE_IMAGE,
        execution_arm="full_image_ocr_context_rerun",
        fallback_input_surface="full_image_original",
    )
    comparison = compare_caption_modes(baseline, rerun)
    assert comparison["same_source_image"] is True
    assert comparison["status_summary"]["both_completed"] is True
    assert comparison["promotion_state"] == "comparison_only_pending_context_review"
    assert comparison["parity_audit"]["ready_for_side_by_side_read"] is True
    assert comparison["parity_audit"]["all_required_present"] is True
    assert comparison["parity_audit"]["same_model"] is True
    assert comparison["parity_audit"]["same_image_id"] is False
    assert "image_id" in comparison["parity_audit"]["nonblocking_drift"]
    assert "prompt_version" in comparison["parity_audit"]["nonblocking_drift"]
    assert comparison["signal_comparison"]["delta"]["gained"] == ["mentions_relation"]
    assert baseline.context_package_present is False
    assert rerun.context_package_present is True
    assert rerun.context_review_status == "pending_review"


def test_determine_promotion_gate_states() -> None:
    assert determine_promotion_gate("accepted")["promotion_state"] == "candidate_ready"
    assert determine_promotion_gate("reviewed_candidate")["promotion_state"] == "comparison_ready_reviewed_branch"
    assert determine_promotion_gate("pending_review")["promotion_state"] == "comparison_only_pending_context_review"
    assert determine_promotion_gate(None)["promotion_state"] == "blocked_by_context_review"


def test_build_parity_audit_on_real_records() -> None:
    baseline = extract_mode_record(
        ledger_path=BASELINE_LEDGER,
        source_image_path=SOURCE_IMAGE,
        execution_arm="full_image_baseline",
        fallback_input_surface="extracted_full_image",
    )
    rerun = extract_mode_record(
        ledger_path=RERUN_LEDGER,
        source_image_path=SOURCE_IMAGE,
        execution_arm="full_image_ocr_context_rerun",
        fallback_input_surface="full_image_original",
    )
    audit = build_comparison_parity_audit(baseline, rerun)
    assert audit["same_source_image"] is True
    assert audit["same_image_id"] is False
    assert audit["ready_for_side_by_side_read"] is True
    assert "image_id" in audit["nonblocking_drift"]
    assert audit["review_statuses"] == [None, "pending_review"]


def test_compare_real_three_mode_caption_records() -> None:
    baseline = extract_mode_record(
        ledger_path=BASELINE_LEDGER,
        source_image_path=SOURCE_IMAGE,
        execution_arm="full_image_baseline",
        fallback_input_surface="extracted_full_image",
    )
    rerun = extract_mode_record(
        ledger_path=RERUN_LEDGER,
        source_image_path=SOURCE_IMAGE,
        execution_arm="full_image_ocr_context_rerun",
        fallback_input_surface="full_image_original",
    )
    parser_rerun = extract_mode_record(
        ledger_path=PARSER_RERUN_LEDGER,
        source_image_path=SOURCE_IMAGE,
        execution_arm="parser_table_enriched_rerun",
        fallback_input_surface="full_image_original",
    )
    comparison = compare_ready_caption_arms(baseline, rerun, parser_rerun)
    assert comparison["mode_count"] == 3
    assert comparison["comparison_ready"] is True
    assert comparison["status_summary"]["ready_arm_count"] == 3
    assert comparison["blocked_arms"] == []
    assert comparison["modes"][2]["context_variant"] == "parser_table_enriched"
    assert comparison["per_arm_promotion"]["parser_table_enriched_rerun"]["promotion_state"] == "comparison_only_pending_context_review"


def test_parse_candidate_arm_spec_defaults_and_explicit_surface() -> None:
    execution_arm, ledger_path, fallback_surface = parse_candidate_arm_spec(
        f"parser_table_enriched_rerun={PARSER_RERUN_LEDGER}"
    )
    assert execution_arm == "parser_table_enriched_rerun"
    assert ledger_path == str(PARSER_RERUN_LEDGER)
    assert fallback_surface == "full_image_original"

    execution_arm, ledger_path, fallback_surface = parse_candidate_arm_spec(
        f"reviewed_isolated_component_caption_arm={RERUN_LEDGER}::reviewed_component_crop"
    )
    assert execution_arm == "reviewed_isolated_component_caption_arm"
    assert ledger_path == str(RERUN_LEDGER)
    assert fallback_surface == "reviewed_component_crop"


def test_build_candidate_records_from_specs() -> None:
    records = build_candidate_records(
        candidate_specs=[
            f"full_image_ocr_context_rerun={RERUN_LEDGER}::full_image_original",
            f"parser_table_enriched_rerun={PARSER_RERUN_LEDGER}::full_image_original",
        ],
        source_image_path=str(SOURCE_IMAGE),
    )
    assert [record.execution_arm for record in records] == [
        "full_image_ocr_context_rerun",
        "parser_table_enriched_rerun",
    ]
    assert records[0].context_variant is None
    assert records[1].context_variant == "parser_table_enriched"


def test_infer_ready_arm_report_title() -> None:
    assert infer_ready_arm_report_title(2) == "Phase 0 Two-Mode Caption Comparison"
    assert infer_ready_arm_report_title(3) == "Phase 0 Three-Mode Caption Comparison"
    assert infer_ready_arm_report_title(4) == "Phase 0 4-Mode Caption Comparison"


def test_extract_reviewed_component_record_anchors_to_parent_source_image() -> None:
    reviewed = extract_mode_record(
        ledger_path=REVIEWED_COMPONENT_RERUN_LEDGER,
        source_image_path=SOURCE_IMAGE,
        execution_arm="reviewed_isolated_component_rerun",
        fallback_input_surface="reviewed_table_component_crop",
    )
    assert reviewed.source_image_path == _normalized_path_key(SOURCE_IMAGE)
    assert reviewed.input_surface == "reviewed_table_component_crop"
    assert reviewed.context_variant == "reviewed_isolated_component"
    assert determine_promotion_gate(reviewed.context_review_status)["promotion_state"] == "comparison_ready_reviewed_branch"
    assert reviewed.ocr_status == "usable"


def test_build_eval_bundle_from_real_four_mode_comparison() -> None:
    baseline = extract_mode_record(
        ledger_path=BASELINE_LEDGER,
        source_image_path=SOURCE_IMAGE,
        execution_arm="full_image_baseline",
        fallback_input_surface="extracted_full_image",
    )
    rerun = extract_mode_record(
        ledger_path=RERUN_LEDGER,
        source_image_path=SOURCE_IMAGE,
        execution_arm="full_image_ocr_context_rerun",
        fallback_input_surface="full_image_original",
    )
    parser_rerun = extract_mode_record(
        ledger_path=PARSER_RERUN_LEDGER,
        source_image_path=SOURCE_IMAGE,
        execution_arm="parser_table_enriched_rerun",
        fallback_input_surface="full_image_original",
    )
    reviewed = extract_mode_record(
        ledger_path=REVIEWED_COMPONENT_RERUN_LEDGER,
        source_image_path=SOURCE_IMAGE,
        execution_arm="reviewed_isolated_component_rerun",
        fallback_input_surface="reviewed_table_component_crop",
    )
    comparison = compare_ready_caption_arms(baseline, rerun, parser_rerun, reviewed)
    bundle = build_eval_bundle_from_comparison(comparison)
    assert bundle["mode_count"] == 4
    assert bundle["comparison_ready"] is True
    assert bundle["ready_arms"] == [
        "full_image_baseline",
        "full_image_ocr_context_rerun",
        "parser_table_enriched_rerun",
        "reviewed_isolated_component_rerun",
    ]
    assert bundle["arms"][-1]["context_variant"] == "reviewed_isolated_component"


def test_build_small_batch_bundle_from_candidates() -> None:
    candidate_selection = build_small_batch_candidate_selection(
        target_image_count=3,
        included_candidates=[
            {
                "candidate_label": "image11",
                "source_image_path": str(SOURCE_IMAGE),
                "decision": "include",
                "decision_reason": "existing_four_mode_bundle_present",
                "single_image_bundle_path": "phase0_bundle.json",
                "gpt_visual_confirmation": {"status": "not_required"},
                "four_arm_readiness": {
                    "full_image_baseline": "ready",
                    "full_image_ocr_context_rerun": "ready",
                    "parser_table_enriched_rerun": "ready",
                    "reviewed_isolated_component_rerun": "ready",
                },
            }
        ],
        excluded_candidates=[
            {
                "candidate_label": "image7",
                "source_image_path": "image7.png",
                "decision": "exclude",
                "decision_reason": "derived_arms_not_frozen",
                "gpt_visual_confirmation": {"status": "confirmed_table_centric"},
                "four_arm_readiness": {
                    "full_image_baseline": "ready",
                    "full_image_ocr_context_rerun": "not_frozen",
                    "parser_table_enriched_rerun": "not_frozen",
                    "reviewed_isolated_component_rerun": "not_frozen",
                },
            }
        ],
    )
    baseline = extract_mode_record(
        ledger_path=BASELINE_LEDGER,
        source_image_path=SOURCE_IMAGE,
        execution_arm="full_image_baseline",
        fallback_input_surface="extracted_full_image",
    )
    rerun = extract_mode_record(
        ledger_path=RERUN_LEDGER,
        source_image_path=SOURCE_IMAGE,
        execution_arm="full_image_ocr_context_rerun",
        fallback_input_surface="full_image_original",
    )
    parser_rerun = extract_mode_record(
        ledger_path=PARSER_RERUN_LEDGER,
        source_image_path=SOURCE_IMAGE,
        execution_arm="parser_table_enriched_rerun",
        fallback_input_surface="full_image_original",
    )
    reviewed = extract_mode_record(
        ledger_path=REVIEWED_COMPONENT_RERUN_LEDGER,
        source_image_path=SOURCE_IMAGE,
        execution_arm="reviewed_isolated_component_rerun",
        fallback_input_surface="reviewed_table_component_crop",
    )
    comparison = compare_ready_caption_arms(baseline, rerun, parser_rerun, reviewed)
    single_bundle = build_eval_bundle_from_comparison(comparison)
    batch_bundle = build_small_batch_bundle_from_candidates(
        candidate_selection=candidate_selection,
        included_image_bundles=[single_bundle],
    )
    assert candidate_selection["summary"]["included_count"] == 1
    assert candidate_selection["summary"]["minimum_target_met"] is False
    assert batch_bundle["included_image_count"] == 1
    assert batch_bundle["excluded_image_count"] == 1
    assert batch_bundle["minimum_target_met"] is False
    assert batch_bundle["included_images"][0]["bundle_summary"]["mode_count"] == 4


def main() -> int:
    test_compare_real_two_mode_caption_records()
    test_determine_promotion_gate_states()
    test_build_parity_audit_on_real_records()
    test_compare_real_three_mode_caption_records()
    test_parse_candidate_arm_spec_defaults_and_explicit_surface()
    test_build_candidate_records_from_specs()
    test_infer_ready_arm_report_title()
    test_extract_reviewed_component_record_anchors_to_parent_source_image()
    test_build_eval_bundle_from_real_four_mode_comparison()
    test_build_small_batch_bundle_from_candidates()
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
