# Phase 0 Table Parser Comparison Report

## Purpose

Compare the bounded Apple helper normalized output and the bounded Paddle normalized output for the same PPT-derived table image.

The goal is not to pick a new primary parser today.
The goal is to decide whether the current evidence supports a `structure-first / text-repair` merge policy.

## Inputs

- Apple normalized table:
  - `control/project_domain/resources/manifests/phase0_apple_document_structure_normalized_at2026_03_28.json`
- Paddle normalized table:
  - `control/project_domain/resources/manifests/phase0_paddleocr_table_parse_normalized_at2026_03_28.json`
- comparison runner:
  - `scripts/run_table_parser_comparison.py`

## Produced Artifact

- machine-readable comparison:
  - `control/project_domain/resources/manifests/phase0_table_parser_comparison_at2026_03_28.json`

## Result

Completed.

## Verified

- both normalized outputs point to the same bounded source:
  - `document_id = 01_full_presentation_2026-03-17`
  - `page = 24`
  - `table_id = t1`
- structure alignment is fully compatible:
  - row count matches
  - column count matches
  - cell count matches
- current drift is concentrated in cell text, not grid shape

## Observed Differences

Shared structure:

- `4 x 4` table
- `16` cells
- same logical row and column positions

Text drift summary:

- total differing cells: `6`
- repairable candidate differences: `5`
- explicit review-required conflicts: `1`

Current differing cells:

- header conflict:
  - `65Q` vs `650`
- decimal or numeric format drift:
  - `0.757` vs `0 757`
  - `0.815` vs `815`
  - `0.622` vs `.622`
  - `0.554` vs `554`
- missing Paddle value:
  - `0.670` vs `[blank]`

## Interpretation

The current evidence supports this bounded conclusion:

- Apple helper is strong enough to guide structure
- Paddle remains usable as an active parser path
- text quality must still be repaired cell by cell

So the current policy should be:

- `Apple = structure-first`
- `Paddle or OCR = text-repair evidence`
- `numbers and header conflicts = review targets`

## Boundary

This report does not mean:

- Apple helper replaces Paddle as the default parser
- differing numeric values should be auto-committed without review
- one-image evidence is enough for batch-wide merge rollout

It does mean:

- the dual-parser comparison is now grounded in one real PPT-derived table
- the current workspace can compare parser families after both have been normalized into the same canonical shape
- a bounded merge candidate can be designed without reading raw parser payloads directly

## Next Step

The next bounded action is one of:

1. create a merged candidate manifest that keeps Apple structure, preserves both text candidates, and marks numeric cells as `pending_review`
2. repeat the same comparison on one more triage-approved table image
3. use OCR evidence as a third text-repair source before any auto-merge rule is widened
