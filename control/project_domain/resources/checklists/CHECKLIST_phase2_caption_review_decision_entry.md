# Phase 2 Caption Review Decision Entry Checklist

## Before Editing

- [ ] Open [REVIEW_phase2_caption_four_mode_corpus_review-at2026-03-30-22-45.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/reports/REVIEW_phase2_caption_four_mode_corpus_review-at2026-03-30-22-45.md)
- [ ] Open [phase2_caption_review_decision_seed_at2026_03_30.jsonl](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase2_caption_review_decision_seed_at2026_03_30.jsonl)
- [ ] Confirm only one active writer is editing the canonical seed JSONL
- [ ] Confirm fixed truth is unchanged
- [ ] Review images in priority order: `image11, image7, image8, image10, image12, image13, image14, image9, image15`

## Per Row

- [ ] Leave machine-prefilled fields unchanged
- [ ] Set `selected_caption_arm`
- [ ] Set `selected_caption_promotion_state`
- [ ] Set `caption_decision`
- [ ] Set `caption_edit_required`
- [ ] Set `approved_caption`
- [ ] Set `approved_alt_text`
- [ ] Set `use_for_retrieval`
- [ ] Set `mapping_review_required`
- [ ] Set `outlier_candidate`
- [ ] Set `review_status`
- [ ] Set `reviewer_id`
- [ ] Set `reviewed_at`
- [ ] Set `decision_rationale`
- [ ] If `use_for_retrieval = false`, set `retrieval_block_reason`
- [ ] If `outlier_candidate = true`, set `outlier_reason`
- [ ] Add `reviewer_notes` when needed

## Completed Row Rules

- [ ] `review_status = completed`
- [ ] `approved_caption` is non-empty
- [ ] `approved_alt_text` is non-empty
- [ ] `selected_caption_arm` is non-null
- [ ] `caption_decision` is non-null
- [ ] `reviewer_id` is non-null
- [ ] `reviewed_at` is non-null
- [ ] If `selected_caption_arm = llm_edited_caption`, set `selected_caption_promotion_state = null`
- [ ] If `selected_caption_arm` is not `llm_edited_caption`, set `selected_caption_promotion_state`

## Rebuild Ingestion

- [ ] Run `python3 scripts/build_phase2_review_decision_ingestion.py --review-surface-json control/project_domain/resources/manifests/phase2_caption_four_mode_corpus_review_surface_at2026_03_30.json ...`
- [ ] Reopen [phase2_caption_review_decision_ingestion_at2026_03_30.json](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase2_caption_review_decision_ingestion_at2026_03_30.json)
- [ ] Confirm no `Machine-prefilled field drift detected` error was raised
- [ ] Check `review_status_counts`
- [ ] Check `retrieval_ready_count`
- [ ] Check `mapping_ready_count`
- [ ] Check `retrieval_ready_image_ids`
- [ ] Check `mapping_ready_image_ids`

## Stop Conditions

- [ ] Stop if a row needs arm regeneration
- [ ] Stop if a row seems to require corpus truth change
- [ ] Stop if a row requires actual retrieval or mapping execution
