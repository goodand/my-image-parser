from __future__ import annotations

import argparse
import glob
import json
import os
import shutil
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


SEOUL = ZoneInfo("Asia/Seoul")


@dataclass(frozen=True)
class ReviewRecord:
    dataset: str
    ledger_name: str
    image_id: str
    filename: str
    status: str
    image_path: Path
    source_pptx: str | None
    slide_numbers: list[int]
    new_filename_candidate: str | None
    caption: str | None
    alt_text: str | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build an Obsidian-friendly markdown review with local image embeds."
    )
    parser.add_argument(
        "--ledger-glob",
        required=True,
        help="Glob for worker ledger JSON files.",
    )
    parser.add_argument(
        "--exclude-glob",
        action="append",
        default=["*smoke*"],
        help="Glob patterns to exclude from ledger matches.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Target markdown path.",
    )
    parser.add_argument(
        "--asset-dir",
        help="Directory where copied review images should be written when --copy-assets is set.",
    )
    parser.add_argument(
        "--copy-assets",
        action="store_true",
        help="Copy source images into --asset-dir and link to those copies instead of original files.",
    )
    parser.add_argument(
        "--source-root",
        help="Common source root for image files when generating symlink-backed embed paths.",
    )
    parser.add_argument(
        "--embed-prefix",
        help="Embed path prefix to use with --source-root, for example 'img/pptx_jobs'.",
    )
    parser.add_argument(
        "--review-title",
        default="Caption Review",
        help="Heading text shown at the top of the generated markdown review.",
    )
    return parser.parse_args()


def should_exclude(path: Path, patterns: list[str]) -> bool:
    return any(path.match(pattern) for pattern in patterns)


def resolve_dataset(record: dict) -> str:
    source_context = record.get("source_context") or {}
    image_id = source_context.get("image_id")
    if isinstance(image_id, str) and ":" in image_id:
        return image_id.split(":", 1)[0]
    path_value = source_context.get("image_path") or record.get("path") or ""
    marker = "/pptx_jobs/"
    if marker in path_value:
        remainder = path_value.split(marker, 1)[1]
        return remainder.split("/", 1)[0]
    return "unknown_dataset"


def load_records(ledger_paths: list[Path]) -> list[ReviewRecord]:
    records: list[ReviewRecord] = []
    for ledger_path in ledger_paths:
        payload = json.loads(ledger_path.read_text(encoding="utf-8"))
        for item in payload.get("records", []):
            source_context = item.get("source_context") or {}
            image_path = Path(source_context.get("image_path") or item.get("path") or "")
            records.append(
                ReviewRecord(
                    dataset=resolve_dataset(item),
                    ledger_name=ledger_path.name,
                    image_id=item.get("image_id") or "",
                    filename=item.get("filename") or image_path.name or "unknown",
                    status=item.get("status") or "unknown",
                    image_path=image_path,
                    source_pptx=Path(source_context.get("source_pptx", "")).name or None,
                    slide_numbers=list(source_context.get("slide_numbers") or []),
                    new_filename_candidate=item.get("new_filename_candidate"),
                    caption=item.get("caption"),
                    alt_text=item.get("alt_text"),
                )
            )
    return records


def unique_target_name(dataset_dir: Path, record: ReviewRecord) -> str:
    base_name = record.filename
    candidate = dataset_dir / base_name
    if not candidate.exists():
        return base_name
    try:
        if candidate.samefile(record.image_path):
            return base_name
    except FileNotFoundError:
        return base_name
    return f"{record.image_id}_{base_name}"


def copy_assets(records: list[ReviewRecord], asset_root: Path, output_dir: Path) -> dict[tuple[str, str, str], str]:
    relative_map: dict[tuple[str, str, str], str] = {}
    for record in records:
        key = (record.dataset, record.image_id, record.filename)
        if record.status != "completed" or not record.image_path.is_file():
            continue
        dataset_dir = asset_root / record.dataset
        dataset_dir.mkdir(parents=True, exist_ok=True)
        target_name = unique_target_name(dataset_dir, record)
        target_path = dataset_dir / target_name
        if not target_path.exists():
            shutil.copy2(record.image_path, target_path)
        relative_map[key] = target_path.relative_to(output_dir).as_posix()
    return relative_map


def direct_image_paths(records: list[ReviewRecord], output_dir: Path) -> dict[tuple[str, str, str], str]:
    relative_map: dict[tuple[str, str, str], str] = {}
    for record in records:
        key = (record.dataset, record.image_id, record.filename)
        if record.status != "completed" or not record.image_path.is_file():
            continue
        relative_map[key] = os.path.relpath(record.image_path, output_dir)
    return relative_map


def prefixed_image_paths(
    records: list[ReviewRecord],
    source_root: Path,
    embed_prefix: str,
) -> dict[tuple[str, str, str], str]:
    relative_map: dict[tuple[str, str, str], str] = {}
    normalized_prefix = embed_prefix.rstrip("/")
    for record in records:
        key = (record.dataset, record.image_id, record.filename)
        if record.status != "completed" or not record.image_path.is_file():
            continue
        suffix = record.image_path.relative_to(source_root).as_posix()
        relative_map[key] = f"{normalized_prefix}/{suffix}"
    return relative_map


def build_markdown(
    records: list[ReviewRecord],
    image_rel_paths: dict[tuple[str, str, str], str],
    review_title: str,
    ledger_glob: str,
) -> str:
    generated_at = datetime.now(SEOUL).strftime("%Y-%m-%d %H:%M %Z")
    dataset_groups: dict[str, list[ReviewRecord]] = defaultdict(list)
    completed = 0
    for record in records:
        dataset_groups[record.dataset].append(record)
        if record.status == "completed":
            completed += 1

    lines: list[str] = [
        f"# Review: {review_title}",
        "",
        "## Summary",
        "",
        f"- generated_at: {generated_at}",
        f"- worker ledgers: {len({record.ledger_name for record in records})}",
        f"- total records: {len(records)}",
        f"- completed: {completed}",
        f"- non-completed: {len(records) - completed}",
        f"- source ledgers: `{ledger_glob}`",
        "- rendering hint: open this file in Obsidian Live Preview or Reading View",
        "",
        "## Dataset Index",
        "",
    ]

    for dataset in sorted(dataset_groups):
        lines.append(f"- `{dataset}`: {len(dataset_groups[dataset])} items")

    for dataset in sorted(dataset_groups):
        lines.extend(["", f"## Dataset: `{dataset}`", ""])
        for record in sorted(dataset_groups[dataset], key=lambda item: item.filename):
            lines.extend(
                [
                    f"### {record.filename}",
                    "",
                    f"- status: `{record.status}`",
                    f"- image_id: `{record.image_id}`",
                    f"- source_pptx: `{record.source_pptx or 'unknown'}`",
                    f"- slide_numbers: `{', '.join(str(n) for n in record.slide_numbers) if record.slide_numbers else 'n/a'}`",
                    f"- filename_candidate: `{record.new_filename_candidate or 'n/a'}`",
                    f"- ledger: `{record.ledger_name}`",
                    "",
                ]
            )

            image_key = (record.dataset, record.image_id, record.filename)
            image_rel_path = image_rel_paths.get(image_key)
            if image_rel_path:
                display_path = image_rel_path if image_rel_path.startswith("..") else f"./{image_rel_path}"
                lines.extend(
                    [
                        f"![{record.filename}]({display_path})",
                        "",
                        f"- image_path: `{display_path}`",
                        "",
                    ]
                )
            else:
                lines.extend(
                    [
                        f"- image_path: `{record.image_path.as_posix()}`",
                        "",
                    ]
                )

            lines.extend(["**Caption**", ""])
            lines.append(f"> {record.caption}" if record.caption else "> n/a")
            lines.extend(["", "**Alt Text**", ""])
            lines.append(f"> {record.alt_text}" if record.alt_text else "> n/a")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ledger_paths = [
        Path(path).resolve()
        for path in sorted(glob.glob(args.ledger_glob))
        if not should_exclude(Path(path), args.exclude_glob)
    ]
    if not ledger_paths:
        raise SystemExit("No ledger files matched.")

    records = load_records(ledger_paths)
    if args.embed_prefix:
        if not args.source_root:
            raise SystemExit("--source-root is required when --embed-prefix is set.")
        image_rel_paths = prefixed_image_paths(records, Path(args.source_root).resolve(), args.embed_prefix)
    elif args.copy_assets:
        if not args.asset_dir:
            raise SystemExit("--asset-dir is required when --copy-assets is set.")
        asset_root = Path(args.asset_dir).resolve()
        asset_root.mkdir(parents=True, exist_ok=True)
        image_rel_paths = copy_assets(records, asset_root, output_path.parent)
    else:
        image_rel_paths = direct_image_paths(records, output_path.parent)
    markdown = build_markdown(records, image_rel_paths, args.review_title, args.ledger_glob)
    output_path.write_text(markdown, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
