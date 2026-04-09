# Phase 0 Four-Mode Eval Bundle

## Scope

- source_image_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image11.png`
- mode_count: `4`
- comparison_scope: `ready_arm_anchor`
- comparison_ready: `True`
- recommended_current_default: `full_image_baseline`
- next_gate: `review_context_package`

## Ready Arms

- ready_arms: `full_image_baseline, full_image_ocr_context_rerun, parser_table_enriched_rerun, reviewed_isolated_component_rerun`
- blocked_arms: `none`

## Parity Audit

- ready_for_side_by_side_read: `True`
- same_source_image: `True`
- same_model: `True`
- nonblocking_drift: `image_id, prompt_version, input_surface, review_status, context_variant, ocr_status, context_package_present`
- blocking_reasons: `none`

## Arms

### full_image_baseline

- status: `completed`
- input_surface: `extracted_full_image`
- prompt_version: `openai-gpt-4.1-caption-v1`
- context_variant: `n/a`
- context_review_status: `n/a`
- ocr_status: `n/a`

A table compares metrics between 70Q and 65Q with corresponding delta values, under the heading 'Two-Phase Hyde-PC (65Q, 오류 5건 제외)'. The table presents values for DH@10, MRR, and CR@10.

### full_image_ocr_context_rerun

- status: `completed`
- input_surface: `full_image_original`
- prompt_version: `openai-gpt-4.1-caption-context-v1`
- context_variant: `n/a`
- context_review_status: `pending_review`
- ocr_status: `usable`

This image shows a table comparing metrics for 'Two-Phase Hyde-PC' on '70Q' and '65Q' scenarios, with delta values for each metric. The metrics include DH@10, MRR, and CR@10, with 65Q values generally higher than 70Q.

### parser_table_enriched_rerun

- status: `completed`
- input_surface: `full_image_original`
- prompt_version: `openai-gpt-4.1-caption-context-v1`
- context_variant: `parser_table_enriched`
- context_review_status: `pending_review`
- ocr_status: `usable`

A table compares DH@10, MRR, and CR@10 metrics for 70Q and 65Q under the Two-Phase Hyde-PC condition, showing the delta for each metric.

### reviewed_isolated_component_rerun

- status: `completed`
- input_surface: `reviewed_table_component_crop`
- prompt_version: `openai-gpt-4.1-caption-context-v1`
- context_variant: `reviewed_isolated_component`
- context_review_status: `reviewed_candidate`
- ocr_status: `usable`

A table compares three metrics (DH@10, MRR, CR@10) across two columns (70Q and 65Q) and shows the differences (Delta). The 65Q column has higher values for all metrics.
