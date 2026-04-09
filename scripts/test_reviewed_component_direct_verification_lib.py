from __future__ import annotations

from reviewed_component_direct_verification_lib import render_direct_verification_report


def main() -> None:
    result = {
        "source_image_path": "/tmp/full.png",
        "reviewed_component_image_path": "/tmp/crop.png",
        "model": "gpt-4.1",
        "prompt_kind": "reviewed_component_direct_verification_v1",
        "full_context_review_status": "pending_review",
        "reviewed_context_review_status": "pending_review",
        "result": {
            "decision": "promote_reviewed_component",
            "winner_surface": "reviewed_table_component_crop",
            "confidence": "medium",
            "full_image_scores": {
                "table_completeness": 5,
                "caption_fitness": 4,
                "noise_suppression": 2,
            },
            "reviewed_component_scores": {
                "table_completeness": 5,
                "caption_fitness": 5,
                "noise_suppression": 5,
            },
            "key_observations": ["obs1", "obs2"],
            "rationale": "crop wins",
        },
    }
    report = render_direct_verification_report(result)
    assert "decision: `promote_reviewed_component`" in report
    assert "reviewed_table_component_crop" in report


if __name__ == "__main__":
    main()
