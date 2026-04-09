#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from reviewed_component_promotion_lib import (
    apply_reviewed_component_verdict,
    load_json,
    write_promoted_outputs,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply direct reviewed-component verification to a four-mode comparison and emit a promoted eval bundle."
    )
    parser.add_argument("--comparison-json", required=True)
    parser.add_argument("--verification-json", required=True)
    parser.add_argument("--output-comparison-json", required=True)
    parser.add_argument("--output-report-md", required=True)
    parser.add_argument("--output-bundle-json", required=True)
    parser.add_argument("--output-bundle-report-md", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    verification = load_json(args.verification_json)
    verification["verification_json_path"] = str(Path(args.verification_json).resolve())
    promoted_comparison = apply_reviewed_component_verdict(
        comparison=load_json(args.comparison_json),
        verification=verification,
    )
    eval_bundle = write_promoted_outputs(
        promoted_comparison=promoted_comparison,
        comparison_output_json=Path(args.output_comparison_json).resolve(),
        comparison_report_md=Path(args.output_report_md).resolve(),
        eval_bundle_output_json=Path(args.output_bundle_json).resolve(),
        eval_bundle_report_md=Path(args.output_bundle_report_md).resolve(),
    )
    print(
        json.dumps(
            {
                "comparison_ready": promoted_comparison.get("comparison_ready"),
                "reviewed_component_decision": (verification.get("result") or {}).get("decision"),
                "bundle_ready": eval_bundle.get("comparison_ready"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
