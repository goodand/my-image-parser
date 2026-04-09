#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from caption_arm_comparison_lib import (
    CaptionModeRecord,
    build_eval_bundle_from_comparison,
    compare_ready_caption_arms,
    compare_caption_modes,
    extract_mode_record,
    render_eval_bundle_report,
    render_multi_mode_comparison_report,
    render_comparison_report,
)


def parse_candidate_arm_spec(spec: str) -> tuple[str, str, str]:
    execution_arm, separator, remainder = spec.partition("=")
    if not separator or not execution_arm.strip() or not remainder.strip():
        raise ValueError(
            "Candidate arm spec must look like "
            "'execution_arm=/abs/or/relative/ledger.json::fallback_input_surface'."
        )
    ledger_path, surface_separator, fallback_surface = remainder.partition("::")
    fallback_input_surface = fallback_surface.strip() if surface_separator else "full_image_original"
    if not ledger_path.strip():
        raise ValueError("Candidate arm spec ledger path cannot be empty.")
    if not fallback_input_surface:
        raise ValueError("Candidate arm spec fallback input surface cannot be empty.")
    return execution_arm.strip(), ledger_path.strip(), fallback_input_surface


def infer_ready_arm_report_title(mode_count: int) -> str:
    if mode_count == 2:
        return "Phase 0 Two-Mode Caption Comparison"
    if mode_count == 3:
        return "Phase 0 Three-Mode Caption Comparison"
    return f"Phase 0 {mode_count}-Mode Caption Comparison"


def build_candidate_records(
    *,
    candidate_specs: list[str],
    source_image_path: str,
) -> list[CaptionModeRecord]:
    records: list[CaptionModeRecord] = []
    seen_execution_arms: set[str] = set()
    for spec in candidate_specs:
        execution_arm, ledger_path, fallback_input_surface = parse_candidate_arm_spec(spec)
        if execution_arm in seen_execution_arms:
            raise ValueError(f"Duplicate candidate execution_arm: {execution_arm}")
        seen_execution_arms.add(execution_arm)
        records.append(
            extract_mode_record(
                ledger_path=ledger_path,
                source_image_path=source_image_path,
                execution_arm=execution_arm,
                fallback_input_surface=fallback_input_surface,
            )
        )
    return records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare caption arms on one shared source image.")
    parser.add_argument("--source-image-path", required=True)
    parser.add_argument("--baseline-ledger", required=True)
    parser.add_argument("--rerun-ledger")
    parser.add_argument("--parser-rerun-ledger")
    parser.add_argument(
        "--candidate-arm",
        action="append",
        default=[],
        help=(
            "Reusable candidate arm spec. Format: "
            "'execution_arm=ledger_path::fallback_input_surface'. "
            "Repeat this flag to compare any number of ready arms without patching code."
        ),
    )
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--report-md", required=True)
    parser.add_argument("--bundle-json")
    parser.add_argument("--bundle-report-md")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    baseline = extract_mode_record(
        ledger_path=args.baseline_ledger,
        source_image_path=args.source_image_path,
        execution_arm="full_image_baseline",
        fallback_input_surface="extracted_full_image",
    )
    candidate_specs = list(args.candidate_arm)
    if not candidate_specs:
        if not args.rerun_ledger:
            raise ValueError("Either --rerun-ledger or one or more --candidate-arm flags are required.")
        candidate_specs.append(
            f"full_image_ocr_context_rerun={args.rerun_ledger}::full_image_original"
        )
        if args.parser_rerun_ledger:
            candidate_specs.append(
                f"parser_table_enriched_rerun={args.parser_rerun_ledger}::full_image_original"
            )
    candidate_records = build_candidate_records(
        candidate_specs=candidate_specs,
        source_image_path=args.source_image_path,
    )
    if len(candidate_records) == 1:
        rerun = candidate_records[0]
        comparison = compare_caption_modes(baseline, rerun)
        report_text = render_comparison_report(comparison)
    else:
        comparison = compare_ready_caption_arms(baseline, *candidate_records)
        report_text = render_multi_mode_comparison_report(
            comparison,
            title=infer_ready_arm_report_title(comparison["mode_count"]),
        )
    output_json = Path(args.output_json).resolve()
    report_md = Path(args.report_md).resolve()
    output_json.write_text(json.dumps(comparison, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_md.write_text(report_text, encoding="utf-8")
    if args.bundle_json and args.bundle_report_md:
        bundle = build_eval_bundle_from_comparison(comparison)
        bundle_json = Path(args.bundle_json).resolve()
        bundle_report_md = Path(args.bundle_report_md).resolve()
        bundle_json.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        bundle_report_md.write_text(
            render_eval_bundle_report(bundle, title="Phase 0 Four-Mode Eval Bundle"),
            encoding="utf-8",
        )
    print(json.dumps(comparison, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
