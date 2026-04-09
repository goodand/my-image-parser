#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from alpha_component_lib import (
    DEFAULT_ALPHA_THRESHOLD,
    DEFAULT_MIN_COMPONENTS_FOR_SUCCESS,
    DEFAULT_MIN_PIXELS,
    DEFAULT_PADDING,
)
from component_split_ocr_lib import default_output_root, write_component_package


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Split a transparent image into alpha-connected components, "
            "build a component table, and run OCR on each separated component."
        )
    )
    parser.add_argument("--image-path", required=True, help="Absolute or repo-relative image path.")
    parser.add_argument(
        "--output-root",
        default=str(default_output_root()),
        help="Root directory for component split OCR outputs.",
    )
    parser.add_argument("--alpha-threshold", type=int, default=DEFAULT_ALPHA_THRESHOLD)
    parser.add_argument("--min-pixels", type=int, default=DEFAULT_MIN_PIXELS)
    parser.add_argument("--padding", type=int, default=DEFAULT_PADDING)
    parser.add_argument("--min-components-for-success", type=int, default=DEFAULT_MIN_COMPONENTS_FOR_SUCCESS)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    image_path = Path(args.image_path).resolve()
    if not image_path.is_file():
        raise SystemExit(f"Image not found: {image_path}")

    package = write_component_package(
        image_path=image_path,
        output_root=Path(args.output_root).resolve(),
        alpha_threshold=args.alpha_threshold,
        min_pixels=args.min_pixels,
        padding=args.padding,
        min_components_for_success=args.min_components_for_success,
    )
    print(json.dumps(asdict(package), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
