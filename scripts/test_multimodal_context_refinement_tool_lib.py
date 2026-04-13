from __future__ import annotations

from multimodal_context_refinement_tool_lib import (
    build_bundle_from_example_record,
    build_multimodal_context_bundle,
    load_example_record,
    render_bundle_report,
    validate_multimodal_context_bundle,
)


def test_build_multimodal_context_bundle_minimal() -> None:
    bundle = build_multimodal_context_bundle(
        source_image_path="control/project_domain/resources/pptx_jobs/02_1/media/image27.png",
        task_intent="ppt_support",
        provider_policy={"whole_image_ocr": "allowed"},
        loop_budget={"max_passes": 3, "stop_condition": "close_or_leave_explicit_pending_reason"},
    )
    assert bundle["tool_name"] == "multimodal_context_refinement_tool"
    assert bundle["source_record"]["task_intent"] == "ppt_support"
    assert bundle["loop_state"]["next_focus"] is None
    validate_multimodal_context_bundle(bundle)


def test_build_bundle_from_example_record() -> None:
    example = load_example_record("image23_portfolio_table")
    bundle = build_bundle_from_example_record(example)
    assert bundle["example_id"] == "image23_portfolio_table"
    assert bundle["normalized_interpretation"]["image_type"] == "table_evidence"
    assert bundle["form_preservation_assessment"]["status"] == "underspecified"
    assert bundle["loop_state"]["next_focus"] == "run_component_or_structure_level_extraction_before_claiming_value_safe_regeneration"


def test_render_bundle_report_contains_core_fields() -> None:
    example = load_example_record("image27_system_diagram")
    bundle = build_bundle_from_example_record(example)
    report = render_bundle_report(bundle, bundle_path="/tmp/example.json")
    assert "# Multimodal Context Bundle Report" in report
    assert "System diagram" in report
    assert "closure_state" in report


def main() -> int:
    test_build_multimodal_context_bundle_minimal()
    test_build_bundle_from_example_record()
    test_render_bundle_report_contains_core_fields()
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
