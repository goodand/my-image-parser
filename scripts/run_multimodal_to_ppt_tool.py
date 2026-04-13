#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from multimodal_to_ppt_tool_lib import (
    DEFAULT_EXAMPLE_IO_JSON,
    build_ppt_package_from_example_io,
    build_ppt_package_from_input,
    load_example_io,
    load_json,
    render_ppt_package_report,
    validate_ppt_package,
    write_ppt_package_outputs,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Emit a thin multimodal_to_ppt_tool package that other agents can hand off to the pptx authoring surface."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    emit_package = subparsers.add_parser(
        "emit-package", help="Build a PPT-prep package from explicit multimodal context bundle inputs."
    )
    emit_package.add_argument("--input-json", required=True)
    emit_package.add_argument("--output-dir", required=True)
    emit_package.add_argument("--output-report")

    emit_example = subparsers.add_parser(
        "emit-example", help="Build a PPT-prep package from the stored example IO manifest."
    )
    emit_example.add_argument("--example-io-json", default=str(DEFAULT_EXAMPLE_IO_JSON))
    emit_example.add_argument("--output-dir", required=True)
    emit_example.add_argument("--output-report")

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "emit-package":
        package = build_ppt_package_from_input(load_json(args.input_json))
    else:
        package = build_ppt_package_from_example_io(load_example_io(args.example_io_json))

    validate_ppt_package(package)
    output_paths = write_ppt_package_outputs(args.output_dir, package)

    if args.output_report:
        output_report = Path(args.output_report)
        output_report.parent.mkdir(parents=True, exist_ok=True)
        output_report.write_text(
            render_ppt_package_report(package, output_paths=output_paths),
            encoding="utf-8",
        )

    print(
        json.dumps(
            {
                "package_manifest": output_paths["package_manifest"],
                "story_plan": output_paths["story_plan"],
                "slide_role_matrix": output_paths["slide_role_matrix"],
                "ppt_regeneration_handoff_bundle": output_paths["ppt_regeneration_handoff_bundle"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
