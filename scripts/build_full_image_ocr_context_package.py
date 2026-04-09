#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from full_image_ocr_context_package_lib import (
    DEFAULT_MANIFEST_JSONL,
    DEFAULT_OUTPUT_ROOT,
    build_context_package,
    print_json,
    update_context_package_manifest,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a full-image standalone OCR context package for one PPT-extracted image "
            "and persist markdown/json artifacts plus a manifest row."
        )
    )
    parser.add_argument("--image-path", required=True, help="Absolute path to the source image.")
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_OUTPUT_ROOT),
        help="Root directory for context-package outputs.",
    )
    parser.add_argument(
        "--manifest-jsonl",
        default=str(DEFAULT_MANIFEST_JSONL),
        help="Manifest JSONL that should receive or replace the image row.",
    )
    parser.add_argument(
        "--ocr-json",
        help="Optional existing OCR result JSON file. If set, the builder will not invoke OCR itself.",
    )
    parser.add_argument(
        "--ppt-local-summary",
        help="Optional override for the generated PPT-local summary.",
    )
    parser.add_argument(
        "--note",
        action="append",
        default=[],
        help="Repeatable note appended to the context package.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    image_path = Path(args.image_path).resolve()
    output_root = Path(args.output_root).resolve()
    manifest_jsonl = Path(args.manifest_jsonl).resolve()

    ocr_result = None
    if args.ocr_json:
        ocr_result = json.loads(Path(args.ocr_json).resolve().read_text(encoding="utf-8"))

    package, output_paths = build_context_package(
        image_path=image_path,
        output_root=output_root,
        ocr_result=ocr_result,
        ppt_local_summary_override=args.ppt_local_summary,
        extra_notes=args.note,
    )
    update_context_package_manifest(manifest_jsonl, package)

    print_json(
        {
            "status": "completed",
            "image_id": package.image_id,
            "source_image_path": package.source_image_path,
            "ocr_status": package.ocr_status,
            "review_status": package.review_status,
            "output_paths": {name: str(path) for name, path in output_paths.items()},
            "manifest_jsonl": str(manifest_jsonl),
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
