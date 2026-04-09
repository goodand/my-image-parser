# Phase 0 Four-Mode Eval Bundle

## Scope

- source_image_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image7.png`
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

A table displays four performance metrics, their improvements from worst to best values, and the percentage improvement rates. The metrics include Context Coherence, Information Concentration, Chunk Recall, and Mean Reciprocal Rank.

### full_image_ocr_context_rerun

- status: `completed`
- input_surface: `full_image_original`
- prompt_version: `openai-gpt-4.1-caption-context-v1`
- context_variant: `n/a`
- context_review_status: `pending_review`
- ocr_status: `usable`

A table compares four evaluation metrics with their lowest and highest values and percentage improvements. The metrics are CC, IC, CR@10, and MRR.

### parser_table_enriched_rerun

- status: `completed`
- input_surface: `full_image_original`
- prompt_version: `openai-gpt-4.1-caption-context-v1`
- context_variant: `parser_table_enriched`
- context_review_status: `pending_review`
- ocr_status: `usable`

A table shows the improvement rates of four evaluation metrics: Context Coherence, Information Concentration, Chunk Recall, and Mean Reciprocal Rank, with percentage improvements from worst to best cases.

### reviewed_isolated_component_rerun

- status: `completed`
- input_surface: `reviewed_table_component_crop`
- prompt_version: `openai-gpt-4.1-caption-context-v1`
- context_variant: `reviewed_isolated_component`
- context_review_status: `pending_review`
- ocr_status: `usable`

A table compares four metrics across WORST and BEST values and percentage improvements: Context Coherence, Information Concentration, Chunk Recall at 10, and Mean Reciprocal Rank.
