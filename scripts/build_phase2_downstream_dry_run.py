#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from review_decision_downstream_dry_run_lib import (
    build_mapping_dry_run_manifest,
    build_retrieval_dry_run_manifest,
    dumps_json,
    load_json,
    load_jsonl,
    render_downstream_dry_run_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build phase2 retrieval and mapping dry-run manifests from "
            "review-decision ingestion outputs."
        )
    )
    parser.add_argument("--decision-ingestion-json", required=True)
    parser.add_argument("--retrieval-ready-jsonl", required=True)
    parser.add_argument("--mapping-ready-jsonl", required=True)
    parser.add_argument("--output-retrieval-dry-run-json", required=True)
    parser.add_argument("--output-mapping-dry-run-json", required=True)
    parser.add_argument("--output-report-md", required=True)
    return parser.parse_args()


def write_text(path: str | Path, text: str) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")


def main() -> int:
    args = parse_args()
    ingestion_manifest = load_json(args.decision_ingestion_json)
    retrieval_ready_rows = load_jsonl(args.retrieval_ready_jsonl)
    mapping_ready_rows = load_jsonl(args.mapping_ready_jsonl)
    retrieval_manifest = build_retrieval_dry_run_manifest(
        ingestion_manifest,
        retrieval_ready_rows,
        retrieval_ready_rows_path=str(Path(args.retrieval_ready_jsonl).resolve()),
    )
    mapping_manifest = build_mapping_dry_run_manifest(
        ingestion_manifest,
        mapping_ready_rows,
        mapping_ready_rows_path=str(Path(args.mapping_ready_jsonl).resolve()),
    )
    report = render_downstream_dry_run_report(retrieval_manifest, mapping_manifest)

    write_text(args.output_retrieval_dry_run_json, dumps_json(retrieval_manifest))
    write_text(args.output_mapping_dry_run_json, dumps_json(mapping_manifest))
    write_text(args.output_report_md, report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

