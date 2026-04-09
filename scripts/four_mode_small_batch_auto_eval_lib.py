from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


METRIC_TOKENS = ("dh@10", "mrr", "cr@10")
RELATION_TOKENS = (
    "higher than",
    "lower than",
    "greater than",
    "less than",
    "higher for all metrics",
    "higher values for all metrics",
)
TITLE_TOKENS = (
    "two-phase hyde-pc",
    "오류 5건 제외",
)


@dataclass(frozen=True)
class ArmAutoScore:
    execution_arm: str
    promotion_state: str
    default_ready: bool
    metric_mention_coverage: float
    comparative_relation_signal: float
    caption_completeness: float
    title_context_fidelity: float
    parser_structure_support: float
    ocr_evidence_support: float
    non_table_noise_suppression_proxy: float
    promotion_state_adjustment: float
    total_score: float
    strengths: list[str]
    weaknesses: list[str]


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _infer_bundle_kind(payload: dict[str, Any]) -> str:
    if isinstance(payload.get("images"), list) and "bundle_name" in payload:
        return "aggregate_small_batch_bundle"
    if isinstance(payload.get("arms"), list) and payload.get("source_image_path"):
        return "per_image_eval_bundle"
    raise ValueError("Unsupported bundle payload: expected per-image eval bundle or aggregate small-batch bundle")


def _append_unique_path(paths: list[str], seen: set[str], candidate: str | Path) -> None:
    resolved = str(Path(candidate).resolve())
    if resolved not in seen:
        seen.add(resolved)
        paths.append(resolved)


def resolve_per_image_bundle_paths(
    bundle_paths: list[str | Path] | None = None,
    *,
    aggregate_bundle_paths: list[str | Path] | None = None,
) -> dict[str, Any]:
    requested_bundle_paths = [str(Path(path).resolve()) for path in bundle_paths or []]
    requested_aggregate_bundle_paths = [str(Path(path).resolve()) for path in aggregate_bundle_paths or []]
    resolved_per_image_bundle_paths: list[str] = []
    expanded_aggregate_bundle_paths: list[str] = []
    seen: set[str] = set()

    for path in requested_bundle_paths:
        payload = load_json(path)
        bundle_kind = _infer_bundle_kind(payload)
        if bundle_kind == "per_image_eval_bundle":
            _append_unique_path(resolved_per_image_bundle_paths, seen, path)
            continue
        expanded_aggregate_bundle_paths.append(str(Path(path).resolve()))
        for image in payload.get("images", []):
            bundle_path = image.get("bundle_path")
            if not bundle_path:
                raise ValueError(f"Aggregate bundle image entry missing bundle_path: {path}")
            _append_unique_path(resolved_per_image_bundle_paths, seen, bundle_path)

    for path in requested_aggregate_bundle_paths:
        payload = load_json(path)
        bundle_kind = _infer_bundle_kind(payload)
        if bundle_kind != "aggregate_small_batch_bundle":
            raise ValueError(f"Expected aggregate small-batch bundle: {path}")
        expanded_aggregate_bundle_paths.append(str(Path(path).resolve()))
        for image in payload.get("images", []):
            bundle_path = image.get("bundle_path")
            if not bundle_path:
                raise ValueError(f"Aggregate bundle image entry missing bundle_path: {path}")
            _append_unique_path(resolved_per_image_bundle_paths, seen, bundle_path)

    if not resolved_per_image_bundle_paths:
        raise ValueError("No per-image bundle paths resolved for auto-eval")

    if requested_aggregate_bundle_paths and requested_bundle_paths:
        actual_input_mode = "mixed"
    elif requested_aggregate_bundle_paths or expanded_aggregate_bundle_paths:
        actual_input_mode = "aggregate_bundle"
    else:
        actual_input_mode = "per_image_bundle_list"

    return {
        "requested_bundle_paths": requested_bundle_paths,
        "requested_aggregate_bundle_paths": requested_aggregate_bundle_paths,
        "expanded_aggregate_bundle_paths": sorted(set(expanded_aggregate_bundle_paths)),
        "resolved_per_image_bundle_paths": resolved_per_image_bundle_paths,
        "actual_input_mode": actual_input_mode,
    }


def _lower(text: str | None) -> str:
    return (text or "").lower()


def _mentions_all_metrics(text: str) -> bool:
    lower = _lower(text)
    return all(token in lower for token in METRIC_TOKENS)


def _metric_mention_coverage(caption: str, alt_text: str) -> float:
    joined = f"{caption}\n{alt_text}".lower()
    count = sum(1 for token in METRIC_TOKENS if token in joined)
    return float(count)


def _comparative_relation_signal(caption: str) -> float:
    lower = _lower(caption)
    score = 0.0
    if "table" in lower and "70q" in lower and "65q" in lower:
        score += 1.0
    if "delta" in lower or "differences" in lower or "deltas" in lower:
        score += 1.0
    if any(token in lower for token in RELATION_TOKENS):
        score += 1.0
    return score


def _caption_completeness(caption: str, alt_text: str) -> float:
    joined = f"{caption}\n{alt_text}".lower()
    score = 0.0
    if "table" in joined:
        score += 1.0
    if "70q" in joined and "65q" in joined:
        score += 1.0
    if _mentions_all_metrics(joined):
        score += 1.0
    if "delta" in joined or "differences" in joined or "deltas" in joined:
        score += 1.0
    return score


def _title_context_fidelity(caption: str, alt_text: str) -> float:
    joined = f"{caption}\n{alt_text}".lower()
    score = 0.0
    if "two-phase hyde-pc" in joined:
        score += 1.0
    if "오류 5건 제외" in joined:
        score += 1.0
    return score


def _parser_structure_support(context_variant: str | None) -> float:
    return 1.0 if context_variant == "parser_table_enriched" else 0.0


def _ocr_evidence_support(ocr_status: str | None) -> float:
    return 1.0 if ocr_status == "usable" else 0.0


def _non_table_noise_suppression_proxy(input_surface: str, context_variant: str | None) -> float:
    if context_variant == "reviewed_isolated_component" or input_surface == "reviewed_table_component_crop":
        return 2.0
    if context_variant == "parser_table_enriched":
        return 1.0
    if input_surface == "full_image_original":
        return 0.5
    return 0.5


def _promotion_state_for_arm(bundle: dict[str, Any], execution_arm: str) -> str:
    if execution_arm == bundle.get("recommended_current_default"):
        return "default_ready_anchor"
    gate = (bundle.get("per_arm_promotion") or {}).get(execution_arm) or {}
    return str(gate.get("promotion_state") or "unknown")


def _promotion_state_adjustment(promotion_state: str) -> float:
    if promotion_state == "default_ready_anchor":
        return 1.0
    if promotion_state == "comparison_ready_reviewed_branch":
        return -0.5
    if promotion_state == "comparison_only_pending_context_review":
        return -0.75
    if promotion_state == "blocked_by_context_review":
        return -1.5
    return -0.5


def _strengths_and_weaknesses(arm: dict[str, Any], score: ArmAutoScore) -> tuple[list[str], list[str]]:
    strengths: list[str] = []
    weaknesses: list[str] = []
    caption = _lower(arm.get("caption"))
    if score.metric_mention_coverage == 3.0:
        strengths.append("all_core_metrics_present")
    else:
        weaknesses.append("missing_metric_mentions")
    if score.comparative_relation_signal >= 3.0:
        strengths.append("explicit_relation_signal")
    elif score.comparative_relation_signal < 2.0:
        weaknesses.append("weak_relation_signal")
    if score.title_context_fidelity >= 1.0:
        strengths.append("title_or_condition_context_present")
    else:
        weaknesses.append("weak_title_context_fidelity")
    if score.parser_structure_support > 0:
        strengths.append("parser_structure_support")
    if score.ocr_evidence_support > 0:
        strengths.append("ocr_evidence_support")
    if score.non_table_noise_suppression_proxy >= 2.0:
        strengths.append("strong_noise_suppression_proxy")
    elif score.non_table_noise_suppression_proxy <= 0.5 and "this image shows" in caption:
        weaknesses.append("generic_image_framing_noise")
    if score.promotion_state_adjustment < 0:
        weaknesses.append(f"promotion_penalty:{score.promotion_state}")
    if score.default_ready:
        strengths.append("default_ready_anchor")
    return strengths, weaknesses


def score_arm(bundle: dict[str, Any], arm: dict[str, Any]) -> ArmAutoScore:
    execution_arm = str(arm["execution_arm"])
    promotion_state = _promotion_state_for_arm(bundle, execution_arm)
    default_ready = execution_arm == bundle.get("recommended_current_default")
    metric_mention_coverage = _metric_mention_coverage(str(arm.get("caption") or ""), str(arm.get("alt_text") or ""))
    comparative_relation_signal = _comparative_relation_signal(str(arm.get("caption") or ""))
    caption_completeness = _caption_completeness(str(arm.get("caption") or ""), str(arm.get("alt_text") or ""))
    title_context_fidelity = _title_context_fidelity(str(arm.get("caption") or ""), str(arm.get("alt_text") or ""))
    parser_structure_support = _parser_structure_support(arm.get("context_variant"))
    ocr_evidence_support = _ocr_evidence_support(arm.get("ocr_status"))
    non_table_noise_suppression_proxy = _non_table_noise_suppression_proxy(
        str(arm.get("input_surface") or ""),
        arm.get("context_variant"),
    )
    promotion_state_adjustment = _promotion_state_adjustment(promotion_state)
    total_score = (
        metric_mention_coverage
        + comparative_relation_signal
        + caption_completeness
        + title_context_fidelity
        + parser_structure_support
        + ocr_evidence_support
        + non_table_noise_suppression_proxy
        + promotion_state_adjustment
    )
    provisional = ArmAutoScore(
        execution_arm=execution_arm,
        promotion_state=promotion_state,
        default_ready=default_ready,
        metric_mention_coverage=metric_mention_coverage,
        comparative_relation_signal=comparative_relation_signal,
        caption_completeness=caption_completeness,
        title_context_fidelity=title_context_fidelity,
        parser_structure_support=parser_structure_support,
        ocr_evidence_support=ocr_evidence_support,
        non_table_noise_suppression_proxy=non_table_noise_suppression_proxy,
        promotion_state_adjustment=promotion_state_adjustment,
        total_score=total_score,
        strengths=[],
        weaknesses=[],
    )
    strengths, weaknesses = _strengths_and_weaknesses(arm, provisional)
    return ArmAutoScore(**{**provisional.__dict__, "strengths": strengths, "weaknesses": weaknesses})


def _winner_sort_key(score: ArmAutoScore) -> tuple[float, float, float, float]:
    return (
        score.total_score,
        score.comparative_relation_signal,
        score.non_table_noise_suppression_proxy,
        score.title_context_fidelity,
    )


def evaluate_bundle(bundle: dict[str, Any], bundle_path: str | Path) -> dict[str, Any]:
    arm_scores = [score_arm(bundle, arm) for arm in bundle.get("arms", [])]
    ordered = sorted(arm_scores, key=_winner_sort_key, reverse=True)
    winner = ordered[0]
    runner_up = ordered[1] if len(ordered) > 1 else None
    edge_case_review_recommended = bool(
        runner_up is not None and abs(winner.total_score - runner_up.total_score) <= 0.5
    )
    return {
        "bundle_path": str(Path(bundle_path).resolve()),
        "source_image_path": bundle.get("source_image_path"),
        "image_id": Path(str(bundle.get("source_image_path") or "")).stem or None,
        "mode_count": bundle.get("mode_count"),
        "comparison_ready": bundle.get("comparison_ready"),
        "recommended_current_default": bundle.get("recommended_current_default"),
        "qualitative_winner_candidate": winner.execution_arm,
        "baseline_retained": bundle.get("recommended_current_default") == "full_image_baseline",
        "edge_case_review_recommended": edge_case_review_recommended,
        "edge_case_review_reason": (
            "top proxy scores are close; use GPT direct image verification for this image if a stronger semantic tie-break is needed"
            if edge_case_review_recommended
            else None
        ),
        "per_arm_scores": [score.__dict__ for score in arm_scores],
        "winner_reason": (
            "highest proxy total with strongest comparative takeaway and noise suppression "
            "while keeping core metric coverage"
        ),
    }


def build_batch_auto_eval(
    bundle_paths: list[str | Path] | None = None,
    *,
    aggregate_bundle_paths: list[str | Path] | None = None,
    semantic_judge_available: bool,
) -> dict[str, Any]:
    input_resolution = resolve_per_image_bundle_paths(
        bundle_paths or [],
        aggregate_bundle_paths=aggregate_bundle_paths or [],
    )
    evaluations: list[dict[str, Any]] = []
    winner_frequency: dict[str, int] = {}
    strengths_by_arm: dict[str, list[str]] = {}
    weaknesses_by_arm: dict[str, list[str]] = {}
    baseline_retained = True
    for bundle_path in input_resolution["resolved_per_image_bundle_paths"]:
        bundle = load_json(bundle_path)
        evaluation = evaluate_bundle(bundle, bundle_path)
        evaluations.append(evaluation)
        winner = str(evaluation["qualitative_winner_candidate"])
        winner_frequency[winner] = winner_frequency.get(winner, 0) + 1
        baseline_retained = baseline_retained and bool(evaluation["baseline_retained"])
        for arm_score in evaluation["per_arm_scores"]:
            arm = str(arm_score["execution_arm"])
            strengths_by_arm.setdefault(arm, [])
            weaknesses_by_arm.setdefault(arm, [])
            strengths_by_arm[arm].extend(arm_score["strengths"])
            weaknesses_by_arm[arm].extend(arm_score["weaknesses"])
    return {
        "auto_eval_name": "phase1_caption_four_mode_small_batch_auto_eval",
        "schema_version": "v1",
        "semantic_judge_available": semantic_judge_available,
        "bundle_paths_used": input_resolution["resolved_per_image_bundle_paths"],
        "actual_input_mode": input_resolution["actual_input_mode"],
        "requested_bundle_paths": input_resolution["requested_bundle_paths"],
        "requested_aggregate_bundle_paths": input_resolution["requested_aggregate_bundle_paths"],
        "expanded_aggregate_bundle_paths": input_resolution["expanded_aggregate_bundle_paths"],
        "resolved_per_image_bundle_paths": input_resolution["resolved_per_image_bundle_paths"],
        "input_resolution": input_resolution,
        "image_count": len(evaluations),
        "image_ids": [evaluation["image_id"] for evaluation in evaluations],
        "evaluations": evaluations,
        "winner_frequency": winner_frequency,
        "baseline_retained": baseline_retained,
        "batch_summary": {
            "winner_frequency": winner_frequency,
            "baseline_retained": baseline_retained,
            "strong_patterns_by_arm": {
                arm: sorted(set(values)) for arm, values in strengths_by_arm.items()
            },
            "weak_patterns_by_arm": {
                arm: sorted(set(values)) for arm, values in weaknesses_by_arm.items()
            },
        },
    }


def render_auto_eval_report(auto_eval: dict[str, Any]) -> str:
    lines = [
        "# Phase 1 Caption Four-Mode Small-Batch Auto Eval",
        "",
        "## Input Resolution",
        "",
        f"- actual_input_mode: `{auto_eval['input_resolution']['actual_input_mode']}`",
        f"- image_count: `{auto_eval['image_count']}`",
        f"- image_ids: `{auto_eval['image_ids']}`",
        "",
        "### Requested Aggregate Bundle Paths",
        "",
    ]
    requested_aggregate = auto_eval["input_resolution"]["requested_aggregate_bundle_paths"]
    if requested_aggregate:
        for bundle_path in requested_aggregate:
            lines.append(f"- `{bundle_path}`")
    else:
        lines.append("- `none`")
    lines.extend(["", "### Resolved Per-Image Bundle Paths", ""])
    for bundle_path in auto_eval["bundle_paths_used"]:
        lines.append(f"- `{bundle_path}`")
    lines.extend(
        [
            "",
            "## Semantic Judge Availability",
            "",
            f"- semantic_judge_available: `{auto_eval['semantic_judge_available']}`",
            "",
            "## Batch Summary",
            "",
            f"- batch_level_winner_frequency: `{auto_eval['batch_summary']['winner_frequency']}`",
            f"- default_baseline_retained: `{auto_eval['batch_summary']['baseline_retained']}`",
            "",
            "## Per-Image Results",
            "",
        ]
    )
    for evaluation in auto_eval["evaluations"]:
        lines.extend(
            [
                f"### {evaluation['source_image_path']}",
                "",
                f"- image_id: `{evaluation['image_id']}`",
                f"- bundle_path: `{evaluation['bundle_path']}`",
                f"- comparison_ready: `{evaluation['comparison_ready']}`",
                f"- default_ready_arm: `{evaluation['recommended_current_default']}`",
                f"- qualitative_winner_candidate: `{evaluation['qualitative_winner_candidate']}`",
                f"- baseline_retained: `{evaluation['baseline_retained']}`",
                f"- edge_case_review_recommended: `{evaluation['edge_case_review_recommended']}`",
                "",
                "| arm | total | promotion | strengths | weaknesses |",
                "| --- | ---: | --- | --- | --- |",
            ]
        )
        for score in evaluation["per_arm_scores"]:
            lines.append(
                f"| `{score['execution_arm']}` | `{score['total_score']:.2f}` | "
                f"`{score['promotion_state']}` | "
                f"`{', '.join(score['strengths']) or 'none'}` | "
                f"`{', '.join(score['weaknesses']) or 'none'}` |"
            )
        lines.append("")
    lines.extend(
        [
            "## Baseline Retention",
            "",
            "- qualitative winner and default-ready arm are tracked separately",
            "- keep `full_image_baseline` as the active default unless a later promotion gate changes that status",
            "",
        ]
    )
    if any(evaluation["edge_case_review_recommended"] for evaluation in auto_eval["evaluations"]):
        lines.extend(
            [
                "## Edge-Case Handling",
                "",
                "- when top proxy scores remain close, prefer GPT direct image verification over human pixel review",
                "- keep that escalation as an evidence-seeking tie-break, not as a default replacement rule",
                "",
            ]
        )
    return "\n".join(lines)


def render_semantic_judge_waiver(auto_eval: dict[str, Any]) -> str:
    lines = [
        "# Phase 1 Caption Four-Mode Small-Batch Semantic Judge Waiver",
        "",
        "## Purpose",
        "",
        "Record that the current auto-eval lane closed without a repo-local semantic judge harness, and preserve the proxy-scored bundle inputs as the canonical downstream surface.",
        "",
        "## Input Resolution",
        "",
    ]
    lines.append(f"- actual_input_mode: `{auto_eval['input_resolution']['actual_input_mode']}`")
    lines.append(f"- image_ids: `{auto_eval['image_ids']}`")
    lines.append("")
    lines.append("### Resolved Per-Image Bundle Paths")
    lines.append("")
    for bundle_path in auto_eval["bundle_paths_used"]:
        lines.append(f"- `{bundle_path}`")
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            f"- semantic_judge_available: `{auto_eval['semantic_judge_available']}`",
            "- current lane closure: `proxy auto-eval + semantic judge waiver`",
            "",
            "## Guardrail",
            "",
            "- do not treat the qualitative winner as a default replacement",
            "- keep the proxy score as comparison evidence only",
            "- prefer a future judge consumer that reads the existing frozen bundle instead of regenerating arms",
            "",
        ]
    )
    return "\n".join(lines)
