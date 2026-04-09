# Table Merge Candidate Manifest

This document defines the bounded manifest created after:

- Apple helper normalized output exists
- Paddle normalized output exists
- a canonical comparison artifact exists

## Purpose

The merged candidate manifest is not a final truth file.

It is a review-oriented intermediate artifact that keeps:

- Apple structure
- both text candidates
- one provisional recommended text
- one explicit review status per cell

## Baseline Policy

Current baseline is `baseline_v1`.

It applies these rules:

1. use Apple as the structure source when structure compatibility already matches
2. choose a provisional `recommended_text` from the comparison artifact
3. keep all numeric-like cells as `pending_review`
4. keep header conflicts as `pending_review`
5. allow stable non-numeric cells to become `auto_accept_candidate`

## Current Shape

The manifest stores:

- top-level source metadata
- merge summary
- row list
- cell-level evidence and review status

Example cell shape:

```json
{
  "cell_id": "t1_r1_c2",
  "row_index": 1,
  "col_index": 2,
  "structure_source": "apple",
  "apple_text": "0.815",
  "paddle_text": "815",
  "recommended_text": "0.815",
  "recommended_text_source": "apple",
  "difference_classification": "decimal_point_drift",
  "review_status": "pending_review",
  "review_reason": "numeric_cell_review_gate"
}
```

## Why This Exists

The comparison artifact tells us where the two parsers differ.
The merged candidate manifest turns that comparison into a reviewable table surface.

That makes it useful for:

- human review
- later auto-merge policy refinement
- downstream export planning

without pretending that the table is already final truth.

## Boundary

This manifest does not:

- overwrite the canonical normalized parser outputs
- remove source-specific evidence
- auto-approve risky numeric cells

It exists to stage a later review or merge decision.
