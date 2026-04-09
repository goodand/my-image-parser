from __future__ import annotations

import json
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
INVENTORY_PATH = (
    REPO_ROOT
    / "control/team/resources/migration/control_runs_migration_inventory_at2026_03_30.json"
)
REPORT_PATH = (
    REPO_ROOT
    / "control/team/resources/reports/REPORT_control_runs_immediate_migration_execution-at2026-03-30-15-30.md"
)

TEXT_ROOTS = [
    REPO_ROOT / "control",
    REPO_ROOT / "scripts",
    REPO_ROOT / "skills",
]

SKIP_PREFIXES = [
    REPO_ROOT / "control/team/resources/migration",
]

SKIP_FILES = {
    REPO_ROOT / "scripts/build_control_runs_migration_inventory.py",
    REPO_ROOT / "scripts/apply_control_runs_migration.py",
    REPO_ROOT / "control/team/resources/reports/REPORT_control_structure_16_bucket_migration-at2026-03-27.md",
}

SKIP_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".pdf",
    ".emf",
    ".ico",
    ".pyc",
    ".db",
    ".sqlite",
}

TOP_LEVEL_RUNS = [
    REPO_ROOT / "control/project_domain/runs",
    REPO_ROOT / "control/project_agent_ops/runs",
    REPO_ROOT / "control/user_decisions/runs",
    REPO_ROOT / "control/team/runs",
]


def load_inventory() -> dict:
    return json.loads(INVENTORY_PATH.read_text())


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def move_entries(entries: list[dict]) -> list[dict]:
    moved = []
    for entry in entries:
        source = REPO_ROOT / entry["source_path"]
        target = REPO_ROOT / entry["target_path"]
        if not source.exists():
            continue
        ensure_parent(target)
        shutil.move(str(source), str(target))
        moved.append(
            {
                "source_path": entry["source_path"],
                "target_path": entry["target_path"],
                "source_kind": entry["source_kind"],
                "target_action_unit": entry["target_action_unit"],
                "project_meaning": entry["project_meaning"],
            }
        )
    return moved


def should_skip(path: Path) -> bool:
    if path in SKIP_FILES:
        return True
    if path.suffix.lower() in SKIP_SUFFIXES:
        return True
    return any(path.is_relative_to(prefix) for prefix in SKIP_PREFIXES)


def replace_text_references(replacements: list[tuple[str, str]]) -> list[str]:
    changed: list[str] = []
    for root in TEXT_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or should_skip(path):
                continue
            try:
                original = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            updated = original
            for old, new in replacements:
                updated = updated.replace(old, new)
            if updated != original:
                path.write_text(updated, encoding="utf-8")
                changed.append(str(path.relative_to(REPO_ROOT)))
    return sorted(changed)


def remove_empty_runs_dirs() -> list[str]:
    removed = []
    for path in TOP_LEVEL_RUNS:
        if path.exists() and not any(path.iterdir()):
            path.rmdir()
            removed.append(str(path.relative_to(REPO_ROOT)))
    return removed


def write_report(
    moved: list[dict], changed_files: list[str], removed_runs_dirs: list[str]
) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Control Runs Immediate Migration Execution",
        "",
        "## Result",
        "",
        "- status: `completed`",
        "- execution date: `2026-03-30`",
        f"- moved entries: `{len(moved)}`",
        f"- changed text files: `{len(changed_files)}`",
        f"- removed top-level runs directories: `{len(removed_runs_dirs)}`",
        "",
        "## Removed Top-Level Runs Directories",
        "",
    ]
    if removed_runs_dirs:
        lines.extend([f"- `{item}`" for item in removed_runs_dirs])
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Moved Entries",
            "",
        ]
    )
    for item in moved:
        lines.append(
            f"- `{item['source_path']}` -> `{item['target_path']}` "
            f"(`{item['project_meaning']}` / `{item['target_action_unit']}`)"
        )
    lines.extend(
        [
            "",
            "## Text Files Updated",
            "",
        ]
    )
    if changed_files:
        lines.extend([f"- `{item}`" for item in changed_files])
    else:
        lines.append("- none")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    inventory = load_inventory()
    entries = inventory["entries"]
    moved = move_entries(entries)
    replacements = sorted(
        (
            (entry["source_path"], entry["target_path"])
            for entry in entries
        ),
        key=lambda item: len(item[0]),
        reverse=True,
    )
    changed_files = replace_text_references(replacements)
    removed_runs_dirs = remove_empty_runs_dirs()
    write_report(moved, changed_files, removed_runs_dirs)


if __name__ == "__main__":
    main()
