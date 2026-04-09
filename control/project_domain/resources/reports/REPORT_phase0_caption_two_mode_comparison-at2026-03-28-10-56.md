# Phase 0 Two-Mode Caption Comparison

## Scope

- source image path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image11.png`
- modes compared: `full_image_baseline` vs `full_image_ocr_context_rerun`

## Status

- same_source_image: `True`
- both_completed: `True`
- promotion_state: `comparison_only_pending_context_review`
- recommended_current_default: `full_image_baseline`
- next_gate: `review_context_package`

## Parity Audit

- ready_for_side_by_side_read: `True`
- all_required_present: `True`
- same_image_id: `False`
- same_model: `True`
- prompt_versions: `openai-gpt-4.1-caption-v1, openai-gpt-4.1-caption-context-v1`
- input_surfaces: `extracted_full_image, full_image_original`
- nonblocking_drift: `image_id, prompt_version, input_surface, review_status`
- blocking_reasons: `none`

## Baseline Mode

- execution_arm: `full_image_baseline`
- ledger_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w1.json`
- input_surface: `extracted_full_image`
- prompt_version: `openai-gpt-4.1-caption-v1`

A table shows the performance metrics DH@10, MRR, and CR@10 for 70Q and 65Q in the Two-Phase Hyde-PC test, including delta comparisons.

## Rerun Mode

- execution_arm: `full_image_ocr_context_rerun`
- ledger_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_agent_ops/registry/jobs/image_caption_jobs/phase0_full_image_context_rerun_image11_at2026_03_28.json`
- input_surface: `full_image_original`
- prompt_version: `openai-gpt-4.1-caption-context-v1`
- context_package_present: `True`
- context_review_status: `pending_review`
- ocr_status: `usable`

This image shows a table comparing metrics for 'Two-Phase Hyde-PC' on '70Q' and '65Q' scenarios, with delta values for each metric. The metrics include DH@10, MRR, and CR@10, with 65Q values generally higher than 70Q.

## Signal Delta

- gained: `mentions_relation`
- lost: `none`
- preserved: `mentions_65q, mentions_70q, mentions_cr10, mentions_delta, mentions_dh10, mentions_mrr, mentions_table`

## Interpretation

- This comparison is comparison-only evidence until the context package review gate closes.
- The rerun can add useful relation/detail signals without yet replacing the baseline automatically.
- Keep the full-image baseline as the active default until reviewed context packages are accepted.
