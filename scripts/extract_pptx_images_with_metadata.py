#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import shutil
import subprocess
import zipfile
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Dict, Iterable, List
from xml.etree import ElementTree as ET


IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".tif",
    ".tiff",
    ".emf",
    ".wmf",
    ".svg",
}

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
}


@dataclass
class SlideUsage:
    slide: int
    occurrence: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract image assets from PPTX files and write a metadata manifest."
    )
    parser.add_argument(
        "pptx_files",
        nargs="*",
        help="Optional PPTX files. If omitted, all .pptx files from --input-dir are processed.",
    )
    parser.add_argument(
        "--input-dir",
        default="control/project_domain/resources/assets/pptx_inputs",
        help="Directory to scan for .pptx files when positional files are omitted.",
    )
    parser.add_argument(
        "--output-root",
        default="control/project_domain/resources/pptx_jobs",
        help="Root directory for extracted outputs.",
    )
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_output_name(index: int, stem: str) -> str:
    ascii_stem = stem.encode("ascii", "ignore").decode("ascii")
    ascii_stem = re.sub(r"[^A-Za-z0-9._-]+", "_", ascii_stem).strip("._-")
    if not ascii_stem:
        ascii_stem = "pptx"
    return f"{index:02d}_{ascii_stem}"


def discover_pptx_files(args: argparse.Namespace) -> List[Path]:
    if args.pptx_files:
        return [Path(item).expanduser().resolve() for item in args.pptx_files]
    input_dir = Path(args.input_dir).resolve()
    return sorted(path.resolve() for path in input_dir.glob("*.pptx"))


def normalize_rel_target(target: str) -> str:
    base = PurePosixPath("ppt/slides")
    joined = base / target
    return posixpath.normpath(str(joined))


def collect_slide_usage(pptx_path: Path) -> Dict[str, List[SlideUsage]]:
    usage: Dict[str, List[SlideUsage]] = defaultdict(list)
    with zipfile.ZipFile(pptx_path) as zf:
        slide_paths = sorted(
            name
            for name in zf.namelist()
            if name.startswith("ppt/slides/slide") and name.endswith(".xml")
        )
        for slide_path in slide_paths:
            slide_name = PurePosixPath(slide_path).name
            slide_no_match = re.search(r"slide(\d+)\.xml$", slide_name)
            if not slide_no_match:
                continue
            slide_no = int(slide_no_match.group(1))
            rels_path = f"ppt/slides/_rels/{slide_name}.rels"
            if rels_path not in zf.namelist():
                continue
            rels_root = ET.fromstring(zf.read(rels_path))
            rel_map: Dict[str, str] = {}
            for rel in rels_root.findall("pr:Relationship", NS):
                rel_id = rel.attrib.get("Id")
                target = rel.attrib.get("Target")
                if rel_id and target:
                    rel_map[rel_id] = normalize_rel_target(target)
            slide_root = ET.fromstring(zf.read(slide_path))
            occurrence_by_media: Dict[str, int] = defaultdict(int)
            for blip in slide_root.findall(".//a:blip", NS):
                rel_id = blip.attrib.get(f"{{{NS['r']}}}embed")
                if not rel_id:
                    continue
                target = rel_map.get(rel_id)
                if not target or not target.startswith("ppt/media/"):
                    continue
                occurrence_by_media[target] += 1
                usage[target].append(
                    SlideUsage(slide=slide_no, occurrence=occurrence_by_media[target])
                )
    return usage


def extract_images(pptx_path: Path, output_dir: Path, slide_usage: Dict[str, List[SlideUsage]]) -> List[dict]:
    media_dir = output_dir / "media"
    media_dir.mkdir(parents=True, exist_ok=True)
    exported: List[dict] = []
    with zipfile.ZipFile(pptx_path) as zf:
        media_paths = sorted(
            name
            for name in zf.namelist()
            if name.startswith("ppt/media/")
            and Path(name).suffix.lower() in IMAGE_EXTENSIONS
        )
        for media_path in media_paths:
            filename = Path(media_path).name
            output_path = media_dir / filename
            with zf.open(media_path) as src, output_path.open("wb") as dst:
                shutil.copyfileobj(src, dst)
            exported.append(
                {
                    "file": filename,
                    "source_zip_path": media_path,
                    "output_path": str(output_path.resolve()),
                    "extension": output_path.suffix.lower(),
                    "bytes": output_path.stat().st_size,
                    "sha256": sha256_file(output_path),
                    "slide_usages": [
                        {"slide": item.slide, "occurrence": item.occurrence}
                        for item in slide_usage.get(media_path, [])
                    ],
                }
            )
    return exported


def collect_exiftool_metadata(paths: Iterable[Path]) -> Dict[str, dict]:
    paths = list(paths)
    if not paths:
        return {}
    command = ["exiftool", "-m", "-j", "-n", *[str(path) for path in paths]]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr.strip() or "exiftool metadata extraction failed")
    if not result.stdout.strip():
        return {}
    records = json.loads(result.stdout)
    by_path: Dict[str, dict] = {}
    for record in records:
        source = record.pop("SourceFile", None)
        if source:
            by_path[str(Path(source).resolve())] = record
    return by_path


def summarize_extensions(exported: List[dict]) -> Dict[str, int]:
    counts: Dict[str, int] = defaultdict(int)
    for item in exported:
        counts[item["extension"]] += 1
    return dict(sorted(counts.items()))


def build_manifest(pptx_path: Path, output_dir: Path, exported: List[dict]) -> dict:
    output_paths = [Path(item["output_path"]) for item in exported]
    metadata_by_path = collect_exiftool_metadata(output_paths)
    for item in exported:
        item["embedded_metadata"] = metadata_by_path.get(item["output_path"], {})
    slide_ref_count = sum(len(item["slide_usages"]) for item in exported)
    return {
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(),
        "source_pptx": str(pptx_path),
        "source_filename": pptx_path.name,
        "output_dir": str(output_dir.resolve()),
        "summary": {
            "exported_image_count": len(exported),
            "slide_reference_count": slide_ref_count,
            "extensions": summarize_extensions(exported),
        },
        "exported_images": exported,
    }


def process_pptx(index: int, pptx_path: Path, output_root: Path) -> Path:
    job_dir = output_root / safe_output_name(index, pptx_path.stem)
    job_dir.mkdir(parents=True, exist_ok=True)
    slide_usage = collect_slide_usage(pptx_path)
    exported = extract_images(pptx_path, job_dir, slide_usage)
    manifest = build_manifest(pptx_path, job_dir, exported)
    manifest_path = job_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    return manifest_path


def main() -> int:
    args = parse_args()
    pptx_files = discover_pptx_files(args)
    if not pptx_files:
        raise SystemExit("No .pptx files found to process.")
    output_root = Path(args.output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    manifest_paths = []
    for index, pptx_path in enumerate(pptx_files, start=1):
        manifest_paths.append(process_pptx(index, pptx_path, output_root))
    for manifest_path in manifest_paths:
        print(manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
