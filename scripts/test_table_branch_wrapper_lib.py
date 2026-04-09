#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from table_branch_wrapper_lib import (
    AmbiguousTableIdError,
    TableBranchWrapper,
    TableNotFoundError,
)


ROOT_DIR = Path(__file__).resolve().parents[1]
NORMALIZED_FIXTURE = (
    ROOT_DIR
    / "control"
    / "project_domain"
    / "runs"
    / "manifests"
    / "phase0_paddleocr_table_parse_normalized_at2026_03_28.json"
)


def test_get_tables_from_real_fixture() -> None:
    wrapper = TableBranchWrapper(
        manifest_glob=str(NORMALIZED_FIXTURE),
    )
    tables = wrapper.get_tables("01_full_presentation_2026-03-17")
    assert len(tables) == 1
    assert tables[0]["table_id"] == "t1"
    assert tables[0]["row_count"] == 4
    assert tables[0]["column_count"] == 4
    assert tables[0]["page"] == 24


def test_get_table_rows_from_real_fixture() -> None:
    wrapper = TableBranchWrapper(
        manifest_glob=str(NORMALIZED_FIXTURE),
    )
    rows = wrapper.get_table_rows("t1")
    assert len(rows) == 4
    assert rows[0]["row_index"] == 0
    assert rows[0]["cell_count"] == 4
    assert rows[0]["cells"][0]["text"] == "Metric"


def test_get_cells_from_real_fixture() -> None:
    wrapper = TableBranchWrapper(
        manifest_glob=str(NORMALIZED_FIXTURE),
    )
    cells = wrapper.get_cells("t1")
    assert len(cells) == 16
    assert cells[0]["cell_id"] == "t1_r0_c0"
    assert cells[-1]["cell_id"] == "t1_r3_c3"


def test_missing_document_fails() -> None:
    wrapper = TableBranchWrapper(
        manifest_glob=str(NORMALIZED_FIXTURE),
    )
    try:
        wrapper.get_tables("missing-document")
    except TableNotFoundError:
        return
    raise AssertionError("Expected TableNotFoundError for missing document_id.")


def test_ambiguous_table_id_fails() -> None:
    payload = json.loads(NORMALIZED_FIXTURE.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        first = root / "first_table_normalized.json"
        second = root / "second_table_normalized.json"
        first.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        payload["document_id"] = "another-document"
        second.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        wrapper = TableBranchWrapper(
            manifest_glob=str(root / "*table_normalized.json"),
        )
        try:
            wrapper.get_table_rows("t1")
        except AmbiguousTableIdError:
            return
    raise AssertionError("Expected AmbiguousTableIdError for duplicated table_id.")


def main() -> int:
    test_get_tables_from_real_fixture()
    test_get_table_rows_from_real_fixture()
    test_get_cells_from_real_fixture()
    test_missing_document_fails()
    test_ambiguous_table_id_fails()
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
