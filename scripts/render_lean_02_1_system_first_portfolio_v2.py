from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "control/project_domain/resources/assets/portfolio_drafts/lean_02_1_system_first_v2"
RENDER_SOURCE_DIR = OUTPUT_DIR / "render_sources"
RENDER_DIR = OUTPUT_DIR / "renders"


def repo_relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def render_one(source_path: Path, output_path: Path) -> None:
    temp_dir = Path(tempfile.mkdtemp(prefix="qlrender-", dir="/tmp"))
    try:
        relative_source = source_path.relative_to(ROOT)
        subprocess.run(
            [
                "qlmanage",
                "-t",
                "-s",
                "2200",
                "-o",
                str(temp_dir),
                str(relative_source),
            ],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        png_path = temp_dir / f"{source_path.name}.png"
        if not png_path.exists():
            raise FileNotFoundError(f"Quick Look thumbnail missing for {source_path}")
        with Image.open(png_path) as image:
            image.convert("RGB").save(output_path, "JPEG", quality=92)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    for source_path in sorted(RENDER_SOURCE_DIR.glob("slide-*-source.pptx")):
        slide_no = source_path.stem.split("-")[1]
        output_path = RENDER_DIR / f"slide-{slide_no}.jpg"
        render_one(source_path, output_path)
        manifest.append({"render_source": repo_relative(source_path), "render_output": repo_relative(output_path)})
    print(json.dumps({"renders": manifest}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
