# Phase 0 Table Merge Candidate Builder Report

## Purpose

Create the first bounded merged candidate manifest from:

- Apple normalized table output
- Paddle normalized table output
- canonical parser comparison output

The merged candidate is a review-stage artifact, not final truth.

## Inputs

- Apple normalized table:
  - `control/project_domain/resources/manifests/phase0_apple_document_structure_normalized_at2026_03_28.json`
- Paddle normalized table:
  - `control/project_domain/resources/manifests/phase0_paddleocr_table_parse_normalized_at2026_03_28.json`
- comparison manifest:
  - `control/project_domain/resources/manifests/phase0_table_parser_comparison_at2026_03_28.json`
- builder runner:
  - `scripts/run_table_merge_candidate_builder.py`

## Produced Artifact

- merged candidate manifest:
  - `control/project_domain/resources/manifests/phase0_table_merge_candidate_at2026_03_28.json`

## Baseline Policy

This run uses `baseline_v1`.

Hook chain:

- `BaselineTextSelectionHook`
- `BaselineReviewGateHook`

Operational reading:

- Apple provides the structure surface
- comparison output selects the provisional text source
- numeric-like cells remain `pending_review`
- header conflicts remain `pending_review`
- stable non-numeric cells become `auto_accept_candidate`

## Result

Completed.

## Summary

- total cells: `16`
- auto-accept candidates: `6`
- pending review: `10`
- comparison difference count carried in: `6`

Review targets include:

- one header conflict:
  - `t1_r0_c2` = `65Q` vs `650`
- nine numeric cells that must still be checked before promotion beyond candidate status

## Practical Reading

The merged candidate now keeps, per cell:

- Apple structure
- Apple text
- Paddle text
- one provisional recommended text
- one explicit review status

Example bounded result:

- `t1_r1_c2`
  - Apple: `0.815`
  - Paddle: `815`
  - recommended: `0.815`
  - review_status: `pending_review`

## Interpretation

This closes the first merge-stage gap.

The workspace now has:

- parser-native raw sidecars
- canonical normalized outputs
- a parser comparison surface
- a first merged candidate manifest for human review

This does not yet mean:

- the merged candidate is final truth
- numeric values are auto-approved
- the policy is ready for batch-wide rollout

## Next Step

The next bounded step is one of:

1. build an Obsidian or review-friendly surface for the merged candidate manifest
2. add OCR text as a third candidate source and rerun the same builder
3. repeat the same merge candidate experiment on a second triage-approved table image
