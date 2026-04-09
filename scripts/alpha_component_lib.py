#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import deque
from pathlib import Path
from typing import Any

DEFAULT_ALPHA_THRESHOLD = 1
DEFAULT_MIN_PIXELS = 32
DEFAULT_PADDING = 4
DEFAULT_MIN_COMPONENTS_FOR_SUCCESS = 2


def _compute_components(mask: Any) -> list[dict[str, Any]]:
    import numpy as np

    height, width = mask.shape
    visited = np.zeros((height, width), dtype=bool)
    components: list[dict[str, Any]] = []
    ys, xs = np.nonzero(mask)
    for y, x in zip(ys.tolist(), xs.tolist()):
        if visited[y, x]:
            continue
        queue: deque[tuple[int, int]] = deque([(y, x)])
        visited[y, x] = True
        pixels: list[tuple[int, int]] = []
        min_y = max_y = y
        min_x = max_x = x
        while queue:
            cy, cx = queue.popleft()
            pixels.append((cy, cx))
            min_y = min(min_y, cy)
            max_y = max(max_y, cy)
            min_x = min(min_x, cx)
            max_x = max(max_x, cx)
            for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                if 0 <= ny < height and 0 <= nx < width and mask[ny, nx] and not visited[ny, nx]:
                    visited[ny, nx] = True
                    queue.append((ny, nx))
        components.append(
            {
                "pixel_count": len(pixels),
                "bbox": [min_x, min_y, max_x + 1, max_y + 1],
                "pixels": pixels,
            }
        )
    return components


def collect_alpha_components(
    source_image: Path,
    alpha_threshold: int = DEFAULT_ALPHA_THRESHOLD,
    min_pixels: int = DEFAULT_MIN_PIXELS,
) -> dict[str, Any]:
    import numpy as np
    from PIL import Image

    image = Image.open(source_image).convert("RGBA")
    rgba = np.array(image, dtype=np.uint8)
    alpha = rgba[:, :, 3]
    foreground = alpha > alpha_threshold
    height, width = foreground.shape
    if not foreground.any():
        return {
            "image_width": width,
            "image_height": height,
            "component_count": 0,
            "components": [],
        }

    raw_components = _compute_components(foreground)
    filtered = [component for component in raw_components if component["pixel_count"] >= min_pixels]
    filtered.sort(key=lambda item: item["pixel_count"], reverse=True)
    components = [
        {
            "index": index,
            "pixel_count": int(component["pixel_count"]),
            "bbox": [int(value) for value in component["bbox"]],
            "pixels": component["pixels"],
        }
        for index, component in enumerate(filtered, start=1)
    ]
    return {
        "image_width": width,
        "image_height": height,
        "component_count": len(components),
        "components": components,
    }


def run_alpha_split(
    source_image: Path,
    output_dir: Path,
    alpha_threshold: int = DEFAULT_ALPHA_THRESHOLD,
    min_pixels: int = DEFAULT_MIN_PIXELS,
    padding: int = DEFAULT_PADDING,
    min_components_for_success: int = DEFAULT_MIN_COMPONENTS_FOR_SUCCESS,
) -> dict[str, Any]:
    from PIL import Image

    alpha_components = collect_alpha_components(
        source_image=source_image,
        alpha_threshold=alpha_threshold,
        min_pixels=min_pixels,
    )
    if not alpha_components["components"]:
        return {
            "attempted": True,
            "sufficient": False,
            "reason": "No foreground pixels above the alpha threshold were found.",
            "component_count": 0,
            "components": [],
        }

    image = Image.open(source_image).convert("RGBA")
    component_dir = output_dir / "alpha_components"
    component_dir.mkdir(parents=True, exist_ok=True)
    exported: list[dict[str, Any]] = []
    height = int(alpha_components["image_height"])
    width = int(alpha_components["image_width"])

    for component in alpha_components["components"]:
        index = int(component["index"])
        x1, y1, x2, y2 = component["bbox"]
        crop_x1 = max(0, x1 - padding)
        crop_y1 = max(0, y1 - padding)
        crop_x2 = min(width, x2 + padding)
        crop_y2 = min(height, y2 + padding)

        crop = np.array(image.crop((crop_x1, crop_y1, crop_x2, crop_y2)), dtype=np.uint8)
        local_mask = np.zeros((crop_y2 - crop_y1, crop_x2 - crop_x1), dtype=bool)
        for py, px in component["pixels"]:
            local_mask[py - crop_y1, px - crop_x1] = True
        crop[~local_mask] = 0
        output_path = component_dir / f"alpha_component_{index:02d}.png"
        Image.fromarray(crop, mode="RGBA").save(output_path)
        exported.append(
            {
                "index": index,
                "pixel_count": component["pixel_count"],
                "bbox": [crop_x1, crop_y1, crop_x2, crop_y2],
                "output_path": str(output_path),
            }
        )

    manifest_path = component_dir / "alpha_components.json"
    manifest_path.write_text(json.dumps(exported, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    component_count = len(exported)
    return {
        "attempted": True,
        "sufficient": component_count >= min_components_for_success,
        "reason": (
            f"Alpha split found {component_count} component(s) at or above the pixel threshold."
        if component_count
        else "Alpha split found only tiny fragments below the pixel threshold."
    ),
        "component_count": component_count,
        "components": exported,
        "manifest_path": str(manifest_path),
    }


__all__ = [
    "DEFAULT_ALPHA_THRESHOLD",
    "DEFAULT_MIN_COMPONENTS_FOR_SUCCESS",
    "DEFAULT_MIN_PIXELS",
    "DEFAULT_PADDING",
    "collect_alpha_components",
    "run_alpha_split",
]
