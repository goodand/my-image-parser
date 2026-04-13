# NOTE_retrieval_measurement_without_execution_policy-at2026-04-09-19-19

## Intent

Freeze the downstream policy after master-plan closure: retrieval runtime execution is not mandatory for the current cycle, but retrieval measurement is mandatory.

## Context Clarification

This required measurement is not a simple runtime smoke check.

In downstream workspaces such as `my-second-identity`, source documents may contain meaningful multimodal form. The purpose of measurement is therefore also to check whether approved captions preserve enough form-bearing information for later downstream use, instead of flattening those multimodal structures into generic noise.

## Frozen Decision

For the next downstream opening:

1. `retrieval execution` is **optional**
2. `retrieval measurement` is **required**
3. the required measurement lane is a `dry-run / preflight` lane, not a live retrieval runtime lane

## Required Measurement Surface

The required measurement must answer:

1. how many rows are retrieval-ready
2. which image IDs are retrieval-ready
3. which rows are blocked
4. why blocked rows are blocked
5. what the later retrieval runtime would consume if execution is opened
6. whether any row still risks losing meaningful multimodal form if promoted downstream as-is

Canonical dry-run references:

- [Phase 2 Downstream Dry Run](../../../../project_domain/resources/specs/prose/SPEC_phase2_downstream_dry_run.md)
- [Decision ingestion manifest](../../../../project_domain/resources/manifests/phase2_caption_review_decision_ingestion_at2026_03_30.json)
- [Retrieval-ready rows](../../../../project_domain/resources/manifests/phase2_retrieval_ready_rows_at2026_03_30.jsonl)
- [Retrieval dry-run manifest](../../../../project_domain/resources/manifests/phase2_retrieval_dry_run_at2026_03_30.json)

## Explicit Non-Requirement

The current cycle does **not** require:

- running live retrieval
- running reranking
- finalizing mapping
- opening regeneration

Those may become later scopes, but they are not required by this decision.

## One-Line Summary

The next downstream gate is `retrieval measurement first`; actual retrieval execution stays optional until a later scope explicitly opens it, and that measurement must include multimodal form-preservation adequacy rather than treating all non-text structure as noise.
