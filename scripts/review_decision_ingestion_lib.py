from __future__ import annotations

import json
from pathlib import Path
from typing import Any


MACHINE_PREFILLED_FIELD_MAP: dict[str, str] = {
    "source_image_path": "source_image_path",
    "review_surface_path": "__review_surface_path__",
    "review_markdown_path": "__top_level_review_markdown_path__",
    "bundle_path": "bundle_path",
    "active_default_arm": "current_default",
    "comparison_winner": "comparison_winner",
    "comparison_winner_promotion_state": "winner_promotion_state",
    "baseline_retained": "baseline_retained",
    "review_priority_label": "priority_label",
    "pending_context_review_arms": "pending_context_review_arms",
}


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


def dumps_jsonl(rows: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)


def _expected_prefilled_lookup(
    review_surface: dict[str, Any],
    *,
    review_surface_path: str,
) -> tuple[list[str], dict[str, dict[str, Any]]]:
    images = sorted(
        review_surface.get("images", []),
        key=lambda item: item.get("priority_rank", 10**9),
    )
    expected_order = [item["image_id"] for item in images]
    lookup: dict[str, dict[str, Any]] = {}
    for item in images:
        lookup[item["image_id"]] = {
            "source_image_path": item["source_image_path"],
            "review_surface_path": review_surface_path,
            "review_markdown_path": review_surface["review_markdown_path"],
            "bundle_path": item["bundle_path"],
            "active_default_arm": item["current_default"],
            "comparison_winner": item["comparison_winner"],
            "comparison_winner_promotion_state": item["winner_promotion_state"],
            "baseline_retained": item["baseline_retained"],
            "review_priority_label": item["priority_label"],
            "pending_context_review_arms": item["pending_context_review_arms"],
        }
    return expected_order, lookup


def validate_machine_prefilled_fields(
    decision_rows: list[dict[str, Any]],
    *,
    review_surface: dict[str, Any],
    review_surface_path: str,
) -> None:
    expected_order, lookup = _expected_prefilled_lookup(
        review_surface,
        review_surface_path=review_surface_path,
    )
    actual_order = [row["image_id"] for row in decision_rows]
    if actual_order != expected_order:
        raise ValueError(
            "Decision row order drift detected: "
            f"expected {expected_order}, got {actual_order}"
        )

    drifts: list[str] = []
    for row in decision_rows:
        image_id = row["image_id"]
        expected_row = lookup.get(image_id)
        if expected_row is None:
            drifts.append(f"{image_id}: missing from review surface")
            continue
        for field_name in MACHINE_PREFILLED_FIELD_MAP:
            if row.get(field_name) != expected_row.get(field_name):
                drifts.append(
                    f"{image_id}.{field_name}: "
                    f"expected {expected_row.get(field_name)!r}, got {row.get(field_name)!r}"
                )
    if drifts:
        raise ValueError(
            "Machine-prefilled field drift detected:\n- " + "\n- ".join(drifts)
        )


def is_retrieval_eligible(row: dict[str, Any]) -> bool:
    approved_caption = row.get("approved_caption")
    return (
        row.get("review_status") == "completed"
        and row.get("use_for_retrieval") is True
        and isinstance(approved_caption, str)
        and approved_caption.strip() != ""
    )


def is_mapping_eligible(row: dict[str, Any]) -> bool:
    if not is_retrieval_eligible(row):
        return False
    return row.get("mapping_review_required") is not False


def build_ingestion_manifest(
    decision_rows: list[dict[str, Any]],
    *,
    decision_seed_path: str,
    retrieval_ready_path: str,
    mapping_ready_path: str,
) -> dict[str, Any]:
    retrieval_ready = [row for row in decision_rows if is_retrieval_eligible(row)]
    mapping_ready = [row for row in decision_rows if is_mapping_eligible(row)]
    pending = [row for row in decision_rows if row.get("review_status") == "pending"]
    deferred = [row for row in decision_rows if row.get("review_status") == "deferred"]
    completed = [row for row in decision_rows if row.get("review_status") == "completed"]
    return {
        "schema_version": "phase2_review_decision_ingestion.v1",
        "decision_seed_path": decision_seed_path,
        "input_row_count": len(decision_rows),
        "review_status_counts": {
            "pending": len(pending),
            "completed": len(completed),
            "deferred": len(deferred),
        },
        "retrieval_ready_count": len(retrieval_ready),
        "mapping_ready_count": len(mapping_ready),
        "retrieval_ready_image_ids": [row["image_id"] for row in retrieval_ready],
        "mapping_ready_image_ids": [row["image_id"] for row in mapping_ready],
        "blocked_image_ids": [row["image_id"] for row in decision_rows if not is_retrieval_eligible(row)],
        "generated_outputs": {
            "retrieval_ready_rows_jsonl": retrieval_ready_path,
            "mapping_ready_rows_jsonl": mapping_ready_path,
        },
        "next_action": (
            "fill human decision rows and rerun ingestion"
            if not retrieval_ready
            else "run retrieval/mapping preflight on ready rows"
        ),
    }


def render_ingestion_report(manifest: dict[str, Any]) -> str:
    lines = [
        "# Phase 2 Review Decision Ingestion",
        "",
        "## Purpose",
        "",
        "Consume the corpus review decision rows and materialize only the retrieval-ready and mapping-ready subsets.",
        "",
        "## Input",
        "",
        f"- decision seed path: `{manifest['decision_seed_path']}`",
        f"- input_row_count: `{manifest['input_row_count']}`",
        "",
        "## Review Status Counts",
        "",
    ]
    for key, value in manifest["review_status_counts"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            "## Ready Counts",
            "",
            f"- retrieval_ready_count: `{manifest['retrieval_ready_count']}`",
            f"- mapping_ready_count: `{manifest['mapping_ready_count']}`",
            f"- retrieval_ready_image_ids: `{', '.join(manifest['retrieval_ready_image_ids']) if manifest['retrieval_ready_image_ids'] else 'none'}`",
            f"- mapping_ready_image_ids: `{', '.join(manifest['mapping_ready_image_ids']) if manifest['mapping_ready_image_ids'] else 'none'}`",
            "",
            "## Outputs",
            "",
            f"- retrieval ready rows: `{manifest['generated_outputs']['retrieval_ready_rows_jsonl']}`",
            f"- mapping ready rows: `{manifest['generated_outputs']['mapping_ready_rows_jsonl']}`",
            "",
            "## Next Action",
            "",
            f"- {manifest['next_action']}",
        ]
    )
    return "\n".join(lines) + "\n"
