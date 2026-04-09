from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from caption_arm_comparison_lib import (
    build_eval_bundle_from_comparison,
    render_eval_bundle_report,
    render_multi_mode_comparison_report,
)


REVIEWED_ARM = "reviewed_isolated_component_rerun"


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def apply_reviewed_component_verdict(
    *,
    comparison: dict[str, Any],
    verification: dict[str, Any],
) -> dict[str, Any]:
    verdict = ((verification.get("result") or {}).get("decision") or "").strip()
    winner_surface = ((verification.get("result") or {}).get("winner_surface") or "").strip()
    promoted = verdict == "promote_reviewed_component" and winner_surface == "reviewed_table_component_crop"
    updated = json.loads(json.dumps(comparison))
    updated["reviewed_component_direct_verification"] = {
        "decision": verdict,
        "winner_surface": winner_surface,
        "confidence": (verification.get("result") or {}).get("confidence"),
        "verification_json_path": verification.get("verification_json_path"),
    }
    if not promoted:
        updated.setdefault("notes", [])
        updated["notes"].append(
            "Reviewed isolated component remains comparison-evidence only because direct verification did not promote it."
        )
        return updated

    for mode in updated.get("modes", []):
        if mode.get("execution_arm") == REVIEWED_ARM:
            mode["context_review_status"] = "reviewed_candidate"
    updated.setdefault("per_arm_promotion", {})
    updated["per_arm_promotion"][REVIEWED_ARM] = {
        "promotion_state": "comparison_ready_reviewed_branch",
        "next_gate": "review_context_package",
        "notes": [
            "Direct GPT image verification promoted the reviewed isolated component as a comparison-ready reviewed branch.",
            "Keep the full-image baseline as the default until a later promotion gate explicitly changes that status.",
        ],
    }
    updated["ready_arms"] = [mode["execution_arm"] for mode in updated.get("modes", []) if mode.get("status") == "completed"]
    updated["blocked_arms"] = [
        item
        for item in updated.get("blocked_arms", [])
        if item.get("execution_arm") != REVIEWED_ARM
    ]
    updated.setdefault("status_summary", {})
    updated["status_summary"]["ready_arm_count"] = len(updated["ready_arms"])
    updated["status_summary"]["blocked_arm_count"] = len(updated["blocked_arms"])
    parity_ready = bool(((updated.get("parity_audit") or {}).get("ready_for_side_by_side_read")))
    updated["comparison_ready"] = parity_ready and not updated["blocked_arms"]
    updated.setdefault("notes", [])
    updated["notes"].append(
        "Reviewed isolated component was promoted to comparison_ready_reviewed_branch via direct GPT image verification."
    )
    return updated


def write_promoted_outputs(
    *,
    promoted_comparison: dict[str, Any],
    comparison_output_json: Path,
    comparison_report_md: Path,
    eval_bundle_output_json: Path,
    eval_bundle_report_md: Path,
) -> dict[str, Any]:
    eval_bundle = build_eval_bundle_from_comparison(promoted_comparison)
    comparison_output_json.write_text(
        json.dumps(promoted_comparison, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    comparison_report_md.write_text(
        render_multi_mode_comparison_report(
            promoted_comparison,
            title="Phase 1 Image-Specific Four-Mode Caption Comparison",
        ),
        encoding="utf-8",
    )
    eval_bundle_output_json.write_text(
        json.dumps(eval_bundle, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    eval_bundle_report_md.write_text(
        render_eval_bundle_report(
            eval_bundle,
            title="Phase 1 Image-Specific Four-Mode Eval Bundle",
        ),
        encoding="utf-8",
    )
    return eval_bundle
