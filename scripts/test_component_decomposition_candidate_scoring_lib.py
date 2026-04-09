from __future__ import annotations

from component_decomposition_candidate_scoring_lib import score_candidate_surfaces


def _sample_probe_manifest() -> dict:
    return {
        "source_image_path": "/tmp/image4.png",
        "image_width": 1000,
        "image_height": 800,
        "component_proposals": [
            {"component_id": "full_dashboard", "component_kind": "full_dashboard"},
            {"component_id": "title_block", "component_kind": "title_block"},
            {"component_id": "chart_region", "component_kind": "chart_region"},
            {"component_id": "table_like_region", "component_kind": "table_like_region"},
        ],
        "regrouped_candidates": [
            {"candidate_name": "full_dashboard", "bbox": [0, 0, 1000, 800], "component_ids": ["full_dashboard"]},
            {"candidate_name": "title_plus_chart_set", "bbox": [0, 0, 1000, 350], "component_ids": ["title_block", "chart_region"]},
            {"candidate_name": "title_plus_table", "bbox": [0, 0, 800, 700], "component_ids": ["title_block", "table_like_region"]},
            {"candidate_name": "table_only", "bbox": [0, 400, 700, 780], "component_ids": ["table_like_region"]},
        ],
        "interpretation": {"image_kind_guess": "compound_dashboard_like"},
    }


def test_candidate_scoring_prefers_full_dashboard_for_dashboard_objective() -> None:
    payload = score_candidate_surfaces(_sample_probe_manifest())
    assert payload["profiles"]["dashboard_overview_caption_input"]["winner_candidate"] == "full_dashboard"


def test_candidate_scoring_prefers_title_plus_table_for_table_focus() -> None:
    payload = score_candidate_surfaces(_sample_probe_manifest())
    assert payload["profiles"]["embedded_table_focus"]["winner_candidate"] == "title_plus_table"
