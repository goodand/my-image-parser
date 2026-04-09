#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from parser_enriched_context_package_lib import (
    DEFAULT_OUTPUT_ROOT,
    build_parser_enriched_context_package,
    load_json,
    update_manifest_json,
    write_parser_enriched_context_package,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a parser-enriched caption context package by combining an existing "
            "full-image OCR baseline package with a merged table candidate manifest."
        )
    )
    parser.add_argument("--base-context-json", required=True)
    parser.add_argument("--merged-candidate-json", required=True)
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--manifest-json", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_context = load_json(args.base_context_json)
    merged_candidate = load_json(args.merged_candidate_json)
    package = build_parser_enriched_context_package(
        base_context_package=base_context,
        merged_candidate=merged_candidate,
    )
    output_paths = write_parser_enriched_context_package(
        package=package,
        output_root=Path(args.output_root),
    )
    package["context_package_json_path"] = str(output_paths["context_package_json_path"])
    package["context_package_markdown_path"] = str(output_paths["context_package_markdown_path"])
    output_paths = write_parser_enriched_context_package(
        package=package,
        output_root=Path(args.output_root),
    )
    update_manifest_json(Path(args.manifest_json), package)
    print(
        json.dumps(
            {
                "status": "completed",
                "source_image_path": package["source_image_path"],
                "review_status": package["review_status"],
                "context_package_json_path": str(output_paths["context_package_json_path"]),
                "context_package_markdown_path": str(output_paths["context_package_markdown_path"]),
                "manifest_json": str(Path(args.manifest_json).resolve()),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
