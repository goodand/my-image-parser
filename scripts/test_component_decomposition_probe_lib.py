from __future__ import annotations

import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

from component_decomposition_probe_lib import probe_component_decomposition


def _build_synthetic_dashboard(path: Path) -> None:
    image = Image.new("RGBA", (900, 600), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((120, 35, 780, 80), fill=(20, 20, 20, 255))
    for index in range(4):
        x1 = 60 + index * 205
        x2 = x1 + 160
        draw.rectangle((x1, 140, x2, 330), outline=(0, 0, 0, 255), width=3)
        draw.rectangle((x1 + 20, 190, x1 + 45, 325), fill=(40, 130, 240, 255))
        draw.rectangle((x1 + 70, 220, x1 + 95, 325), fill=(240, 90, 60, 255))
        draw.rectangle((x1 + 120, 165, x1 + 145, 325), fill=(60, 180, 80, 255))
    draw.rectangle((120, 410, 520, 520), outline=(0, 0, 0, 255), width=3)
    for row in range(1, 4):
        draw.line((120, 410 + row * 27, 520, 410 + row * 27), fill=(0, 0, 0, 255), width=2)
    for col in range(1, 4):
        draw.line((120 + col * 100, 410, 120 + col * 100, 520), fill=(0, 0, 0, 255), width=2)
    image.save(path)


def test_probe_component_decomposition_detects_dashboard_regions() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        image_path = Path(tmpdir) / "synthetic_dashboard.png"
        _build_synthetic_dashboard(image_path)
        manifest = probe_component_decomposition(image_path)

    summary = manifest["summary"]
    assert summary["found_title_block"] is True
    assert summary["found_chart_region"] is True
    assert summary["found_lower_region"] is True
    assert summary["chart_panel_count"] >= 3
    candidate_names = {candidate["candidate_name"] for candidate in manifest["regrouped_candidates"]}
    assert "full_dashboard" in candidate_names
    assert "title_plus_chart_set" in candidate_names
