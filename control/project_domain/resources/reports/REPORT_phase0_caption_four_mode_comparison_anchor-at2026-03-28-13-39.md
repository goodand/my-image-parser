# Phase 0 4-Mode Caption Comparison

## Scope

- source image path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image11.png`
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

A table shows the performance metrics DH@10, MRR, and CR@10 for 70Q and 65Q in the Two-Phase Hyde-PC test, including delta comparisons.

### full_image_ocr_context_rerun

- status: `completed`
- input_surface: `full_image_original`
- prompt_version: `openai-gpt-4.1-caption-context-v1`
- context_variant: `n/a`
- context_review_status: `pending_review`

This image shows a table comparing metrics for 'Two-Phase Hyde-PC' on '70Q' and '65Q' scenarios, with delta values for each metric. The metrics include DH@10, MRR, and CR@10, with 65Q values generally higher than 70Q.

### parser_table_enriched_rerun

- status: `completed`
- input_surface: `full_image_original`
- prompt_version: `openai-gpt-4.1-caption-context-v1`
- context_variant: `parser_table_enriched`
- context_review_status: `pending_review`

A table compares DH@10, MRR, and CR@10 metrics for 70Q and 65Q under the Two-Phase Hyde-PC condition, showing the delta for each metric.

### reviewed_isolated_component_rerun

- status: `completed`
- input_surface: `reviewed_table_component_crop`
- prompt_version: `openai-gpt-4.1-caption-context-v1`
- context_variant: `reviewed_isolated_component`
- context_review_status: `reviewed_candidate`

A table compares three metrics (DH@10, MRR, CR@10) across two columns (70Q and 65Q) and shows the differences (Delta). The 65Q column has higher values for all metrics.

## Per-Arm Promotion

### full_image_ocr_context_rerun

- promotion_state: `comparison_only_pending_context_review`
- next_gate: `review_context_package`

### parser_table_enriched_rerun

- promotion_state: `comparison_only_pending_context_review`
- next_gate: `review_context_package`

### reviewed_isolated_component_rerun

- promotion_state: `comparison_ready_reviewed_branch`
- next_gate: `review_context_package`

## Readiness

- ready_arms: `full_image_baseline, full_image_ocr_context_rerun, parser_table_enriched_rerun, reviewed_isolated_component_rerun`
- blocked_arms: `none`

## Notes

- Compare the rerun only as bounded evidence until the context package moves beyond pending_review.
- Keep the full-image baseline as the default until the rerun path is explicitly accepted.
- The rerun passed a reviewed-branch gate and may participate in bounded comparison as a non-default arm.
- Keep the baseline active until this reviewed branch is explicitly promoted beyond comparison scope.
