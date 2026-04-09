from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = (
    REPO_ROOT
    / "control/team/resources/migration/control_runs_migration_inventory_at2026_03_30.json"
)


MAPPINGS = [
    {
        "source": "control/project_domain/runs/added_screenshots",
        "target": "control/project_domain/resources/assets/added_screenshots",
        "project_meaning": "project_domain",
        "target_action_unit": "resources",
        "reason": "generated image assets that are still reread as domain support material",
    },
    {
        "source": "control/project_domain/runs/component_split_ocr",
        "target": "control/project_domain/archive/component_split_ocr",
        "project_meaning": "project_domain",
        "target_action_unit": "archive",
        "reason": "historical experiment output kept for traceability, not current active truth",
    },
    {
        "source": "control/project_domain/runs/context_packages",
        "target": "control/project_domain/resources/context_packages",
        "project_meaning": "project_domain",
        "target_action_unit": "resources",
        "reason": "active canonical context package bodies consumed downstream",
    },
    {
        "source": "control/project_domain/runs/cross_validation",
        "target": "control/project_domain/resources/cross_validation",
        "project_meaning": "project_domain",
        "target_action_unit": "resources",
        "reason": "active domain validation material reread as canonical experiment support",
    },
    {
        "source": "control/project_domain/runs/experiment_plans",
        "target": "control/project_domain/resources/experiment_plans",
        "project_meaning": "project_domain",
        "target_action_unit": "resources",
        "reason": "active domain planning documents are canonical resources",
    },
    {
        "source": "control/project_domain/runs/imported_fourarm",
        "target": "control/project_domain/resources/imported_fourarm",
        "project_meaning": "project_domain",
        "target_action_unit": "resources",
        "reason": "imported canonical experiment artifacts remain active domain resources",
    },
    {
        "source": "control/project_domain/runs/intermediates",
        "target": "control/project_domain/archive/intermediates",
        "project_meaning": "project_domain",
        "target_action_unit": "archive",
        "reason": "intermediate derivations are historical support, not primary active truth",
    },
    {
        "source": "control/project_domain/runs/logs",
        "target": "control/project_domain/archive/logs",
        "project_meaning": "project_domain",
        "target_action_unit": "archive",
        "reason": "run logs are retained history, not active canonical resources",
    },
    {
        "source": "control/project_domain/runs/manifests",
        "target": "control/project_domain/resources/manifests",
        "project_meaning": "project_domain",
        "target_action_unit": "resources",
        "reason": "manifests are machine-readable canonical resource bodies",
    },
    {
        "source": "control/project_domain/runs/object_isolation",
        "target": "control/project_domain/archive/object_isolation",
        "project_meaning": "project_domain",
        "target_action_unit": "archive",
        "reason": "historical isolation output is preserved for traceability but not active truth",
    },
    {
        "source": "control/project_domain/runs/pptx_extract",
        "target": "control/project_domain/archive/pptx_extract",
        "project_meaning": "project_domain",
        "target_action_unit": "archive",
        "reason": "legacy extracted media is superseded by active pptx job resources",
    },
    {
        "source": "control/project_domain/runs/pptx_jobs",
        "target": "control/project_domain/resources/pptx_jobs",
        "project_meaning": "project_domain",
        "target_action_unit": "resources",
        "reason": "pptx job manifests and media are active canonical domain resources",
    },
    {
        "source": "control/project_domain/runs/reports",
        "target": "control/project_domain/resources/reports",
        "project_meaning": "project_domain",
        "target_action_unit": "resources",
        "reason": "reports are reread canonical bodies rather than index state",
    },
    {
        "source": "control/project_domain/runs/smoke",
        "target": "control/project_domain/resources/smoke",
        "project_meaning": "project_domain",
        "target_action_unit": "resources",
        "reason": "kept smoke artifacts are reread reference material for future work",
    },
    {
        "source": "control/project_agent_ops/runs/experiment_plans",
        "target": "control/project_agent_ops/resources/experiment_plans",
        "project_meaning": "project_agent_ops",
        "target_action_unit": "resources",
        "reason": "agent-ops plans are active reusable operational resources",
    },
    {
        "source": "control/project_agent_ops/runs/logs",
        "target": "control/project_agent_ops/archive/logs",
        "project_meaning": "project_agent_ops",
        "target_action_unit": "archive",
        "reason": "agent-ops logs are historical trace material",
    },
    {
        "source": "control/project_agent_ops/runs/manifests",
        "target": "control/project_agent_ops/resources/manifests",
        "project_meaning": "project_agent_ops",
        "target_action_unit": "resources",
        "reason": "operational manifests are active machine-readable resources",
    },
    {
        "source": "control/project_agent_ops/runs/reports",
        "target": "control/project_agent_ops/resources/reports",
        "project_meaning": "project_agent_ops",
        "target_action_unit": "resources",
        "reason": "operational reports are canonical reread bodies",
    },
    {
        "source": "control/project_agent_ops/runs/smoke",
        "target": "control/project_agent_ops/resources/smoke",
        "project_meaning": "project_agent_ops",
        "target_action_unit": "resources",
        "reason": "smoke outputs are kept as active operational reference material",
    },
    {
        "source": "control/team/runs/REPORT_control_structure_16_bucket_migration-at2026-03-27.md",
        "target": "control/team/resources/reports/REPORT_control_structure_16_bucket_migration-at2026-03-27.md",
        "project_meaning": "team",
        "target_action_unit": "resources",
        "reason": "team migration report remains active governance reference material",
    },
    {
        "source": "control/user_decisions/runs/REPORT_legacy_boundary_decision_capture-at2026-03-27.md",
        "target": "control/user_decisions/resources/reports/REPORT_legacy_boundary_decision_capture-at2026-03-27.md",
        "project_meaning": "user_decisions",
        "target_action_unit": "resources",
        "reason": "decision capture report is reread canonical decision material",
    },
    {
        "source": "control/user_decisions/runs/REVIEW_phase1_caption_10w_obsidian_caption_review-at2026-03-27-19-08.md",
        "target": "control/user_decisions/resources/reports/REVIEW_phase1_caption_10w_obsidian_caption_review-at2026-03-27-19-08.md",
        "project_meaning": "user_decisions",
        "target_action_unit": "resources",
        "reason": "review body is active decision-support material",
    },
    {
        "source": "control/user_decisions/runs/img",
        "target": "control/user_decisions/resources/assets/review_support_img",
        "project_meaning": "user_decisions",
        "target_action_unit": "resources",
        "reason": "embedded review images are active supporting assets for decision reread",
    },
]


def collect_runs_roots() -> dict[str, list[str]]:
    roots = {
        "project_domain": REPO_ROOT / "control/project_domain/runs",
        "project_agent_ops": REPO_ROOT / "control/project_agent_ops/runs",
        "user_decisions": REPO_ROOT / "control/user_decisions/runs",
        "team": REPO_ROOT / "control/team/runs",
    }
    snapshot: dict[str, list[str]] = {}
    for key, root in roots.items():
        if not root.exists():
            snapshot[key] = []
            continue
        snapshot[key] = sorted(
            str(path.relative_to(REPO_ROOT))
            for path in root.iterdir()
        )
    return snapshot


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    entries = []
    mapped_sources = set()
    for item in MAPPINGS:
        source = REPO_ROOT / item["source"]
        target = REPO_ROOT / item["target"]
        mapped_sources.add(item["source"])
        if source.exists() and not target.exists():
            migration_status = "planned"
        elif (not source.exists()) and target.exists():
            migration_status = "completed"
        elif source.exists() and target.exists():
            migration_status = "conflict"
        else:
            migration_status = "missing"
        entries.append(
            {
                "source_path": item["source"],
                "source_exists": source.exists(),
                "source_kind": "directory" if source.is_dir() else "file",
                "project_meaning": item["project_meaning"],
                "target_action_unit": item["target_action_unit"],
                "target_path": item["target"],
                "target_exists": target.exists(),
                "reason": item["reason"],
                "migration_status": migration_status,
            }
        )

    current_roots = collect_runs_roots()
    unresolved = []
    for paths in current_roots.values():
        for rel in paths:
            if rel not in mapped_sources:
                unresolved.append(rel)

    summary_by_action_unit: dict[str, int] = {}
    summary_by_project_meaning: dict[str, int] = {}
    for entry in entries:
        summary_by_action_unit[entry["target_action_unit"]] = (
            summary_by_action_unit.get(entry["target_action_unit"], 0) + 1
        )
        summary_by_project_meaning[entry["project_meaning"]] = (
            summary_by_project_meaning.get(entry["project_meaning"], 0) + 1
        )

    payload = {
        "generated_at": "2026-03-30",
        "model_source": "ADR_0002_workspace_plane_and_control_action_units",
        "purpose": "Immediate migration inventory for replacing top-level control/*/runs buckets under the 3-action-unit model.",
        "preferred_depth_sequence": [
            "control",
            "project_meaning",
            "action_unit",
        ],
        "action_units": ["resources", "registry", "archive"],
        "top_level_runs_snapshot": current_roots,
        "entries": entries,
        "unresolved_top_level_entries": unresolved,
        "summary": {
            "planned_entry_count": len(entries),
            "unresolved_top_level_entry_count": len(unresolved),
            "by_action_unit": summary_by_action_unit,
            "by_project_meaning": summary_by_project_meaning,
        },
    }

    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
