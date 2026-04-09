#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from reviewed_component_direct_verification_lib import (
    DirectVerificationConfig,
    load_json,
    render_direct_verification_report,
    run_direct_verification,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run direct GPT image verification for a reviewed isolated-component candidate."
    )
    parser.add_argument("--source-image-path", required=True)
    parser.add_argument("--reviewed-component-image-path", required=True)
    parser.add_argument("--full-context-json")
    parser.add_argument("--reviewed-context-json")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--report-md", required=True)
    parser.add_argument("--model", default="gpt-4.1")
    parser.add_argument("--detail", choices=["low", "high", "auto"], default="high")
    parser.add_argument("--max-output-tokens", type=int, default=900)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root_dir = Path(__file__).resolve().parents[1]
    result = run_direct_verification(
        root_dir=root_dir,
        full_image_path=Path(args.source_image_path).resolve(),
        reviewed_component_image_path=Path(args.reviewed_component_image_path).resolve(),
        full_context_package=load_json(args.full_context_json),
        reviewed_context_package=load_json(args.reviewed_context_json),
        config=DirectVerificationConfig(
            model=args.model,
            detail=args.detail,
            max_output_tokens=args.max_output_tokens,
        ),
    )
    output_json = Path(args.output_json).resolve()
    report_md = Path(args.report_md).resolve()
    output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_md.write_text(render_direct_verification_report(result), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
