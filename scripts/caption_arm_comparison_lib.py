from __future__ import annotations

import json
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CaptionModeRecord:
    execution_arm: str
    ledger_path: str
    job_id: str
    model: str | None
    prompt_version: str | None
    image_id: str
    source_image_path: str
    status: str
    input_surface: str
    caption: str
    alt_text: str
    context_package_present: bool
    context_review_status: str | None
    ocr_status: str | None
    context_package_json_path: str | None
    context_variant: str | None


COMPARISON_REQUIRED_FIELDS = (
    "execution_arm",
    "ledger_path",
    "job_id",
    "image_id",
    "source_image_path",
    "status",
    "input_surface",
    "caption",
    "alt_text",
    "prompt_version",
)


def load_ledger(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _normalized_path_key(path: str | Path) -> str:
    return unicodedata.normalize("NFC", str(Path(path).resolve()))


def _record_match_paths(record: dict[str, Any]) -> list[str]:
    context_package = record.get("context_package") or {}
    reviewed_component_enrichment = context_package.get("reviewed_component_enrichment") or {}
    candidates = [
        record.get("path"),
        context_package.get("source_image_path"),
        context_package.get("parent_source_image_path"),
        reviewed_component_enrichment.get("parent_source_image_path"),
    ]
    normalized: list[str] = []
    for candidate in candidates:
        if not candidate:
            continue
        normalized_candidate = _normalized_path_key(str(candidate))
        if normalized_candidate not in normalized:
            normalized.append(normalized_candidate)
    return normalized


def find_record_by_source_image_path(ledger: dict[str, Any], source_image_path: str | Path) -> dict[str, Any]:
    normalized_target = _normalized_path_key(source_image_path)
    matches = [
        record
        for record in ledger.get("records", [])
        if normalized_target in _record_match_paths(record)
    ]
    if not matches:
        raise ValueError(f"No record found for source image: {normalized_target}")
    if len(matches) > 1:
        raise ValueError(f"Ambiguous source image match in ledger: {normalized_target}")
    return matches[0]


def _surface_for_record(record: dict[str, Any], fallback: str) -> str:
    context_package = record.get("context_package") or {}
    return str(context_package.get("image_surface") or fallback)


def _comparison_anchor_source_image_path(record: dict[str, Any], requested_source_image_path: str | Path) -> str:
    context_package = record.get("context_package") or {}
    reviewed_component_enrichment = context_package.get("reviewed_component_enrichment") or {}
    preferred = (
        reviewed_component_enrichment.get("parent_source_image_path")
        or context_package.get("parent_source_image_path")
        or requested_source_image_path
    )
    return _normalized_path_key(preferred)


def extract_mode_record(
    *,
    ledger_path: str | Path,
    source_image_path: str | Path,
    execution_arm: str,
    fallback_input_surface: str,
) -> CaptionModeRecord:
    ledger_file = Path(ledger_path).resolve()
    ledger = load_ledger(ledger_file)
    record = find_record_by_source_image_path(ledger, source_image_path)
    context_package = record.get("context_package") or {}
    return CaptionModeRecord(
        execution_arm=execution_arm,
        ledger_path=str(ledger_file),
        job_id=str(record.get("job_id") or ledger.get("job_id") or ""),
        model=ledger.get("model"),
        prompt_version=ledger.get("prompt_version"),
        image_id=str(record.get("image_id") or ""),
        source_image_path=_comparison_anchor_source_image_path(record, source_image_path),
        status=str(record.get("status") or ""),
        input_surface=_surface_for_record(record, fallback_input_surface),
        caption=str(record.get("caption") or ""),
        alt_text=str(record.get("alt_text") or ""),
        context_package_present=bool(record.get("context_package")),
        context_review_status=(
            str(context_package.get("review_status")) if context_package.get("review_status") is not None else None
        ),
        ocr_status=(str(context_package.get("ocr_status")) if context_package.get("ocr_status") is not None else None),
        context_package_json_path=(
            str(context_package.get("context_package_json_path"))
            if context_package.get("context_package_json_path") is not None
            else None
        ),
        context_variant=(
            str(context_package.get("context_variant"))
            if context_package.get("context_variant") is not None
            else None
        ),
    )


def _caption_signals(caption: str) -> dict[str, bool]:
    lower = caption.lower()
    return {
        "mentions_table": "table" in lower,
        "mentions_dh10": "dh@10" in lower,
        "mentions_mrr": "mrr" in lower,
        "mentions_cr10": "cr@10" in lower,
        "mentions_70q": "70q" in lower,
        "mentions_65q": "65q" in lower,
        "mentions_delta": "delta" in lower,
        "mentions_relation": any(
            phrase in lower
            for phrase in (
                "higher than",
                "lower than",
                "greater than",
                "less than",
                "compared with",
                "compared to",
            )
        ),
    }


def _signal_delta(left: dict[str, bool], right: dict[str, bool]) -> dict[str, list[str]]:
    gained = sorted([key for key, value in right.items() if value and not left.get(key, False)])
    lost = sorted([key for key, value in left.items() if value and not right.get(key, False)])
    preserved = sorted([key for key, value in right.items() if value and left.get(key, False)])
    return {"gained": gained, "lost": lost, "preserved": preserved}


def build_comparison_parity_audit(*records: CaptionModeRecord) -> dict[str, Any]:
    if not records:
        raise ValueError("At least one comparison record is required.")

    serialized = [asdict(record) for record in records]
    missing_required_fields: dict[str, list[str]] = {}
    for record in serialized:
        missing = [
            field
            for field in COMPARISON_REQUIRED_FIELDS
            if record.get(field) in (None, "")
        ]
        if missing:
            missing_required_fields[str(record["execution_arm"])] = missing

    source_paths = [str(record["source_image_path"]) for record in serialized]
    image_ids = [str(record["image_id"]) for record in serialized]
    models = [record.get("model") for record in serialized]
    prompt_versions = [record.get("prompt_version") for record in serialized]
    input_surfaces = [record.get("input_surface") for record in serialized]
    review_statuses = [record.get("context_review_status") for record in serialized]
    context_variants = [record.get("context_variant") for record in serialized]
    ocr_statuses = [record.get("ocr_status") for record in serialized]
    context_package_presence = [record.get("context_package_present") for record in serialized]

    same_source_image = len(set(source_paths)) == 1
    same_image_id = len(set(image_ids)) == 1
    same_model = len(set(models)) == 1
    all_required_present = not missing_required_fields
    nonblocking_drift: list[str] = []
    blocking_reasons: list[str] = []

    if not same_image_id:
        nonblocking_drift.append("image_id")
    if len(set(prompt_versions)) > 1:
        nonblocking_drift.append("prompt_version")
    if len(set(input_surfaces)) > 1:
        nonblocking_drift.append("input_surface")
    if len(set(review_statuses)) > 1:
        nonblocking_drift.append("review_status")
    if len(set(context_variants)) > 1:
        nonblocking_drift.append("context_variant")
    if len(set(ocr_statuses)) > 1:
        nonblocking_drift.append("ocr_status")
    if len(set(context_package_presence)) > 1:
        nonblocking_drift.append("context_package_present")
    if not all_required_present:
        blocking_reasons.append("missing_required_fields")
    if not same_source_image:
        blocking_reasons.append("different_source_image")

    return {
        "required_fields": list(COMPARISON_REQUIRED_FIELDS),
        "all_required_present": all_required_present,
        "missing_required_fields": missing_required_fields,
        "same_source_image": same_source_image,
        "same_image_id": same_image_id,
        "same_model": same_model,
        "source_paths": source_paths,
        "image_ids": image_ids,
        "models": models,
        "prompt_versions": prompt_versions,
        "input_surfaces": input_surfaces,
        "review_statuses": review_statuses,
        "context_variants": context_variants,
        "ocr_statuses": ocr_statuses,
        "context_package_presence": context_package_presence,
        "nonblocking_drift": nonblocking_drift,
        "blocking_reasons": blocking_reasons,
        "ready_for_side_by_side_read": all_required_present and same_source_image,
    }


def determine_promotion_gate(context_review_status: str | None) -> dict[str, Any]:
    if context_review_status == "accepted":
        promotion_state = "candidate_ready"
        notes = [
            "The rerun passed the context review gate and can be considered as a promotion candidate.",
            "Keep a bounded comparison record so later multi-arm merges can still trace the pre-promotion baseline.",
        ]
    elif context_review_status == "reviewed_candidate":
        promotion_state = "comparison_ready_reviewed_branch"
        notes = [
            "The rerun passed a reviewed-branch gate and may participate in bounded comparison as a non-default arm.",
            "Keep the baseline active until this reviewed branch is explicitly promoted beyond comparison scope.",
        ]
    elif context_review_status == "pending_review":
        promotion_state = "comparison_only_pending_context_review"
        notes = [
            "Compare the rerun only as bounded evidence until the context package moves beyond pending_review.",
            "Keep the full-image baseline as the default until the rerun path is explicitly accepted.",
        ]
    else:
        promotion_state = "blocked_by_context_review"
        notes = [
            "The rerun is not promotion-ready because its review gate is unresolved.",
            "Keep the baseline active and do not treat this rerun as a default candidate until review metadata is repaired.",
        ]
    return {
        "promotion_state": promotion_state,
        "next_gate": "review_context_package",
        "notes": notes,
    }


def compare_caption_modes(
    baseline: CaptionModeRecord,
    rerun: CaptionModeRecord,
) -> dict[str, Any]:
    baseline_signals = _caption_signals(baseline.caption)
    rerun_signals = _caption_signals(rerun.caption)
    signal_delta = _signal_delta(baseline_signals, rerun_signals)
    parity_audit = build_comparison_parity_audit(baseline, rerun)
    promotion_gate = determine_promotion_gate(rerun.context_review_status)

    return {
        "source_image_path": baseline.source_image_path,
        "same_source_image": baseline.source_image_path == rerun.source_image_path,
        "mode_count": 2,
        "modes": [asdict(baseline), asdict(rerun)],
        "parity_audit": parity_audit,
        "status_summary": {
            "baseline_status": baseline.status,
            "rerun_status": rerun.status,
            "both_completed": baseline.status == "completed" and rerun.status == "completed",
        },
        "signal_comparison": {
            "baseline": baseline_signals,
            "rerun": rerun_signals,
            "delta": signal_delta,
        },
        "promotion_state": promotion_gate["promotion_state"],
        "recommended_current_default": "full_image_baseline",
        "next_gate": promotion_gate["next_gate"],
        "notes": promotion_gate["notes"],
    }


def compare_ready_caption_arms(
    baseline: CaptionModeRecord,
    *candidate_arms: CaptionModeRecord,
) -> dict[str, Any]:
    if not candidate_arms:
        raise ValueError("At least one candidate arm is required.")

    all_records = [baseline, *candidate_arms]
    parity_audit = build_comparison_parity_audit(*all_records)
    signal_comparison: dict[str, Any] = {
        "baseline": _caption_signals(baseline.caption),
        "per_candidate": {},
    }
    per_arm_promotion: dict[str, Any] = {}
    ready_arms = [baseline.execution_arm]
    blocked_arms: list[dict[str, Any]] = []
    next_gates: list[str] = []
    notes: list[str] = []

    for candidate in candidate_arms:
        delta = _signal_delta(_caption_signals(baseline.caption), _caption_signals(candidate.caption))
        signal_comparison["per_candidate"][candidate.execution_arm] = {
            "signals": _caption_signals(candidate.caption),
            "delta_vs_baseline": delta,
        }
        promotion_gate = determine_promotion_gate(candidate.context_review_status)
        per_arm_promotion[candidate.execution_arm] = promotion_gate
        next_gates.append(promotion_gate["next_gate"])
        notes.extend(promotion_gate["notes"])
        if candidate.status == "completed" and promotion_gate["promotion_state"] != "blocked_by_context_review":
            ready_arms.append(candidate.execution_arm)
        else:
            blocked_arms.append(
                {
                    "execution_arm": candidate.execution_arm,
                    "status": candidate.status,
                    "promotion_state": promotion_gate["promotion_state"],
                }
            )

    unique_notes: list[str] = []
    for note in notes:
        if note not in unique_notes:
            unique_notes.append(note)

    ready_for_comparison = parity_audit["ready_for_side_by_side_read"] and not blocked_arms

    return {
        "source_image_path": baseline.source_image_path,
        "same_source_image": all(
            record.source_image_path == baseline.source_image_path for record in candidate_arms
        ),
        "mode_count": len(all_records),
        "modes": [asdict(record) for record in all_records],
        "parity_audit": parity_audit,
        "status_summary": {
            "baseline_status": baseline.status,
            "all_completed": all(record.status == "completed" for record in all_records),
            "ready_arm_count": len(ready_arms),
            "blocked_arm_count": len(blocked_arms),
        },
        "signal_comparison": signal_comparison,
        "per_arm_promotion": per_arm_promotion,
        "ready_arms": ready_arms,
        "blocked_arms": blocked_arms,
        "comparison_scope": "ready_arm_anchor",
        "recommended_current_default": baseline.execution_arm,
        "next_gate": "review_context_package" if next_gates else "none",
        "comparison_ready": ready_for_comparison,
        "notes": unique_notes,
    }


def build_eval_bundle_from_comparison(comparison: dict[str, Any]) -> dict[str, Any]:
    modes = comparison.get("modes", [])
    return {
        "bundle_name": "phase0_caption_eval_bundle",
        "bundle_version": "v1",
        "source_image_path": comparison["source_image_path"],
        "mode_count": comparison["mode_count"],
        "comparison_scope": comparison.get("comparison_scope", "two_mode"),
        "comparison_ready": comparison.get("comparison_ready", False),
        "recommended_current_default": comparison["recommended_current_default"],
        "next_gate": comparison["next_gate"],
        "ready_arms": comparison.get("ready_arms", [modes[0]["execution_arm"]] if modes else []),
        "blocked_arms": comparison.get("blocked_arms", []),
        "parity_audit": comparison["parity_audit"],
        "per_arm_promotion": comparison.get("per_arm_promotion", {}),
        "arms": [
            {
                "execution_arm": mode["execution_arm"],
                "status": mode["status"],
                "ledger_path": mode["ledger_path"],
                "model": mode.get("model"),
                "prompt_version": mode.get("prompt_version"),
                "image_id": mode.get("image_id"),
                "source_image_path": mode.get("source_image_path"),
                "input_surface": mode.get("input_surface"),
                "context_variant": mode.get("context_variant"),
                "context_review_status": mode.get("context_review_status"),
                "ocr_status": mode.get("ocr_status"),
                "context_package_present": mode.get("context_package_present"),
                "context_package_json_path": mode.get("context_package_json_path"),
                "caption": mode.get("caption"),
                "alt_text": mode.get("alt_text"),
            }
            for mode in modes
        ],
    }


def render_eval_bundle_report(bundle: dict[str, Any], *, title: str) -> str:
    lines = [
        f"# {title}",
        "",
        "## Scope",
        "",
        f"- source_image_path: `{bundle['source_image_path']}`",
        f"- mode_count: `{bundle['mode_count']}`",
        f"- comparison_scope: `{bundle['comparison_scope']}`",
        f"- comparison_ready: `{bundle['comparison_ready']}`",
        f"- recommended_current_default: `{bundle['recommended_current_default']}`",
        f"- next_gate: `{bundle['next_gate']}`",
        "",
        "## Ready Arms",
        "",
        f"- ready_arms: `{', '.join(bundle['ready_arms']) or 'none'}`",
        f"- blocked_arms: `{', '.join([item['execution_arm'] for item in bundle['blocked_arms']]) or 'none'}`",
        "",
        "## Parity Audit",
        "",
        f"- ready_for_side_by_side_read: `{bundle['parity_audit']['ready_for_side_by_side_read']}`",
        f"- same_source_image: `{bundle['parity_audit']['same_source_image']}`",
        f"- same_model: `{bundle['parity_audit']['same_model']}`",
        f"- nonblocking_drift: `{', '.join(bundle['parity_audit']['nonblocking_drift']) or 'none'}`",
        f"- blocking_reasons: `{', '.join(bundle['parity_audit']['blocking_reasons']) or 'none'}`",
        "",
        "## Arms",
        "",
    ]
    for arm in bundle["arms"]:
        lines.extend(
            [
                f"### {arm['execution_arm']}",
                "",
                f"- status: `{arm['status']}`",
                f"- input_surface: `{arm['input_surface']}`",
                f"- prompt_version: `{arm['prompt_version'] or 'n/a'}`",
                f"- context_variant: `{arm['context_variant'] or 'n/a'}`",
                f"- context_review_status: `{arm['context_review_status'] or 'n/a'}`",
                f"- ocr_status: `{arm['ocr_status'] or 'n/a'}`",
                "",
                arm["caption"] or "_empty_",
                "",
            ]
        )
    return "\n".join(lines)


def render_comparison_report(comparison: dict[str, Any]) -> str:
    baseline = comparison["modes"][0]
    rerun = comparison["modes"][1]
    delta = comparison["signal_comparison"]["delta"]
    lines = [
        "# Phase 0 Two-Mode Caption Comparison",
        "",
        "## Scope",
        "",
        "- source image path: "
        f"`{comparison['source_image_path']}`",
        "- modes compared: `full_image_baseline` vs `full_image_ocr_context_rerun`",
        "",
        "## Status",
        "",
        f"- same_source_image: `{comparison['same_source_image']}`",
        f"- both_completed: `{comparison['status_summary']['both_completed']}`",
        f"- promotion_state: `{comparison['promotion_state']}`",
        f"- recommended_current_default: `{comparison['recommended_current_default']}`",
        f"- next_gate: `{comparison['next_gate']}`",
        "",
        "## Parity Audit",
        "",
        f"- ready_for_side_by_side_read: `{comparison['parity_audit']['ready_for_side_by_side_read']}`",
        f"- all_required_present: `{comparison['parity_audit']['all_required_present']}`",
        f"- same_image_id: `{comparison['parity_audit']['same_image_id']}`",
        f"- same_model: `{comparison['parity_audit']['same_model']}`",
        f"- prompt_versions: `{', '.join([value or 'n/a' for value in comparison['parity_audit']['prompt_versions']])}`",
        f"- input_surfaces: `{', '.join([value or 'n/a' for value in comparison['parity_audit']['input_surfaces']])}`",
        f"- context_variants: `{', '.join([value or 'n/a' for value in comparison['parity_audit']['context_variants']])}`",
        f"- ocr_statuses: `{', '.join([value or 'n/a' for value in comparison['parity_audit']['ocr_statuses']])}`",
        f"- nonblocking_drift: `{', '.join(comparison['parity_audit']['nonblocking_drift']) or 'none'}`",
        f"- blocking_reasons: `{', '.join(comparison['parity_audit']['blocking_reasons']) or 'none'}`",
        "",
        "## Baseline Mode",
        "",
        f"- execution_arm: `{baseline['execution_arm']}`",
        f"- ledger_path: `{baseline['ledger_path']}`",
        f"- input_surface: `{baseline['input_surface']}`",
        f"- prompt_version: `{baseline['prompt_version']}`",
        "",
        baseline["caption"] or "_empty_",
        "",
        "## Rerun Mode",
        "",
        f"- execution_arm: `{rerun['execution_arm']}`",
        f"- ledger_path: `{rerun['ledger_path']}`",
        f"- input_surface: `{rerun['input_surface']}`",
        f"- prompt_version: `{rerun['prompt_version']}`",
        f"- context_package_present: `{rerun['context_package_present']}`",
        f"- context_review_status: `{rerun['context_review_status'] or 'n/a'}`",
        f"- ocr_status: `{rerun['ocr_status'] or 'n/a'}`",
        "",
        rerun["caption"] or "_empty_",
        "",
        "## Signal Delta",
        "",
        f"- gained: `{', '.join(delta['gained']) or 'none'}`",
        f"- lost: `{', '.join(delta['lost']) or 'none'}`",
        f"- preserved: `{', '.join(delta['preserved']) or 'none'}`",
        "",
        "## Interpretation",
        "",
        "- This comparison is comparison-only evidence until the context package review gate closes.",
        "- The rerun can add useful relation/detail signals without yet replacing the baseline automatically.",
        "- Keep the full-image baseline as the active default until reviewed context packages are accepted.",
        "",
    ]
    return "\n".join(lines)


def render_multi_mode_comparison_report(comparison: dict[str, Any], *, title: str) -> str:
    lines = [
        f"# {title}",
        "",
        "## Scope",
        "",
        f"- source image path: `{comparison['source_image_path']}`",
        f"- mode_count: `{comparison['mode_count']}`",
        "",
        "## Status",
        "",
        f"- same_source_image: `{comparison['same_source_image']}`",
        f"- all_completed: `{comparison['status_summary']['all_completed']}`",
        f"- ready_arm_count: `{comparison['status_summary']['ready_arm_count']}`",
        f"- blocked_arm_count: `{comparison['status_summary']['blocked_arm_count']}`",
        f"- comparison_ready: `{comparison['comparison_ready']}`",
        f"- recommended_current_default: `{comparison['recommended_current_default']}`",
        f"- next_gate: `{comparison['next_gate']}`",
        "",
        "## Parity Audit",
        "",
        f"- ready_for_side_by_side_read: `{comparison['parity_audit']['ready_for_side_by_side_read']}`",
        f"- all_required_present: `{comparison['parity_audit']['all_required_present']}`",
        f"- same_model: `{comparison['parity_audit']['same_model']}`",
        f"- context_variants: `{', '.join([value or 'n/a' for value in comparison['parity_audit']['context_variants']])}`",
        f"- ocr_statuses: `{', '.join([value or 'n/a' for value in comparison['parity_audit']['ocr_statuses']])}`",
        f"- nonblocking_drift: `{', '.join(comparison['parity_audit']['nonblocking_drift']) or 'none'}`",
        f"- blocking_reasons: `{', '.join(comparison['parity_audit']['blocking_reasons']) or 'none'}`",
        "",
        "## Arms",
        "",
    ]
    for mode in comparison["modes"]:
        lines.extend(
            [
                f"### {mode['execution_arm']}",
                "",
                f"- status: `{mode['status']}`",
                f"- input_surface: `{mode['input_surface']}`",
                f"- prompt_version: `{mode['prompt_version'] or 'n/a'}`",
                f"- context_variant: `{mode.get('context_variant') or 'n/a'}`",
                f"- context_review_status: `{mode.get('context_review_status') or 'n/a'}`",
                "",
                mode["caption"] or "_empty_",
                "",
            ]
        )

    lines.extend(
        [
            "## Per-Arm Promotion",
            "",
        ]
    )
    for execution_arm, gate in comparison["per_arm_promotion"].items():
        lines.extend(
            [
                f"### {execution_arm}",
                "",
                f"- promotion_state: `{gate['promotion_state']}`",
                f"- next_gate: `{gate['next_gate']}`",
                "",
            ]
        )

    lines.extend(
        [
            "## Readiness",
            "",
            f"- ready_arms: `{', '.join(comparison['ready_arms'])}`",
            f"- blocked_arms: `{', '.join([item['execution_arm'] for item in comparison['blocked_arms']]) or 'none'}`",
            "",
            "## Notes",
            "",
        ]
    )
    for note in comparison["notes"]:
        lines.append(f"- {note}")
    if not comparison["notes"]:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


def build_small_batch_candidate_selection(
    *,
    target_image_count: int,
    included_candidates: list[dict[str, Any]],
    excluded_candidates: list[dict[str, Any]],
    default_baseline: str = "full_image_baseline",
    confirmation_policy: str = "evidence_only_default_with_gpt_confirmation_for_edge_cases",
) -> dict[str, Any]:
    included_paths = [str(item["source_image_path"]) for item in included_candidates]
    excluded_paths = [str(item["source_image_path"]) for item in excluded_candidates]
    return {
        "experiment": "phase1_caption_four_mode_small_batch_candidate_selection",
        "status": "completed",
        "target_image_count": target_image_count,
        "confirmation_policy": confirmation_policy,
        "default_baseline": default_baseline,
        "included_candidates": included_candidates,
        "excluded_candidates": excluded_candidates,
        "summary": {
            "included_count": len(included_candidates),
            "excluded_count": len(excluded_candidates),
            "minimum_target_met": len(included_candidates) >= target_image_count,
            "included_source_image_paths": included_paths,
            "excluded_source_image_paths": excluded_paths,
        },
    }


def build_small_batch_bundle_from_candidates(
    *,
    candidate_selection: dict[str, Any],
    included_image_bundles: list[dict[str, Any]],
) -> dict[str, Any]:
    included_bundle_paths = [
        str(item.get("single_image_bundle_path"))
        for item in candidate_selection.get("included_candidates", [])
        if item.get("single_image_bundle_path")
    ]
    included_images = []
    for candidate, bundle in zip(candidate_selection.get("included_candidates", []), included_image_bundles):
        included_images.append(
            {
                "candidate_label": candidate.get("candidate_label"),
                "source_image_path": candidate.get("source_image_path"),
                "single_image_bundle_path": candidate.get("single_image_bundle_path"),
                "gpt_visual_confirmation": candidate.get("gpt_visual_confirmation"),
                "four_arm_readiness": candidate.get("four_arm_readiness"),
                "bundle_summary": {
                    "bundle_name": bundle.get("bundle_name"),
                    "mode_count": bundle.get("mode_count"),
                    "comparison_ready": bundle.get("comparison_ready"),
                    "recommended_current_default": bundle.get("recommended_current_default"),
                    "ready_arms": bundle.get("ready_arms", []),
                    "blocked_arms": bundle.get("blocked_arms", []),
                },
            }
        )
    excluded_images = [
        {
            "candidate_label": item.get("candidate_label"),
            "source_image_path": item.get("source_image_path"),
            "decision": item.get("decision"),
            "decision_reason": item.get("decision_reason"),
            "gpt_visual_confirmation": item.get("gpt_visual_confirmation"),
            "four_arm_readiness": item.get("four_arm_readiness"),
        }
        for item in candidate_selection.get("excluded_candidates", [])
    ]
    return {
        "bundle_name": "phase1_caption_four_mode_small_batch_bundle",
        "bundle_version": "v1",
        "status": "completed",
        "target_image_count": candidate_selection["target_image_count"],
        "included_image_count": len(included_images),
        "excluded_image_count": len(excluded_images),
        "minimum_target_met": candidate_selection["summary"]["minimum_target_met"],
        "confirmation_policy": candidate_selection["confirmation_policy"],
        "default_baseline": candidate_selection["default_baseline"],
        "included_bundle_paths": included_bundle_paths,
        "included_images": included_images,
        "excluded_images": excluded_images,
        "next_step": (
            "Consume this bundle in a no-human-review auto-eval lane if minimum_target_met is true; "
            "otherwise expand frozen parser/reviewed-component artifacts for excluded table-centric images first."
        ),
    }


def render_small_batch_readiness_report(
    candidate_selection: dict[str, Any],
    batch_bundle: dict[str, Any],
    *,
    title: str,
) -> str:
    lines = [
        f"# {title}",
        "",
        "## Summary",
        "",
        f"- target_image_count: `{candidate_selection['target_image_count']}`",
        f"- included_image_count: `{candidate_selection['summary']['included_count']}`",
        f"- excluded_image_count: `{candidate_selection['summary']['excluded_count']}`",
        f"- minimum_target_met: `{candidate_selection['summary']['minimum_target_met']}`",
        f"- confirmation_policy: `{candidate_selection['confirmation_policy']}`",
        f"- default_baseline: `{candidate_selection['default_baseline']}`",
        "",
        "## Included Candidates",
        "",
    ]
    for item in candidate_selection.get("included_candidates", []):
        lines.extend(
            [
                f"### {item.get('candidate_label')}",
                "",
                f"- source_image_path: `{item.get('source_image_path')}`",
                f"- decision: `{item.get('decision')}`",
                f"- decision_reason: `{item.get('decision_reason')}`",
                f"- single_image_bundle_path: `{item.get('single_image_bundle_path') or 'n/a'}`",
                f"- gpt_visual_confirmation_status: `{(item.get('gpt_visual_confirmation') or {}).get('status', 'n/a')}`",
                "",
            ]
        )
        for arm_name, arm_state in (item.get("four_arm_readiness") or {}).items():
            lines.append(f"- {arm_name}: `{arm_state}`")
        lines.append("")
    if not candidate_selection.get("included_candidates"):
        lines.extend(["- none", ""])

    lines.extend(["## Excluded Candidates", ""])
    for item in candidate_selection.get("excluded_candidates", []):
        lines.extend(
            [
                f"### {item.get('candidate_label')}",
                "",
                f"- source_image_path: `{item.get('source_image_path')}`",
                f"- decision: `{item.get('decision')}`",
                f"- decision_reason: `{item.get('decision_reason')}`",
                f"- gpt_visual_confirmation_status: `{(item.get('gpt_visual_confirmation') or {}).get('status', 'n/a')}`",
                "",
            ]
        )
        for arm_name, arm_state in (item.get("four_arm_readiness") or {}).items():
            lines.append(f"- {arm_name}: `{arm_state}`")
        lines.append("")
    if not candidate_selection.get("excluded_candidates"):
        lines.extend(["- none", ""])

    lines.extend(
        [
            "## Bundle",
            "",
            f"- bundle_name: `{batch_bundle['bundle_name']}`",
            f"- included_image_count: `{batch_bundle['included_image_count']}`",
            f"- excluded_image_count: `{batch_bundle['excluded_image_count']}`",
            f"- minimum_target_met: `{batch_bundle['minimum_target_met']}`",
            "",
            "## Next Step",
            "",
            f"- {batch_bundle['next_step']}",
            "",
        ]
    )
    return "\n".join(lines)
