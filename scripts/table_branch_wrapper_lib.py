#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT_PATH = (
    ROOT_DIR
    / "control"
    / "project_domain"
    / "resources"
    / "specs"
    / "contracts"
    / "table_branch_wrapper_surface.contract.json"
)


class TableBranchWrapperError(RuntimeError):
    pass


class InvalidNormalizedManifestError(TableBranchWrapperError):
    pass


class TableNotFoundError(TableBranchWrapperError):
    pass


class AmbiguousTableIdError(TableBranchWrapperError):
    pass


@dataclass(frozen=True)
class NormalizedTableRecord:
    normalized_manifest_path: Path
    document_id: str
    page: int | None
    table_id: str
    source_image_path: str
    rows: list[dict[str, Any]]

    @property
    def row_count(self) -> int:
        return len(self.rows)

    @property
    def column_count(self) -> int:
        max_column = 0
        for row in self.rows:
            for cell in row.get("cells", []):
                col_index = int(cell.get("col_index", 0))
                col_span = int(cell.get("col_span", 1))
                max_column = max(max_column, col_index + col_span)
        return max_column


def _load_contract(contract_path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(contract_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise TableBranchWrapperError(f"Wrapper contract not found: {contract_path}") from exc
    except json.JSONDecodeError as exc:
        raise TableBranchWrapperError(f"Wrapper contract is invalid JSON: {contract_path}: {exc}") from exc
    return payload


def _require_fields(payload: dict[str, Any], fields: list[str], manifest_path: Path) -> None:
    missing = [field for field in fields if field not in payload]
    if missing:
        raise InvalidNormalizedManifestError(
            f"Normalized manifest missing required fields {missing}: {manifest_path}"
        )


def _coerce_page(value: Any, manifest_path: Path) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise InvalidNormalizedManifestError(
            f"Normalized manifest has non-integer page={value!r}: {manifest_path}"
        ) from exc


def _parse_record(manifest_path: Path, required_fields: list[str]) -> NormalizedTableRecord:
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise InvalidNormalizedManifestError(
            f"Normalized manifest is invalid JSON: {manifest_path}: {exc}"
        ) from exc

    if not isinstance(payload, dict):
        raise InvalidNormalizedManifestError(f"Normalized manifest is not a JSON object: {manifest_path}")

    _require_fields(payload, required_fields, manifest_path)

    source_image_path = payload.get("source_image_path")
    rows = payload.get("rows")
    if not isinstance(source_image_path, str) or not source_image_path:
        raise InvalidNormalizedManifestError(
            f"Normalized manifest missing source_image_path: {manifest_path}"
        )
    if not isinstance(rows, list):
        raise InvalidNormalizedManifestError(f"Normalized manifest rows is not a list: {manifest_path}")

    for row in rows:
        if not isinstance(row, dict):
            raise InvalidNormalizedManifestError(f"Normalized manifest row is not an object: {manifest_path}")
        if "row_index" not in row or "cells" not in row:
            raise InvalidNormalizedManifestError(
                f"Normalized manifest row missing row_index or cells: {manifest_path}"
            )
        if not isinstance(row["cells"], list):
            raise InvalidNormalizedManifestError(f"Normalized manifest row cells is not a list: {manifest_path}")

    return NormalizedTableRecord(
        normalized_manifest_path=manifest_path.resolve(),
        document_id=str(payload["document_id"]),
        page=_coerce_page(payload.get("page"), manifest_path),
        table_id=str(payload["table_id"]),
        source_image_path=source_image_path,
        rows=rows,
    )


class TableBranchWrapper:
    def __init__(
        self,
        *,
        contract_path: Path = DEFAULT_CONTRACT_PATH,
        manifest_glob: str | None = None,
    ) -> None:
        self.contract_path = contract_path.resolve()
        self.contract = _load_contract(self.contract_path)
        self.required_fields = list(
            self.contract["normalized_read_surface"]["required_top_level_fields"]
        )
        self.manifest_glob = manifest_glob or str(self.contract["normalized_read_surface"]["glob"])
        self.records = self._load_records()

    def _load_records(self) -> list[NormalizedTableRecord]:
        manifest_paths = sorted(Path().glob(self.manifest_glob)) if not Path(self.manifest_glob).is_absolute() else []
        if Path(self.manifest_glob).is_absolute():
            manifest_paths = sorted(Path("/").glob(self.manifest_glob.lstrip("/")))
        if not manifest_paths:
            raise TableBranchWrapperError(
                f"No normalized manifests matched glob: {self.manifest_glob}"
            )
        return [_parse_record(path, self.required_fields) for path in manifest_paths]

    def _resolve_unique_table(self, table_id: str) -> NormalizedTableRecord:
        matches = [record for record in self.records if record.table_id == table_id]
        if not matches:
            raise TableNotFoundError(f"No normalized table found for table_id={table_id!r}.")
        if len(matches) > 1:
            paths = [str(record.normalized_manifest_path) for record in matches]
            raise AmbiguousTableIdError(
                f"Ambiguous table_id={table_id!r} across manifests: {paths}"
            )
        return matches[0]

    def get_tables(self, document_id: str) -> list[dict[str, Any]]:
        matches = [record for record in self.records if record.document_id == document_id]
        if not matches:
            raise TableNotFoundError(
                f"No normalized table exists for document_id={document_id!r}."
            )
        return [
            {
                "document_id": record.document_id,
                "page": record.page,
                "table_id": record.table_id,
                "source_image_path": record.source_image_path,
                "row_count": record.row_count,
                "column_count": record.column_count,
                "normalized_manifest_path": str(record.normalized_manifest_path),
            }
            for record in sorted(matches, key=lambda item: (item.page or -1, item.table_id))
        ]

    def get_table_rows(self, table_id: str) -> list[dict[str, Any]]:
        record = self._resolve_unique_table(table_id)
        rows: list[dict[str, Any]] = []
        for row in sorted(record.rows, key=lambda item: int(item["row_index"])):
            rows.append(
                {
                    "table_id": record.table_id,
                    "row_index": int(row["row_index"]),
                    "cell_count": len(row["cells"]),
                    "cells": row["cells"],
                }
            )
        return rows

    def get_cells(self, table_id: str) -> list[dict[str, Any]]:
        record = self._resolve_unique_table(table_id)
        flattened: list[dict[str, Any]] = []
        for row in sorted(record.rows, key=lambda item: int(item["row_index"])):
            row_index = int(row["row_index"])
            for cell in row["cells"]:
                flattened.append(
                    {
                        "table_id": record.table_id,
                        "row_index": row_index,
                        "cell_id": cell["cell_id"],
                        "col_index": int(cell["col_index"]),
                        "text": cell["text"],
                        "row_span": int(cell["row_span"]),
                        "col_span": int(cell["col_span"]),
                        "bbox": cell["bbox"],
                        "confidence": cell["confidence"],
                    }
                )
        return flattened


def get_tables(document_id: str, *, manifest_glob: str | None = None) -> list[dict[str, Any]]:
    return TableBranchWrapper(manifest_glob=manifest_glob).get_tables(document_id)


def get_table_rows(table_id: str, *, manifest_glob: str | None = None) -> list[dict[str, Any]]:
    return TableBranchWrapper(manifest_glob=manifest_glob).get_table_rows(table_id)


def get_cells(table_id: str, *, manifest_glob: str | None = None) -> list[dict[str, Any]]:
    return TableBranchWrapper(manifest_glob=manifest_glob).get_cells(table_id)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only wrapper over normalized Table -> Row -> Cell manifests."
    )
    parser.add_argument(
        "--manifest-glob",
        default=None,
        help="Override the normalized manifest glob from the wrapper contract.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    tables_parser = subparsers.add_parser("tables", help="Return table summaries for one document_id.")
    tables_parser.add_argument("--document-id", required=True)

    rows_parser = subparsers.add_parser("rows", help="Return ordered rows for one table_id.")
    rows_parser.add_argument("--table-id", required=True)

    cells_parser = subparsers.add_parser("cells", help="Return flattened cells for one table_id.")
    cells_parser.add_argument("--table-id", required=True)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    wrapper = TableBranchWrapper(manifest_glob=args.manifest_glob)
    if args.command == "tables":
        payload = wrapper.get_tables(args.document_id)
    elif args.command == "rows":
        payload = wrapper.get_table_rows(args.table_id)
    else:
        payload = wrapper.get_cells(args.table_id)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
