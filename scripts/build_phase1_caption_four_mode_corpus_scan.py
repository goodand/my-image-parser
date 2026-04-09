#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from build_phase1_caption_four_mode_small_batch_bundle import (
    MEDIA_ROOT,
    baseline_record_for_image,
    build_excluded_edge_candidate,
    build_included_candidate_from_bundle,
    build_excluded_table_candidate,
    bundle_has_stable_workspace_provenance,
    derived_arm_status,
    gpt_visual_confirmation_payload,
    load_json,
    single_image_bundle_path_for,
)
from caption_arm_comparison_lib import build_small_batch_candidate_selection
from four_mode_small_batch_bundle_lib import (
    build_small_batch_bundle,
    render_small_batch_bundle_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Scan the full presentation-image corpus, classify 4-mode eligibility without manual review, "
            "and emit a stable ready-subset aggregate bundle."
        )
    )
    parser.add_argument("--target-image-count", type=int, default=20)
    parser.add_argument("--output-candidates-json", required=True)
    parser.add_argument("--output-bundle-json", required=True)
    parser.add_argument("--output-report-md", required=True)
    parser.add_argument("--output-excluded-json")
    return parser.parse_args()


def sort_key(image_path: Path) -> tuple[int, str]:
    match = re.search(r"(\d+)", image_path.stem)
    return (int(match.group(1)) if match else 10**9, image_path.stem)


def _generic_confirmation(image_stem: str) -> dict[str, Any]:
    return gpt_visual_confirmation_payload(
        status="not_required",
        reviewer=None,
        edge_case=False,
        rationale=(
            f"Corpus scan used artifact evidence only for `{image_stem}` and did not require direct image review."
        ),
        risks=[],
    )


def _confirmed_table_centric_confirmation(image_stem: str, rationale: str) -> dict[str, Any]:
    return gpt_visual_confirmation_payload(
        status="confirmed_table_centric",
        reviewer="Codex",
        edge_case=False,
        rationale=rationale,
        risks=[],
    )


def _confirmed_exclude_confirmation(
    *,
    image_stem: str,
    rationale: str,
    risks: list[str],
    edge_case: bool = False,
) -> dict[str, Any]:
    return gpt_visual_confirmation_payload(
        status="confirmed_exclude",
        reviewer="Codex",
        edge_case=edge_case,
        rationale=rationale,
        risks=risks,
    )


def _build_confirmed_exclude_candidate(
    *,
    image_stem: str,
    decision_reason: str,
    blocked_reason: str,
    rationale: str,
    risks: list[str],
    edge_case: bool = False,
) -> dict[str, Any]:
    candidate = build_excluded_table_candidate(
        image_stem=image_stem,
        gpt_visual_confirmation=_confirmed_exclude_confirmation(
            image_stem=image_stem,
            rationale=rationale,
            risks=risks,
            edge_case=edge_case,
        ),
    )
    candidate["decision_reason"] = decision_reason
    candidate["four_arm_readiness"] = {
        "full_image_baseline": "ready",
        "full_image_ocr_context_rerun": blocked_reason,
        "parser_table_enriched_rerun": blocked_reason,
        "reviewed_isolated_component_rerun": blocked_reason,
    }
    return candidate


def _unstable_bundle_candidate(
    *,
    image_stem: str,
    bundle_path: Path,
    bundle: dict[str, Any],
) -> dict[str, Any]:
    baseline = baseline_record_for_image(image_stem)
    return {
        "candidate_label": image_stem,
        "source_image_path": str(bundle["source_image_path"]),
        "decision": "exclude",
        "decision_reason": "unstable_nonworkspace_frozen_bundle_present",
        "single_image_bundle_path": str(bundle_path.resolve()),
        "gpt_visual_confirmation": _generic_confirmation(image_stem),
        "evidence": {
            "single_image_bundle_present": True,
            "single_image_bundle_path": str(bundle_path.resolve()),
            "comparison_ready": bool(bundle.get("comparison_ready")),
            "stable_workspace_provenance": False,
            "baseline_ledger_path": baseline["ledger_path"],
            "baseline_status": baseline["status"],
        },
        "four_arm_readiness": {
            "full_image_baseline": "ready",
            "full_image_ocr_context_rerun": "ready_but_unstable_provenance",
            "parser_table_enriched_rerun": "ready_but_unstable_provenance",
            "reviewed_isolated_component_rerun": "ready_but_unstable_provenance",
        },
    }


def build_corpus_candidate(image_stem: str) -> dict[str, Any]:
    if image_stem == "image4":
        return build_excluded_edge_candidate()

    if image_stem == "image1":
        return _build_confirmed_exclude_candidate(
            image_stem=image_stem,
            decision_reason="chart_dominant_non_table_image_confirmed_by_gpt",
            blocked_reason="blocked_by_confirmed_non_table_surface",
            rationale=(
                "Direct GPT visual confirmation found that image1 is chart-only and not a table-centric "
                "caption target for the current 4-mode experiment."
            ),
            risks=[],
        )

    if image_stem == "image2":
        return _build_confirmed_exclude_candidate(
            image_stem=image_stem,
            decision_reason="mixed_chart_table_composite_confirmed_by_gpt",
            blocked_reason="blocked_by_confirmed_chart_table_composite",
            rationale=(
                "Direct GPT visual confirmation found that image2 is a chart-dominant composite with a "
                "small summary table, so table-focused derived arms would under-represent the full image."
            ),
            risks=[
                "table-focused reruns may collapse the chart overview into the small summary table",
            ],
            edge_case=True,
        )

    if image_stem == "image3":
        return _build_confirmed_exclude_candidate(
            image_stem=image_stem,
            decision_reason="chart_dominant_non_table_image_confirmed_by_gpt",
            blocked_reason="blocked_by_confirmed_non_table_surface",
            rationale=(
                "Direct GPT visual confirmation found that image3 is chart-only and not a table-centric "
                "caption target for the current 4-mode experiment."
            ),
            risks=[],
        )

    if image_stem == "image5":
        return _build_confirmed_exclude_candidate(
            image_stem=image_stem,
            decision_reason="diagram_non_table_image_confirmed_by_gpt",
            blocked_reason="blocked_by_confirmed_non_table_surface",
            rationale=(
                "Direct GPT visual confirmation found that image5 is a process/architecture diagram, not a "
                "table-centric image suited to parser/reviewed table-derived arms."
            ),
            risks=[],
        )

    bundle_path = single_image_bundle_path_for(image_stem)
    if bundle_path and bundle_path.is_file():
        bundle = load_json(bundle_path)
        if bundle.get("comparison_ready"):
            confirmation = _generic_confirmation(image_stem)
            if image_stem == "image12":
                confirmation = _confirmed_table_centric_confirmation(
                    image_stem,
                    "Direct GPT visual confirmation found that image12 is a single table-centric surface with category/count/percentage content.",
                )
            elif image_stem == "image13":
                confirmation = _confirmed_table_centric_confirmation(
                    image_stem,
                    "Direct GPT visual confirmation found that image13 is a table-centric comparison surface with method/current-value/problem columns.",
                )
            elif image_stem == "image14":
                confirmation = _confirmed_table_centric_confirmation(
                    image_stem,
                    "Direct GPT visual confirmation found that image14 is a table-centric category/count/description surface.",
                )
            elif image_stem == "image15":
                confirmation = _confirmed_table_centric_confirmation(
                    image_stem,
                    "Direct GPT visual confirmation found that image15 is a table-centric metrics/formula/meaning surface.",
                )
            if bundle_has_stable_workspace_provenance(bundle):
                return build_included_candidate_from_bundle(
                    image_stem=image_stem,
                    single_bundle_path=bundle_path,
                    decision_reason="stable_frozen_four_mode_bundle_present",
                    gpt_visual_confirmation=confirmation,
                )
            return _unstable_bundle_candidate(
                image_stem=image_stem,
                bundle_path=bundle_path,
                bundle=bundle,
            )

    return build_excluded_table_candidate(
        image_stem=image_stem,
        gpt_visual_confirmation=_generic_confirmation(image_stem),
    )


def render_corpus_scan_report(
    *,
    requested_target_count: int,
    available_corpus_count: int,
    candidate_selection: dict[str, Any],
    aggregate_bundle: dict[str, Any],
) -> str:
    included = [item["candidate_label"] for item in candidate_selection["included_candidates"]]
    excluded = [item["candidate_label"] for item in candidate_selection["excluded_candidates"]]
    unstable = [
        item["candidate_label"]
        for item in candidate_selection["excluded_candidates"]
        if item["decision_reason"] == "unstable_nonworkspace_frozen_bundle_present"
    ]
    lines = [
        "# Phase 1 Caption Four-Mode Corpus Scan",
        "",
        "## Summary",
        "",
        f"- requested_target_image_count: `{requested_target_count}`",
        f"- available_corpus_image_count: `{available_corpus_count}`",
        f"- stable_four_mode_ready_count: `{len(included)}`",
        f"- excluded_count: `{len(excluded)}`",
        f"- unstable_bundle_count: `{len(unstable)}`",
        f"- requested_target_met: `{len(included) >= requested_target_count}`",
        "",
        "## Stable Ready Images",
        "",
        f"- included_image_ids: `{', '.join(included) or 'none'}`",
        "",
        "## Excluded Images",
        "",
        f"- excluded_image_ids: `{', '.join(excluded) or 'none'}`",
        "",
    ]
    if unstable:
        lines.extend(
            [
                "## Unstable Bundle Exclusions",
                "",
                f"- unstable_image_ids: `{', '.join(unstable)}`",
                "- rule: bundles that depend on non-workspace `/private/tmp` arm ledgers do not qualify as stable corpus truth",
                "",
            ]
        )
    lines.extend(
        [
            "## Canonical Aggregate Bundle",
            "",
            f"- image_count: `{aggregate_bundle['image_count']}`",
            f"- all_comparison_ready: `{aggregate_bundle['all_comparison_ready']}`",
            f"- default_anchor_consistent: `{aggregate_bundle['default_anchor_consistent']}`",
            "",
            render_small_batch_bundle_report(aggregate_bundle).rstrip(),
            "",
            "## Next Step",
            "",
            "- Use this scan to decide whether to freeze more derived arms or keep the current stable 4-mode-ready subset as the active comparison cohort.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    media_images = sorted(MEDIA_ROOT.glob("image*.png"), key=sort_key)
    candidates = [build_corpus_candidate(image_path.stem) for image_path in media_images]
    included_candidates = [item for item in candidates if item["decision"] == "include"]
    excluded_candidates = [item for item in candidates if item["decision"] != "include"]

    candidate_selection = build_small_batch_candidate_selection(
        target_image_count=args.target_image_count,
        included_candidates=included_candidates,
        excluded_candidates=excluded_candidates,
        confirmation_policy="evidence_only_corpus_scan",
    )

    included_bundle_paths = [
        str(Path(item["single_image_bundle_path"]).resolve())
        for item in included_candidates
        if item.get("single_image_bundle_path")
    ]
    aggregate_bundle = build_small_batch_bundle(included_bundle_paths)
    report_text = render_corpus_scan_report(
        requested_target_count=args.target_image_count,
        available_corpus_count=len(media_images),
        candidate_selection=candidate_selection,
        aggregate_bundle=aggregate_bundle,
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
        Path(args.output_excluded_json).resolve().write_text(
            json.dumps(excluded_candidates, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print(
        json.dumps(
            {
                "status": "completed",
                "requested_target_image_count": args.target_image_count,
                "available_corpus_image_count": len(media_images),
                "stable_four_mode_ready_count": len(included_candidates),
                "excluded_count": len(excluded_candidates),
                "included_image_ids": [item["candidate_label"] for item in included_candidates],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
