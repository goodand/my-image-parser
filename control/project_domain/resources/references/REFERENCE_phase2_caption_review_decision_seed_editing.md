# Phase 2 Caption Review Decision Seed Editing Reference

## Purpose

Provide a compact editing reference for the decision seed JSONL so an operator can update rows consistently without rereading the entire contract spec.

## Seed Path

- [phase2_caption_review_decision_seed_at2026_03_30.jsonl](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase2_caption_review_decision_seed_at2026_03_30.jsonl)

## Allowed `selected_caption_arm`

- `full_image_baseline`
- `full_image_ocr_context_rerun`
- `parser_table_enriched_rerun`
- `reviewed_isolated_component_rerun`
- `llm_edited_caption`

## Allowed `selected_caption_promotion_state`

- `default_ready_anchor`
- `comparison_only_pending_context_review`
- `comparison_ready_reviewed_branch`

## Allowed `caption_decision`

- `select_active_default`
- `select_comparison_winner`
- `select_other_arm`
- `approve_edited_caption`
- `defer`
- `exclude_from_retrieval`

## Allowed `review_status`

- `pending`
- `completed`
- `deferred`

## Allowed `retrieval_block_reason`

- `review_deferred`
- `policy_hold`
- `manual_lane`
- `rejected_for_retrieval`

## Fast Rules

- `select_active_default` means `selected_caption_arm = active_default_arm`
- `select_comparison_winner` means `selected_caption_arm = comparison_winner`
- `approve_edited_caption` means `selected_caption_arm = llm_edited_caption`
- `approve_edited_caption` implies `caption_edit_required = true`
- `selected_caption_arm = llm_edited_caption` requires `selected_caption_promotion_state = null`
- `use_for_retrieval = true` requires non-empty `approved_caption`
- completed rows require non-empty `approved_alt_text`
- `use_for_retrieval = false` requires `retrieval_block_reason`
- `outlier_candidate = true` requires `outlier_reason`
- `caption_decision = defer` requires `review_status = deferred`

## Editing Recommendation

- Edit one full row at a time.
- Do not reorder the rows.
- Preserve the current priority order from the seed.
- After saving, rerun ingestion before starting downstream work.
