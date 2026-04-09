from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dumps_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def dumps_jsonl(rows: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)


def _decision_focus(image: dict[str, Any]) -> list[str]:
    focus = ["caption_quality", "default_vs_winner_decision"]
    if image.get("pending_context_review_arms"):
        focus.append("context_review_confirmation")
    if image.get("winner_promotion_state") == "comparison_ready_reviewed_branch":
        focus.append("reviewed_branch_promotion_check")
    return focus


def _default_retrieval_policy(image: dict[str, Any]) -> str:
    if image.get("default_retention_reason_code") == "winner_is_current_default_anchor":
        return "active_default_is_current_winner"
    return "hold_active_default_until_human_review"


def build_review_decision_seed(
    review_surface: dict[str, Any],
    *,
    review_surface_path: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for image in review_surface["images"]:
        rows.append(
            {
                "schema_version": "v1",
                "decision_capture_kind": "corpus_review_decision",
                "image_id": image["image_id"],
                "source_image_path": image["source_image_path"],
                "review_surface_path": review_surface_path,
                "review_markdown_path": review_surface["review_markdown_path"],
                "bundle_path": image["bundle_path"],
                "active_default_arm": image["current_default"],
                "comparison_winner": image["comparison_winner"],
                "comparison_winner_promotion_state": image["winner_promotion_state"],
                "baseline_retained": image["baseline_retained"],
                "review_priority_label": image["priority_label"],
                "pending_context_review_arms": image["pending_context_review_arms"],
                "selected_caption_arm": None,
                "selected_caption_promotion_state": None,
                "caption_decision": None,
                "caption_edit_required": None,
                "approved_caption": None,
                "approved_alt_text": None,
                "use_for_retrieval": False,
                "mapping_review_required": None,
                "outlier_candidate": False,
                "review_status": "pending",
                "reviewer_id": None,
                "reviewed_at": None,
                "decision_rationale": None,
                "retrieval_block_reason": "policy_hold",
                "outlier_reason": None,
                "reviewer_notes": None,
            }
        )
    return rows


def build_retrieval_input_seed(review_surface: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for image in review_surface["images"]:
        rows.append(
            {
                "image_id": image["image_id"],
                "source_image_path": image["source_image_path"],
                "active_default_arm": image["current_default"],
                "comparison_winner": image["comparison_winner"],
                "winner_promotion_state": image["winner_promotion_state"],
                "default_retention_reason_code": image["default_retention_reason_code"],
                "priority_label": image["priority_label"],
                "priority_rank": image["priority_rank"],
                "retrieval_ready": False,
                "retrieval_blockers": [
                    "caption_review_pending",
                    "approved_caption_not_selected",
                ],
                "retrieval_caption_source_policy": _default_retrieval_policy(image),
                "required_human_fields": [
                    "selected_caption_arm",
                    "approved_caption",
                    "use_for_retrieval",
                ],
                "fallback_reference_fields": [
                    "current_default",
                    "comparison_winner",
                    "winner_promotion_state",
                ],
            }
        )
    return rows


def build_mapping_review_seed(review_surface: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for image in review_surface["images"]:
        rows.append(
            {
                "image_id": image["image_id"],
                "source_image_path": image["source_image_path"],
                "active_default_arm": image["current_default"],
                "comparison_winner": image["comparison_winner"],
                "winner_promotion_state": image["winner_promotion_state"],
                "priority_label": image["priority_label"],
                "priority_rank": image["priority_rank"],
                "mapping_ready": False,
                "mapping_blockers": [
                    "caption_review_pending",
                    "retrieval_not_run",
                ],
                "required_human_fields": [
                    "mapping_review_required",
                    "outlier_candidate",
                    "reviewer_notes",
                ],
                "mapping_resolution_template": {
                    "selected_document_id": None,
                    "resolution": "pending_review",
                    "manual_description_required": None,
                },
            }
        )
    return rows


def build_preflight_manifest(
    review_surface: dict[str, Any],
    *,
    review_surface_path: str,
    decision_seed_path: str,
    retrieval_seed_path: str,
    mapping_seed_path: str,
) -> dict[str, Any]:
    image_ids = review_surface["priority_sorted_image_ids"]
    return {
        "schema_version": "phase2_review_to_retrieval_preflight.v1",
        "used_truth_source": review_surface_path,
        "machine_truth_mode": review_surface["machine_truth_contract"]["machine_truth_source"],
        "machine_truth_manifest_only": review_surface["machine_truth_contract"]["session_b_may_use_manifest_only"],
        "image_count": review_surface["image_count"],
        "image_ids": image_ids,
        "active_default_baseline": review_surface["images"][0]["current_default"] if review_surface["images"] else None,
        "comparison_winner_candidates": {
            image["image_id"]: image["comparison_winner"] for image in review_surface["images"]
        },
        "default_retention_reason_codes": {
            image["image_id"]: image["default_retention_reason_code"] for image in review_surface["images"]
        },
        "priority_sorted_image_ids": image_ids,
        "highest_priority_image_ids": review_surface.get("highest_priority_image_ids", []),
        "high_priority_image_ids": review_surface.get("high_priority_image_ids", []),
        "required_human_decision_fields": [
            "selected_caption_arm",
            "approved_caption",
            "approved_alt_text",
            "use_for_retrieval",
            "mapping_review_required",
            "outlier_candidate",
            "reviewer_notes",
        ],
        "downstream_status": {
            "retrieval_ready": False,
            "mapping_ready": False,
            "regeneration_ready": False,
        },
        "generated_outputs": {
            "decision_seed_jsonl": decision_seed_path,
            "retrieval_input_seed_jsonl": retrieval_seed_path,
            "mapping_review_seed_jsonl": mapping_seed_path,
        },
    }


def render_preflight_report(preflight: dict[str, Any]) -> str:
    lines = [
        "# Phase 2 Corpus Review To Retrieval Preflight",
        "",
        "## Purpose",
        "",
        "Bridge the human-facing corpus review surface into machine-readable decision, retrieval, and mapping seeds without regenerating any caption arms.",
        "",
        "## Used Truth Source",
        "",
        f"- review surface manifest: `{preflight['used_truth_source']}`",
        f"- machine truth mode: `{preflight['machine_truth_mode']}`",
        f"- manifest-only consumer: `{str(preflight['machine_truth_manifest_only']).lower()}`",
        "",
        "## Corpus Summary",
        "",
        f"- image_count: `{preflight['image_count']}`",
        f"- image_ids: `{', '.join(preflight['image_ids'])}`",
        f"- active default baseline: `{preflight['active_default_baseline']}`",
        "",
        "## Human Review Carry-Over",
        "",
        f"- highest priority: `{', '.join(preflight['highest_priority_image_ids'])}`",
        f"- high priority: `{', '.join(preflight['high_priority_image_ids'])}`",
        "",
        "## Output Seeds",
        "",
        f"- decision seed: `{preflight['generated_outputs']['decision_seed_jsonl']}`",
        f"- retrieval input seed: `{preflight['generated_outputs']['retrieval_input_seed_jsonl']}`",
        f"- mapping review seed: `{preflight['generated_outputs']['mapping_review_seed_jsonl']}`",
        "",
        "## Guardrails",
        "",
        "- keep `full_image_baseline` as the active default until a later explicit promotion decision closes",
        "- do not treat comparison winners as default replacements",
        "- treat reviewed or parser reruns in pending-review state as comparison-only inputs",
        "- do not run retrieval or mapping in this slice; only prepare seeds",
        "",
        "## Required Human Decision Fields",
        "",
    ]
    for field in preflight["required_human_decision_fields"]:
        lines.append(f"- `{field}`")
    lines.extend(
        [
            "",
            "## Current Downstream Status",
            "",
            f"- retrieval_ready: `{str(preflight['downstream_status']['retrieval_ready']).lower()}`",
            f"- mapping_ready: `{str(preflight['downstream_status']['mapping_ready']).lower()}`",
            f"- regeneration_ready: `{str(preflight['downstream_status']['regeneration_ready']).lower()}`",
        ]
    )
    return "\n".join(lines) + "\n"
