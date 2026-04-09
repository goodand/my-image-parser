# Phase 2 Downstream Dry Run

## Purpose

Define the dry-run-only handoff between review-decision ingestion and later retrieval or mapping execution.

This surface exists so the workspace can freeze the next runtime contract even when all current review rows remain pending.

## Canonical Inputs

- decision ingestion manifest:
  - [phase2_caption_review_decision_ingestion_at2026_03_30.json](../../manifests/phase2_caption_review_decision_ingestion_at2026_03_30.json)
- retrieval-ready subset:
  - [phase2_retrieval_ready_rows_at2026_03_30.jsonl](../../manifests/phase2_retrieval_ready_rows_at2026_03_30.jsonl)
- mapping-ready subset:
  - [phase2_mapping_ready_rows_at2026_03_30.jsonl](../../manifests/phase2_mapping_ready_rows_at2026_03_30.jsonl)
- decision capture contract:
  - [SPEC_corpus_review_decision_capture.md](./SPEC_corpus_review_decision_capture.md)

## Design Rule

The dry-run layer must not execute retrieval, reranking, or mapping. It only freezes whether those lanes are ready and what artifacts they would expect next.

## Retrieval Dry Run

Retrieval becomes ready only when:

- decision ingestion already marked rows as retrieval-ready
- each row already contains approved caption text
- the selected caption arm and promotion state are present

The dry-run manifest must report:

- ready count
- ready image ids
- blocked reason when ready count is zero
- planned output files for the later real runtime

## Mapping Dry Run

Mapping becomes ready only when:

- mapping-ready rows already exist
- retrieval-ready preconditions already hold

The dry-run manifest must report:

- ready count
- ready image ids
- blocked reason when ready count is zero
- planned output files for the later real runtime

## Non-Goals

- do not execute retrieval
- do not execute reranking
- do not finalize mapping
- do not mutate decision rows
