# Phase 0 Table Wrapper Consumer Smoke Report

## Purpose

Verify that the implemented read-only wrapper can already serve bounded downstream consumers without touching raw parser outputs.

This smoke checks three immediate consumer shapes:

- table summary lookup
- row-chunk projection for row-level retrieval or grounding
- worksheet-style grid projection plus exact cell lookup

## Inputs

- normalized canonical table:
  - `control/project_domain/resources/manifests/phase0_paddleocr_table_parse_normalized_at2026_03_28.json`
- wrapper implementation:
  - `scripts/table_branch_wrapper_lib.py`
- bounded smoke runner:
  - `scripts/run_table_branch_wrapper_consumer_smoke.py`

## Result

Completed.

Machine-readable artifact:

- `control/project_domain/resources/manifests/phase0_table_wrapper_consumer_smoke_at2026_03_28.json`

## Observed Output

- document_id: `01_full_presentation_2026-03-17`
- table_id: `t1`
- table_count: `1`
- row_count: `4`
- cell_count: `16`
- worksheet_shape: `4 x 4`

Header row:

- `Metric | 70Q | 650 | Delta`

Exact lookup example:

- `cell_id=t1_r1_c0`
- `text=DH@10`
- `row_index=1`
- `col_index=0`

## Consumer Checks

- `get_tables(document_id)`: completed
- `get_table_rows(table_id)`: completed
- `get_cells(table_id)`: completed
- row-chunk projection: completed
- worksheet projection: completed
- exact lookup projection: completed

## Interpretation

The table branch is no longer only parser-complete. It is now consumer-usable in a bounded local form.

This does not yet mean:

- batch-wide parser rollout
- worksheet file export
- row-level RAG indexing
- public MCP wrapper exposure

It does mean the current normalized manifest shape is sufficient for one local read-only consumer layer.

## Next Step

The next bounded table-branch action is one of:

1. run one more `PP-StructureV3` smoke on a second triage-approved table image
2. keep the current single-table baseline and move to downstream integration planning

