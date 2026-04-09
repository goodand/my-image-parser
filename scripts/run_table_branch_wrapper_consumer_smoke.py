#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from table_branch_wrapper_lib import TableBranchWrapper


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (
    ROOT_DIR
    / "control"
    / "project_domain"
    / "runs"
    / "manifests"
    / "phase0_table_wrapper_consumer_smoke_at2026_03_28.json"
)
DEFAULT_DOCUMENT_ID = "01_full_presentation_2026-03-17"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a bounded downstream consumer smoke on the table branch read-only wrapper."
    )
    parser.add_argument(
        "--document-id",
        default=DEFAULT_DOCUMENT_ID,
        help="document_id used for get_tables.",
    )
    parser.add_argument(
        "--table-id",
        default="",
        help="Optional explicit table_id. If omitted, the smoke requires exactly one table for the document.",
    )
    parser.add_argument(
        "--output-json",
        default=str(DEFAULT_OUTPUT),
        help="Path to write the machine-readable consumer smoke result.",
    )
    parser.add_argument(
        "--manifest-glob",
        default=None,
        help="Optional override for the normalized manifest glob.",
    )
    return parser.parse_args()


def _build_row_chunks(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    for row in rows:
        texts = [str(cell.get("text", "")).strip() for cell in row["cells"]]
        non_empty_texts = [text for text in texts if text]
        chunks.append(
            {
                "table_id": row["table_id"],
                "row_index": row["row_index"],
                "cell_count": row["cell_count"],
                "non_empty_cell_count": len(non_empty_texts),
                "cell_ids": [cell["cell_id"] for cell in row["cells"]],
                "content": " | ".join(non_empty_texts),
            }
        )
    return chunks


def _build_worksheet_preview(rows: list[dict[str, Any]]) -> list[list[str]]:
    preview: list[list[str]] = []
    for row in rows:
        preview.append([str(cell.get("text", "")) for cell in row["cells"]])
    return preview


def _resolve_table_id(tables: list[dict[str, Any]], requested_table_id: str) -> str:
    if requested_table_id:
        return requested_table_id
    if len(tables) != 1:
        raise RuntimeError(
            "Bounded wrapper smoke requires exactly one table when --table-id is omitted."
        )
    return str(tables[0]["table_id"])


def run_consumer_smoke(args: argparse.Namespace) -> dict[str, Any]:
    wrapper = TableBranchWrapper(manifest_glob=args.manifest_glob)
    tables = wrapper.get_tables(args.document_id)
    table_id = _resolve_table_id(tables, args.table_id)
    rows = wrapper.get_table_rows(table_id)
    cells = wrapper.get_cells(table_id)

    row_chunks = _build_row_chunks(rows)
    worksheet_preview = _build_worksheet_preview(rows)

    exact_lookup_example = next(
        (
            cell
            for cell in cells
            if cell["row_index"] == 1 and cell["col_index"] == 0
        ),
        cells[0] if cells else None,
    )
    header_row = worksheet_preview[0] if worksheet_preview else []

    result = {
        "experiment": "table_branch_wrapper_consumer_smoke",
        "status": "completed",
        "document_id": args.document_id,
        "table_id": table_id,
        "table_count": len(tables),
        "row_count": len(rows),
        "cell_count": len(cells),
        "worksheet_shape": [
            len(worksheet_preview),
            max((len(row) for row in worksheet_preview), default=0),
        ],
        "header_row": header_row,
        "row_chunk_preview": row_chunks,
        "worksheet_preview": worksheet_preview,
        "exact_lookup_example": exact_lookup_example,
        "source_table_summary": next(
            table for table in tables if table["table_id"] == table_id
        ),
        "consumer_checks": {
            "tables_call_completed": True,
            "rows_call_completed": True,
            "cells_call_completed": True,
            "row_chunk_projection_completed": True,
            "worksheet_projection_completed": True,
            "exact_lookup_completed": exact_lookup_example is not None,
        },
    }

    output_path = Path(args.output_json).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def main() -> None:
    args = _parse_args()
    result = run_consumer_smoke(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
