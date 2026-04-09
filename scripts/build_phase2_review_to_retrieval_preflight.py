#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from review_to_retrieval_preflight_lib import (
    build_mapping_review_seed,
    build_preflight_manifest,
    build_review_decision_seed,
    build_retrieval_input_seed,
    dumps_json,
    dumps_jsonl,
    load_json,
    render_preflight_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build machine-readable decision, retrieval, and mapping preflight "
            "seeds from a corpus review surface manifest."
        )
    )
    parser.add_argument("--review-surface-json", required=True)
    parser.add_argument("--output-preflight-json", required=True)
    parser.add_argument("--output-decision-seed-jsonl", required=True)
    parser.add_argument("--output-retrieval-seed-jsonl", required=True)
    parser.add_argument("--output-mapping-seed-jsonl", required=True)
    parser.add_argument("--output-report-md", required=True)
    return parser.parse_args()


def write_text(path: str | Path, text: str) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")


def main() -> int:
    args = parse_args()
    review_surface = load_json(args.review_surface_json)
    decision_seed = build_review_decision_seed(
        review_surface,
        review_surface_path=str(Path(args.review_surface_json).resolve()),
    )
    retrieval_seed = build_retrieval_input_seed(review_surface)
    mapping_seed = build_mapping_review_seed(review_surface)
    preflight = build_preflight_manifest(
        review_surface,
        review_surface_path=str(Path(args.review_surface_json).resolve()),
        decision_seed_path=str(Path(args.output_decision_seed_jsonl).resolve()),
        retrieval_seed_path=str(Path(args.output_retrieval_seed_jsonl).resolve()),
        mapping_seed_path=str(Path(args.output_mapping_seed_jsonl).resolve()),
    )
    report = render_preflight_report(preflight)

    write_text(args.output_decision_seed_jsonl, dumps_jsonl(decision_seed))
    write_text(args.output_retrieval_seed_jsonl, dumps_jsonl(retrieval_seed))
    write_text(args.output_mapping_seed_jsonl, dumps_jsonl(mapping_seed))
    write_text(args.output_preflight_json, dumps_json(preflight))
    write_text(args.output_report_md, report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
