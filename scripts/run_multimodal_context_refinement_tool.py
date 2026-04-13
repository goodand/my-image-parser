#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from multimodal_context_refinement_tool_lib import (
    DEFAULT_EXAMPLES_JSON,
    build_bundle_from_example_record,
    build_multimodal_context_bundle,
    load_example_record,
    load_json,
    render_bundle_report,
    write_json,
)


def _load_optional_json(path: str | None) -> dict[str, Any] | None:
    if path is None:
        return None
    return load_json(path)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Emit a thin multimodal_context_refinement_tool bundle from supplied evidence or from a stored example record."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    emit_bundle = subparsers.add_parser("emit-bundle", help="Build a bundle from explicit JSON inputs.")
    emit_bundle.add_argument("--source-image-path", required=True)
    emit_bundle.add_argument("--task-intent", required=True)
    emit_bundle.add_argument("--provider-policy-json", required=True)
    emit_bundle.add_argument("--loop-budget-json", required=True)
    emit_bundle.add_argument("--baseline-context-json")
    emit_bundle.add_argument("--evidence-bundle-json")
    emit_bundle.add_argument("--normalized-interpretation-json")
    emit_bundle.add_argument("--form-preservation-json")
    emit_bundle.add_argument("--loop-state-json")
    emit_bundle.add_argument("--output-json", required=True)
    emit_bundle.add_argument("--output-report")

    emit_example = subparsers.add_parser("emit-example", help="Build a bundle from a stored example record.")
    emit_example.add_argument("--example-id", required=True)
    emit_example.add_argument("--examples-json", default=str(DEFAULT_EXAMPLES_JSON))
    emit_example.add_argument("--output-json", required=True)
    emit_example.add_argument("--output-report")

    return parser


def _emit_bundle(args: argparse.Namespace) -> dict[str, Any]:
    bundle = build_multimodal_context_bundle(
        source_image_path=args.source_image_path,
        task_intent=args.task_intent,
        provider_policy=load_json(args.provider_policy_json),
        loop_budget=load_json(args.loop_budget_json),
        baseline_context=_load_optional_json(args.baseline_context_json),
        evidence_bundle=_load_optional_json(args.evidence_bundle_json),
        normalized_interpretation=_load_optional_json(args.normalized_interpretation_json),
        form_preservation_assessment=_load_optional_json(args.form_preservation_json),
        loop_state=_load_optional_json(args.loop_state_json),
    )
    return bundle


def _emit_example(args: argparse.Namespace) -> dict[str, Any]:
    example_record = load_example_record(args.example_id, args.examples_json)
    return build_bundle_from_example_record(example_record)


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    if args.command == "emit-bundle":
        bundle = _emit_bundle(args)
    else:
        bundle = _emit_example(args)

    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    write_json(output_json, bundle)

    if args.output_report:
        output_report = Path(args.output_report)
        output_report.parent.mkdir(parents=True, exist_ok=True)
        output_report.write_text(
            render_bundle_report(bundle, bundle_path=str(output_json)),
            encoding="utf-8",
        )

    print(json.dumps(bundle, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
