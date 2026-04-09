#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from table_parser_sidecar_promotion_lib import promote_raw_sidecar_to_canonical


ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_FIXTURE = (
    ROOT_DIR
    / "control"
    / "project_domain"
    / "resources"
    / "manifests"
    / "phase0_paddleocr_table_parse_raw_at2026_03_28.json"
)
NORMALIZED_FIXTURE = (
    ROOT_DIR
    / "control"
    / "project_domain"
    / "resources"
    / "manifests"
    / "phase0_paddleocr_table_parse_normalized_at2026_03_28.json"
)


def test_promote_raw_sidecar_to_canonical_with_real_fixture() -> None:
    result = promote_raw_sidecar_to_canonical(raw_sidecar_json=RAW_FIXTURE)
    expected = json.loads(NORMALIZED_FIXTURE.read_text(encoding="utf-8"))
    assert result.normalized_status == "completed"
    assert result.normalized_record is not None
    assert result.normalized_record["document_id"] == expected["document_id"]
    assert result.normalized_record["page"] == expected["page"]
    assert result.normalized_record["table_id"] == expected["table_id"]
    assert result.normalized_record["source_image_path"] == expected["source_image_path"]
    assert result.normalized_record["parser_backend"] == expected["parser_backend"]
    assert len(result.normalized_record["rows"]) == len(expected["rows"])
    assert result.normalized_record["rows"][0]["cells"][0]["text"] == expected["rows"][0]["cells"][0]["text"]
    assert result.normalized_record["rows"][1]["cells"][0]["cell_id"] == expected["rows"][1]["cells"][0]["cell_id"]


def test_promote_script_default_output_naming() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        raw_copy = Path(tmp_dir) / "sample_raw_result.json"
        raw_copy.write_text(RAW_FIXTURE.read_text(encoding="utf-8"), encoding="utf-8")
        result = promote_raw_sidecar_to_canonical(raw_sidecar_json=raw_copy)
        assert result.normalized_status == "completed"
        assert result.manifest_path is not None


def test_promote_apple_helper_sidecar_to_canonical_with_synthetic_fixture() -> None:
    expected = json.loads(NORMALIZED_FIXTURE.read_text(encoding="utf-8"))
    image_path = expected["source_image_path"]
    helper_payload = {
        "status": "completed",
        "backend": "apple_vision_recognize_documents_request",
        "helper_role": "table_structure_hint_sidecar",
        "ownership_skill": "parser-sidecar-to-canonical-schema-promotion",
        "input_path": image_path,
        "documents": [
            {
                "document_index": 0,
                "tables": [
                    {
                        "table_index": 0,
                        "row_count": 2,
                        "column_count": 2,
                        "cell_count": 4,
                        "cells": [
                            {
                                "row_range": [0, 0],
                                "column_range": [0, 0],
                                "transcript": "Metric",
                                "line_candidates": [{"confidence": 0.91, "transcript": "Metric"}],
                                "bounding_region": {
                                    "bounding_box": {"x": 0.1, "y": 0.2, "width": 0.2, "height": 0.1}
                                },
                            },
                            {
                                "row_range": [0, 0],
                                "column_range": [1, 1],
                                "transcript": "70Q",
                                "line_candidates": [{"confidence": 0.92, "transcript": "70Q"}],
                                "bounding_region": {
                                    "bounding_box": {"x": 0.3, "y": 0.2, "width": 0.2, "height": 0.1}
                                },
                            },
                            {
                                "row_range": [1, 1],
                                "column_range": [0, 0],
                                "transcript": "DH@10",
                                "line_candidates": [{"confidence": 0.93, "transcript": "DH@10"}],
                                "bounding_region": {
                                    "bounding_box": {"x": 0.1, "y": 0.3, "width": 0.2, "height": 0.1}
                                },
                            },
                            {
                                "row_range": [1, 1],
                                "column_range": [1, 1],
                                "transcript": "0.757",
                                "line_candidates": [{"confidence": 0.94, "transcript": "0.757"}],
                                "bounding_region": {
                                    "bounding_box": {"x": 0.3, "y": 0.3, "width": 0.2, "height": 0.1}
                                },
                            },
                        ],
                    }
                ],
            }
        ],
    }

    with tempfile.TemporaryDirectory() as tmp_dir:
        raw_helper = Path(tmp_dir) / "apple_helper_sidecar.json"
        raw_helper.write_text(json.dumps(helper_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        result = promote_raw_sidecar_to_canonical(raw_sidecar_json=raw_helper)

    assert result.normalized_status == "completed"
    assert result.normalized_record is not None
    assert result.normalized_record["document_id"] == expected["document_id"]
    assert result.normalized_record["page"] == expected["page"]
    assert result.normalized_record["parser_backend"] == "apple_vision_recognize_documents_request"
    assert result.normalized_record["normalization_mode"] == "documents[0].tables[0].cells"
    assert len(result.normalized_record["rows"]) == 2
    assert result.normalized_record["rows"][0]["cells"][0]["text"] == "Metric"
    assert result.normalized_record["rows"][1]["cells"][1]["text"] == "0.757"
    assert result.normalized_record["rows"][0]["cells"][0]["confidence"] == 0.91


def main() -> int:
    test_promote_raw_sidecar_to_canonical_with_real_fixture()
    test_promote_script_default_output_naming()
    test_promote_apple_helper_sidecar_to_canonical_with_synthetic_fixture()
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
