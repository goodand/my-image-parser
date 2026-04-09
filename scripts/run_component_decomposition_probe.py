#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from component_decomposition_probe_lib import (
    DEFAULT_MANIFEST_PATH,
    probe_component_decomposition,
    render_probe_report,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a bounded deterministic component decomposition probe on a composite image."
    )
    parser.add_argument("--image-path", required=True)
    parser.add_argument("--output-json", default=str(DEFAULT_MANIFEST_PATH))
    parser.add_argument(
        "--output-report-md",
        default="",
        help="Optional markdown report path. Defaults to a timestamped canonical report near the manifest.",
    )
    return parser.parse_args()


def default_report_path(output_json: Path) -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    return (
        output_json.parents[1]
        / "reports"
        / f"REPORT_phase1_image4_component_decomposition_probe-at{timestamp}.md"
    )


def main() -> int:
    args = parse_args()
    image_path = Path(args.image_path).resolve()
    output_json = Path(args.output_json).resolve()
    output_report = Path(args.output_report_md).resolve() if args.output_report_md else default_report_path(output_json)

    manifest = probe_component_decomposition(image_path)
    write_json(output_json, manifest)
    output_report.parent.mkdir(parents=True, exist_ok=True)
    output_report.write_text(render_probe_report(manifest), encoding="utf-8")
    print(output_json)
    print(output_report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
