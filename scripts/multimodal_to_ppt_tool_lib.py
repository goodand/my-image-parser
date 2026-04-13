from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_EXAMPLE_IO_JSON = (
    ROOT_DIR
    / "control"
    / "project_domain"
    / "resources"
    / "manifests"
    / "multimodal_to_ppt_tool_example_io_v0_1_at2026_04_13.json"
)

BAND8_OWNER_REF = "<CLAUDE_SKILLS_ROOT>/Skills-Create-Project/multimodal-evidence-refinement-loop/SKILL.md"
BAND8_SPECIALIST_REF = "<CLAUDE_SKILLS_ROOT>/Skills-Create-Project/image-text-cot-review/SKILL.md"
MCP_LIFECYCLE_OWNER_REF = "skills/vendored-mcp-onboarding/SKILL.md"
DEFAULT_PPTX_OWNER_REF = "<CODEX_HOME>/skills/pptx/SKILL.md"
DEFAULT_COPY_SUPPORT_REF = "<CLAUDE_SKILLS_ROOT>/semantic-clarity-enhanced/SKILL.md"
SLIDES_GRAB_LOCAL_CLONE_REF = (
    "<EXTERNAL_REVIEW_SURFACE_ROOT>/control/team/resources/external_repos/slides-grab"
)
SLIDES_GRAB_SKILL_REF = (
    "<EXTERNAL_REVIEW_SURFACE_ROOT>/control/team/resources/external_repos/slides-grab/skills/slides-grab/SKILL.md"
)
SLIDES_GRAB_EXPORT_SKILL_REF = (
    "<EXTERNAL_REVIEW_SURFACE_ROOT>/control/team/resources/external_repos/slides-grab/skills/slides-grab-export/SKILL.md"
)
SLIDES_GRAB_UPSTREAM_REPO = "https://github.com/vkehfdl1/slides-grab"

ROLE_BY_IMAGE_TYPE = {
    "system_diagram": "architecture_hero",
    "ui_screenshot_pair": "product_configuration_ui",
    "profile_summary_plus_portrait": "profile_summary",
    "code_and_problem_screen": "problem_and_code_proof",
    "table_evidence": "portfolio_evidence_table",
    "workflow_ui": "applied_ai_workflow_ui",
}

TITLE_BY_IMAGE_TYPE = {
    "system_diagram": "시스템을 구조로 설계하고 증명합니다",
    "ui_screenshot_pair": "입력과 결과가 한 흐름으로 이어집니다",
    "profile_summary_plus_portrait": "개인 맥락이 신뢰를 만듭니다",
    "code_and_problem_screen": "문제와 구현을 한 화면에 둡니다",
    "table_evidence": "프로젝트 표가 실행 이력을 증명합니다",
    "workflow_ui": "적용형 AI 흐름을 끝까지 닫습니다",
}

TEXT_GOAL_BY_IMAGE_TYPE = {
    "system_diagram": "시스템 사고가 첫 인상으로 보이도록 만든다.",
    "ui_screenshot_pair": "설정 화면과 결과 화면이 하나의 경험으로 이어진다는 점을 보여준다.",
    "profile_summary_plus_portrait": "정리된 이력과 실제 인물 이미지가 함께 신뢰도를 만든다는 점을 강조한다.",
    "code_and_problem_screen": "문제 해결형 개발자라는 점을 시각 증거로 보여준다.",
    "table_evidence": "실행 범위와 지속성을 포트폴리오 증거 표로 보여준다.",
    "workflow_ui": "실험 결과를 실제 사용 흐름으로 이어 붙일 수 있다는 점을 강조한다.",
}

LAYOUT_BY_IMAGE_TYPE = {
    "system_diagram": "top_header_large_diagram_bottom_notes",
    "ui_screenshot_pair": "top_header_pair_ui_bottom_notes",
    "profile_summary_plus_portrait": "top_header_profile_band_bottom_notes",
    "code_and_problem_screen": "top_header_full_problem_code_bottom_notes",
    "table_evidence": "top_header_full_table_bottom_notes",
    "workflow_ui": "top_header_tall_ui_bottom_notes",
}

PRESERVE_BY_IMAGE_TYPE = {
    "system_diagram": [
        "keep the architecture diagram as the dominant visual block",
        "preserve node labels and flow boundaries as one structured whole",
    ],
    "ui_screenshot_pair": [
        "keep the input UI and the generated-output UI as one paired flow",
        "preserve visible UI labels and spacing cues that make the before/after relationship obvious",
    ],
    "profile_summary_plus_portrait": [
        "keep the summary page dominant and the portrait supportive",
        "preserve the sense that profile data and real identity belong to one portfolio story",
    ],
    "code_and_problem_screen": [
        "preserve the problem statement and implementation as one proof surface",
        "keep code readable enough that the slide still functions as implementation evidence",
    ],
    "table_evidence": [
        "preserve the table as the dominant visual block",
        "preserve row, column, and value-level readability rather than reducing the slide to a table-presence claim",
    ],
    "workflow_ui": [
        "preserve the main interaction region as the dominant visual block",
        "preserve the visible workflow cues so the slide reads as applied usage rather than tool branding",
    ],
}

MANUAL_BY_IMAGE_TYPE = {
    "system_diagram": [
        "do not overcompress labels until the system diagram loses legibility",
        "if copy changes, keep the slide system-first rather than product-first",
    ],
    "ui_screenshot_pair": [
        "if one UI must be reduced, keep the pair readable rather than enlarging one side only",
        "avoid rewriting this slide into generic product marketing copy",
    ],
    "profile_summary_plus_portrait": [
        "do not turn the portrait into the hero at the expense of the profile summary",
        "keep the slide image-led and credibility-oriented",
    ],
    "code_and_problem_screen": [
        "if the slide is tightened, protect the problem/solution pairing first",
        "do not reduce the code block until it loses proof value",
    ],
    "table_evidence": [
        "table-internal values must remain legible after any regeneration step",
        "do not collapse this slide into a generic summary if the table stops being readable",
    ],
    "workflow_ui": [
        "if copy changes, keep the slide about applied workflow closure rather than tool listing",
        "do not crop out the main interaction region",
    ],
}


def iso_timestamp() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: str | Path, payload: Any) -> None:
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _truncate_sentence(text: str, *, limit: int = 64) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 1].rstrip() + "…"


def _normalize_source_slide_numbers(values: Any) -> list[dict[str, int]]:
    if not values:
        return []
    if all(isinstance(item, dict) and "slide" in item for item in values):
        normalized: list[dict[str, int]] = []
        for item in values:
            slide_no = int(item["slide"])
            occurrence = int(item.get("occurrence", 1))
            normalized.append({"slide": slide_no, "occurrence": occurrence})
        return normalized
    if all(isinstance(item, int) for item in values):
        counts = Counter(values)
        emitted: dict[int, int] = {}
        normalized = []
        for slide_no in values:
            emitted[slide_no] = emitted.get(slide_no, 0) + 1
            normalized.append({"slide": slide_no, "occurrence": emitted[slide_no]})
        return normalized
    raise ValueError("source slide numbers must be all ints or all mapping objects.")


def _path_basename(path: str) -> str:
    return Path(path).name


def _parse_selector_ref(ref: str) -> tuple[Path, str | None, str | None]:
    raw_path, _, selector = ref.partition("#")
    selector_key = None
    selector_value = None
    if selector:
        selector_key, _, selector_value = selector.partition("=")
    return ROOT_DIR / raw_path, selector_key or None, selector_value or None


def _select_from_role_matrix_refs(role_matrix_refs: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ref in role_matrix_refs:
        path, selector_key, selector_value = _parse_selector_ref(ref)
        matrix = load_json(path)
        if not isinstance(matrix, list):
            raise ValueError(f"role matrix ref is not a list payload: {ref}")
        if selector_key is None:
            rows.extend(matrix)
            continue
        for row in matrix:
            if str(row.get(selector_key)) == selector_value:
                rows.append(row)
                break
        else:
            raise ValueError(f"selector did not match any role matrix row: {ref}")
    return rows


def _filter_handoff_bundle(
    handoff_ref: dict[str, Any], *, example_status: str | None = None
) -> dict[str, Any]:
    path = ROOT_DIR / handoff_ref["path"]
    selected_slide_nos = set(handoff_ref.get("selected_target_slide_nos", []))
    bundle = load_json(path)
    bundle["slides"] = [
        slide for slide in bundle.get("slides", []) if slide.get("target_slide_no") in selected_slide_nos
    ]
    bundle["selected_target_slide_nos"] = sorted(selected_slide_nos)
    if example_status:
        bundle["bundle_status"] = example_status
    bundle["source_truth"]["derived_from_ref"] = handoff_ref["path"]
    return bundle


def _infer_title(bundle: dict[str, Any], slide_no: int) -> str:
    image_type = bundle["normalized_interpretation"].get("image_type")
    if image_type in TITLE_BY_IMAGE_TYPE:
        return TITLE_BY_IMAGE_TYPE[image_type]
    summary = bundle["normalized_interpretation"].get("form_bearing_summary") or bundle["normalized_interpretation"].get(
        "candidate_caption"
    )
    if summary:
        return _truncate_sentence(str(summary), limit=36)
    return f"Slide {slide_no}"


def _infer_portfolio_role(image_type: str | None) -> str:
    if image_type and image_type in ROLE_BY_IMAGE_TYPE:
        return ROLE_BY_IMAGE_TYPE[image_type]
    return "image_evidence"


def _infer_layout_role(image_type: str | None) -> str:
    if image_type and image_type in LAYOUT_BY_IMAGE_TYPE:
        return LAYOUT_BY_IMAGE_TYPE[image_type]
    return "top_header_full_image_bottom_notes"


def _infer_text_goal(image_type: str | None, bundle: dict[str, Any]) -> str:
    if image_type and image_type in TEXT_GOAL_BY_IMAGE_TYPE:
        return TEXT_GOAL_BY_IMAGE_TYPE[image_type]
    summary = bundle["normalized_interpretation"].get("form_bearing_summary")
    if summary:
        return _truncate_sentence(str(summary), limit=80)
    return "이미지 증거가 먼저 읽히도록 supporting text를 제한한다."


def _derive_bundle_status(bundle: dict[str, Any]) -> str:
    assessment = bundle.get("form_preservation_assessment", {})
    loop_state = bundle.get("loop_state", {})
    if assessment.get("status") == "enough_for_downstream":
        return "ready_for_manual_regeneration_with_text_promotion_pending"
    if loop_state.get("closure_state") == "closed":
        return "manual_regeneration_gate_required"
    return "pending_additional_context_before_regeneration"


def _derive_manual_remaining(bundle: dict[str, Any], image_type: str | None) -> list[str]:
    assessment = bundle.get("form_preservation_assessment", {})
    loop_state = bundle.get("loop_state", {})
    manual = list(MANUAL_BY_IMAGE_TYPE.get(image_type or "", []))
    if assessment.get("value_level_coverage_status") not in (None, "achieved", "not_applicable"):
        manual.append("confirm value-level readability before approving the regenerated PPT surface")
    for reason in loop_state.get("pending_reasons", []):
        manual.append(f"pending_reason:{reason}")
    unresolved = loop_state.get("unresolved_fields", [])
    if unresolved:
        manual.append(f"unresolved_fields:{', '.join(unresolved)}")
    return manual


def _derive_source_images(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    source_path = bundle["source_record"]["source_image_path"]
    source_slides = bundle["source_record"].get("baseline_context", {}).get("source_slide_numbers", [])
    return [
        {
            "role": "primary",
            "path": source_path,
            "source_slide_numbers": [item["slide"] for item in _normalize_source_slide_numbers(source_slides)],
        }
    ]


def build_story_plan_from_bundles(
    bundles: list[dict[str, Any]],
    *,
    presentation_intent: str,
    story_intent: str | None,
) -> list[dict[str, Any]]:
    story_plan = []
    for index, bundle in enumerate(bundles, start=1):
        title = _infer_title(bundle, index)
        story_plan.append(
            {
                "slide_no": index,
                "title": title,
                "source_image_path": bundle["source_record"]["source_image_path"],
                "image_type": bundle["normalized_interpretation"].get("image_type"),
                "presentation_intent": presentation_intent,
                "story_intent": story_intent,
                "reason": bundle["normalized_interpretation"].get("form_bearing_summary")
                or bundle["normalized_interpretation"].get("candidate_caption"),
            }
        )
    return story_plan


def build_slide_role_matrix_from_bundles(
    bundles: list[dict[str, Any]], *, slide_plan: dict[str, Any]
) -> list[dict[str, Any]]:
    rows = []
    top_bottom_split = bool(slide_plan.get("top_bottom_layout_allowed"))
    for index, bundle in enumerate(bundles, start=1):
        image_type = bundle["normalized_interpretation"].get("image_type")
        rows.append(
            {
                "slide_no": index,
                "slide_title": _infer_title(bundle, index),
                "visual_type": image_type,
                "image_filename": _path_basename(bundle["source_record"]["source_image_path"]),
                "support_images": [],
                "portfolio_role": _infer_portfolio_role(image_type),
                "source_slide_numbers": _normalize_source_slide_numbers(
                    bundle["source_record"].get("baseline_context", {}).get("source_slide_numbers", [])
                ),
                "supporting_text_goal": _infer_text_goal(image_type, bundle),
                "layout_role": _infer_layout_role(image_type),
                "top_bottom_split": top_bottom_split,
                "bundle_status": _derive_bundle_status(bundle),
                "bundle_manual_remaining": _derive_manual_remaining(bundle, image_type),
            }
        )
    return rows


def build_handoff_bundle_from_bundles(
    bundles: list[dict[str, Any]],
    *,
    presentation_intent: str,
    story_intent: str | None,
    slide_plan: dict[str, Any],
    ppt_authoring_policy: dict[str, Any],
    page_link_matrix_ref: str | None = None,
    existing_deck_ref: str | None = None,
    review_index_ref: str | None = None,
    visual_qa_report_ref: str | None = None,
) -> dict[str, Any]:
    slides = []
    manual_gates: list[str] = []
    for index, bundle in enumerate(bundles, start=1):
        image_type = bundle["normalized_interpretation"].get("image_type")
        slide_manual_remaining = _derive_manual_remaining(bundle, image_type)
        if slide_manual_remaining:
            manual_gates.extend(slide_manual_remaining)
        slides.append(
            {
                "target_slide_no": index,
                "target_slide_title": _infer_title(bundle, index),
                "presentation_role": _infer_portfolio_role(image_type),
                "visual_type": image_type,
                "source_images": _derive_source_images(bundle),
                "current_pages": {
                    "source": [bundle["source_record"]["source_image_path"]],
                    "evidence": [
                        bundle["source_record"].get("baseline_context", {}).get("caption_review_ref")
                    ]
                    if bundle["source_record"].get("baseline_context", {}).get("caption_review_ref")
                    else [],
                    "loop_review": [f"context_bundle:{_path_basename(bundle['source_record']['source_image_path'])}"],
                    "ppt_target": [],
                    "publication": [review_index_ref] if review_index_ref else [],
                },
                "text_promotion_state": {
                    "approved_caption": "candidate_only_not_human_promoted",
                    "approved_alt_text": "candidate_only_not_human_promoted",
                    "candidate_caption": bundle["normalized_interpretation"].get("candidate_caption"),
                    "candidate_alt_text": bundle["normalized_interpretation"].get("candidate_alt_text"),
                    "current_basis": "multimodal_context_bundle",
                },
                "regeneration_handoff": {
                    "authoring_mode": "build_or_edit_via_pptx_surface",
                    "supporting_text_goal": _infer_text_goal(image_type, bundle),
                    "layout_role": _infer_layout_role(image_type),
                    "crop_required": False,
                    "preserve": list(PRESERVE_BY_IMAGE_TYPE.get(image_type or "", [])),
                    "manual_remaining": slide_manual_remaining,
                },
            }
        )

    bundle_status = (
        "ready_for_manual_regeneration_with_text_promotion_pending"
        if all(
            bundle.get("form_preservation_assessment", {}).get("status") == "enough_for_downstream"
            for bundle in bundles
        )
        else "manual_regeneration_gate_required"
    )
    return {
        "version": "0.1",
        "generated_at": iso_timestamp(),
        "scope": f"{presentation_intent}_{story_intent or 'default'}",
        "bundle_kind": "ppt_regeneration_handoff",
        "bundle_status": bundle_status,
        "source_truth": {
            "page_link_matrix": page_link_matrix_ref,
            "existing_deck": existing_deck_ref,
            "review_index": review_index_ref,
            "qa_report": visual_qa_report_ref,
        },
        "routing": {
            "band8_owner_ref": BAND8_OWNER_REF,
            "band8_specialist_ref": BAND8_SPECIALIST_REF,
            "mcp_lifecycle_owner_ref": MCP_LIFECYCLE_OWNER_REF,
            "ppt_authoring_surface_ref": ppt_authoring_policy.get("owner_surface_ref", DEFAULT_PPTX_OWNER_REF),
            "claude_copy_support_ref": ppt_authoring_policy.get(
                "copy_support_ref", DEFAULT_COPY_SUPPORT_REF
            ),
        },
        "external_tool_refs": {
            "slides_grab_local_clone_ref": SLIDES_GRAB_LOCAL_CLONE_REF,
            "slides_grab_skill_ref": SLIDES_GRAB_SKILL_REF,
            "slides_grab_export_skill_ref": SLIDES_GRAB_EXPORT_SKILL_REF,
            "slides_grab_upstream_repo": SLIDES_GRAB_UPSTREAM_REPO,
            "usage_boundary": "reference_only_not_source_of_truth",
        },
        "non_goals": [
            "do not rerun generic multimodal loop by default",
            "do not replace the global pptx authoring owner surface",
            "do not reopen provider onboarding through this tool",
            "do not mutate source image metadata or approval records",
        ],
        "manual_gates": sorted(set(manual_gates)),
        "quality_rules": [
            "one dominant visual block per slide",
            "preserve form when the source image itself is evidence",
            "table-heavy slides must remain readable at value level",
            "supporting text must remain image-led",
            "top-bottom layouts are allowed when wide slide geometry improves legibility",
        ],
        "slide_plan": slide_plan,
        "slides": slides,
    }


def _validate_required_mapping(name: str, payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict) or not payload:
        raise ValueError(f"{name} must be a non-empty JSON object.")
    return payload


def _load_context_bundles_from_input(input_payload: dict[str, Any]) -> list[dict[str, Any]]:
    if "multimodal_context_bundles" in input_payload:
        bundles = input_payload["multimodal_context_bundles"]
        if not isinstance(bundles, list) or not bundles:
            raise ValueError("multimodal_context_bundles must be a non-empty list.")
        return bundles
    refs = input_payload.get("multimodal_context_bundle_refs")
    if isinstance(refs, list) and refs:
        return [load_json(ROOT_DIR / ref) for ref in refs]
    raise ValueError("input payload must provide multimodal_context_bundles or multimodal_context_bundle_refs.")


def build_ppt_package_from_input(input_payload: dict[str, Any]) -> dict[str, Any]:
    presentation_intent = str(input_payload.get("presentation_intent", "")).strip()
    if not presentation_intent:
        raise ValueError("presentation_intent must not be empty.")
    slide_plan = _validate_required_mapping("slide_plan", input_payload.get("slide_plan"))
    ppt_authoring_policy = _validate_required_mapping(
        "ppt_authoring_policy", input_payload.get("ppt_authoring_policy")
    )
    bundles = _load_context_bundles_from_input(input_payload)
    target_slide_count = slide_plan.get("target_slide_count")
    if isinstance(target_slide_count, int) and target_slide_count < len(bundles):
        raise ValueError("target_slide_count must be >= number of supplied context bundles.")

    story_intent = input_payload.get("story_intent")
    story_plan = build_story_plan_from_bundles(
        bundles,
        presentation_intent=presentation_intent,
        story_intent=story_intent,
    )
    role_matrix = build_slide_role_matrix_from_bundles(bundles, slide_plan=slide_plan)
    handoff_bundle = build_handoff_bundle_from_bundles(
        bundles,
        presentation_intent=presentation_intent,
        story_intent=story_intent,
        slide_plan=slide_plan,
        ppt_authoring_policy=ppt_authoring_policy,
        page_link_matrix_ref=input_payload.get("page_link_matrix_ref"),
        existing_deck_ref=input_payload.get("existing_deck_ref"),
        review_index_ref=input_payload.get("review_index_ref"),
        visual_qa_report_ref=input_payload.get("visual_qa_report_ref"),
    )
    return {
        "tool_name": "multimodal_to_ppt_tool",
        "generated_at": iso_timestamp(),
        "mode": "explicit_bundle_assembly",
        "input_summary": {
            "presentation_intent": presentation_intent,
            "story_intent": story_intent,
            "bundle_count": len(bundles),
            "page_link_matrix_ref": input_payload.get("page_link_matrix_ref"),
            "existing_deck_ref": input_payload.get("existing_deck_ref"),
        },
        "story_plan": story_plan,
        "slide_role_matrix": role_matrix,
        "ppt_regeneration_handoff_bundle": handoff_bundle,
        "optional_refs": {
            "review_index_ref": input_payload.get("review_index_ref"),
            "visual_qa_report_ref": input_payload.get("visual_qa_report_ref"),
        },
    }


def build_ppt_package_from_example_io(
    example_payload: dict[str, Any],
) -> dict[str, Any]:
    output_example = example_payload["output_example"]
    story_plan = output_example["story_plan"]
    role_matrix = _select_from_role_matrix_refs(output_example["role_matrix_refs"])
    handoff_bundle = _filter_handoff_bundle(
        output_example["ppt_regeneration_handoff_ref"],
        example_status=example_payload.get("status"),
    )
    return {
        "tool_name": "multimodal_to_ppt_tool",
        "generated_at": iso_timestamp(),
        "mode": "example_io_bridge",
        "input_summary": {
            "presentation_intent": example_payload["input_example"].get("presentation_intent"),
            "story_intent": example_payload["input_example"].get("story_intent"),
            "selected_example_ids": example_payload["input_example"].get("selected_example_ids", []),
            "page_link_matrix_ref": example_payload["input_example"].get("page_link_matrix_ref"),
        },
        "story_plan": story_plan,
        "slide_role_matrix": role_matrix,
        "ppt_regeneration_handoff_bundle": handoff_bundle,
        "optional_refs": {
            "existing_deck_ref": output_example.get("optional_regenerated_deck_ref"),
            "review_index_ref": output_example.get("review_index_ref"),
            "visual_qa_report_ref": output_example.get("visual_qa_report_ref"),
        },
        "manual_gates": output_example.get("manual_gates", []),
    }


def load_example_io(path: str | Path = DEFAULT_EXAMPLE_IO_JSON) -> dict[str, Any]:
    payload = load_json(path)
    if not isinstance(payload, dict):
        raise ValueError("example io payload must be an object.")
    return payload


def validate_ppt_package(package: dict[str, Any]) -> None:
    for key in ("tool_name", "generated_at", "mode", "story_plan", "slide_role_matrix", "ppt_regeneration_handoff_bundle"):
        if key not in package:
            raise ValueError(f"package missing required field: {key}")
    if package["tool_name"] != "multimodal_to_ppt_tool":
        raise ValueError("tool_name must be multimodal_to_ppt_tool.")
    if not isinstance(package["story_plan"], list) or not package["story_plan"]:
        raise ValueError("story_plan must be a non-empty list.")
    if not isinstance(package["slide_role_matrix"], list) or not package["slide_role_matrix"]:
        raise ValueError("slide_role_matrix must be a non-empty list.")
    handoff = package["ppt_regeneration_handoff_bundle"]
    if not isinstance(handoff, dict):
        raise ValueError("ppt_regeneration_handoff_bundle must be an object.")
    if handoff.get("bundle_kind") != "ppt_regeneration_handoff":
        raise ValueError("handoff bundle must declare bundle_kind=ppt_regeneration_handoff.")
    if not isinstance(handoff.get("slides"), list) or not handoff["slides"]:
        raise ValueError("handoff bundle must contain non-empty slides.")


def write_ppt_package_outputs(output_dir: str | Path, package: dict[str, Any]) -> dict[str, str]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "package_manifest": output_dir / "ppt_prep_package_manifest.json",
        "story_plan": output_dir / "ppt_story_plan.json",
        "slide_role_matrix": output_dir / "ppt_slide_role_matrix.json",
        "ppt_regeneration_handoff_bundle": output_dir / "ppt_regeneration_handoff_bundle.json",
    }
    write_json(paths["package_manifest"], package)
    write_json(paths["story_plan"], package["story_plan"])
    write_json(paths["slide_role_matrix"], package["slide_role_matrix"])
    write_json(paths["ppt_regeneration_handoff_bundle"], package["ppt_regeneration_handoff_bundle"])
    return {key: str(path) for key, path in paths.items()}


def _story_row_source_label(story_row: dict[str, Any]) -> str:
    source_image_path = story_row.get("source_image_path")
    if source_image_path:
        return Path(str(source_image_path)).name
    source_example_id = story_row.get("source_example_id")
    if source_example_id:
        return str(source_example_id)
    return "unknown-source"


def render_ppt_package_report(package: dict[str, Any], *, output_paths: dict[str, str] | None = None) -> str:
    handoff = package["ppt_regeneration_handoff_bundle"]
    lines = [
        "# Multimodal To PPT Tool Package Report",
        "",
        "## Summary",
        "",
        f"- generated_at: `{package['generated_at']}`",
        f"- mode: `{package['mode']}`",
        f"- presentation_intent: `{package['input_summary'].get('presentation_intent')}`",
        f"- story_intent: `{package['input_summary'].get('story_intent')}`",
        f"- slide_count: `{len(package['story_plan'])}`",
        f"- handoff_bundle_status: `{handoff.get('bundle_status')}`",
    ]
    if output_paths:
        lines.extend(
            [
                "",
                "## Output Paths",
                "",
                f"- package_manifest: `{output_paths['package_manifest']}`",
                f"- story_plan: `{output_paths['story_plan']}`",
                f"- slide_role_matrix: `{output_paths['slide_role_matrix']}`",
                f"- ppt_regeneration_handoff_bundle: `{output_paths['ppt_regeneration_handoff_bundle']}`",
            ]
        )
    lines.extend(["", "## Slides", ""])
    for story_row in package["story_plan"]:
        lines.append(
            f"- slide {story_row['slide_no']}: `{story_row['title']}` from `{_story_row_source_label(story_row)}`"
        )
    manual_gates = package.get("manual_gates") or handoff.get("manual_gates") or []
    lines.extend(["", "## Manual Gates", ""])
    if manual_gates:
        lines.extend([f"- {gate}" for gate in manual_gates])
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This tool emits PPT-prep artifacts only.",
            f"- PPT authoring remains the owner surface: `{handoff['routing']['ppt_authoring_surface_ref']}`.",
            "- The runner does not generate or edit a .pptx deck directly.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"
