#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from full_image_ocr_context_package_lib import (
    build_context_package,
    determine_ocr_status,
    determine_review_status,
    find_manifest_record,
    update_context_package_manifest,
)


ROOT_DIR = Path(__file__).resolve().parents[1]
SAMPLE_IMAGE = (
    ROOT_DIR
    / "control"
    / "project_domain"
    / "resources"
    / "pptx_jobs"
    / "01_full_presentation_2026-03-17"
    / "media"
    / "image11.png"
)


def test_manifest_lookup() -> None:
    record = find_manifest_record(SAMPLE_IMAGE)
    assert record is not None
    assert record.dataset == "01_full_presentation_2026-03-17"
    assert record.image_file == "image11.png"
    assert record.slide_numbers == [24]


def test_status_mapping() -> None:
    assert determine_ocr_status({"error": "boom"}) == "error"
    assert determine_ocr_status({"annotation_count": 0, "full_text": ""}) == "no_text"
    assert determine_ocr_status({"annotation_count": 1, "full_text": "650"}) == "weak_text"
    assert determine_ocr_status({"annotation_count": 18, "full_text": "DH@10 MRR CR@10 70Q 65Q delta"}) == "usable"
    assert determine_review_status("usable") == "pending_review"
    assert determine_review_status("weak_text") == "needs_more_context"
    assert determine_review_status("error") == "rejected"


def test_build_context_package_with_fixture_ocr() -> None:
    fixture_ocr = {
        "filename": "image11.png",
        "annotations": [{"text": "DH@10", "confidence": 0.9, "bounding_box": None}],
        "annotation_count": 18,
        "full_text": "DH@10 MRR CR@10 70Q 65Q delta values table",
        "engine": "ocrmac",
    }
    with tempfile.TemporaryDirectory() as tmpdir:
        output_root = Path(tmpdir)
        package, output_paths = build_context_package(
            image_path=SAMPLE_IMAGE,
            output_root=output_root,
            ocr_result=fixture_ocr,
            extra_notes=["fixture run"],
        )
        assert package.image_id == "01_full_presentation_2026-03-17:image11.png"
        assert package.ocr_status == "usable"
        assert package.review_status == "pending_review"
        assert "full_presentation_2026-03-17.pptx" in package.ppt_local_summary
        assert package.ppt_provenance_context is not None
        assert package.ppt_provenance_context["source_kind"] == "ppt_export_manifest"
        assert package.ppt_provenance_context["source_slide_numbers"] == [24]
        assert package.ocr_evidence_context is not None
        assert package.ocr_evidence_context["ocr_surface"] == "full_image_standalone_ocr"
        assert package.ocr_evidence_context["ocr_status"] == "usable"
        assert output_paths["context_package_markdown_path"].is_file()
        assert output_paths["context_package_json_path"].is_file()
        assert output_paths["ocr_result_json_path"].is_file()
        manifest_jsonl = output_root / "manifest.jsonl"
        update_context_package_manifest(manifest_jsonl, package)
        rows = [json.loads(line) for line in manifest_jsonl.read_text(encoding="utf-8").splitlines() if line.strip()]
        assert len(rows) == 1
        assert rows[0]["image_id"] == package.image_id


def main() -> int:
    test_manifest_lookup()
    test_status_mapping()
    test_build_context_package_with_fixture_ocr()
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
