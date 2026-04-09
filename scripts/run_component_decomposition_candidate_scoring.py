#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from component_decomposition_candidate_scoring_lib import (
    DEFAULT_OUTPUT_JSON,
    load_json,
    render_candidate_scoring_report,
    score_candidate_surfaces,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Score regrouped component-decomposition candidates for a compound dashboard image."
    )
    parser.add_argument("--probe-manifest-json", required=True)
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT_JSON))
    parser.add_argument("--output-report-md", default="")
    return parser.parse_args()


def default_report_path(output_json: Path) -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    return (
        output_json.parents[1]
        / "reports"
        / f"REPORT_phase1_image4_component_decomposition_candidate_scoring-at{timestamp}.md"
    )


def main() -> int:
    args = parse_args()
    probe_manifest_path = Path(args.probe_manifest_json).resolve()
    probe_manifest = load_json(probe_manifest_path)
    probe_manifest["input_probe_manifest_path"] = str(probe_manifest_path)
    output_json = Path(args.output_json).resolve()
    output_report = Path(args.output_report_md).resolve() if args.output_report_md else default_report_path(output_json)

    payload = score_candidate_surfaces(probe_manifest)
    write_json(output_json, payload)
    output_report.parent.mkdir(parents=True, exist_ok=True)
    output_report.write_text(render_candidate_scoring_report(payload), encoding="utf-8")
    print(output_json)
    print(output_report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
