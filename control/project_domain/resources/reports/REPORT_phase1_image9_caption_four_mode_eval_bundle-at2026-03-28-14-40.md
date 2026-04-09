# Phase 0 Four-Mode Eval Bundle

## Scope

- source_image_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image9.png`
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

A table in Korean compares four metrics (CC, IC, CR@10, MRR) for quality and accuracy improvements, showing percentage increases for each. Key improvements are highlighted below the table.

### full_image_ocr_context_rerun

- status: `completed`
- input_surface: `full_image_original`
- prompt_version: `openai-gpt-4.1-caption-context-v1`
- context_variant: `n/a`
- context_review_status: `pending_review`
- ocr_status: `usable`

A table compares four search quality and accuracy metrics, showing percentage increases for each. Additional notes indicate the largest increases in two perspectives.

### parser_table_enriched_rerun

- status: `completed`
- input_surface: `full_image_original`
- prompt_version: `openai-gpt-4.1-caption-context-v1`
- context_variant: `parser_table_enriched`
- context_review_status: `pending_review`
- ocr_status: `usable`

A table in Korean compares four metrics (CC, IC, CR@10, MRR) related to search quality and accuracy, showing their percentage increases. Notes under the table summarize the largest increases by category.

### reviewed_isolated_component_rerun

- status: `completed`
- input_surface: `reviewed_table_component_crop`
- prompt_version: `openai-gpt-4.1-caption-context-v1`
- context_variant: `reviewed_isolated_component`
- context_review_status: `pending_review`
- ocr_status: `usable`

A table in Korean compares four performance indicators (CC, IC, CR@10, MRR) with their descriptions and respective percentage improvements. The table is structured into three columns: indicator, description, and relative increase.
