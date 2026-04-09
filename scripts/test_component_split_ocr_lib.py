#!/usr/bin/env python3
from __future__ import annotations

import tempfile
from pathlib import Path

from PIL import Image

from component_split_ocr_lib import build_component_rows, write_component_package


def _make_fixture_image(path: Path) -> None:
    image = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    for x in range(4, 20):
        for y in range(6, 24):
            image.putpixel((x, y), (255, 0, 0, 255))
    for x in range(36, 56):
        for y in range(8, 22):
            image.putpixel((x, y), (0, 128, 255, 255))
    image.save(path)


def _fake_ocr(component_path: Path) -> dict[str, object]:
    if "01" in component_path.name:
        return {"engine": "fake", "annotation_count": 2, "full_text": "OBJ 1"}
    return {"engine": "fake", "annotation_count": 0, "full_text": ""}


def test_build_component_rows() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        image_path = root / "fixture.png"
        output_dir = root / "out"
        _make_fixture_image(image_path)
        alpha_result, rows = build_component_rows(
            image_path=image_path,
            output_dir=output_dir,
            min_pixels=20,
            min_components_for_success=2,
            ocr_runner=_fake_ocr,
        )
        assert alpha_result["component_count"] == 2
        assert len(rows) == 2
        assert rows[0].ocr_status == "weak_text"
        assert rows[1].ocr_status == "no_text"


def test_write_component_package() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        image_path = root / "fixture.png"
        output_root = root / "packages"
        _make_fixture_image(image_path)
        package = write_component_package(
            image_path=image_path,
            output_root=output_root,
            min_pixels=20,
            min_components_for_success=2,
            ocr_runner=_fake_ocr,
        )
        assert package.alpha_component_count == 2
        assert Path(package.component_table_markdown_path).is_file()
        assert Path(package.component_table_json_path).is_file()


def main() -> int:
    test_build_component_rows()
    test_write_component_package()
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
