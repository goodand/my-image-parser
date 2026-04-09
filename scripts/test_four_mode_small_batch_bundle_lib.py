from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from four_mode_small_batch_bundle_lib import build_small_batch_bundle


def main() -> None:
    with TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        bundle_a = root / "a.json"
        bundle_b = root / "b.json"
        sample = {
            "source_image_path": "/tmp/img.png",
            "comparison_ready": True,
            "recommended_current_default": "full_image_baseline",
            "ready_arms": ["full_image_baseline", "reviewed_isolated_component_rerun"],
            "blocked_arms": [],
            "arms": [],
            "per_arm_promotion": {},
        }
        bundle_a.write_text(json.dumps(sample), encoding="utf-8")
        sample_b = dict(sample)
        sample_b["source_image_path"] = "/tmp/img2.png"
        bundle_b.write_text(json.dumps(sample_b), encoding="utf-8")
        bundle = build_small_batch_bundle([bundle_a, bundle_b])
        assert bundle["image_count"] == 2
        assert bundle["all_comparison_ready"] is True
        assert bundle["default_anchor_consistent"] is True


if __name__ == "__main__":
    main()
