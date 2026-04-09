# Phase 2 Review Decision Downstream Dry Run

## Purpose

Freeze the next runtime contract after review decision ingestion without executing retrieval or mapping.

## Retrieval Dry Run

- retrieval_ready_count: `0`
- retrieval_ready_image_ids: `none`
- ready_to_execute: `false`
- blocked_reason: `no_completed_review_rows_marked_for_retrieval`

Planned outputs:
- `retrieval_input.jsonl`
- `retrieval_candidates.jsonl`
- `reranked_top5.jsonl`

## Mapping Dry Run

- mapping_ready_count: `0`
- mapping_ready_image_ids: `none`
- ready_to_execute: `false`
- blocked_reason: `no_completed_review_rows_ready_for_mapping`

Planned outputs:
- `mapping_review.jsonl`
- `mapping_selected.jsonl`
- `outlier_labeled.jsonl`

## Guardrails

- do not execute retrieval in this slice
- do not execute reranking in this slice
- do not finalize mapping in this slice
- rerun this dry-run builder after human review rows move from pending to completed
