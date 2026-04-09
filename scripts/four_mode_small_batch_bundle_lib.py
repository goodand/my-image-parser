from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def build_small_batch_bundle(bundle_paths: list[str | Path]) -> dict[str, Any]:
    images: list[dict[str, Any]] = []
    for bundle_path in bundle_paths:
        bundle = load_json(bundle_path)
        images.append(
            {
                "bundle_path": str(Path(bundle_path).resolve()),
                "source_image_path": bundle.get("source_image_path"),
                "comparison_ready": bundle.get("comparison_ready"),
                "recommended_current_default": bundle.get("recommended_current_default"),
                "ready_arms": bundle.get("ready_arms") or [],
                "blocked_arms": bundle.get("blocked_arms") or [],
                "arms": bundle.get("arms") or [],
                "per_arm_promotion": bundle.get("per_arm_promotion") or {},
            }
        )
    return {
        "bundle_name": "phase1_caption_four_mode_small_batch_bundle",
        "schema_version": "v1",
        "image_count": len(images),
        "bundle_paths_used": [item["bundle_path"] for item in images],
        "all_comparison_ready": all(bool(item["comparison_ready"]) for item in images),
        "default_anchor_consistent": len(
            {item["recommended_current_default"] for item in images}
        )
        == 1 if images else True,
        "images": images,
    }


def render_small_batch_bundle_report(bundle: dict[str, Any]) -> str:
    lines = [
        "# Phase 1 Caption Four-Mode Small-Batch Bundle",
        "",
        "## Summary",
        "",
        f"- image_count: `{bundle['image_count']}`",
        f"- all_comparison_ready: `{bundle['all_comparison_ready']}`",
        f"- default_anchor_consistent: `{bundle['default_anchor_consistent']}`",
        "",
        "## Images",
        "",
    ]
    for image in bundle["images"]:
        lines.extend(
            [
                f"### {image['source_image_path']}",
                "",
                f"- bundle_path: `{image['bundle_path']}`",
                f"- comparison_ready: `{image['comparison_ready']}`",
                f"- recommended_current_default: `{image['recommended_current_default']}`",
                f"- ready_arms: `{', '.join(image['ready_arms']) or 'none'}`",
                f"- blocked_arms: `{', '.join(item['execution_arm'] for item in image['blocked_arms']) or 'none'}`",
                "",
            ]
        )
    return "\n".join(lines)
