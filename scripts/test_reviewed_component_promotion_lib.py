from __future__ import annotations

from reviewed_component_promotion_lib import apply_reviewed_component_verdict


def main() -> None:
    comparison = {
        "comparison_ready": False,
        "modes": [
            {"execution_arm": "full_image_baseline", "status": "completed", "context_review_status": None},
            {"execution_arm": "reviewed_isolated_component_rerun", "status": "completed", "context_review_status": "pending_review"},
        ],
        "per_arm_promotion": {
            "reviewed_isolated_component_rerun": {
                "promotion_state": "comparison_only_pending_context_review",
                "next_gate": "review_context_package",
                "notes": [],
            }
        },
        "ready_arms": ["full_image_baseline"],
        "blocked_arms": [{"execution_arm": "reviewed_isolated_component_rerun"}],
        "status_summary": {"ready_arm_count": 1, "blocked_arm_count": 1},
        "parity_audit": {"ready_for_side_by_side_read": True},
        "notes": [],
    }
    verification = {
        "verification_json_path": "/tmp/v.json",
        "result": {
            "decision": "promote_reviewed_component",
            "winner_surface": "reviewed_table_component_crop",
            "confidence": "medium",
        },
    }
    updated = apply_reviewed_component_verdict(comparison=comparison, verification=verification)
    assert updated["comparison_ready"] is True
    assert "reviewed_isolated_component_rerun" in updated["ready_arms"]
    assert updated["per_arm_promotion"]["reviewed_isolated_component_rerun"]["promotion_state"] == "comparison_ready_reviewed_branch"


if __name__ == "__main__":
    main()
