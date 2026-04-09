#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from four_mode_small_batch_bundle_lib import build_small_batch_bundle, render_small_batch_bundle_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assemble a true multi-image four-mode small-batch bundle from per-image eval bundles."
    )
    parser.add_argument("--bundle-json", action="append", required=True, help="Repeat for each per-image eval bundle.")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--report-md", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    bundle = build_small_batch_bundle(args.bundle_json)
    output_json = Path(args.output_json).resolve()
    report_md = Path(args.report_md).resolve()
    output_json.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_md.write_text(render_small_batch_bundle_report(bundle), encoding="utf-8")
    print(json.dumps(bundle, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
