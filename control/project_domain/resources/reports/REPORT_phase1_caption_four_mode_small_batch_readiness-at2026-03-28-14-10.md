# Phase 1 Caption Four-Mode Small-Batch Readiness

## Summary

- target_image_count: `3`
- included_image_count: `5`
- excluded_image_count: `1`
- minimum_target_met: `True`
- confirmation_policy: `evidence_only_default_with_gpt_confirmation_for_edge_cases`
- default_baseline: `full_image_baseline`

## Included Candidates

### image11

- source_image_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image11.png`
- decision: `include`
- decision_reason: `existing_four_mode_bundle_present`
- single_image_bundle_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase0_caption_four_mode_eval_bundle_at2026_03_28.json`
- gpt_visual_confirmation_status: `not_required`

- full_image_baseline: `ready`
- full_image_ocr_context_rerun: `ready`
- parser_table_enriched_rerun: `ready`
- reviewed_isolated_component_rerun: `ready`

### image7

- source_image_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image7.png`
- decision: `include`
- decision_reason: `frozen_four_mode_bundle_present`
- single_image_bundle_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase1_image7_caption_four_mode_eval_bundle_at2026_03_28.json`
- gpt_visual_confirmation_status: `confirmed_table_centric`

- full_image_baseline: `ready`
- full_image_ocr_context_rerun: `ready`
- parser_table_enriched_rerun: `ready`
- reviewed_isolated_component_rerun: `ready`

### image8

- source_image_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image8.png`
- decision: `include`
- decision_reason: `frozen_four_mode_bundle_present`
- single_image_bundle_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase1_image8_caption_four_mode_eval_bundle_at2026_03_28.json`
- gpt_visual_confirmation_status: `not_required`

- full_image_baseline: `ready`
- full_image_ocr_context_rerun: `ready`
- parser_table_enriched_rerun: `ready`
- reviewed_isolated_component_rerun: `ready`

### image10

- source_image_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image10.png`
- decision: `include`
- decision_reason: `frozen_four_mode_bundle_present`
- single_image_bundle_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase1_image10_caption_four_mode_eval_bundle_at2026_03_28.json`
- gpt_visual_confirmation_status: `not_required`

- full_image_baseline: `ready`
- full_image_ocr_context_rerun: `ready`
- parser_table_enriched_rerun: `ready`
- reviewed_isolated_component_rerun: `ready`

### image9

- source_image_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image9.png`
- decision: `include`
- decision_reason: `frozen_four_mode_bundle_present`
- single_image_bundle_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase1_image9_caption_four_mode_eval_bundle_at2026_03_28.json`
- gpt_visual_confirmation_status: `confirmed_table_centric`

- full_image_baseline: `ready`
- full_image_ocr_context_rerun: `ready`
- parser_table_enriched_rerun: `ready`
- reviewed_isolated_component_rerun: `ready`

## Excluded Candidates

### image4

- source_image_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image4.png`
- decision: `exclude`
- decision_reason: `mixed_chart_table_edge_case_and_no_frozen_derived_arms`
- gpt_visual_confirmation_status: `gpt_confirmation_required`

- full_image_baseline: `ready`
- full_image_ocr_context_rerun: `blocked_by_edge_case_confirmation`
- parser_table_enriched_rerun: `blocked_by_edge_case_confirmation`
- reviewed_isolated_component_rerun: `blocked_by_edge_case_confirmation`

## Bundle

- bundle_name: `phase1_caption_four_mode_small_batch_bundle`
- included_image_count: `5`
- excluded_image_count: `1`
- minimum_target_met: `True`

## Next Step

- Use the canonical aggregate bundle below as the downstream consumer truth-source. Do not consume stale 2-image bundle artifacts.

## Canonical Aggregate Closure

- included_image_ids: `image11, image7, image8, image10, image9`
- excluded_image_ids: `image4`
- canonical_bundle_image_count: `5`
- stale_drift_closed: `True`
- downstream_truth_source: `phase1_caption_four_mode_small_batch_bundle`

# Phase 1 Caption Four-Mode Small-Batch Bundle

## Summary

- image_count: `5`
- all_comparison_ready: `True`
- default_anchor_consistent: `True`

## Images

### /Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image11.png

- bundle_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase0_caption_four_mode_eval_bundle_at2026_03_28.json`
- comparison_ready: `True`
- recommended_current_default: `full_image_baseline`
- ready_arms: `full_image_baseline, full_image_ocr_context_rerun, parser_table_enriched_rerun, reviewed_isolated_component_rerun`
- blocked_arms: `none`

### /Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image7.png

- bundle_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase1_image7_caption_four_mode_eval_bundle_at2026_03_28.json`
- comparison_ready: `True`
- recommended_current_default: `full_image_baseline`
- ready_arms: `full_image_baseline, full_image_ocr_context_rerun, parser_table_enriched_rerun, reviewed_isolated_component_rerun`
- blocked_arms: `none`

### /Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image8.png

- bundle_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase1_image8_caption_four_mode_eval_bundle_at2026_03_28.json`
- comparison_ready: `True`
- recommended_current_default: `full_image_baseline`
- ready_arms: `full_image_baseline, full_image_ocr_context_rerun, parser_table_enriched_rerun, reviewed_isolated_component_rerun`
- blocked_arms: `none`

### /Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image10.png

- bundle_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase1_image10_caption_four_mode_eval_bundle_at2026_03_28.json`
- comparison_ready: `True`
- recommended_current_default: `full_image_baseline`
- ready_arms: `full_image_baseline, full_image_ocr_context_rerun, parser_table_enriched_rerun, reviewed_isolated_component_rerun`
- blocked_arms: `none`

### /Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image9.png

- bundle_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase1_image9_caption_four_mode_eval_bundle_at2026_03_28.json`
- comparison_ready: `True`
- recommended_current_default: `full_image_baseline`
- ready_arms: `full_image_baseline, full_image_ocr_context_rerun, parser_table_enriched_rerun, reviewed_isolated_component_rerun`
- blocked_arms: `none`

