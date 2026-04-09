#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from review_decision_ingestion_lib import (
    build_ingestion_manifest,
    dumps_json,
    dumps_jsonl,
    is_mapping_eligible,
    is_retrieval_eligible,
    load_json,
    load_jsonl,
    render_ingestion_report,
    validate_machine_prefilled_fields,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Consume phase2 review decision rows and emit retrieval-ready "
            "and mapping-ready subsets."
        )
    )
    parser.add_argument("--decision-seed-jsonl", required=True)
    parser.add_argument("--review-surface-json", required=True)
    parser.add_argument("--output-ingestion-json", required=True)
    parser.add_argument("--output-retrieval-ready-jsonl", required=True)
    parser.add_argument("--output-mapping-ready-jsonl", required=True)
    parser.add_argument("--output-report-md", required=True)
    return parser.parse_args()


def write_text(path: str | Path, text: str) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")


def main() -> int:
    args = parse_args()
    rows = load_jsonl(args.decision_seed_jsonl)
    review_surface = load_json(args.review_surface_json)
    validate_machine_prefilled_fields(
        rows,
        review_surface=review_surface,
        review_surface_path=str(Path(args.review_surface_json).resolve()),
    )
    retrieval_ready = [row for row in rows if is_retrieval_eligible(row)]
    mapping_ready = [row for row in rows if is_mapping_eligible(row)]
    manifest = build_ingestion_manifest(
        rows,
        decision_seed_path=str(Path(args.decision_seed_jsonl).resolve()),
        retrieval_ready_path=str(Path(args.output_retrieval_ready_jsonl).resolve()),
        mapping_ready_path=str(Path(args.output_mapping_ready_jsonl).resolve()),
    )
    report = render_ingestion_report(manifest)

    write_text(args.output_retrieval_ready_jsonl, dumps_jsonl(retrieval_ready))
    write_text(args.output_mapping_ready_jsonl, dumps_jsonl(mapping_ready))
    write_text(args.output_ingestion_json, dumps_json(manifest))
    write_text(args.output_report_md, report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
