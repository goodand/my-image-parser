#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from reviewed_component_context_package_lib import (
    DEFAULT_ALPHA_COMPONENT_MIN_PIXELS,
    DEFAULT_COMPONENT_PROXIMITY_PADDING,
    DEFAULT_MAX_EXTERNAL_COMPONENTS_FOR_RECROP,
    DEFAULT_OUTPUT_ROOT,
    build_reviewed_component_bundle,
    load_json,
    write_dataset_jsonl,
    write_json_manifest,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a reviewed isolated-component context package from a merged table candidate, "
            "export a bounded crop, run standalone OCR, and emit dataset/manifest surfaces "
            "for a caption rerun."
        )
    )
    parser.add_argument("--base-context-json", required=True, help="Existing full-image context package JSON.")
    parser.add_argument("--merged-candidate-json", required=True, help="Merged table candidate JSON.")
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_OUTPUT_ROOT),
        help="Root directory for reviewed isolated-component outputs.",
    )
    parser.add_argument(
        "--manifest-json",
        required=True,
        help="JSON manifest that should receive the reviewed isolated-component row.",
    )
    parser.add_argument(
        "--dataset-jsonl",
        required=True,
        help="Single-row dataset JSONL for caption_images_openai.py.",
    )
    parser.add_argument(
        "--padding",
        type=int,
        default=8,
        help="Padding in pixels around the merged reviewed component bbox.",
    )
    parser.add_argument(
        "--alpha-min-pixels",
        type=int,
        default=DEFAULT_ALPHA_COMPONENT_MIN_PIXELS,
        help="Ignore alpha components smaller than this when building multi-component recrop candidates.",
    )
    parser.add_argument(
        "--component-proximity-padding",
        type=int,
        default=DEFAULT_COMPONENT_PROXIMITY_PADDING,
        help="Extra padding around the seed bbox when collecting nearby alpha components for recrop.",
    )
    parser.add_argument(
        "--max-external-components-for-recrop",
        type=int,
        default=DEFAULT_MAX_EXTERNAL_COMPONENTS_FOR_RECROP,
        help="Skip alpha-augmented recrop when too many external components cluster around the seed bbox.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_context_package = load_json(args.base_context_json)
    merged_candidate = load_json(args.merged_candidate_json)
    package, output_paths, dataset_row, manifest_row = build_reviewed_component_bundle(
        base_context_package=base_context_package,
        merged_candidate=merged_candidate,
        output_root=Path(args.output_root).resolve(),
        padding=args.padding,
        alpha_min_pixels=args.alpha_min_pixels,
        component_proximity_padding=args.component_proximity_padding,
        max_external_components_for_recrop=args.max_external_components_for_recrop,
    )

    write_json_manifest(Path(args.manifest_json).resolve(), [manifest_row])
    write_dataset_jsonl(Path(args.dataset_jsonl).resolve(), [dataset_row])

    payload = {
        "status": "completed",
        "image_id": package["image_id"],
        "review_status": package["review_status"],
        "ocr_status": package["ocr_status"],
        "output_paths": {name: str(path) for name, path in output_paths.items()},
        "manifest_json": str(Path(args.manifest_json).resolve()),
        "dataset_jsonl": str(Path(args.dataset_jsonl).resolve()),
        "reviewed_component_image_path": package["reviewed_component_enrichment"]["component_image_path"],
        "selected_candidate_name": package["reviewed_component_enrichment"]["candidate_selection"]["selected_candidate_name"],
        "evidence_comparison": package["reviewed_component_enrichment"]["evidence_comparison"],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
