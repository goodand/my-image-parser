from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST_PATH = (
    ROOT_DIR
    / "control"
    / "project_domain"
    / "resources"
    / "manifests"
    / "phase1_image4_component_decomposition_probe_at2026_03_30.json"
)


@dataclass(frozen=True)
class ComponentProposal:
    component_id: str
    component_kind: str
    bbox: list[int]
    source: str
    confidence: str
    rationale: str
    stats: dict[str, Any]


def _foreground_mask(rgba: np.ndarray, *, white_threshold: int = 245, alpha_threshold: int = 1) -> np.ndarray:
    alpha = rgba[:, :, 3]
    rgb = rgba[:, :, :3]
    return (alpha > alpha_threshold) & np.any(rgb < white_threshold, axis=2)


def _bbox_from_mask(mask: np.ndarray, *, x_offset: int = 0, y_offset: int = 0) -> list[int] | None:
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return [
        int(xs.min() + x_offset),
        int(ys.min() + y_offset),
        int(xs.max() + x_offset + 1),
        int(ys.max() + y_offset + 1),
    ]


def _axis_density(mask: np.ndarray, axis: int) -> np.ndarray:
    if axis == 0:
        return mask.mean(axis=0)
    if axis == 1:
        return mask.mean(axis=1)
    raise ValueError(f"Unsupported axis: {axis}")


def _find_dense_segments(
    values: np.ndarray,
    *,
    min_density: float,
    min_length: int,
    max_gap: int,
) -> list[tuple[int, int]]:
    dense = values >= min_density
    segments: list[tuple[int, int]] = []
    start: int | None = None
    gap_count = 0

    for index, is_dense in enumerate(dense.tolist()):
        if is_dense:
            if start is None:
                start = index
            gap_count = 0
            continue
        if start is None:
            continue
        gap_count += 1
        if gap_count > max_gap:
            end = index - gap_count + 1
            if end - start >= min_length:
                segments.append((start, end))
            start = None
            gap_count = 0

    if start is not None:
        end = len(values)
        if end - start >= min_length:
            segments.append((start, end))
    return segments


def _proposal(
    *,
    component_id: str,
    component_kind: str,
    bbox: list[int],
    source: str,
    confidence: str,
    rationale: str,
    stats: dict[str, Any],
) -> ComponentProposal:
    return ComponentProposal(
        component_id=component_id,
        component_kind=component_kind,
        bbox=[int(v) for v in bbox],
        source=source,
        confidence=confidence,
        rationale=rationale,
        stats=stats,
    )


def _union_bbox(boxes: list[list[int]]) -> list[int]:
    return [
        min(box[0] for box in boxes),
        min(box[1] for box in boxes),
        max(box[2] for box in boxes),
        max(box[3] for box in boxes),
    ]


def _candidate(name: str, boxes: list[list[int]], component_ids: list[str], rationale: str) -> dict[str, Any]:
    return {
        "candidate_name": name,
        "bbox": _union_bbox(boxes),
        "component_ids": component_ids,
        "rationale": rationale,
    }


def probe_component_decomposition(
    image_path: Path,
    *,
    title_top_ratio: float = 0.22,
    title_min_density: float = 0.015,
    content_band_min_density: float = 0.025,
    chart_column_min_density: float = 0.02,
) -> dict[str, Any]:
    with Image.open(image_path) as image:
        rgba = np.array(image.convert("RGBA"), dtype=np.uint8)

    height, width = rgba.shape[:2]
    foreground = _foreground_mask(rgba)
    foreground_bbox = _bbox_from_mask(foreground) or [0, 0, width, height]

    proposals: list[ComponentProposal] = [
        _proposal(
            component_id="full_dashboard",
            component_kind="full_dashboard",
            bbox=[0, 0, width, height],
            source="deterministic_full_image",
            confidence="high",
            rationale="Always preserve the complete dashboard as a candidate anchor.",
            stats={"width": width, "height": height},
        )
    ]

    row_density = _axis_density(foreground, axis=1)
    title_limit = max(1, int(height * title_top_ratio))
    title_segments = _find_dense_segments(
        row_density[:title_limit],
        min_density=title_min_density,
        min_length=max(6, height // 80),
        max_gap=6,
    )

    title_bbox: list[int] | None = None
    if title_segments:
        top_start, top_end = title_segments[0]
        title_mask = foreground[top_start:top_end, :]
        title_bbox = _bbox_from_mask(title_mask, y_offset=top_start)
        if title_bbox is not None:
            proposals.append(
                _proposal(
                    component_id="title_block",
                    component_kind="title_block",
                    bbox=title_bbox,
                    source="projection_profile",
                    confidence="medium",
                    rationale="Top-band dense foreground suggests a title-level summary block.",
                    stats={"row_segment": [top_start, top_end], "density_peak": float(row_density[top_start:top_end].max())},
                )
            )

    content_start = min(height, (title_bbox[3] + 8) if title_bbox else 0)
    content_mask = foreground[content_start:, :]
    content_row_density = _axis_density(content_mask, axis=1) if content_mask.size else np.array([], dtype=float)
    band_segments = _find_dense_segments(
        content_row_density,
        min_density=content_band_min_density,
        min_length=max(24, height // 25),
        max_gap=12,
    )

    chart_region_bbox: list[int] | None = None
    lower_region_bbox: list[int] | None = None
    chart_panel_ids: list[str] = []

    if band_segments:
        band_boxes: list[list[int]] = []
        for index, (start, end) in enumerate(band_segments, start=1):
            band_mask = content_mask[start:end, :]
            band_bbox = _bbox_from_mask(band_mask, y_offset=content_start + start)
            if band_bbox is None:
                continue
            band_boxes.append(band_bbox)
            proposals.append(
                _proposal(
                    component_id=f"content_band_{index}",
                    component_kind="content_band",
                    bbox=band_bbox,
                    source="projection_profile",
                    confidence="medium",
                    rationale="Dense horizontal foreground band in the post-title content area.",
                    stats={"row_segment": [content_start + start, content_start + end]},
                )
            )

        if band_boxes:
            upper_boxes = [box for box in band_boxes if (box[1] + box[3]) / 2 < height * 0.62]
            lower_boxes = [box for box in band_boxes if (box[1] + box[3]) / 2 >= height * 0.62]
            if upper_boxes:
                chart_region_bbox = _union_bbox(upper_boxes)
                proposals.append(
                    _proposal(
                        component_id="chart_region",
                        component_kind="chart_region",
                        bbox=chart_region_bbox,
                        source="regrouped_projection",
                        confidence="medium",
                        rationale="Upper dense bands merged into a likely chart-set region.",
                        stats={"band_count": len(upper_boxes)},
                    )
                )
            if lower_boxes:
                lower_region_bbox = _union_bbox(lower_boxes)
                lower_kind = "table_like_region" if lower_region_bbox[2] - lower_region_bbox[0] >= width * 0.22 else "lower_summary_region"
                proposals.append(
                    _proposal(
                        component_id=lower_kind,
                        component_kind=lower_kind,
                        bbox=lower_region_bbox,
                        source="regrouped_projection",
                        confidence="low" if lower_kind == "lower_summary_region" else "medium",
                        rationale="Lower dense bands merged into a likely embedded summary/table region.",
                        stats={"band_count": len(lower_boxes)},
                    )
                )

    if chart_region_bbox is not None:
        x1, y1, x2, y2 = chart_region_bbox
        chart_mask = foreground[y1:y2, x1:x2]
        col_density = _axis_density(chart_mask, axis=0)
        col_segments = _find_dense_segments(
            col_density,
            min_density=chart_column_min_density,
            min_length=max(40, width // 18),
            max_gap=16,
        )
        for index, (start, end) in enumerate(col_segments, start=1):
            panel_mask = chart_mask[:, start:end]
            panel_bbox = _bbox_from_mask(panel_mask, x_offset=x1 + start, y_offset=y1)
            if panel_bbox is None:
                continue
            proposal_id = f"chart_panel_{index}"
            chart_panel_ids.append(proposal_id)
            proposals.append(
                _proposal(
                    component_id=proposal_id,
                    component_kind="chart_panel",
                    bbox=panel_bbox,
                    source="projection_profile",
                    confidence="low" if len(col_segments) < 2 else "medium",
                    rationale="Vertical density slice within the upper chart region.",
                    stats={"column_segment": [x1 + start, x1 + end], "panel_index": index},
                )
            )

    proposal_by_id = {proposal.component_id: proposal for proposal in proposals}
    regrouped_candidates: list[dict[str, Any]] = []
    regrouped_candidates.append(
        _candidate(
            "full_dashboard",
            [[0, 0, width, height]],
            ["full_dashboard"],
            "Keep the full dashboard as the no-loss baseline candidate.",
        )
    )
    if title_bbox and chart_region_bbox:
        regrouped_candidates.append(
            _candidate(
                "title_plus_chart_set",
                [title_bbox, chart_region_bbox],
                ["title_block", "chart_region"],
                "Preserve title context together with the upper chart set.",
            )
        )
    if chart_region_bbox:
        regrouped_candidates.append(
            _candidate(
                "chart_set",
                [chart_region_bbox],
                ["chart_region"],
                "Preserve the chart-heavy analytical surface without the full dashboard.",
            )
        )
    if title_bbox and lower_region_bbox:
        regrouped_candidates.append(
            _candidate(
                "title_plus_table",
                [title_bbox, lower_region_bbox],
                ["title_block", proposal_by_id[[p for p in proposal_by_id if p in {'table_like_region', 'lower_summary_region'}][0]].component_id]
                if any(p in proposal_by_id for p in {"table_like_region", "lower_summary_region"})
                else ["title_block"],
                "Preserve title context together with the lower summary/table region.",
            )
        )
    if lower_region_bbox:
        lower_id = "table_like_region" if "table_like_region" in proposal_by_id else "lower_summary_region"
        regrouped_candidates.append(
            _candidate(
                "table_only" if lower_id == "table_like_region" else "lower_summary_only",
                [lower_region_bbox],
                [lower_id],
                "Isolate the lower dense region as a possible metrics table or summary crop.",
            )
        )

    summary = {
        "found_title_block": title_bbox is not None,
        "chart_panel_count": len(chart_panel_ids),
        "found_chart_region": chart_region_bbox is not None,
        "found_lower_region": lower_region_bbox is not None,
        "found_table_like_region": "table_like_region" in proposal_by_id,
        "foreground_bbox": foreground_bbox,
    }
    interpretation = {
        "image_kind_guess": "compound_dashboard_like" if summary["found_chart_region"] and summary["found_lower_region"] else "unknown",
        "decomposition_ready_for_regrouping": bool(summary["found_chart_region"] or summary["found_lower_region"]),
        "selection_recommendation": (
            "decomposition_stage_candidate_available"
            if summary["found_title_block"] and summary["found_chart_region"] and summary["found_lower_region"]
            else "needs_stronger_proposal_generation"
        ),
    }

    return {
        "experiment": "component_decomposition_projection_probe",
        "status": "completed",
        "source_image_path": str(image_path.resolve()),
        "image_width": width,
        "image_height": height,
        "component_proposals": [asdict(proposal) for proposal in proposals],
        "regrouped_candidates": regrouped_candidates,
        "summary": summary,
        "interpretation": interpretation,
    }


def render_probe_report(manifest: dict[str, Any]) -> str:
    summary = manifest["summary"]
    interpretation = manifest["interpretation"]
    lines = [
        "# Phase1 Image4 Component Decomposition Probe",
        "",
        "## Input",
        "",
        f"- source_image_path: `{manifest['source_image_path']}`",
        f"- image_size: `{manifest['image_width']}x{manifest['image_height']}`",
        "",
        "## Summary",
        "",
        f"- found_title_block: `{summary['found_title_block']}`",
        f"- found_chart_region: `{summary['found_chart_region']}`",
        f"- chart_panel_count: `{summary['chart_panel_count']}`",
        f"- found_lower_region: `{summary['found_lower_region']}`",
        f"- found_table_like_region: `{summary['found_table_like_region']}`",
        f"- image_kind_guess: `{interpretation['image_kind_guess']}`",
        f"- decomposition_ready_for_regrouping: `{interpretation['decomposition_ready_for_regrouping']}`",
        f"- selection_recommendation: `{interpretation['selection_recommendation']}`",
        "",
        "## Candidate Surfaces",
        "",
    ]
    for candidate in manifest["regrouped_candidates"]:
        lines.append(f"### {candidate['candidate_name']}")
        lines.append("")
        lines.append(f"- bbox: `{candidate['bbox']}`")
        lines.append(f"- component_ids: `{candidate['component_ids']}`")
        lines.append(f"- rationale: {candidate['rationale']}")
        lines.append("")
    lines.extend(
        [
            "## Interpretation",
            "",
            "- This probe does not decide re-entry by itself.",
            "- It tests whether deterministic proposal generation can expose title/chart/lower-summary regions before a stronger decomposition slice exists.",
            "- If the chart region and lower region both appear, the next bounded step should be typed regrouping plus rule-based scoring rather than more ad-hoc recrop tweaks.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


__all__ = [
    "DEFAULT_MANIFEST_PATH",
    "probe_component_decomposition",
    "render_probe_report",
    "write_json",
]
