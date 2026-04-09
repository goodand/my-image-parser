# Phase 0 4-Mode Caption Comparison

## Scope

- source image path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image10.png`
- mode_count: `4`

## Status

- same_source_image: `True`
- all_completed: `True`
- ready_arm_count: `4`
- blocked_arm_count: `0`
- comparison_ready: `True`
- recommended_current_default: `full_image_baseline`
- next_gate: `review_context_package`

## Parity Audit

- ready_for_side_by_side_read: `True`
- all_required_present: `True`
- same_model: `True`
- context_variants: `n/a, n/a, parser_table_enriched, reviewed_isolated_component`
- ocr_statuses: `n/a, usable, usable, usable`
- nonblocking_drift: `image_id, prompt_version, input_surface, review_status, context_variant, ocr_status, context_package_present`
- blocking_reasons: `none`

## Arms

### full_image_baseline

- status: `completed`
- input_surface: `extracted_full_image`
- prompt_version: `openai-gpt-4.1-caption-v1`
- context_variant: `n/a`
- context_review_status: `n/a`

A table in Korean showing three scenarios with calculations and corresponding DH@10 values. Each row lists a scenario, a calculation, and a bolded decimal value.

### full_image_ocr_context_rerun

- status: `completed`
- input_surface: `full_image_original`
- prompt_version: `openai-gpt-4.1-caption-context-v1`
- context_variant: `n/a`
- context_review_status: `pending_review`

A table compares three scenarios using calculation values and DH@10 metrics. It includes scenarios '현재', '오류 5건 제거', and '+ P0 재매핑 hit 전환 시'.

### parser_table_enriched_rerun

- status: `completed`
- input_surface: `full_image_original`
- prompt_version: `openai-gpt-4.1-caption-context-v1`
- context_variant: `parser_table_enriched`
- context_review_status: `pending_review`

A table presents three scenarios comparing calculation values and DH@10 scores. The scenarios include current state, after removing 5 errors, and after P0 remapping hit conversion.

### reviewed_isolated_component_rerun

- status: `completed`
- input_surface: `reviewed_table_component_crop`
- prompt_version: `openai-gpt-4.1-caption-context-v1`
- context_variant: `reviewed_isolated_component`
- context_review_status: `pending_review`

A table in Korean presents three scenarios with corresponding calculations and DH@10 values, showing incremental improvements.

## Per-Arm Promotion

### full_image_ocr_context_rerun

- promotion_state: `comparison_only_pending_context_review`
- next_gate: `review_context_package`

### parser_table_enriched_rerun

- promotion_state: `comparison_only_pending_context_review`
- next_gate: `review_context_package`

### reviewed_isolated_component_rerun

- promotion_state: `comparison_only_pending_context_review`
- next_gate: `review_context_package`

## Readiness

- ready_arms: `full_image_baseline, full_image_ocr_context_rerun, parser_table_enriched_rerun, reviewed_isolated_component_rerun`
- blocked_arms: `none`

## Notes

- Compare the rerun only as bounded evidence until the context package moves beyond pending_review.
- Keep the full-image baseline as the default until the rerun path is explicitly accepted.
