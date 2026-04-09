#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from itertools import groupby
from pathlib import Path
from typing import Any


class _FirstTableHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._table_depth = 0
        self._capture = False
        self._current_row: list[dict[str, Any]] | None = None
        self._current_cell: dict[str, Any] | None = None
        self._cell_text_parts: list[str] = []
        self.rows: list[list[dict[str, Any]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "table":
            self._table_depth += 1
            if self._table_depth == 1:
                self._capture = True
            return

        if not self._capture:
            return

        if tag == "tr":
            self._current_row = []
            return

        if tag in {"td", "th"} and self._current_row is not None:
            attrs_map = {key: value for key, value in attrs}
            self._current_cell = {
                "tag": tag,
                "row_span": int(attrs_map.get("rowspan") or "1"),
                "col_span": int(attrs_map.get("colspan") or "1"),
            }
            self._cell_text_parts = []

    def handle_data(self, data: str) -> None:
        if self._capture and self._current_cell is not None:
            self._cell_text_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "table" and self._capture:
            self._table_depth -= 1
            if self._table_depth == 0:
                self._capture = False
            return

        if not self._capture:
            return

        if tag in {"td", "th"} and self._current_cell is not None and self._current_row is not None:
            text = re.sub(r"\s+", " ", "".join(self._cell_text_parts)).strip()
            self._current_row.append(
                {
                    "text": text,
                    "row_span": self._current_cell["row_span"],
                    "col_span": self._current_cell["col_span"],
                }
            )
            self._current_cell = None
            self._cell_text_parts = []
            return

        if tag == "tr" and self._current_row is not None:
            if self._current_row:
                self.rows.append(self._current_row)
            self._current_row = None


@dataclass(frozen=True)
class ParserSidecarPromotionResult:
    raw_sidecar_json: Path
    image_path: Path
    manifest_path: Path | None
    normalized_record: dict[str, Any] | None

    @property
    def normalized_status(self) -> str:
        return "completed" if self.normalized_record else "no_table_found"


def _parse_float_list(value: Any) -> list[float]:
    if isinstance(value, list):
        return [float(item) for item in value]
    if isinstance(value, str):
        return [float(item) for item in re.findall(r"-?\d+(?:\.\d+)?", value)]
    return []


def _parse_bbox_list(value: Any) -> list[int]:
    if isinstance(value, list):
        return [int(round(float(item))) for item in value]
    if isinstance(value, str):
        return [int(round(float(item))) for item in re.findall(r"-?\d+(?:\.\d+)?", value)]
    return [0, 0, 0, 0]


def load_raw_sidecar(raw_sidecar_json: Path) -> dict[str, Any]:
    return json.loads(raw_sidecar_json.read_text(encoding="utf-8"))


def extract_text_items_from_raw_sidecar(raw_payload: dict[str, Any]) -> list[str]:
    text_items: list[str] = []
    for item in raw_payload.get("content", []):
        if isinstance(item, dict) and item.get("type") == "text" and item.get("text"):
            text_items.append(str(item["text"]))
    return text_items


def infer_image_path_from_raw_sidecar(raw_payload: dict[str, Any]) -> Path:
    candidate_keys = ("image_path", "input_path", "source_image_path")
    image_path = next(
        (
            raw_payload.get(key)
            for key in candidate_keys
            if isinstance(raw_payload.get(key), str) and raw_payload.get(key)
        ),
        None,
    )
    if not isinstance(image_path, str) or not image_path:
        raise ValueError("Raw parser sidecar does not contain a usable image_path.")
    return Path(image_path).resolve()


def resolve_manifest_for_image(image_path: Path) -> Path | None:
    try:
        media_dir = image_path.parent
        job_dir = media_dir.parent
        candidate = job_dir / "manifest.json"
        return candidate if candidate.is_file() else None
    except Exception:
        return None


def load_slide_usages(manifest_path: Path | None, image_name: str) -> list[dict[str, Any]]:
    if manifest_path is None:
        return []
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    for item in data.get("exported_images", []):
        if item.get("file") == image_name or str(item.get("output_path", "")).endswith(image_name):
            return item.get("slide_usages", [])
    return []


def extract_first_table_html(text_items: list[str]) -> str | None:
    for text in text_items:
        match = re.search(r"<table\b.*?</table>", text, flags=re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(0)
    return None


def extract_detailed_table_payload(text_items: list[str]) -> dict[str, Any] | None:
    for text in text_items:
        stripped = text.strip()
        if not stripped.startswith("{"):
            continue
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        table_res_list = payload.get("table_res_list")
        if isinstance(table_res_list, list) and table_res_list:
            return table_res_list[0]
    return None


def _extract_apple_helper_table(raw_payload: dict[str, Any]) -> dict[str, Any] | None:
    documents = raw_payload.get("documents")
    if not isinstance(documents, list):
        return None

    for document in documents:
        if not isinstance(document, dict):
            continue
        tables = document.get("tables")
        if not isinstance(tables, list):
            continue
        for table in tables:
            if isinstance(table, dict) and isinstance(table.get("cells"), list) and table.get("cells"):
                return table
    return None


def _bbox_from_apple_cell(cell: dict[str, Any]) -> list[float]:
    bounding_region = cell.get("bounding_region")
    if not isinstance(bounding_region, dict):
        return [0.0, 0.0, 0.0, 0.0]
    bounding_box = bounding_region.get("bounding_box")
    if not isinstance(bounding_box, dict):
        return [0.0, 0.0, 0.0, 0.0]
    try:
        return [
            round(float(bounding_box.get("x", 0.0)), 6),
            round(float(bounding_box.get("y", 0.0)), 6),
            round(float(bounding_box.get("width", 0.0)), 6),
            round(float(bounding_box.get("height", 0.0)), 6),
        ]
    except (TypeError, ValueError):
        return [0.0, 0.0, 0.0, 0.0]


def _confidence_from_apple_cell(cell: dict[str, Any]) -> float:
    line_candidates = cell.get("line_candidates")
    if not isinstance(line_candidates, list) or not line_candidates:
        return 0.0
    confidences: list[float] = []
    for line in line_candidates:
        if not isinstance(line, dict):
            continue
        confidence = line.get("confidence")
        if isinstance(confidence, (int, float)):
            confidences.append(float(confidence))
    if not confidences:
        return 0.0
    return round(max(confidences), 6)


def normalize_first_table_from_apple_helper(
    *,
    image_path: Path,
    raw_payload: dict[str, Any],
    slide_usages: list[dict[str, Any]],
    table_id: str = "t1",
    parser_backend: str = "apple_vision_recognize_documents_request",
) -> dict[str, Any] | None:
    table_payload = _extract_apple_helper_table(raw_payload)
    if table_payload is None:
        return None

    raw_cells = table_payload.get("cells")
    if not isinstance(raw_cells, list) or not raw_cells:
        return None

    normalized_cells: list[dict[str, Any]] = []
    for cell in raw_cells:
        if not isinstance(cell, dict):
            continue
        row_range = cell.get("row_range")
        column_range = cell.get("column_range")
        if not (
            isinstance(row_range, list)
            and len(row_range) == 2
            and isinstance(column_range, list)
            and len(column_range) == 2
        ):
            continue

        row_start = int(row_range[0])
        row_end = int(row_range[1])
        col_start = int(column_range[0])
        col_end = int(column_range[1])
        normalized_cells.append(
            {
                "row_index": row_start,
                "cell": {
                    "cell_id": f"{table_id}_r{row_start}_c{col_start}",
                    "col_index": col_start,
                    "text": str(cell.get("transcript") or ""),
                    "row_span": max(1, row_end - row_start + 1),
                    "col_span": max(1, col_end - col_start + 1),
                    "bbox": _bbox_from_apple_cell(cell),
                    "confidence": _confidence_from_apple_cell(cell),
                },
            }
        )

    if not normalized_cells:
        return None

    normalized_cells.sort(key=lambda item: (item["row_index"], item["cell"]["col_index"]))
    normalized_rows = [
        {
            "row_index": row_index,
            "cells": [entry["cell"] for entry in row_entries],
        }
        for row_index, row_entries in (
            (key, list(group))
            for key, group in groupby(normalized_cells, key=lambda item: item["row_index"])
        )
    ]

    slide_number = slide_usages[0]["slide"] if slide_usages else None
    document_id = image_path.parent.parent.name

    return {
        "document_id": document_id,
        "page": slide_number,
        "table_id": table_id,
        "source_image_path": str(image_path),
        "source_slide_usages": slide_usages,
        "parser_backend": parser_backend,
        "normalization_mode": "documents[0].tables[0].cells",
        "rows": normalized_rows,
    }


def normalize_first_table_from_text_items(
    *,
    image_path: Path,
    text_items: list[str],
    slide_usages: list[dict[str, Any]],
    table_id: str = "t1",
    parser_backend: str = "paddleocr-mcp/pp_structurev3",
) -> dict[str, Any] | None:
    detailed_table = extract_detailed_table_payload(text_items)
    table_html = (
        detailed_table.get("pred_html")
        if isinstance(detailed_table, dict) and detailed_table.get("pred_html")
        else extract_first_table_html(text_items)
    )
    if not table_html:
        return None

    parser = _FirstTableHTMLParser()
    parser.feed(table_html)
    if not parser.rows:
        return None

    cell_bboxes = []
    cell_confidences = []
    if isinstance(detailed_table, dict):
        cell_bboxes = [_parse_bbox_list(item) for item in detailed_table.get("cell_box_list", [])]
        table_ocr_pred = detailed_table.get("table_ocr_pred", {})
        cell_confidences = _parse_float_list(table_ocr_pred.get("rec_scores", []))

    active_rowspans: dict[int, int] = {}
    normalized_rows: list[dict[str, Any]] = []
    linear_cell_index = 0

    for row_index, row in enumerate(parser.rows):
        cells: list[dict[str, Any]] = []
        col_index = 0
        while active_rowspans.get(col_index, 0) > 0:
            active_rowspans[col_index] -= 1
            if active_rowspans[col_index] == 0:
                active_rowspans.pop(col_index, None)
            col_index += 1

        for cell in row:
            while active_rowspans.get(col_index, 0) > 0:
                active_rowspans[col_index] -= 1
                if active_rowspans[col_index] == 0:
                    active_rowspans.pop(col_index, None)
                col_index += 1

            row_span = int(cell["row_span"])
            col_span = int(cell["col_span"])
            cells.append(
                {
                    "cell_id": f"{table_id}_r{row_index}_c{col_index}",
                    "col_index": col_index,
                    "text": cell["text"],
                    "row_span": row_span,
                    "col_span": col_span,
                    "bbox": (
                        cell_bboxes[linear_cell_index]
                        if linear_cell_index < len(cell_bboxes)
                        else [0, 0, 0, 0]
                    ),
                    "confidence": (
                        round(cell_confidences[linear_cell_index], 6)
                        if linear_cell_index < len(cell_confidences)
                        else 0.0
                    ),
                }
            )
            if row_span > 1:
                for span_offset in range(col_span):
                    active_rowspans[col_index + span_offset] = row_span - 1
            col_index += col_span
            linear_cell_index += 1

        normalized_rows.append({"row_index": row_index, "cells": cells})

        for occupied_col in list(active_rowspans):
            if active_rowspans[occupied_col] <= 0:
                active_rowspans.pop(occupied_col, None)

    slide_number = slide_usages[0]["slide"] if slide_usages else None
    document_id = image_path.parent.parent.name

    return {
        "document_id": document_id,
        "page": slide_number,
        "table_id": table_id,
        "source_image_path": str(image_path),
        "source_slide_usages": slide_usages,
        "parser_backend": parser_backend,
        "normalization_mode": (
            "table_res_list[0].pred_html"
            if isinstance(detailed_table, dict) and detailed_table.get("pred_html")
            else "first_html_table_from_markdown"
        ),
        "rows": normalized_rows,
    }


def promote_raw_sidecar_to_canonical(
    *,
    raw_sidecar_json: Path,
    image_path: Path | None = None,
    table_id: str = "t1",
    parser_backend: str = "paddleocr-mcp/pp_structurev3",
) -> ParserSidecarPromotionResult:
    payload = load_raw_sidecar(raw_sidecar_json)
    resolved_image_path = image_path.resolve() if image_path is not None else infer_image_path_from_raw_sidecar(payload)
    manifest_path = resolve_manifest_for_image(resolved_image_path)
    slide_usages = load_slide_usages(manifest_path, resolved_image_path.name)
    effective_parser_backend = (
        payload.get("backend")
        if parser_backend == "paddleocr-mcp/pp_structurev3" and isinstance(payload.get("backend"), str)
        else parser_backend
    )
    normalized_record = normalize_first_table_from_text_items(
        image_path=resolved_image_path,
        text_items=extract_text_items_from_raw_sidecar(payload),
        slide_usages=slide_usages,
        table_id=table_id,
        parser_backend=effective_parser_backend,
    )
    if normalized_record is None:
        normalized_record = normalize_first_table_from_apple_helper(
            image_path=resolved_image_path,
            raw_payload=payload,
            slide_usages=slide_usages,
            table_id=table_id,
            parser_backend=effective_parser_backend,
        )
    return ParserSidecarPromotionResult(
        raw_sidecar_json=raw_sidecar_json.resolve(),
        image_path=resolved_image_path,
        manifest_path=manifest_path.resolve() if manifest_path else None,
        normalized_record=normalized_record,
    )
