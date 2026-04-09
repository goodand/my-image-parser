from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        rows.append(json.loads(stripped))
    return rows


def dumps_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def build_retrieval_dry_run_manifest(
    ingestion_manifest: dict[str, Any],
    retrieval_ready_rows: list[dict[str, Any]],
    *,
    retrieval_ready_rows_path: str,
) -> dict[str, Any]:
    return {
        "schema_version": "phase2_retrieval_dry_run.v1",
        "decision_ingestion_path": ingestion_manifest["decision_seed_path"],
        "retrieval_ready_rows_path": retrieval_ready_rows_path,
        "input_row_count": ingestion_manifest["input_row_count"],
        "retrieval_ready_count": len(retrieval_ready_rows),
        "retrieval_ready_image_ids": [row["image_id"] for row in retrieval_ready_rows],
        "active_default_baseline": "full_image_baseline",
        "execution_mode": "dry_run_only",
        "ready_to_execute": len(retrieval_ready_rows) > 0,
        "blocked_reason": (
            None
            if retrieval_ready_rows
            else "no_completed_review_rows_marked_for_retrieval"
        ),
        "next_runtime_inputs": [
            "approved_caption",
            "source_image_path",
            "selected_caption_arm",
            "selected_caption_promotion_state",
        ],
        "planned_outputs": [
            "retrieval_input.jsonl",
            "retrieval_candidates.jsonl",
            "reranked_top5.jsonl",
        ],
    }


def build_mapping_dry_run_manifest(
    ingestion_manifest: dict[str, Any],
    mapping_ready_rows: list[dict[str, Any]],
    *,
    mapping_ready_rows_path: str,
) -> dict[str, Any]:
    return {
        "schema_version": "phase2_mapping_dry_run.v1",
        "decision_ingestion_path": ingestion_manifest["decision_seed_path"],
        "mapping_ready_rows_path": mapping_ready_rows_path,
        "input_row_count": ingestion_manifest["input_row_count"],
        "mapping_ready_count": len(mapping_ready_rows),
        "mapping_ready_image_ids": [row["image_id"] for row in mapping_ready_rows],
        "execution_mode": "dry_run_only",
        "ready_to_execute": len(mapping_ready_rows) > 0,
        "blocked_reason": (
            None
            if mapping_ready_rows
            else "no_completed_review_rows_ready_for_mapping"
        ),
        "next_runtime_inputs": [
            "approved_caption",
            "selected_caption_arm",
            "selected_caption_promotion_state",
            "mapping_review_required",
        ],
        "planned_outputs": [
            "mapping_review.jsonl",
            "mapping_selected.jsonl",
            "outlier_labeled.jsonl",
        ],
    }


def render_downstream_dry_run_report(
    retrieval_manifest: dict[str, Any],
    mapping_manifest: dict[str, Any],
) -> str:
    lines = [
        "# Phase 2 Review Decision Downstream Dry Run",
        "",
        "## Purpose",
        "",
        "Freeze the next runtime contract after review decision ingestion without executing retrieval or mapping.",
        "",
        "## Retrieval Dry Run",
        "",
        f"- retrieval_ready_count: `{retrieval_manifest['retrieval_ready_count']}`",
        f"- retrieval_ready_image_ids: `{', '.join(retrieval_manifest['retrieval_ready_image_ids']) if retrieval_manifest['retrieval_ready_image_ids'] else 'none'}`",
        f"- ready_to_execute: `{str(retrieval_manifest['ready_to_execute']).lower()}`",
        f"- blocked_reason: `{retrieval_manifest['blocked_reason'] or 'none'}`",
        "",
        "Planned outputs:",
    ]
    for item in retrieval_manifest["planned_outputs"]:
        lines.append(f"- `{item}`")
    lines.extend(
        [
            "",
            "## Mapping Dry Run",
            "",
            f"- mapping_ready_count: `{mapping_manifest['mapping_ready_count']}`",
            f"- mapping_ready_image_ids: `{', '.join(mapping_manifest['mapping_ready_image_ids']) if mapping_manifest['mapping_ready_image_ids'] else 'none'}`",
            f"- ready_to_execute: `{str(mapping_manifest['ready_to_execute']).lower()}`",
            f"- blocked_reason: `{mapping_manifest['blocked_reason'] or 'none'}`",
            "",
            "Planned outputs:",
        ]
    )
    for item in mapping_manifest["planned_outputs"]:
        lines.append(f"- `{item}`")
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- do not execute retrieval in this slice",
            "- do not execute reranking in this slice",
            "- do not finalize mapping in this slice",
            "- rerun this dry-run builder after human review rows move from pending to completed",
        ]
    )
    return "\n".join(lines) + "\n"

