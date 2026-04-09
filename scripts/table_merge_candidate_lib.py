from __future__ import annotations

from dataclasses import dataclass
import json
import re
from pathlib import Path
from typing import Any, Protocol

from table_parser_comparison_lib import load_normalized_table


def _cell_index(table: dict[str, Any]) -> dict[tuple[int, int], dict[str, Any]]:
    indexed: dict[tuple[int, int], dict[str, Any]] = {}
    for row in table.get("rows", []):
        row_index = int(row["row_index"])
        for cell in row.get("cells", []):
            indexed[(row_index, int(cell["col_index"]))] = cell
    return indexed


def _difference_index(comparison: dict[str, Any]) -> dict[tuple[int, int], dict[str, Any]]:
    indexed: dict[tuple[int, int], dict[str, Any]] = {}
    for item in comparison.get("differences", []):
        indexed[(int(item["row_index"]), int(item["col_index"]))] = item
    return indexed


def _is_numeric_like(text: str) -> bool:
    compact = text.strip().replace(" ", "")
    return bool(re.fullmatch(r"[+-]?(?:\d+(?:\.\d+)?|\.\d+)", compact))


@dataclass(frozen=True)
class MergeCellContext:
    row_index: int
    col_index: int
    apple_cell: dict[str, Any]
    paddle_cell: dict[str, Any]
    difference: dict[str, Any] | None


class MergeHook(Protocol):
    def apply(self, candidate: dict[str, Any], context: MergeCellContext) -> None: ...


class BaselineTextSelectionHook:
    def apply(self, candidate: dict[str, Any], context: MergeCellContext) -> None:
        difference = context.difference
        apple_text = str(context.apple_cell.get("text", ""))
        paddle_text = str(context.paddle_cell.get("text", ""))
        classification = difference["classification"] if difference else "identical"
        recommended_source = difference["recommended_text_source"] if difference else "either"

        if recommended_source == "apple":
            recommended_text = apple_text
            final_source = "apple"
        elif recommended_source == "paddle":
            recommended_text = paddle_text
            final_source = "paddle"
        elif recommended_source == "either":
            recommended_text = apple_text or paddle_text
            final_source = "apple" if apple_text else "paddle"
        else:
            recommended_text = apple_text or paddle_text
            final_source = "apple_provisional" if apple_text else "paddle_provisional"

        candidate["difference_classification"] = classification
        candidate["recommended_text"] = recommended_text
        candidate["recommended_text_source"] = final_source


class BaselineReviewGateHook:
    def apply(self, candidate: dict[str, Any], context: MergeCellContext) -> None:
        classification = candidate["difference_classification"]
        recommended_text = str(candidate["recommended_text"])
        numeric_sensitive = _is_numeric_like(recommended_text)

        if classification in {"header_character_substitution", "lexical_conflict"}:
            candidate["review_status"] = "pending_review"
            candidate["review_priority"] = "high"
            candidate["review_reason"] = classification
            return

        if numeric_sensitive:
            candidate["review_status"] = "pending_review"
            candidate["review_priority"] = "high"
            candidate["review_reason"] = "numeric_cell_review_gate"
            return

        candidate["review_status"] = "auto_accept_candidate"
        candidate["review_priority"] = "normal"
        candidate["review_reason"] = "stable_non_numeric_candidate"


class TableMergeCandidateBuilder:
    def __init__(
        self,
        *,
        hooks: list[MergeHook] | None = None,
        experiment: str = "table_merge_candidate_builder",
        policy_name: str = "baseline_v1",
    ) -> None:
        self.hooks = hooks or [BaselineTextSelectionHook(), BaselineReviewGateHook()]
        self.experiment = experiment
        self.policy_name = policy_name

    def build(
        self,
        *,
        apple_table: dict[str, Any],
        paddle_table: dict[str, Any],
        comparison: dict[str, Any],
        source_manifests: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        structure_alignment = comparison.get("structure_alignment", {})
        if not structure_alignment.get("compatible_for_shared_wrapper"):
            raise ValueError("Apple and Paddle normalized tables are not structure-compatible enough for a merged candidate.")

        paddle_cells = _cell_index(paddle_table)
        diff_index = _difference_index(comparison)
        rows: list[dict[str, Any]] = []
        review_targets: list[str] = []

        for row in apple_table.get("rows", []):
            row_index = int(row["row_index"])
            merged_cells: list[dict[str, Any]] = []
            for apple_cell in row.get("cells", []):
                col_index = int(apple_cell["col_index"])
                paddle_cell = paddle_cells.get((row_index, col_index), {})
                difference = diff_index.get((row_index, col_index))
                candidate = {
                    "cell_id": apple_cell["cell_id"],
                    "row_index": row_index,
                    "col_index": col_index,
                    "row_span": apple_cell["row_span"],
                    "col_span": apple_cell["col_span"],
                    "bbox": apple_cell["bbox"],
                    "structure_source": comparison["merge_policy"]["structure_source"],
                    "apple_text": str(apple_cell.get("text", "")),
                    "paddle_text": str(paddle_cell.get("text", "")),
                    "apple_confidence": apple_cell.get("confidence"),
                    "paddle_confidence": paddle_cell.get("confidence"),
                }
                context = MergeCellContext(
                    row_index=row_index,
                    col_index=col_index,
                    apple_cell=apple_cell,
                    paddle_cell=paddle_cell,
                    difference=difference,
                )
                for hook in self.hooks:
                    hook.apply(candidate, context)
                if candidate["review_status"] == "pending_review":
                    review_targets.append(candidate["cell_id"])
                merged_cells.append(candidate)
            rows.append({"row_index": row_index, "cells": merged_cells})

        total_cells = sum(len(row["cells"]) for row in rows)
        pending_review_count = len(review_targets)
        auto_accept_count = total_cells - pending_review_count

        return {
            "experiment": self.experiment,
            "status": "completed",
            "policy_name": self.policy_name,
            "hook_chain": [hook.__class__.__name__ for hook in self.hooks],
            "document_id": apple_table["document_id"],
            "page": apple_table["page"],
            "table_id": apple_table["table_id"],
            "structure_source": comparison["merge_policy"]["structure_source"],
            "apple_backend": comparison["apple_backend"],
            "paddle_backend": comparison["paddle_backend"],
            "source_manifests": source_manifests or {},
            "comparison_difference_count": comparison["difference_count"],
            "merge_summary": {
                "total_cells": total_cells,
                "auto_accept_candidate_count": auto_accept_count,
                "pending_review_count": pending_review_count,
                "review_target_cell_ids": review_targets,
            },
            "rows": rows,
        }


def build_merged_candidate_from_paths(
    *,
    apple_normalized_json: str | Path,
    paddle_normalized_json: str | Path,
    comparison_json: str | Path,
    source_manifests: dict[str, str] | None = None,
) -> dict[str, Any]:
    builder = TableMergeCandidateBuilder()
    apple_table = load_normalized_table(apple_normalized_json)
    paddle_table = load_normalized_table(paddle_normalized_json)
    comparison = json.loads(Path(comparison_json).read_text())
    return builder.build(
        apple_table=apple_table,
        paddle_table=paddle_table,
        comparison=comparison,
        source_manifests=source_manifests,
    )


def build_single_source_candidate(
    *,
    normalized_table: dict[str, Any],
    parser_backend: str,
    structure_source: str = "apple_single_source",
    source_manifests: dict[str, str] | None = None,
    experiment: str = "table_merge_candidate_builder",
    policy_name: str = "single_source_fallback_v1",
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    review_targets: list[str] = []
    review_hook = BaselineReviewGateHook()

    for row in normalized_table.get("rows", []):
        row_index = int(row["row_index"])
        merged_cells: list[dict[str, Any]] = []
        for source_cell in row.get("cells", []):
            text = str(source_cell.get("text", ""))
            candidate = {
                "cell_id": source_cell["cell_id"],
                "row_index": row_index,
                "col_index": int(source_cell["col_index"]),
                "row_span": source_cell["row_span"],
                "col_span": source_cell["col_span"],
                "bbox": source_cell["bbox"],
                "structure_source": structure_source,
                "apple_text": text,
                "paddle_text": text,
                "apple_confidence": source_cell.get("confidence"),
                "paddle_confidence": source_cell.get("confidence"),
                "difference_classification": "single_source_fallback",
                "recommended_text": text,
                "recommended_text_source": structure_source,
            }
            review_hook.apply(
                candidate,
                MergeCellContext(
                    row_index=row_index,
                    col_index=int(source_cell["col_index"]),
                    apple_cell=source_cell,
                    paddle_cell=source_cell,
                    difference=None,
                ),
            )
            if candidate["review_status"] == "pending_review":
                review_targets.append(candidate["cell_id"])
            merged_cells.append(candidate)
        rows.append({"row_index": row_index, "cells": merged_cells})

    total_cells = sum(len(row["cells"]) for row in rows)
    pending_review_count = len(review_targets)
    auto_accept_count = total_cells - pending_review_count

    return {
        "experiment": experiment,
        "status": "completed",
        "policy_name": policy_name,
        "hook_chain": ["SingleSourceFallback", "BaselineReviewGateHook"],
        "document_id": normalized_table["document_id"],
        "page": normalized_table["page"],
        "table_id": normalized_table["table_id"],
        "structure_source": structure_source,
        "apple_backend": parser_backend,
        "paddle_backend": parser_backend,
        "source_manifests": source_manifests or {},
        "comparison_difference_count": 0,
        "merge_summary": {
            "total_cells": total_cells,
            "auto_accept_candidate_count": auto_accept_count,
            "pending_review_count": pending_review_count,
            "review_target_cell_ids": review_targets,
        },
        "rows": rows,
    }


def build_single_source_candidate_from_path(
    *,
    normalized_json: str | Path,
    parser_backend: str,
    structure_source: str = "apple_single_source",
    source_manifests: dict[str, str] | None = None,
) -> dict[str, Any]:
    table = load_normalized_table(normalized_json)
    return build_single_source_candidate(
        normalized_table=table,
        parser_backend=parser_backend,
        structure_source=structure_source,
        source_manifests=source_manifests,
    )
