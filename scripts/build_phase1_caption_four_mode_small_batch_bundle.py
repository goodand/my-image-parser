#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from caption_arm_comparison_lib import (
    build_small_batch_candidate_selection,
    render_small_batch_readiness_report,
    extract_mode_record,
)
from four_mode_small_batch_bundle_lib import (
    build_small_batch_bundle,
    render_small_batch_bundle_report,
)


ROOT = Path(__file__).resolve().parents[1]
PHASE0_SINGLE_IMAGE_BUNDLE = (
    ROOT
    / "control"
    / "project_domain"
    / "resources"
    / "manifests"
    / "phase0_caption_four_mode_eval_bundle_at2026_03_28.json"
)
PHASE1_W01_BASELINE_LEDGER = (
    ROOT
    / "control"
    / "project_agent_ops"
    / "registry"
    / "jobs"
    / "image_caption_jobs"
    / "phase1_caption_10w_01_full_presentation_2026-03-17_w01.json"
)
PHASE1_W02_BASELINE_LEDGER = (
    ROOT
    / "control"
    / "project_agent_ops"
    / "registry"
    / "jobs"
    / "image_caption_jobs"
    / "phase1_caption_10w_01_full_presentation_2026-03-17_w02.json"
)
PHASE1_BASELINE_LEDGERS = (
    PHASE1_W01_BASELINE_LEDGER,
    PHASE1_W02_BASELINE_LEDGER,
)
ALPHA_SPLIT_ROOT = (
    ROOT
    / "control"
    / "project_domain"
    / "archive"
    / "object_isolation"
    / "alpha_split_batch"
    / "2026-03-27-15-05"
    / "01_full_presentation_2026-03-17"
)
MEDIA_ROOT = (
    ROOT
    / "control"
    / "project_domain"
    / "resources"
    / "pptx_jobs"
    / "01_full_presentation_2026-03-17"
    / "media"
)
CAPTION_JOB_ROOT = (
    ROOT
    / "control"
    / "project_agent_ops"
    / "registry"
    / "jobs"
    / "image_caption_jobs"
)
PHASE1_IMAGE_BUNDLE_ROOT = ROOT / "control" / "project_domain" / "resources" / "manifests"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a phase1 small-batch 4-mode candidate manifest and frozen bundle "
            "without manual image review, using evidence-only gates plus GPT confirmation "
            "for flagged edge cases."
        )
    )
    parser.add_argument("--target-image-count", type=int, default=3)
    parser.add_argument("--output-candidates-json", required=True)
    parser.add_argument("--output-bundle-json", required=True)
    parser.add_argument("--output-report-md", required=True)
    parser.add_argument("--output-excluded-json")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def latest_matching_file(root: Path, pattern: str) -> Path | None:
    matches = sorted(root.glob(pattern))
    if not matches:
        return None
    return matches[-1]


def load_alpha_worker_result(image_stem: str) -> dict[str, Any]:
    worker_path = ALPHA_SPLIT_ROOT / image_stem / "worker_result.json"
    return load_json(worker_path)


def baseline_record_for_image(image_stem: str) -> dict[str, Any]:
    source_image_path = MEDIA_ROOT / f"{image_stem}.png"
    record = None
    for ledger_path in PHASE1_BASELINE_LEDGERS:
        try:
            record = extract_mode_record(
                ledger_path=ledger_path,
                source_image_path=source_image_path,
                execution_arm="full_image_baseline",
                fallback_input_surface="extracted_full_image",
            )
            break
        except ValueError:
            continue
    if record is None:
        raise ValueError(f"No baseline record found for {source_image_path}")
    return {
        "execution_arm": record.execution_arm,
        "image_id": record.image_id,
        "ledger_path": record.ledger_path,
        "status": record.status,
        "caption": record.caption,
        "alt_text": record.alt_text,
        "prompt_version": record.prompt_version,
    }


def derived_ledger_path(image_stem: str, execution_arm: str) -> Path | None:
    pattern_map = {
        "full_image_ocr_context_rerun": f"phase1_full_image_context_rerun_{image_stem}_at*.json",
        "parser_table_enriched_rerun": f"phase1_parser_enriched_rerun_{image_stem}_at*.json",
        "reviewed_isolated_component_rerun": f"phase1_reviewed_isolated_component_rerun_{image_stem}_at*.json",
    }
    pattern = pattern_map.get(execution_arm)
    if not pattern:
        return None
    return latest_matching_file(CAPTION_JOB_ROOT, pattern)


def derived_arm_status(image_stem: str, execution_arm: str) -> str:
    ledger_path = derived_ledger_path(image_stem, execution_arm)
    if ledger_path and ledger_path.is_file():
        return "ready"
    return "not_frozen"


def gpt_visual_confirmation_payload(
    *,
    status: str,
    reviewer: str,
    edge_case: bool,
    rationale: str,
    risks: list[str],
) -> dict[str, Any]:
    return {
        "status": status,
        "reviewer": reviewer,
        "edge_case": edge_case,
        "rationale": rationale,
        "risks": risks,
    }


def single_image_bundle_path_for(image_stem: str) -> Path | None:
    if image_stem == "image11":
        return PHASE0_SINGLE_IMAGE_BUNDLE
    return latest_matching_file(
        PHASE1_IMAGE_BUNDLE_ROOT,
        f"phase1_{image_stem}_caption_four_mode_eval_bundle_at*.json",
    )


def _path_is_workspace_stable(path_value: str | None) -> bool:
    if not path_value:
        return False
    try:
        resolved = Path(path_value).resolve()
    except FileNotFoundError:
        resolved = Path(path_value)
    return str(resolved).startswith(str(ROOT))


def bundle_has_stable_workspace_provenance(bundle: dict[str, Any]) -> bool:
    for arm in bundle.get("arms", []):
        if not _path_is_workspace_stable(arm.get("ledger_path")):
            return False
    return True


def build_included_candidate_from_bundle(
    *,
    image_stem: str,
    single_bundle_path: Path,
    decision_reason: str,
    gpt_visual_confirmation: dict[str, Any],
) -> dict[str, Any]:
    bundle = load_json(single_bundle_path)
    source_image_path = str(bundle["source_image_path"])
    status_summary = bundle.get("status_summary") or {}
    return {
        "candidate_label": image_stem,
        "source_image_path": source_image_path,
        "decision": "include",
        "decision_reason": decision_reason,
        "single_image_bundle_path": str(single_bundle_path.resolve()),
        "gpt_visual_confirmation": gpt_visual_confirmation,
        "evidence": {
            "single_image_bundle_present": True,
            "single_image_bundle_path": str(single_bundle_path.resolve()),
            "comparison_ready": bool(bundle.get("comparison_ready")),
            "ready_arm_count": int(status_summary.get("ready_arm_count") or 0),
            "blocked_arm_count": int(status_summary.get("blocked_arm_count") or 0),
        },
        "four_arm_readiness": {
            "full_image_baseline": "ready",
            "full_image_ocr_context_rerun": "ready",
            "parser_table_enriched_rerun": "ready",
            "reviewed_isolated_component_rerun": "ready",
        },
    }


def build_included_image11_candidate(single_bundle_path: Path) -> dict[str, Any]:
    return build_included_candidate_from_bundle(
        image_stem="image11",
        single_bundle_path=single_bundle_path,
        decision_reason="existing_four_mode_bundle_present",
        gpt_visual_confirmation={
            "status": "not_required",
            "reviewer": None,
            "edge_case": False,
            "rationale": "The source image already has a completed 4-mode bundle and does not need a secondary visual confirmation gate.",
            "risks": [],
        },
    )


def build_excluded_table_candidate(
    *,
    image_stem: str,
    gpt_visual_confirmation: dict[str, Any],
) -> dict[str, Any]:
    source_image_path = MEDIA_ROOT / f"{image_stem}.png"
    baseline = baseline_record_for_image(image_stem)
    alpha = load_alpha_worker_result(image_stem)
    full_image_ocr_ledger = derived_ledger_path(image_stem, "full_image_ocr_context_rerun")
    parser_ledger = derived_ledger_path(image_stem, "parser_table_enriched_rerun")
    reviewed_ledger = derived_ledger_path(image_stem, "reviewed_isolated_component_rerun")
    return {
        "candidate_label": image_stem,
        "source_image_path": str(source_image_path.resolve()),
        "decision": "exclude",
        "decision_reason": "missing_frozen_context_and_rerun_artifacts_for_derived_arms",
        "single_image_bundle_path": None,
        "gpt_visual_confirmation": gpt_visual_confirmation,
        "evidence": {
            "baseline_ledger_path": baseline["ledger_path"],
            "baseline_status": baseline["status"],
            "full_image_ocr_context_rerun_ledger_path": (
                str(full_image_ocr_ledger.resolve()) if full_image_ocr_ledger and full_image_ocr_ledger.is_file() else None
            ),
            "parser_table_enriched_rerun_ledger_path": (
                str(parser_ledger.resolve()) if parser_ledger and parser_ledger.is_file() else None
            ),
            "reviewed_isolated_component_rerun_ledger_path": (
                str(reviewed_ledger.resolve()) if reviewed_ledger and reviewed_ledger.is_file() else None
            ),
            "alpha_component_count": alpha["alpha_split"]["component_count"],
            "alpha_split_sufficient": alpha["alpha_split"]["sufficient"],
            "alpha_split_reason": alpha["alpha_split"]["reason"],
            "table_centric_caption_hint": baseline["caption"],
        },
        "four_arm_readiness": {
            "full_image_baseline": "ready",
            "full_image_ocr_context_rerun": derived_arm_status(image_stem, "full_image_ocr_context_rerun"),
            "parser_table_enriched_rerun": derived_arm_status(image_stem, "parser_table_enriched_rerun"),
            "reviewed_isolated_component_rerun": derived_arm_status(image_stem, "reviewed_isolated_component_rerun"),
        },
    }


def build_table_candidate(
    *,
    image_stem: str,
    gpt_visual_confirmation: dict[str, Any],
) -> dict[str, Any]:
    bundle_path = single_image_bundle_path_for(image_stem)
    if bundle_path and load_json(bundle_path).get("comparison_ready"):
        return build_included_candidate_from_bundle(
            image_stem=image_stem,
            single_bundle_path=bundle_path,
            decision_reason="frozen_four_mode_bundle_present",
            gpt_visual_confirmation=gpt_visual_confirmation,
        )
    return build_excluded_table_candidate(
        image_stem=image_stem,
        gpt_visual_confirmation=gpt_visual_confirmation,
    )


def build_excluded_edge_candidate() -> dict[str, Any]:
    image_stem = "image4"
    source_image_path = MEDIA_ROOT / f"{image_stem}.png"
    baseline = baseline_record_for_image(image_stem)
    alpha = load_alpha_worker_result(image_stem)
    gpt_visual_confirmation = gpt_visual_confirmation_payload(
        status="confirmed_exclude",
        reviewer="Codex",
        edge_case=True,
        rationale=(
            "Direct GPT visual confirmation found that the image is chart-dominant overall. "
            "The embedded structure table is secondary, so table-focused derived arms would "
            "under-represent the full image meaning."
        ),
        risks=[
            "parser arm may over-focus on the small embedded table and miss chart context",
            "reviewed-crop arm may pick an unstable crop and lose merged-metrics context",
        ],
    )
    return {
        "candidate_label": image_stem,
        "source_image_path": str(source_image_path.resolve()),
        "decision": "exclude",
        "decision_reason": "mixed_chart_table_edge_case_confirmed_by_gpt_and_no_frozen_derived_arms",
        "single_image_bundle_path": None,
        "gpt_visual_confirmation": gpt_visual_confirmation,
        "evidence": {
            "baseline_ledger_path": baseline["ledger_path"],
            "baseline_status": baseline["status"],
            "alpha_component_count": alpha["alpha_split"]["component_count"],
            "alpha_split_sufficient": alpha["alpha_split"]["sufficient"],
            "alpha_split_reason": alpha["alpha_split"]["reason"],
            "table_centric_caption_hint": baseline["caption"],
        },
        "four_arm_readiness": {
            "full_image_baseline": "ready",
            "full_image_ocr_context_rerun": "blocked_by_confirmed_mixed_chart_table_edge_case",
            "parser_table_enriched_rerun": "blocked_by_confirmed_mixed_chart_table_edge_case",
            "reviewed_isolated_component_rerun": "blocked_by_confirmed_mixed_chart_table_edge_case",
        },
    }


def render_phase1_small_batch_report(
    *,
    candidate_selection: dict[str, Any],
    aggregate_bundle: dict[str, Any],
    title: str,
) -> str:
    readiness_text = render_small_batch_readiness_report(
        candidate_selection,
        {
            "bundle_name": aggregate_bundle["bundle_name"],
            "included_image_count": aggregate_bundle["image_count"],
            "excluded_image_count": candidate_selection["summary"]["excluded_count"],
            "minimum_target_met": candidate_selection["summary"]["minimum_target_met"],
            "next_step": (
                "Use the canonical aggregate bundle below as the downstream consumer truth-source. "
                "Do not consume stale 2-image bundle artifacts."
            ),
        },
        title=title,
    )
    aggregate_text = render_small_batch_bundle_report(aggregate_bundle)
    included_labels = [item["candidate_label"] for item in candidate_selection["included_candidates"]]
    excluded_labels = [item["candidate_label"] for item in candidate_selection["excluded_candidates"]]
    closure_lines = [
        "## Canonical Aggregate Closure",
        "",
        f"- included_image_ids: `{', '.join(included_labels) or 'none'}`",
        f"- excluded_image_ids: `{', '.join(excluded_labels) or 'none'}`",
        f"- canonical_bundle_image_count: `{aggregate_bundle['image_count']}`",
        f"- stale_drift_closed: `{aggregate_bundle['image_count'] == len(included_labels)}`",
        f"- downstream_truth_source: `{aggregate_bundle['bundle_name']}`",
        "",
    ]
    return "\n".join([readiness_text.rstrip(), "", *closure_lines, aggregate_text.rstrip(), ""]) + "\n"


def main() -> int:
    args = parse_args()
    included_candidates = [
        build_included_image11_candidate(PHASE0_SINGLE_IMAGE_BUNDLE),
        build_table_candidate(
            image_stem="image7",
            gpt_visual_confirmation=gpt_visual_confirmation_payload(
                status="confirmed_table_centric",
                reviewer="Volta",
                edge_case=False,
                rationale=(
                    "The image is dominated by a clear grid table with aligned header and data rows. "
                    "There is little non-table visual content."
                ),
                risks=[
                    "mixed Korean and English text may cause OCR inconsistency",
                    "tight reviewed crop may truncate left metric labels or top header",
                ],
            ),
        ),
        build_table_candidate(
            image_stem="image8",
            gpt_visual_confirmation=gpt_visual_confirmation_payload(
                status="not_required",
                reviewer=None,
                edge_case=False,
                rationale=(
                    "A stable four-mode bundle now exists for image8, so the small-batch builder can "
                    "promote it by artifact evidence without a fresh visual confirmation pass."
                ),
                risks=[
                    "parser arm remains comparison-only until its pending-review gate clears",
                    "reviewed isolated arm is still a reviewed branch rather than a default replacement",
                ],
            ),
        ),
        build_table_candidate(
            image_stem="image10",
            gpt_visual_confirmation=gpt_visual_confirmation_payload(
                status="not_required",
                reviewer=None,
                edge_case=False,
                rationale=(
                    "A stable four-mode bundle already exists for image10, so the small-batch builder can "
                    "promote it by artifact evidence without a fresh visual confirmation pass."
                ),
                risks=[
                    "parser and reviewed arms remain comparison-only until their pending-review gates clear",
                ],
            ),
        ),
        build_table_candidate(
            image_stem="image9",
            gpt_visual_confirmation=gpt_visual_confirmation_payload(
                status="confirmed_table_centric",
                reviewer="Boole",
                edge_case=False,
                rationale=(
                    "The image is centered on a clear 3-column, 4-row table with headers and numeric outcome values. "
                    "Bottom notes are secondary."
                ),
                risks=[
                    "bottom bullet notes may leak into table OCR",
                    "crop decision may need to keep or drop explanatory bullets consistently",
                ],
            ),
        ),
    ]
    excluded_candidates = [
        build_excluded_edge_candidate(),
    ]

    candidate_selection = build_small_batch_candidate_selection(
        target_image_count=args.target_image_count,
        included_candidates=included_candidates,
        excluded_candidates=excluded_candidates,
    )
    included_bundle_paths = [
        str(Path(item["single_image_bundle_path"]).resolve())
        for item in included_candidates
        if item.get("single_image_bundle_path")
    ]
    aggregate_bundle = build_small_batch_bundle(included_bundle_paths)
    report_text = render_phase1_small_batch_report(
        candidate_selection=candidate_selection,
        aggregate_bundle=aggregate_bundle,
        title="Phase 1 Caption Four-Mode Small-Batch Readiness",
    )

    output_candidates_json = Path(args.output_candidates_json).resolve()
    output_bundle_json = Path(args.output_bundle_json).resolve()
    output_report_md = Path(args.output_report_md).resolve()
    output_candidates_json.write_text(
        json.dumps(candidate_selection, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    output_bundle_json.write_text(
        json.dumps(aggregate_bundle, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    output_report_md.write_text(report_text, encoding="utf-8")

    if args.output_excluded_json:
        excluded_json = Path(args.output_excluded_json).resolve()
        excluded_json.write_text(
            json.dumps(excluded_candidates, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print(
        json.dumps(
            {
                "status": "completed",
                "included_count": candidate_selection["summary"]["included_count"],
                "excluded_count": candidate_selection["summary"]["excluded_count"],
                "minimum_target_met": candidate_selection["summary"]["minimum_target_met"],
                "aggregate_bundle_image_count": aggregate_bundle["image_count"],
                "aggregate_bundle_paths_used": aggregate_bundle["bundle_paths_used"],
                "output_candidates_json": str(output_candidates_json),
                "output_bundle_json": str(output_bundle_json),
                "output_report_md": str(output_report_md),
                "output_excluded_json": str(Path(args.output_excluded_json).resolve()) if args.output_excluded_json else None,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
