from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def load_normalized_table(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def _cell_index(table: dict[str, Any]) -> dict[tuple[int, int], dict[str, Any]]:
    indexed: dict[tuple[int, int], dict[str, Any]] = {}
    for row in table.get("rows", []):
        row_index = int(row["row_index"])
        for cell in row.get("cells", []):
            indexed[(row_index, int(cell["col_index"]))] = cell
    return indexed


def _row_count(table: dict[str, Any]) -> int:
    return len(table.get("rows", []))


def _column_count(table: dict[str, Any]) -> int:
    return max((len(row.get("cells", [])) for row in table.get("rows", [])), default=0)


def _cell_count(table: dict[str, Any]) -> int:
    return sum(len(row.get("cells", [])) for row in table.get("rows", []))


def _normalize_basic(text: str) -> str:
    return re.sub(r"\s+", "", text.strip())


def _normalize_decimal_string(text: str) -> str:
    compact = _normalize_basic(text)
    if re.fullmatch(r"[+-]?\.\d+", compact):
        return f"{compact[0]}0{compact[1:]}" if compact.startswith(("+", "-")) else f"0{compact}"
    if re.fullmatch(r"[+-]?\d+\.\d+", compact):
        return compact
    if re.fullmatch(r"[+-]?\d+", compact):
        return compact
    if re.fullmatch(r"[+-]?\d+\d+", compact):
        return compact
    if re.fullmatch(r"[+-]?\d+\s+\d+", text.strip()):
        head, tail = text.strip().split()
        return f"{head}.{tail}"
    return compact


def classify_text_difference(apple_text: str, paddle_text: str, row_index: int) -> dict[str, str]:
    apple = apple_text.strip()
    paddle = paddle_text.strip()
    if apple == paddle:
        return {"classification": "identical", "recommended_text_source": "either"}
    if apple and not paddle:
        return {"classification": "missing_in_paddle", "recommended_text_source": "apple"}
    if paddle and not apple:
        return {"classification": "missing_in_apple", "recommended_text_source": "paddle"}

    apple_basic = _normalize_basic(apple)
    paddle_basic = _normalize_basic(paddle)
    if apple_basic == paddle_basic:
        return {"classification": "spacing_drift", "recommended_text_source": "apple"}

    apple_decimal = _normalize_decimal_string(apple)
    paddle_decimal = _normalize_decimal_string(paddle)
    if apple_decimal == paddle_decimal:
        return {"classification": "numeric_format_drift", "recommended_text_source": "apple"}

    apple_digits = re.sub(r"\D", "", apple).lstrip("0") or "0"
    paddle_digits = re.sub(r"\D", "", paddle).lstrip("0") or "0"
    if apple_digits and apple_digits == paddle_digits and apple != paddle:
        preferred = "apple" if "." in apple or apple.startswith("0.") else "paddle" if "." in paddle or paddle.startswith("0.") else "review"
        return {"classification": "decimal_point_drift", "recommended_text_source": preferred}

    if row_index == 0 and bool(re.search(r"[A-Za-z]", apple)) != bool(re.search(r"[A-Za-z]", paddle)):
        return {"classification": "header_character_substitution", "recommended_text_source": "review"}

    return {"classification": "lexical_conflict", "recommended_text_source": "review"}


def compare_normalized_tables(apple_table: dict[str, Any], paddle_table: dict[str, Any]) -> dict[str, Any]:
    apple_cells = _cell_index(apple_table)
    paddle_cells = _cell_index(paddle_table)
    coords = sorted(set(apple_cells) | set(paddle_cells))

    diffs: list[dict[str, Any]] = []
    repairable = 0
    review_required = 0
    identical = 0

    for row_index, col_index in coords:
        apple_cell = apple_cells.get((row_index, col_index), {})
        paddle_cell = paddle_cells.get((row_index, col_index), {})
        apple_text = str(apple_cell.get("text", ""))
        paddle_text = str(paddle_cell.get("text", ""))
        decision = classify_text_difference(apple_text, paddle_text, row_index)
        if decision["classification"] == "identical":
            identical += 1
            continue
        if decision["recommended_text_source"] == "review":
            review_required += 1
        else:
            repairable += 1
        diffs.append(
            {
                "row_index": row_index,
                "col_index": col_index,
                "cell_id": apple_cell.get("cell_id") or paddle_cell.get("cell_id"),
                "apple_text": apple_text,
                "paddle_text": paddle_text,
                "classification": decision["classification"],
                "recommended_text_source": decision["recommended_text_source"],
            }
        )

    structure_alignment = {
        "same_document_id": apple_table.get("document_id") == paddle_table.get("document_id"),
        "same_page": apple_table.get("page") == paddle_table.get("page"),
        "same_table_id": apple_table.get("table_id") == paddle_table.get("table_id"),
        "same_row_count": _row_count(apple_table) == _row_count(paddle_table),
        "same_column_count": _column_count(apple_table) == _column_count(paddle_table),
        "same_cell_count": _cell_count(apple_table) == _cell_count(paddle_table),
    }
    structure_alignment["compatible_for_shared_wrapper"] = all(structure_alignment.values())

    merge_policy = {
        "structure_source": "apple" if structure_alignment["compatible_for_shared_wrapper"] else "review",
        "text_source_policy": [
            "prefer non-empty text when the other parser is empty",
            "prefer cleaner normalized numeric formatting when values match after normalization",
            "prefer the decimal-bearing candidate for decimal-point drift, but keep the cell reviewable",
            "send lexical or header substitution conflicts to review instead of silently merging",
        ],
        "review_gate": "numbers and conflicting header labels remain review targets even when Apple structure is accepted",
    }

    return {
        "document_id": apple_table.get("document_id"),
        "page": apple_table.get("page"),
        "table_id": apple_table.get("table_id"),
        "apple_backend": apple_table.get("parser_backend"),
        "paddle_backend": paddle_table.get("parser_backend"),
        "structure_alignment": structure_alignment,
        "difference_count": len(diffs),
        "identical_cell_count": identical,
        "repairable_difference_count": repairable,
        "review_required_count": review_required,
        "differences": diffs,
        "merge_policy": merge_policy,
    }
