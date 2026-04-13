from __future__ import annotations

from multimodal_context_refinement_tool_lib import build_bundle_from_example_record, load_example_record
from multimodal_to_ppt_tool_lib import (
    build_ppt_package_from_example_io,
    build_ppt_package_from_input,
    load_example_io,
    render_ppt_package_report,
    validate_ppt_package,
)


def test_build_ppt_package_from_example_io() -> None:
    package = build_ppt_package_from_example_io(load_example_io())
    assert package["mode"] == "example_io_bridge"
    assert len(package["story_plan"]) == 2
    assert [row["slide_no"] for row in package["slide_role_matrix"]] == [1, 5]
    assert [row["target_slide_no"] for row in package["ppt_regeneration_handoff_bundle"]["slides"]] == [1, 5]
    validate_ppt_package(package)


def test_build_ppt_package_from_input() -> None:
    bundles = [
        build_bundle_from_example_record(load_example_record("image27_system_diagram")),
        build_bundle_from_example_record(load_example_record("image23_portfolio_table")),
    ]
    package = build_ppt_package_from_input(
        {
            "multimodal_context_bundles": bundles,
            "presentation_intent": "portfolio",
            "story_intent": "system_first_with_execution_evidence",
            "slide_plan": {
                "target_slide_count": 2,
                "one_dominant_visual_block_per_slide": True,
                "top_bottom_layout_allowed": True,
            },
            "ppt_authoring_policy": {
                "owner_surface_ref": "<CODEX_HOME>/skills/pptx/SKILL.md",
                "copy_support_ref": "<CLAUDE_SKILLS_ROOT>/semantic-clarity-enhanced/SKILL.md",
            },
            "page_link_matrix_ref": "control/project_domain/resources/manifests/ppt_page_link_matrix_v0_1.json",
        }
    )
    assert package["mode"] == "explicit_bundle_assembly"
    assert len(package["story_plan"]) == 2
    assert package["slide_role_matrix"][0]["visual_type"] == "system_diagram"
    assert package["slide_role_matrix"][1]["visual_type"] == "table_evidence"
    assert "value-level readability" in " ".join(
        package["ppt_regeneration_handoff_bundle"]["slides"][1]["regeneration_handoff"]["preserve"]
    )
    validate_ppt_package(package)


def test_render_ppt_package_report_contains_boundary() -> None:
    package = build_ppt_package_from_example_io(load_example_io())
    report = render_ppt_package_report(package, output_paths={"package_manifest": "/tmp/a.json", "story_plan": "/tmp/b.json", "slide_role_matrix": "/tmp/c.json", "ppt_regeneration_handoff_bundle": "/tmp/d.json"})
    assert "# Multimodal To PPT Tool Package Report" in report
    assert "PPT authoring remains the owner surface" in report


def main() -> int:
    test_build_ppt_package_from_example_io()
    test_build_ppt_package_from_input()
    test_render_ppt_package_report_contains_boundary()
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
