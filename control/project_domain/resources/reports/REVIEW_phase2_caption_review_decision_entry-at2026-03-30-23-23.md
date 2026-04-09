# Review: Phase 2 Caption Review Decision Entry

## Purpose

Turn the current `phase2` corpus review surface into a human-operator entry workflow for the decision seed JSONL.

This guide is the operator surface for filling the current pending decision rows without changing corpus truth, bundle truth, or downstream manifests directly.

## Writer Policy

The canonical decision seed JSONL assumes one active writer at a time.

If multiple reviewers are needed, assign owned image ids before editing or use reviewer-local working copies and merge them back into the canonical seed before ingestion. Do not let multiple reviewers edit the same canonical JSONL concurrently.

## Do Not Modify

Treat these as fixed truth while entering decisions:

- [REPORT_phase1_caption_four_mode_corpus_closure-at2026-03-30-22-19.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/reports/REPORT_phase1_caption_four_mode_corpus_closure-at2026-03-30-22-19.md)
- [phase1_caption_four_mode_corpus_ready_bundle_at2026_03_29.json](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase1_caption_four_mode_corpus_ready_bundle_at2026_03_29.json)
- [phase1_caption_four_mode_corpus_auto_eval_true_batch_at2026_03_30.json](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase1_caption_four_mode_corpus_auto_eval_true_batch_at2026_03_30.json)
- [REVIEW_phase2_caption_four_mode_corpus_review-at2026-03-30-22-45.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/reports/REVIEW_phase2_caption_four_mode_corpus_review-at2026-03-30-22-45.md)
- [phase2_caption_four_mode_corpus_review_surface_at2026_03_30.json](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase2_caption_four_mode_corpus_review_surface_at2026_03_30.json)
- [SPEC_corpus_review_decision_capture.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/specs/prose/SPEC_corpus_review_decision_capture.md)
- [phase2_caption_review_decision_seed_at2026_03_30.jsonl](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase2_caption_review_decision_seed_at2026_03_30.jsonl)
- [phase2_caption_review_decision_ingestion_at2026_03_30.json](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase2_caption_review_decision_ingestion_at2026_03_30.json)

## Active Interpretation

- active corpus:
  - `image7`
  - `image8`
  - `image9`
  - `image10`
  - `image11`
  - `image12`
  - `image13`
  - `image14`
  - `image15`
- active default:
  - `full_image_baseline`
- current rule:
  - `comparison winner != default replacement`
- current seed state:
  - all rows are still `pending`
- current ingestion status:
  - retrieval-ready rows = `0`
  - mapping-ready rows = `0`

## Current Operator Policy

- reviewer count:
  - `1 reviewer`
- `approved_alt_text`:
  - required for every completed row
- `llm_edited_caption`:
  - allowed only when existing arm texts are not good enough
  - use a consistent LLM-assisted rewrite concept, not freehand manual rewriting
  - if used:
    - `selected_caption_promotion_state = null`
    - `caption_edit_required = true`
    - `caption_decision = approve_edited_caption`
- retrieval strictness:
  - `aggressive`
  - if the reviewer can produce a stable final caption, prefer `use_for_retrieval = true`

Policy note:

- [NOTE_phase2_caption_review_operator_policy-at2026-04-05-11-30.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/user_decisions/resources/notes/NOTE_phase2_caption_review_operator_policy-at2026-04-05-11-30.md)

## Review Order

Work in this order unless a separate supervisor overrides it:

1. `image11`
2. `image7`
3. `image8`
4. `image10`
5. `image12`
6. `image13`
7. `image14`
8. `image9`
9. `image15`

This order preserves the fixed priority from the current review surface.

## Read Surface First

For each image:

1. open the corpus review markdown section for that image
2. read:
   - current default
   - comparison winner
   - winner promotion state
   - why default stays default
   - default caption and alt text
   - winner caption and alt text
3. open the matching seed JSONL row
4. fill only the human decision fields

## Machine-Prefilled Fields

Do not edit these unless the review surface itself is regenerated:

- `image_id`
- `source_image_path`
- `review_surface_path`
- `review_markdown_path`
- `bundle_path`
- `active_default_arm`
- `comparison_winner`
- `comparison_winner_promotion_state`
- `baseline_retained`
- `review_priority_label`
- `pending_context_review_arms`

## Human-Filled Fields

Fill these during operator review:

- `selected_caption_arm`
- `selected_caption_promotion_state`
- `caption_decision`
- `approved_caption`
- `approved_alt_text`
- `caption_edit_required`
- `use_for_retrieval`
- `mapping_review_required`
- `outlier_candidate`
- `review_status`
- `reviewer_id`
- `reviewed_at`
- `decision_rationale`
- `retrieval_block_reason`
- `outlier_reason`
- `reviewer_notes`

## Minimum Completed Row

A row is not complete until all of these are set:

- `selected_caption_arm`
- `selected_caption_promotion_state`
- `caption_decision`
- `caption_edit_required`
- `approved_caption`
- `approved_alt_text`
- `use_for_retrieval`
- `review_status = completed`
- `reviewer_id`
- `reviewed_at`

If `use_for_retrieval = false`, also set:

- `retrieval_block_reason`

If `outlier_candidate = true`, also set:

- `outlier_reason`

## Decision Shortcuts

- choose the current default as final:
  - `caption_decision = select_active_default`
  - `selected_caption_arm = active_default_arm`
- choose the current comparison winner as final:
  - `caption_decision = select_comparison_winner`
  - `selected_caption_arm = comparison_winner`
- choose another arm:
  - `caption_decision = select_other_arm`
- approve a bounded LLM-assisted rewrite:
  - `caption_decision = approve_edited_caption`
  - `selected_caption_arm = llm_edited_caption`
  - `selected_caption_promotion_state = null`
  - `caption_edit_required = true`

## Example Completed Row

This is an example only. Do not copy it blindly into the active seed.

```json
{
  "schema_version": "v1",
  "decision_capture_kind": "corpus_review_decision",
  "image_id": "image11",
  "source_image_path": ".../image11.png",
  "review_surface_path": ".../phase2_caption_four_mode_corpus_review_surface_at2026_03_30.json",
  "review_markdown_path": ".../REVIEW_phase2_caption_four_mode_corpus_review-at2026-03-30-22-45.md",
  "bundle_path": ".../phase0_caption_four_mode_eval_bundle_at2026_03_28.json",
  "active_default_arm": "full_image_baseline",
  "comparison_winner": "reviewed_isolated_component_rerun",
  "comparison_winner_promotion_state": "comparison_ready_reviewed_branch",
  "baseline_retained": true,
  "review_priority_label": "highest",
  "pending_context_review_arms": [
    "full_image_ocr_context_rerun",
    "parser_table_enriched_rerun"
  ],
  "selected_caption_arm": "reviewed_isolated_component_rerun",
  "selected_caption_promotion_state": "comparison_ready_reviewed_branch",
  "caption_decision": "select_comparison_winner",
  "caption_edit_required": false,
  "approved_caption": "A table compares DH@10, MRR, and CR@10 for 70Q and 65Q and shows that 65Q is higher on all three metrics.",
  "approved_alt_text": "Table comparing 70Q and 65Q on DH@10, MRR, and CR@10 with 65Q higher across all metrics.",
  "use_for_retrieval": true,
  "mapping_review_required": true,
  "outlier_candidate": false,
  "review_status": "completed",
  "reviewer_id": "human_reviewer_01",
  "reviewed_at": "2026-03-30T23:30:00+09:00",
  "decision_rationale": "Winner is semantically clearer and remains table-faithful.",
  "retrieval_block_reason": null,
  "outlier_reason": null,
  "reviewer_notes": "Safe to use for retrieval preflight."
}
```

## After Editing

Run the ingestion validator and regenerate the ready subsets:

```bash
python3 scripts/build_phase2_review_decision_ingestion.py \
  --decision-seed-jsonl control/project_domain/resources/manifests/phase2_caption_review_decision_seed_at2026_03_30.jsonl \
  --review-surface-json control/project_domain/resources/manifests/phase2_caption_four_mode_corpus_review_surface_at2026_03_30.json \
  --output-ingestion-json control/project_domain/resources/manifests/phase2_caption_review_decision_ingestion_at2026_03_30.json \
  --output-retrieval-ready-jsonl control/project_domain/resources/manifests/phase2_retrieval_ready_rows_at2026_03_30.jsonl \
  --output-mapping-ready-jsonl control/project_domain/resources/manifests/phase2_mapping_ready_rows_at2026_03_30.jsonl \
  --output-report-md control/project_domain/resources/reports/REPORT_phase2_review_decision_ingestion-at2026-03-30-23-12.md
```

Then confirm:

- no `Machine-prefilled field drift detected` error was raised
- `review_status_counts`
- `retrieval_ready_count`
- `mapping_ready_count`
- `retrieval_ready_image_ids`
- `mapping_ready_image_ids`

from [phase2_caption_review_decision_ingestion_at2026_03_30.json](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase2_caption_review_decision_ingestion_at2026_03_30.json)

## Non-Goals

- do not regenerate arms
- do not modify corpus manifests or bundles
- do not execute retrieval
- do not execute mapping
- do not alter the master plan
