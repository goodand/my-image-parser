#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from run_table_branch_wrapper_consumer_smoke import run_consumer_smoke


ROOT_DIR = Path(__file__).resolve().parents[1]
NORMALIZED_FIXTURE = (
    ROOT_DIR
    / "control"
    / "project_domain"
    / "runs"
    / "manifests"
    / "phase0_paddleocr_table_parse_normalized_at2026_03_28.json"
)


class _Args:
    def __init__(self, output_json: str) -> None:
        self.document_id = "01_full_presentation_2026-03-17"
        self.table_id = ""
        self.output_json = output_json
        self.manifest_glob = str(NORMALIZED_FIXTURE)


def test_consumer_smoke_with_real_fixture() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_json = str(Path(tmp_dir) / "consumer_smoke.json")
        result = run_consumer_smoke(_Args(output_json))
        assert result["status"] == "completed"
        assert result["table_count"] == 1
        assert result["row_count"] == 4
        assert result["cell_count"] == 16
        assert result["worksheet_shape"] == [4, 4]
        assert result["header_row"] == ["Metric", "70Q", "650", "Delta"]
        assert result["exact_lookup_example"]["cell_id"] == "t1_r1_c0"
        assert Path(output_json).is_file()
        payload = json.loads(Path(output_json).read_text(encoding="utf-8"))
        assert payload["experiment"] == "table_branch_wrapper_consumer_smoke"


def main() -> int:
    test_consumer_smoke_with_real_fixture()
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
