from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_EXAMPLES_JSON = (
    ROOT_DIR
    / "control"
    / "project_domain"
    / "resources"
    / "manifests"
    / "multimodal_context_refinement_examples_v0_1_at2026_04_13.json"
)

REQUIRED_SECTIONS = (
    "source_record",
    "evidence_bundle",
    "normalized_interpretation",
    "form_preservation_assessment",
    "loop_state",
)
REQUIRED_LOOP_STATE_FIELDS = (
    "pass_count",
    "closure_state",
    "pending_reasons",
    "unresolved_fields",
    "next_focus",
)
REQUIRED_NORMALIZED_FIELDS = (
    "image_type",
    "form_bearing_summary",
    "candidate_caption",
    "candidate_alt_text",
)


def iso_timestamp() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _ensure_mapping(name: str, payload: dict[str, Any] | None) -> dict[str, Any]:
    if payload is None:
        return {}
    if not isinstance(payload, dict):
        raise ValueError(f"{name} must be a JSON object.")
    return payload


def default_evidence_bundle() -> dict[str, Any]:
    return {
        "source_image_ref": None,
        "whole_image_ocr": {"status": "not_executed", "ref": None},
        "component_crops": {"status": "not_executed", "refs": []},
        "component_ocr": {"status": "not_executed", "refs": []},
        "structure_extraction": {"status": "not_executed", "ref": None},
    }


def default_normalized_interpretation() -> dict[str, Any]:
    return {
        "image_type": None,
        "form_bearing_summary": None,
        "candidate_caption": None,
        "candidate_alt_text": None,
    }


def default_form_preservation_assessment() -> dict[str, Any]:
    return {
        "status": "underspecified",
        "value_level_coverage_status": "unknown",
        "why": "No explicit downstream form-preservation assessment was provided.",
    }


def default_loop_state() -> dict[str, Any]:
    return {
        "pass_count": 1,
        "closure_state": "pending",
        "pending_reasons": [],
        "unresolved_fields": [],
        "next_focus": None,
    }


def build_multimodal_context_bundle(
    *,
    source_image_path: str,
    task_intent: str,
    provider_policy: dict[str, Any],
    loop_budget: dict[str, Any],
    baseline_context: dict[str, Any] | None = None,
    evidence_bundle: dict[str, Any] | None = None,
    normalized_interpretation: dict[str, Any] | None = None,
    form_preservation_assessment: dict[str, Any] | None = None,
    loop_state: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    if not source_image_path.strip():
        raise ValueError("source_image_path must not be empty.")
    if not task_intent.strip():
        raise ValueError("task_intent must not be empty.")
    if not provider_policy:
        raise ValueError("provider_policy must not be empty.")
    if not loop_budget:
        raise ValueError("loop_budget must not be empty.")

    bundle = {
        "version": "0.1",
        "tool_name": "multimodal_context_refinement_tool",
        "generated_at": generated_at or iso_timestamp(),
        "source_record": {
            "source_image_path": source_image_path,
            "task_intent": task_intent,
            "baseline_context": _ensure_mapping("baseline_context", baseline_context),
            "provider_policy": _ensure_mapping("provider_policy", provider_policy),
            "loop_budget": _ensure_mapping("loop_budget", loop_budget),
        },
        "evidence_bundle": default_evidence_bundle(),
        "normalized_interpretation": default_normalized_interpretation(),
        "form_preservation_assessment": default_form_preservation_assessment(),
        "loop_state": default_loop_state(),
    }
    bundle["evidence_bundle"].update(_ensure_mapping("evidence_bundle", evidence_bundle))
    bundle["normalized_interpretation"].update(
        _ensure_mapping("normalized_interpretation", normalized_interpretation)
    )
    bundle["form_preservation_assessment"].update(
        _ensure_mapping("form_preservation_assessment", form_preservation_assessment)
    )
    bundle["loop_state"].update(_ensure_mapping("loop_state", loop_state))
    validate_multimodal_context_bundle(bundle)
    return bundle


def validate_multimodal_context_bundle(bundle: dict[str, Any]) -> None:
    for section in REQUIRED_SECTIONS:
        if section not in bundle or not isinstance(bundle[section], dict):
            raise ValueError(f"bundle missing required section: {section}")

    source_record = bundle["source_record"]
    for key in ("source_image_path", "task_intent", "provider_policy", "loop_budget"):
        if key not in source_record:
            raise ValueError(f"source_record missing required field: {key}")
    if not str(source_record["source_image_path"]).strip():
        raise ValueError("source_record.source_image_path must not be empty.")
    if not str(source_record["task_intent"]).strip():
        raise ValueError("source_record.task_intent must not be empty.")
    if not isinstance(source_record["provider_policy"], dict) or not source_record["provider_policy"]:
        raise ValueError("source_record.provider_policy must be a non-empty object.")
    if not isinstance(source_record["loop_budget"], dict) or not source_record["loop_budget"]:
        raise ValueError("source_record.loop_budget must be a non-empty object.")

    normalized = bundle["normalized_interpretation"]
    for field in REQUIRED_NORMALIZED_FIELDS:
        if field not in normalized:
            raise ValueError(f"normalized_interpretation missing required field: {field}")

    loop_state = bundle["loop_state"]
    for field in REQUIRED_LOOP_STATE_FIELDS:
        if field not in loop_state:
            raise ValueError(f"loop_state missing required field: {field}")
    if not isinstance(loop_state["pending_reasons"], list):
        raise ValueError("loop_state.pending_reasons must be a list.")
    if not isinstance(loop_state["unresolved_fields"], list):
        raise ValueError("loop_state.unresolved_fields must be a list.")


def build_bundle_from_example_record(example_record: dict[str, Any]) -> dict[str, Any]:
    bundle = build_multimodal_context_bundle(
        source_image_path=example_record["source_image_path"],
        task_intent=example_record["task_intent"],
        provider_policy=example_record["provider_policy"],
        loop_budget=example_record["loop_budget"],
        baseline_context=example_record.get("baseline_context"),
        evidence_bundle=example_record.get("evidence_bundle"),
        normalized_interpretation=example_record.get("normalized_interpretation"),
        form_preservation_assessment=example_record.get("form_preservation_assessment"),
        loop_state=example_record.get("loop_state"),
    )
    bundle["example_id"] = example_record.get("example_id")
    return bundle


def load_example_record(example_id: str, examples_path: str | Path = DEFAULT_EXAMPLES_JSON) -> dict[str, Any]:
    payload = load_json(examples_path)
    for example in payload.get("examples", []):
        if example.get("example_id") == example_id:
            return example
    raise ValueError(f"example_id not found: {example_id}")


def render_bundle_report(bundle: dict[str, Any], *, bundle_path: str | None = None) -> str:
    source = bundle["source_record"]
    normalized = bundle["normalized_interpretation"]
    assessment = bundle["form_preservation_assessment"]
    loop_state = bundle["loop_state"]
    lines = [
        "# Multimodal Context Bundle Report",
        "",
        "## Summary",
        "",
        f"- generated_at: `{bundle['generated_at']}`",
        f"- source_image_path: `{source['source_image_path']}`",
        f"- task_intent: `{source['task_intent']}`",
        f"- image_type: `{normalized['image_type']}`",
        f"- closure_state: `{loop_state['closure_state']}`",
        f"- form_preservation_status: `{assessment['status']}`",
    ]
    if bundle_path:
        lines.append(f"- bundle_path: `{bundle_path}`")
    lines.extend(
        [
            "",
            "## Candidate Interpretation",
            "",
            f"- candidate_caption: `{normalized['candidate_caption']}`",
            f"- candidate_alt_text: `{normalized['candidate_alt_text']}`",
            "",
            "## Form Preservation",
            "",
            f"- value_level_coverage_status: `{assessment.get('value_level_coverage_status')}`",
            f"- why: `{assessment.get('why')}`",
            "",
            "## Loop State",
            "",
            f"- pass_count: `{loop_state['pass_count']}`",
            f"- pending_reasons: `{', '.join(loop_state['pending_reasons']) or 'none'}`",
            f"- unresolved_fields: `{', '.join(loop_state['unresolved_fields']) or 'none'}`",
            f"- next_focus: `{loop_state['next_focus']}`",
            "",
        ]
    )
    return "\n".join(lines) + "\n"
