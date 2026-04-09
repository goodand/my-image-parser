# Phase 2 Review Decision Ingestion

## Purpose

Consume the corpus review decision rows and materialize only the retrieval-ready and mapping-ready subsets.

## Input

- decision seed path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase2_caption_review_decision_seed_at2026_03_30.jsonl`
- input_row_count: `9`

## Review Status Counts

- pending: `9`
- completed: `0`
- deferred: `0`

## Ready Counts

- retrieval_ready_count: `0`
- mapping_ready_count: `0`
- retrieval_ready_image_ids: `none`
- mapping_ready_image_ids: `none`

## Outputs

- retrieval ready rows: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase2_retrieval_ready_rows_at2026_03_30.jsonl`
- mapping ready rows: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase2_mapping_ready_rows_at2026_03_30.jsonl`

## Next Action

- fill human decision rows and rerun ingestion
