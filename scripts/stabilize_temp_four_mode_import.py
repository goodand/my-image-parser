#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPTION_JOB_ROOT = (
    ROOT
    / "control"
    / "project_agent_ops"
    / "registry"
    / "runs"
    / "image_caption_jobs"
)
DEFAULT_IMPORTED_ROOT = ROOT / "control" / "project_domain" / "runs" / "imported_fourarm"
TEXT_SUFFIXES = {".json", ".jsonl", ".md", ".txt"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Import a temp four-arm workspace into a stable workspace location, rewrite internal path "
            "references, and install canonical derived-arm ledgers for downstream discovery."
        )
    )
    parser.add_argument("--temp-root", required=True)
    parser.add_argument("--image-stem", required=True)
    parser.add_argument("--output-import-root")
    parser.add_argument("--print-json-summary", action="store_true")
    return parser.parse_args()


def copy_tree(source_root: Path, destination_root: Path) -> None:
    destination_root.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_root, destination_root, dirs_exist_ok=True)


def rewrite_internal_prefixes(destination_root: Path, old_prefix: str, new_prefix: str) -> list[str]:
    rewritten_files: list[str] = []
    for path in sorted(destination_root.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        original = path.read_text(encoding="utf-8")
        updated = original.replace(old_prefix, new_prefix)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            rewritten_files.append(str(path.resolve()))
    return rewritten_files


def canonical_ledger_targets(image_stem: str) -> dict[str, Path]:
    return {
        f"phase1_full_image_context_rerun_{image_stem}.json": (
            CAPTION_JOB_ROOT / f"phase1_full_image_context_rerun_{image_stem}_at2026_03_28.json"
        ),
        f"phase1_parser_enriched_rerun_{image_stem}.json": (
            CAPTION_JOB_ROOT / f"phase1_parser_enriched_rerun_{image_stem}_at2026_03_28.json"
        ),
        f"phase1_reviewed_isolated_component_rerun_{image_stem}.json": (
            CAPTION_JOB_ROOT / f"phase1_reviewed_isolated_component_rerun_{image_stem}_at2026_03_28.json"
        ),
    }


def install_canonical_ledgers(destination_root: Path, image_stem: str) -> dict[str, str]:
    installed: dict[str, str] = {}
    for source_name, target_path in canonical_ledger_targets(image_stem).items():
        source_path = destination_root / source_name
        if not source_path.is_file():
            raise FileNotFoundError(f"Missing derived-arm ledger in imported root: {source_path}")
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
        installed[source_name] = str(target_path.resolve())
    return installed


def main() -> int:
    args = parse_args()
    source_root = Path(args.temp_root).resolve()
    if not source_root.is_dir():
        raise FileNotFoundError(f"Temp root not found: {source_root}")

    destination_root = (
        Path(args.output_import_root).resolve()
        if args.output_import_root
        else (DEFAULT_IMPORTED_ROOT / args.image_stem).resolve()
    )

    copy_tree(source_root, destination_root)
    rewritten_files = rewrite_internal_prefixes(
        destination_root,
        old_prefix=str(source_root),
        new_prefix=str(destination_root),
    )
    installed_ledgers = install_canonical_ledgers(destination_root, args.image_stem)

    summary = {
        "status": "completed",
        "image_stem": args.image_stem,
        "source_root": str(source_root),
        "destination_root": str(destination_root),
        "rewritten_file_count": len(rewritten_files),
        "installed_ledger_paths": installed_ledgers,
    }
    if args.print_json_summary:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
