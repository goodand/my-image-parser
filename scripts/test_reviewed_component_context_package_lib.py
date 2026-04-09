#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

from reviewed_component_context_package_lib import (
    DEFAULT_COMPONENT_PROXIMITY_PADDING,
    analyze_alpha_recrop_candidates,
    build_reviewed_component_bundle,
    compare_component_ocr_to_full_image,
    compute_reviewed_table_component_bbox,
    load_json,
)


ROOT_DIR = Path(__file__).resolve().parents[1]
BASE_CONTEXT_JSON = (
    ROOT_DIR
    / "control"
    / "project_domain"
    / "resources"
    / "context_packages"
    / "full_image_ocr_baseline"
    / "01_full_presentation_2026-03-17"
    / "image11"
    / "CONTEXT_PACKAGE.json"
)
MERGED_CANDIDATE_JSON = (
    ROOT_DIR
    / "control"
    / "project_domain"
    / "resources"
    / "manifests"
    / "phase0_table_merge_candidate_at2026_03_28.json"
)


def _fake_ocr_runner(_: Path) -> dict[str, object]:
    return {
        "engine": "fake",
        "annotation_count": 16,
        "full_text": "Metric DH@10 MRR CR@10 70Q 0.757 0.622 0.514 65Q 0.815 0.670 0.554 Delta +0.058 +0.048 +0.040",
        "annotations": [{"text": token} for token in ["Metric", "DH@10", "MRR", "CR@10", "70Q", "65Q", "Delta"]],
    }


def test_compute_reviewed_table_component_bbox() -> None:
    base_context = load_json(BASE_CONTEXT_JSON)
    merged_candidate = load_json(MERGED_CANDIDATE_JSON)
    bbox = compute_reviewed_table_component_bbox(
        merged_candidate=merged_candidate,
        image_width=int(base_context["image_width"]),
        image_height=int(base_context["image_height"]),
        padding=8,
    )
    assert bbox == [6, 64, 511, 307]


def test_compare_component_ocr_to_full_image_prefers_cleaner_component() -> None:
    merged_candidate = load_json(MERGED_CANDIDATE_JSON)
    full_text = "Two-Phase Hyde-PC 52 00 Metric DH@10 MRR CR@10 70Q 0.757 0.622 0.514 65Q 0.815 0.670 0.554 Delta +0.058 +0.048 +0.040"
    component_text = "Metric DH@10 MRR CR@10 70Q 0.757 0.622 0.514 65Q 0.815 0.670 0.554 Delta +0.058 +0.048 +0.040"
    comparison = compare_component_ocr_to_full_image(
        full_image_ocr_text=full_text,
        reviewed_component_ocr_text=component_text,
        merged_candidate=merged_candidate,
    )
    assert comparison["reviewed_component_better_for_caption_input"] is True
    assert comparison["reviewed_component_extra_token_count"] < comparison["full_image_extra_token_count"]


def test_build_reviewed_component_bundle() -> None:
    base_context = load_json(BASE_CONTEXT_JSON)
    merged_candidate = load_json(MERGED_CANDIDATE_JSON)
    with tempfile.TemporaryDirectory() as temp_dir:
        package, output_paths, dataset_row, manifest_row = build_reviewed_component_bundle(
            base_context_package=base_context,
            merged_candidate=merged_candidate,
            output_root=Path(temp_dir),
            padding=8,
            ocr_runner=_fake_ocr_runner,
        )
        assert package["context_variant"] == "reviewed_isolated_component"
        assert package["image_surface"] == "reviewed_table_component_crop"
        assert package["ocr_status"] == "usable"
        assert package["review_status"] == "reviewed_candidate"
        assert package["ppt_provenance_context"]["source_kind"] == "ppt_export_manifest"
        assert package["ocr_evidence_context"]["ocr_surface"] == "reviewed_component_standalone_ocr"
        assert (
            package["ocr_evidence_context"]["comparison_against_full_image"]["reviewed_component_better_for_caption_input"]
            is True
        )
        assert manifest_row["evidence_comparison"]["reviewed_component_better_for_caption_input"] is True
        assert dataset_row["surface_type"] == "reviewed_isolated_component"
        assert Path(package["context_package_json_path"]).is_file()
        assert Path(output_paths["context_package_markdown_path"]).is_file()
        saved = json.loads(Path(package["context_package_json_path"]).read_text(encoding="utf-8"))
        assert saved["reviewed_component_enrichment"]["component_bbox_int"] == [6, 64, 511, 307]


def _write_synthetic_component_image(path: Path) -> None:
    image = Image.new("RGBA", (200, 140), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((60, 64, 156, 108), fill=(255, 255, 255, 255))
    draw.rectangle((60, 28, 170, 54), fill=(255, 255, 255, 255))
    image.save(path)


def _synthetic_base_context(image_path: Path, ocr_text_path: Path) -> dict[str, object]:
    return {
        "image_id": "synthetic:image4",
        "source_image_path": str(image_path),
        "source_dataset": "synthetic_dataset",
        "source_filename": image_path.name,
        "source_pptx": "synthetic.pptx",
        "source_slide_numbers": [18],
        "source_zip_path": "ppt/media/image4.png",
        "image_width": 200,
        "image_height": 140,
        "ocr_text_full_path": str(ocr_text_path),
        "ocr_status": "usable",
        "ocr_surface": "full_image_standalone_ocr",
        "review_status": "pending_review",
        "ppt_local_summary": "Synthetic baseline summary.",
        "notes": [],
    }


def _synthetic_merged_candidate() -> dict[str, object]:
    return {
        "document_id": "synthetic_doc",
        "page": 18,
        "table_id": "t1",
        "status": "completed",
        "comparison_difference_count": 0,
        "source_manifests": {},
        "merge_summary": {
            "total_cells": 2,
            "pending_review_count": 0,
            "auto_accept_candidate_count": 2,
        },
        "rows": [
            {
                "row_index": 0,
                "cells": [
                    {"bbox": [68, 70, 112, 88], "recommended_text": "Metric"},
                    {"bbox": [114, 70, 150, 88], "recommended_text": "Value"},
                ],
            }
        ],
    }


def _synthetic_candidate_ocr_runner(image_path: Path) -> dict[str, object]:
    name = image_path.name
    if "alpha_nearby_union" in name:
        text = "Merged Metrics Overview Metric Value"
        annotations = [{"text": token} for token in ["Merged", "Metrics", "Overview", "Metric", "Value"]]
    else:
        text = "Metric"
        annotations = [{"text": "Metric"}]
    return {
        "engine": "fake",
        "annotation_count": len(annotations),
        "full_text": text,
        "annotations": annotations,
    }


def test_multi_component_recrop_selects_augmented_candidate() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        image_path = root / "image4.png"
        ocr_text_path = root / "full_ocr.txt"
        _write_synthetic_component_image(image_path)
        ocr_text_path.write_text("Noise Metric Value random", encoding="utf-8")
        base_context = _synthetic_base_context(image_path, ocr_text_path)
        merged_candidate = _synthetic_merged_candidate()

        candidates, analysis = analyze_alpha_recrop_candidates(
            source_image_path=image_path,
            seed_bbox_int=compute_reviewed_table_component_bbox(
                merged_candidate=merged_candidate,
                image_width=200,
                image_height=140,
                padding=8,
            ),
            image_width=200,
            image_height=140,
            padding=8,
            component_proximity_padding=DEFAULT_COMPONENT_PROXIMITY_PADDING,
        )
        assert analysis["recrop_candidate_added"] is True
        assert [candidate.candidate_name for candidate in candidates] == ["seed_bbox", "alpha_nearby_union"]

        package, _, _, manifest_row = build_reviewed_component_bundle(
            base_context_package=base_context,
            merged_candidate=merged_candidate,
            output_root=root / "outputs",
            padding=8,
            ocr_runner=_synthetic_candidate_ocr_runner,
        )
        candidate_selection = package["reviewed_component_enrichment"]["candidate_selection"]
        assert candidate_selection["selected_candidate_name"] == "alpha_nearby_union"
        assert candidate_selection["candidate_count"] == 2
        assert manifest_row["selected_candidate_name"] == "alpha_nearby_union"
        saved = json.loads(Path(package["context_package_json_path"]).read_text(encoding="utf-8"))
        assert saved["reviewed_component_enrichment"]["candidate_selection"]["selected_candidate_name"] == "alpha_nearby_union"


if __name__ == "__main__":
    test_compute_reviewed_table_component_bbox()
    test_compare_component_ocr_to_full_image_prefers_cleaner_component()
    test_build_reviewed_component_bundle()
    test_multi_component_recrop_selects_augmented_candidate()
    print("OK")
