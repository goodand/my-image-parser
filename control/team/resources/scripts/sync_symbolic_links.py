#!/usr/bin/env python3
"""Sync user-facing symbolic links with a directory-first policy."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any


DEFAULT_TARGET_DIR = Path(
    "/Users/jaehyuntak/Desktop/Project_____현재_진행중인/Date_Project/sesac_seocho_dataanalysis/Symbolic_links"
)
DEFAULT_CONFIG = Path(
    "control/user_decisions/registry/runtime/user_facing_symbolic_links.json"
)
USER_FACING_MD_ROOTS = (
    "control/user_decisions/resources/notes",
    "control/user_decisions/resources/reports",
)
USER_FACING_PREFIXES = {"REFERENCE", "NOTE", "CHECKLIST", "TEMPLATE", "VISUAL", "REVIEW"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync directory-first user-facing symbolic links and explicit file aliases."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sync_parser = sub.add_parser(
        "sync-defaults",
        help="Sync default directory links and manifest-declared explicit file links.",
    )
    sync_parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Manifest that declares default symbolic-link exports.",
    )

    file_parser = sub.add_parser(
        "link-file",
        help="Create or refresh a file-level symbolic link for an explicitly requested markdown file.",
    )
    file_parser.add_argument("source", type=Path, help="Source markdown file to link.")
    file_parser.add_argument(
        "--alias",
        type=str,
        help="Optional symbolic-link filename. Defaults to workspace-prefixed source filename.",
    )
    file_parser.add_argument(
        "--force",
        action="store_true",
        help="Allow linking markdown files outside the default user-facing roots.",
    )

    for subparser in (sync_parser, file_parser):
        subparser.add_argument(
            "--target-dir",
            type=Path,
            default=DEFAULT_TARGET_DIR,
            help="Destination directory for symbolic links.",
        )

    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def repo_name() -> str:
    return repo_root().name


def repo_relative(path: Path) -> str:
    return os.path.relpath(path.resolve(), repo_root().resolve())


def workspace_prefixed_alias(relative_path: str) -> str:
    stem = relative_path.replace("/", "__")
    return f"{repo_name()}__{stem}"


def user_facing_default_alias(source: Path) -> str:
    return f"{repo_name()}__{source.name}"


def ensure_target_dir(path: Path) -> Path:
    target_dir = path.expanduser().resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir


def load_config(config_path: Path) -> dict[str, Any]:
    candidate = config_path
    if not candidate.is_absolute():
        candidate = repo_root() / candidate
    return json.loads(candidate.read_text(encoding="utf-8"))


def create_or_refresh_link(source: Path, target_dir: Path, alias: str) -> Path:
    target = target_dir / alias
    if target.exists() or target.is_symlink():
        target.unlink()
    target.symlink_to(source)
    return target


def is_allowed_user_facing_markdown(path: Path) -> bool:
    if path.suffix.lower() != ".md":
        return False

    rel = repo_relative(path)
    if any(rel.startswith(prefix) for prefix in USER_FACING_MD_ROOTS):
        return True

    prefix = path.stem.split("_", 1)[0]
    return prefix in USER_FACING_PREFIXES and rel.startswith("control/")


def resolve_repo_path(path_like: str | Path) -> Path:
    candidate = Path(path_like).expanduser()
    if candidate.is_absolute():
        return candidate.resolve()
    return (repo_root() / candidate).resolve()


def command_sync_defaults(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    target_dir = ensure_target_dir(args.target_dir)
    created: list[Path] = []

    for legacy_name in config.get("cleanup_links", []):
        legacy_target = target_dir / legacy_name
        if legacy_target.exists() or legacy_target.is_symlink():
            legacy_target.unlink()

    for item in config.get("directory_links", []):
        source = resolve_repo_path(item["source"])
        alias = item.get("alias") or workspace_prefixed_alias(repo_relative(source))
        created.append(create_or_refresh_link(source, target_dir, alias))

    for item in config.get("explicit_file_links", []):
        source = resolve_repo_path(item["source"])
        alias = item.get("alias") or user_facing_default_alias(source)
        created.append(create_or_refresh_link(source, target_dir, alias))

    for path in created:
        print(path)
    return 0


def command_link_file(args: argparse.Namespace) -> int:
    source = resolve_repo_path(args.source)
    if not source.exists():
        raise SystemExit(f"Source file not found: {source}")
    if source.suffix.lower() != ".md":
        raise SystemExit(f"Source must be a markdown file: {source}")
    if not args.force and not is_allowed_user_facing_markdown(source):
        raise SystemExit(
            "Source is outside the default user-facing markdown scope. "
            "Use --force if you intentionally want to link it."
        )

    target_dir = ensure_target_dir(args.target_dir)
    alias = args.alias or user_facing_default_alias(source)
    target = create_or_refresh_link(source, target_dir, alias)
    print(target)
    return 0


def main() -> int:
    args = parse_args()
    if args.command == "sync-defaults":
        return command_sync_defaults(args)
    if args.command == "link-file":
        return command_link_file(args)
    raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    sys.exit(main())
