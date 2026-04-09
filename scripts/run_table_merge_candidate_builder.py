from __future__ import annotations

import argparse
import json
from pathlib import Path

from table_merge_candidate_lib import (
    build_merged_candidate_from_paths,
    build_single_source_candidate_from_path,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a table candidate manifest from normalized table outputs.")
    parser.add_argument("--apple-normalized-json", default="")
    parser.add_argument("--paddle-normalized-json", default="")
    parser.add_argument("--comparison-json", default="")
    parser.add_argument(
        "--single-source-normalized-json",
        default="",
        help="Fallback mode: build a candidate from one normalized table only.",
    )
    parser.add_argument(
        "--single-source-backend",
        default="apple_vision_recognize_documents_request",
        help="Backend label written into the fallback single-source candidate.",
    )
    parser.add_argument(
        "--single-source-structure",
        default="apple_single_source",
        help="structure_source label for single-source fallback mode.",
    )
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    if args.single_source_normalized_json:
        merged = build_single_source_candidate_from_path(
            normalized_json=args.single_source_normalized_json,
            parser_backend=args.single_source_backend,
            structure_source=args.single_source_structure,
            source_manifests={
                "single_source_normalized_json": str(Path(args.single_source_normalized_json).resolve()),
            },
        )
    else:
        if not args.apple_normalized_json or not args.paddle_normalized_json or not args.comparison_json:
            raise ValueError(
                "Either --single-source-normalized-json or the full Apple/Paddle/comparison triplet is required."
            )
        merged = build_merged_candidate_from_paths(
            apple_normalized_json=args.apple_normalized_json,
            paddle_normalized_json=args.paddle_normalized_json,
            comparison_json=args.comparison_json,
            source_manifests={
                "apple_normalized_json": str(Path(args.apple_normalized_json).resolve()),
                "paddle_normalized_json": str(Path(args.paddle_normalized_json).resolve()),
                "comparison_json": str(Path(args.comparison_json).resolve()),
            },
        )
    Path(args.output_json).write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(merged, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
