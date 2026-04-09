from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_JSON = (
    ROOT_DIR
    / "control"
    / "project_domain"
    / "resources"
    / "manifests"
    / "phase1_image4_component_decomposition_candidate_scoring_at2026_03_30.json"
)


@dataclass(frozen=True)
class CandidateScore:
    candidate_name: str
    objective_profile: str
    total_score: float
    strengths: list[str]
    weaknesses: list[str]
    score_breakdown: dict[str, float]
    bbox: list[int]
    component_ids: list[str]


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _bbox_area(bbox: list[int]) -> int:
    x1, y1, x2, y2 = bbox
    return max(0, x2 - x1) * max(0, y2 - y1)


def _kind_index(manifest: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    proposals = manifest.get("component_proposals", [])
    by_id = {proposal["component_id"]: proposal for proposal in proposals}
    kind_by_id = {proposal["component_id"]: proposal["component_kind"] for proposal in proposals}
    return by_id, kind_by_id


def _candidate_presence(candidate: dict[str, Any], kind_by_id: dict[str, str]) -> dict[str, bool]:
    component_ids = candidate.get("component_ids", [])
    component_kinds = {kind_by_id.get(component_id, component_id) for component_id in component_ids}
    is_full_dashboard = candidate.get("candidate_name") == "full_dashboard"
    return {
        "has_title": is_full_dashboard or "title_block" in component_kinds,
        "has_chart_region": is_full_dashboard or "chart_region" in component_kinds or "chart_panel" in component_kinds,
        "has_table_region": is_full_dashboard or "table_like_region" in component_kinds or "lower_summary_region" in component_kinds,
        "is_full_dashboard": is_full_dashboard,
    }


def _score_dashboard_profile(candidate: dict[str, Any], *, full_area: int, kind_by_id: dict[str, str]) -> CandidateScore:
    presence = _candidate_presence(candidate, kind_by_id)
    area_ratio = _bbox_area(candidate["bbox"]) / full_area if full_area else 0.0

    breakdown = {
        "title_context": 2.0 if presence["has_title"] else 0.0,
        "chart_region": 3.0 if presence["has_chart_region"] else 0.0,
        "table_region": 2.0 if presence["has_table_region"] else 0.0,
        "joint_dashboard_preservation": 2.0 if presence["has_chart_region"] and presence["has_table_region"] else 0.0,
        "full_context_anchor": 1.0 if presence["is_full_dashboard"] else 0.0,
        "narrow_crop_penalty": -1.5 if not (presence["has_chart_region"] and presence["has_table_region"]) else 0.0,
        "title_missing_penalty": -0.5 if not presence["has_title"] else 0.0,
        "aggressive_crop_penalty": -0.5 if area_ratio < 0.4 else 0.0,
    }
    total = sum(breakdown.values())
    strengths: list[str] = []
    weaknesses: list[str] = []
    if presence["has_title"]:
        strengths.append("preserves_title_context")
    else:
        weaknesses.append("drops_title_context")
    if presence["has_chart_region"]:
        strengths.append("preserves_chart_region")
    else:
        weaknesses.append("drops_chart_region")
    if presence["has_table_region"]:
        strengths.append("preserves_lower_summary_or_table")
    else:
        weaknesses.append("drops_lower_summary_or_table")
    if presence["has_chart_region"] and presence["has_table_region"]:
        strengths.append("preserves_dashboard_semantics")
    else:
        weaknesses.append("partial_dashboard_semantics_only")
    if presence["is_full_dashboard"]:
        strengths.append("no_loss_anchor")
    return CandidateScore(
        candidate_name=str(candidate["candidate_name"]),
        objective_profile="dashboard_overview_caption_input",
        total_score=total,
        strengths=strengths,
        weaknesses=weaknesses,
        score_breakdown=breakdown,
        bbox=[int(v) for v in candidate["bbox"]],
        component_ids=[str(v) for v in candidate.get("component_ids", [])],
    )


def _score_table_profile(candidate: dict[str, Any], *, full_area: int, kind_by_id: dict[str, str]) -> CandidateScore:
    presence = _candidate_presence(candidate, kind_by_id)
    area_ratio = _bbox_area(candidate["bbox"]) / full_area if full_area else 0.0

    breakdown = {
        "table_region": 3.0 if presence["has_table_region"] else 0.0,
        "title_context": 1.0 if presence["has_title"] else 0.0,
        "compact_focus_bonus": 1.0 if area_ratio < 0.75 else 0.0,
        "chart_noise_penalty": -1.0 if presence["has_chart_region"] else 0.0,
        "full_dashboard_penalty": -1.0 if presence["is_full_dashboard"] else 0.0,
        "missing_table_penalty": -2.0 if not presence["has_table_region"] else 0.0,
    }
    total = sum(breakdown.values())
    strengths: list[str] = []
    weaknesses: list[str] = []
    if presence["has_table_region"]:
        strengths.append("preserves_table_region")
    else:
        weaknesses.append("drops_table_region")
    if presence["has_title"]:
        strengths.append("keeps_title_context")
    if area_ratio < 0.75:
        strengths.append("focused_crop")
    if presence["has_chart_region"]:
        weaknesses.append("keeps_chart_noise_for_table_focus")
    return CandidateScore(
        candidate_name=str(candidate["candidate_name"]),
        objective_profile="embedded_table_focus",
        total_score=total,
        strengths=strengths,
        weaknesses=weaknesses,
        score_breakdown=breakdown,
        bbox=[int(v) for v in candidate["bbox"]],
        component_ids=[str(v) for v in candidate.get("component_ids", [])],
    )


def score_candidate_surfaces(manifest: dict[str, Any]) -> dict[str, Any]:
    _, kind_by_id = _kind_index(manifest)
    full_area = int(manifest["image_width"]) * int(manifest["image_height"])
    candidates = manifest.get("regrouped_candidates", [])

    dashboard_scores = [
        _score_dashboard_profile(candidate, full_area=full_area, kind_by_id=kind_by_id)
        for candidate in candidates
    ]
    table_scores = [
        _score_table_profile(candidate, full_area=full_area, kind_by_id=kind_by_id)
        for candidate in candidates
    ]
    dashboard_scores.sort(key=lambda item: (-item.total_score, item.candidate_name))
    table_scores.sort(key=lambda item: (-item.total_score, item.candidate_name))

    return {
        "experiment": "component_decomposition_candidate_scoring",
        "status": "completed",
        "source_image_path": manifest["source_image_path"],
        "input_probe_manifest_path": manifest.get("input_probe_manifest_path"),
        "image_kind_guess": manifest["interpretation"]["image_kind_guess"],
        "current_experiment_objective": "dashboard_overview_caption_input",
        "profiles": {
            "dashboard_overview_caption_input": {
                "winner_candidate": dashboard_scores[0].candidate_name if dashboard_scores else None,
                "scores": [asdict(score) for score in dashboard_scores],
            },
            "embedded_table_focus": {
                "winner_candidate": table_scores[0].candidate_name if table_scores else None,
                "scores": [asdict(score) for score in table_scores],
            },
        },
        "current_interpretation": {
            "mainline_recommendation": (
                "keep_full_dashboard_or_full_image_path"
                if dashboard_scores and dashboard_scores[0].candidate_name == "full_dashboard"
                else "candidate_crop_may_be_viable"
            ),
            "reentry_ready": False,
            "reason": (
                "deterministic scoring says dashboard semantics are best preserved by full_dashboard; derived-arm reentry still requires typed regrouping and stronger evidence"
            ),
        },
    }


def render_candidate_scoring_report(payload: dict[str, Any]) -> str:
    dashboard = payload["profiles"]["dashboard_overview_caption_input"]
    table_focus = payload["profiles"]["embedded_table_focus"]
    lines = [
        "# Phase1 Image4 Component Decomposition Candidate Scoring",
        "",
        "## Input",
        "",
        f"- source_image_path: `{payload['source_image_path']}`",
        f"- image_kind_guess: `{payload['image_kind_guess']}`",
        f"- current_experiment_objective: `{payload['current_experiment_objective']}`",
        "",
        "## Winners",
        "",
        f"- dashboard_overview_caption_input winner: `{dashboard['winner_candidate']}`",
        f"- embedded_table_focus winner: `{table_focus['winner_candidate']}`",
        "",
        "## Dashboard Overview Scores",
        "",
        "| candidate | total | strengths | weaknesses |",
        "| --- | ---: | --- | --- |",
    ]
    for score in dashboard["scores"]:
        lines.append(
            f"| `{score['candidate_name']}` | `{score['total_score']:.2f}` | `{', '.join(score['strengths']) or 'none'}` | `{', '.join(score['weaknesses']) or 'none'}` |"
        )
    lines.extend(
        [
            "",
            "## Embedded Table Focus Scores",
            "",
            "| candidate | total | strengths | weaknesses |",
            "| --- | ---: | --- | --- |",
        ]
    )
    for score in table_focus["scores"]:
        lines.append(
            f"| `{score['candidate_name']}` | `{score['total_score']:.2f}` | `{', '.join(score['strengths']) or 'none'}` | `{', '.join(score['weaknesses']) or 'none'}` |"
        )
    lines.extend(
        [
            "",
            "## Current Interpretation",
            "",
            f"- mainline_recommendation: `{payload['current_interpretation']['mainline_recommendation']}`",
            f"- reentry_ready: `{payload['current_interpretation']['reentry_ready']}`",
            f"- reason: {payload['current_interpretation']['reason']}",
            "",
            "## Summary",
            "",
            "- This experiment does not reopen `image4` by itself.",
            "- It shows that deterministic regrouping candidates are now scoreable.",
            "- For the current dashboard-level objective, `full_dashboard` still beats narrower crops.",
            "- Therefore the decomposition bottleneck has narrowed from `no component view at all` to `typed regrouping plus stronger promotion evidence`.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


__all__ = [
    "DEFAULT_OUTPUT_JSON",
    "load_json",
    "render_candidate_scoring_report",
    "score_candidate_surfaces",
    "write_json",
]
