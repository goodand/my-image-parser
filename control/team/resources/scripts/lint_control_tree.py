#!/usr/bin/env python3
"""Lint the canonical control tree against filename and structure rules."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # noqa: BLE001
    yaml = None


CANONICAL_TOP_LEVEL = [
    "user_decisions",
    "project_domain",
    "project_agent_ops",
    "team",
    "legacy",
    "archive",
]
CANONICAL_ACTION_UNITS = {"resources", "registry", "archive"}

MARKDOWN_EXTENSIONS = {".md"}
MACHINE_READABLE_EXTENSIONS = {".json", ".yaml", ".yml"}
OPERATIONAL_PREFIXES = {"PLAN", "REPORT", "SMOKETEST", "AUDIT"}
USER_FACING_NOTE_PREFIXES = {"REFERENCE", "NOTE", "TEMPLATE", "CHECKLIST", "VISUAL"}


@dataclass
class Finding:
    severity: str
    code: str
    path: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Lint canonical control-tree filenames and machine-readable artifacts."
    )
    parser.add_argument(
        "--control-root",
        type=Path,
        default=Path("control"),
        help="Canonical control root. Defaults to control.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON summary.",
    )
    parser.add_argument(
        "--strict-warn",
        action="store_true",
        help="Exit non-zero when warnings are present.",
    )
    parser.add_argument(
        "--pending-delete-stale-days",
        type=int,
        default=30,
        help="Warn when archive/pending_delete files are older than this many days.",
    )
    return parser.parse_args()


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFC", value)
    value = re.sub(r"[^A-Za-z0-9]+", " ", value).strip().lower()
    return re.sub(r"\s+", " ", value)


def normalize_path_string(path: Path) -> str:
    return unicodedata.normalize("NFC", os.path.realpath(str(path)))


def repo_relative_string(path: Path, repo_root: Path) -> str:
    normalized_repo_root = normalize_path_string(repo_root)
    normalized_path = normalize_path_string(path)
    return os.path.relpath(normalized_path, normalized_repo_root)


def strip_timestamp_suffix(stem: str) -> str:
    return re.sub(r"-at\d{4}-\d{2}-\d{2}(?:-\d{2}-\d{2})?$", "", stem)


def stem_without_prefix(stem: str) -> str:
    parts = stem.split("_", 1)
    return parts[1] if len(parts) == 2 else stem


def is_ascii(value: str) -> bool:
    try:
        value.encode("ascii")
        return True
    except UnicodeEncodeError:
        return False


def first_heading(path: Path) -> str | None:
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip()
    except UnicodeDecodeError:
        return None
    return None


def looks_like_decision_support_overlay(path: Path, heading: str | None) -> bool:
    stem = strip_timestamp_suffix(path.stem).lower()
    overlay_markers = {
        "progress_dashboard",
        "task_graph",
        "scoreboard",
        "current_state_snapshot",
        "status_snapshot",
    }
    if any(marker in stem for marker in overlay_markers):
        return True

    heading_text = (heading or "").lower()
    heading_markers = (
        "progress dashboard",
        "task graph",
        "scoreboard",
        "current state snapshot",
        "status snapshot",
    )
    return any(marker in heading_text for marker in heading_markers)


def is_move_redirect_stub(path: Path) -> bool:
    try:
        preview = "\n".join(path.read_text(encoding="utf-8").splitlines()[:20])
    except UnicodeDecodeError:
        return False
    return "## Moved" in preview


def is_user_facing_notes_path(path: Path) -> bool:
    parts = set(path.parts)
    return "user_decisions" in parts and "resources" in parts and "notes" in parts


def yaml_available() -> bool:
    return yaml is not None


def load_contracts(repo_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    filename_contract = load_json(
        repo_root
        / "control"
        / "project_domain"
        / "resources"
        / "specs"
        / "contracts"
        / "filename_and_linting.contract.json"
    )
    legacy_contract = load_json(
        repo_root
        / "control"
        / "project_domain"
        / "resources"
        / "specs"
        / "contracts"
        / "legacy_boundary_lint.contract.json"
    )
    return filename_contract, legacy_contract


def collect_scan_roots(control_root: Path) -> list[Path]:
    roots: list[Path] = []
    for name in CANONICAL_TOP_LEVEL:
        candidate = control_root / name
        if candidate.exists():
            roots.append(candidate)
    return roots


def build_allowed_exact_names(legacy_contract: dict[str, Any], filename_contract: dict[str, Any]) -> set[str]:
    allowed = set(legacy_contract.get("directory_contract_policy", {}).get("accepted_files", []))
    allowed.update(filename_contract.get("filename_policy", {}).get("skill_fixed_files", []))
    return allowed


def is_source_asset_path(path: Path) -> bool:
    return "assets" in path.parts


def lint_control_tree(
    repo_root: Path,
    control_root: Path,
    filename_contract: dict[str, Any],
    legacy_contract: dict[str, Any],
    pending_delete_stale_days: int,
) -> list[Finding]:
    findings: list[Finding] = []
    filename_policy = filename_contract["filename_policy"]
    canonical_prefixes = set(filename_policy["canonical_doc_prefixes"])
    canonical_exts = set(filename_policy["canonical_doc_extensions"])
    machine_readable_pattern = re.compile(filename_policy["machine_readable_pattern"])
    decision_record_pattern = re.compile(filename_policy["decision_record_pattern"])
    dated_operational_pattern = re.compile(filename_policy["dated_operational_pattern"])
    dated_machine_readable_pattern = re.compile(
        r"^[a-z0-9_]+-at\d{4}-\d{2}-\d{2}(?:-\d{2}-\d{2})?\.(json|ya?ml)$"
    )
    allowed_exact_names = build_allowed_exact_names(legacy_contract, filename_contract)

    # Top-level canonical bucket warning.
    for child in control_root.iterdir():
        if not child.is_dir():
            continue
        if child.name not in CANONICAL_TOP_LEVEL:
            findings.append(
                Finding(
                    severity="warn",
                    code="TREE001",
                    path=repo_relative_string(child, repo_root),
                    message="Non-canonical top-level directory under control.",
                )
            )

    # Action-unit and control-local scripts boundary warnings.
    for bucket in CANONICAL_TOP_LEVEL:
        bucket_root = control_root / bucket
        if not bucket_root.exists() or not bucket_root.is_dir():
            continue
        for child in bucket_root.iterdir():
            if not child.is_dir():
                continue
            if child.name not in CANONICAL_ACTION_UNITS:
                findings.append(
                    Finding(
                        severity="warn",
                        code="TREE002",
                        path=repo_relative_string(child, repo_root),
                        message="Non-canonical action-unit directory under project-meaning bucket.",
                    )
                )
        for scripts_dir in bucket_root.rglob("resources/scripts"):
            if repo_relative_string(scripts_dir, repo_root) != "control/team/resources/scripts":
                findings.append(
                    Finding(
                        severity="warn",
                        code="TREE003",
                        path=repo_relative_string(scripts_dir, repo_root),
                        message="control-local scripts are exceptional; prefer root scripts/ unless this is team control-maintenance utility space.",
                    )
                )

    master_plan_dirs: dict[str, list[Path]] = {}

    for scan_root in collect_scan_roots(control_root):
        for path in sorted(scan_root.rglob("*")):
            if not path.is_file():
                continue
            name = path.name
            rel_str = repo_relative_string(path, repo_root)
            source_asset = is_source_asset_path(path)

            if not is_ascii(name):
                findings.append(
                    Finding(
                        "warn" if source_asset else "error",
                        "NAME001",
                        rel_str,
                        "Non-ASCII filename in git-managed control tree."
                        if not source_asset
                        else "Source asset preserves a non-ASCII original filename.",
                    )
                )
            if " " in name:
                findings.append(
                    Finding(
                        "warn" if source_asset else "error",
                        "NAME002",
                        rel_str,
                        "Space in git-managed filename."
                        if not source_asset
                        else "Source asset preserves a spaced original filename.",
                    )
                )
            if "(" in name or ")" in name:
                findings.append(
                    Finding(
                        "warn" if source_asset else "error",
                        "NAME003",
                        rel_str,
                        "Parentheses in git-managed filename."
                        if not source_asset
                        else "Source asset preserves parentheses in the original filename.",
                    )
                )

            if path.suffix in MARKDOWN_EXTENSIONS:
                stem = path.stem
                prefix = stem.split("_", 1)[0]

                if prefix == "ADR" and not decision_record_pattern.match(name):
                    findings.append(
                        Finding("error", "NAME010", rel_str, "ADR filename does not match required pattern.")
                    )

                if prefix in canonical_prefixes and path.suffix in canonical_exts:
                    if re.search(r"-at\d{4}-\d{2}-\d{2}", stem) and not is_user_facing_notes_path(path):
                        findings.append(
                            Finding(
                                "error",
                                "NAME011",
                                rel_str,
                                "Canonical document carries a date suffix.",
                            )
                        )

                    if "master_plans" in path.parts and prefix == "MASTER_PLAN":
                        master_key = str(path.parent)
                        master_plan_dirs.setdefault(master_key, []).append(path)

                heading = first_heading(path)
                if heading:
                    expected = normalize_text(stem_without_prefix(strip_timestamp_suffix(stem)))
                    actual = normalize_text(heading)
                    if expected and actual and expected not in actual and actual not in expected:
                        findings.append(
                            Finding(
                                "warn",
                                "DOC001",
                                rel_str,
                                "Document title and filename appear to drift.",
                            )
                        )

                if (
                    "master_plans" in path.parts
                    and looks_like_decision_support_overlay(path, heading)
                    and not is_move_redirect_stub(path)
                ):
                    findings.append(
                        Finding(
                            "warn",
                            "DOC003",
                            rel_str,
                            "Decision-support overlay belongs under control/user_decisions/resources/notes, not master_plans.",
                        )
                    )

                if (
                    "user_decisions" in path.parts
                    and "resources" in path.parts
                    and "notes" in path.parts
                    and prefix in USER_FACING_NOTE_PREFIXES
                    and not re.search(r"-at\d{4}-\d{2}-\d{2}-\d{2}-\d{2}$", stem)
                ):
                    findings.append(
                        Finding(
                            "warn",
                            "DOC004",
                            rel_str,
                            "User-facing note/reference should carry a minute-level timestamp suffix like -atYYYY-MM-DD-HH-MM.",
                        )
                    )

                if "/resources/" in f"/{rel_str}/":
                    if prefix in OPERATIONAL_PREFIXES and "drafts" not in path.parts:
                        findings.append(
                            Finding(
                                "warn",
                                "DOC002",
                                rel_str,
                                "Operational dated artifact stored in a resources location.",
                            )
                        )

            if path.suffix in MACHINE_READABLE_EXTENSIONS:
                runs_dated_ok = "runs" in path.parts and dated_machine_readable_pattern.match(name)
                if (
                    name not in allowed_exact_names
                    and not machine_readable_pattern.match(name)
                    and not runs_dated_ok
                ):
                    findings.append(
                        Finding(
                            "error",
                            "NAME020",
                            rel_str,
                            "Machine-readable filename is not lowercase snake_case.",
                        )
                    )

                if path.suffix == ".json":
                    try:
                        json.loads(path.read_text(encoding="utf-8"))
                    except Exception as exc:  # noqa: BLE001
                        findings.append(
                            Finding("error", "JSON001", rel_str, f"Invalid JSON syntax: {exc}")
                        )
                elif path.suffix in {".yaml", ".yml"}:
                    if yaml_available():
                        try:
                            yaml.safe_load(path.read_text(encoding="utf-8"))  # type: ignore[union-attr]
                        except Exception as exc:  # noqa: BLE001
                            findings.append(
                                Finding("error", "YAML001", rel_str, f"Invalid YAML syntax: {exc}")
                            )
                    else:
                        findings.append(
                            Finding(
                                "warn",
                                "YAML002",
                                rel_str,
                                "YAML parser unavailable; syntax not validated.",
                            )
                        )

            if "pending_delete" in path.parts:
                age_days = (utc_now() - datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)).days
                if age_days > pending_delete_stale_days:
                    findings.append(
                        Finding(
                            "warn",
                            "ARCH001",
                            rel_str,
                            f"Pending-delete file is stale ({age_days} days).",
                        )
                    )

    for parent, plans in master_plan_dirs.items():
        if len(plans) > 1:
            for plan in plans:
                findings.append(
                    Finding(
                        "error",
                        "NAME030",
                        repo_relative_string(plan, repo_root),
                        "More than one active master plan in the same domain location.",
                    )
                )

    return findings


def summarize(findings: list[Finding]) -> dict[str, Any]:
    errors = [finding for finding in findings if finding.severity == "error"]
    warnings = [finding for finding in findings if finding.severity == "warn"]
    return {
        "generated_at": utc_now().replace(microsecond=0).isoformat(),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "findings": [asdict(finding) for finding in findings],
    }


def render_text(summary: dict[str, Any]) -> str:
    lines = [
        f"errors: {summary['error_count']}",
        f"warnings: {summary['warning_count']}",
    ]
    for finding in summary["findings"]:
        lines.append(
            f"{finding['severity'].upper()} {finding['code']} {finding['path']}: {finding['message']}"
        )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[4]
    control_root = (repo_root / args.control_root).resolve()
    if not control_root.exists():
        raise SystemExit(f"Control root not found: {control_root}")

    filename_contract, legacy_contract = load_contracts(repo_root)
    findings = lint_control_tree(
        repo_root=repo_root,
        control_root=control_root,
        filename_contract=filename_contract,
        legacy_contract=legacy_contract,
        pending_delete_stale_days=args.pending_delete_stale_days,
    )
    summary = summarize(findings)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))

    if summary["error_count"] > 0:
        return 1
    if args.strict_warn and summary["warning_count"] > 0:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
