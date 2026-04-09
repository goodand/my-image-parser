#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from four_mode_small_batch_auto_eval_lib import (
    build_batch_auto_eval,
    render_auto_eval_report,
    render_semantic_judge_waiver,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run proxy auto-eval on one or more 4-mode frozen bundles.")
    parser.add_argument(
        "--bundle-json",
        action="append",
        default=[],
        help="Repeat for each per-image frozen bundle input. Aggregate small-batch bundles are also auto-detected.",
    )
    parser.add_argument(
        "--aggregate-bundle-json",
        action="append",
        default=[],
        help="Repeat for each aggregate small-batch bundle to expand into per-image bundle paths.",
    )
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--report-md", required=True)
    parser.add_argument("--semantic-waiver-md")
    parser.add_argument("--semantic-judge-available", action="store_true")
    args = parser.parse_args()
    if not args.bundle_json and not args.aggregate_bundle_json:
        parser.error("Provide at least one --bundle-json or --aggregate-bundle-json input.")
    return args


def main() -> int:
    args = parse_args()
    auto_eval = build_batch_auto_eval(
        args.bundle_json,
        aggregate_bundle_paths=args.aggregate_bundle_json,
        semantic_judge_available=bool(args.semantic_judge_available),
    )
    output_json = Path(args.output_json).resolve()
    report_md = Path(args.report_md).resolve()
    output_json.write_text(json.dumps(auto_eval, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_md.write_text(render_auto_eval_report(auto_eval), encoding="utf-8")
    if args.semantic_waiver_md and not args.semantic_judge_available:
        waiver_path = Path(args.semantic_waiver_md).resolve()
        waiver_path.write_text(render_semantic_judge_waiver(auto_eval), encoding="utf-8")
    print(json.dumps(auto_eval, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
