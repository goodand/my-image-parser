# Table Branch Wrapper Surface

This document defines the local read-only wrapper surface that sits on top of normalized table parser outputs.

It is a design spec, not an implementation report.

## Current Preconditions

The wrapper surface is now allowed because the bounded phase0 sequence has already produced:

- a triage-selected table candidate
- a successful `paddleocr-mcp` boot smoke
- a successful real-image `PP-StructureV3` parse smoke
- a first canonical `Table -> Row -> Cell` normalized output

Current bounded evidence:

- `control/project_domain/resources/manifests/phase0_paddleocr_table_parse_smoke_at2026_03_28.json`
- `control/project_domain/resources/manifests/phase0_paddleocr_table_parse_raw_at2026_03_28.json`
- `control/project_domain/resources/manifests/phase0_paddleocr_table_parse_normalized_at2026_03_28.json`

## Source Of Truth

The wrapper must read normalized outputs only.

Do not read raw `pp_structurev3` responses directly once a normalized record exists.

Primary current source:

- `control/project_domain/resources/manifests/phase0_paddleocr_table_parse_normalized_at2026_03_28.json`

## Purpose

The wrapper surface exists to expose a stable local read API for downstream consumers:

- row-level RAG
- worksheet export
- MCP-facing table lookup
- later table-aware caption or explanation flows

Its job is not to re-run parsing.

## Current Boundary

The current wrapper design is:

- local
- read-only
- normalized-manifest-backed
- single-document-safe first

This means:

- it may scan or index normalized JSON outputs
- it must not call `paddleocr-mcp` itself
- it must not mutate image files or manifests
- it may reject ambiguous `table_id` lookups until a stronger global ID scheme exists

## Canonical Read Surface

The wrapper reads records shaped like:

```json
{
  "document_id": "01_full_presentation_2026-03-17",
  "page": 24,
  "table_id": "t1",
  "rows": [
    {
      "row_index": 0,
      "cells": [
        {
          "cell_id": "t1_r0_c0",
          "col_index": 0,
          "text": "Metric",
          "row_span": 1,
          "col_span": 1,
          "bbox": [15, 77, 145, 132],
          "confidence": 0.997857
        }
      ]
    }
  ]
}
```

## Wrapper Methods

### `get_tables(document_id)`

Goal:

- return the table headers available for one normalized document surface

Required output fields per table:

- `document_id`
- `page`
- `table_id`
- `source_image_path`
- `row_count`
- `column_count`
- `normalized_manifest_path`

Behavior:

- filter normalized outputs by `document_id`
- return one summary object per table
- fail clearly if no normalized table exists for that document

### `get_table_rows(table_id)`

Goal:

- return ordered row objects for one normalized table

Required output fields per row:

- `table_id`
- `row_index`
- `cell_count`
- `cells`

Behavior:

- resolve one unique normalized table record by `table_id`
- preserve row order from the normalized source
- fail if `table_id` is ambiguous across multiple normalized records

### `get_cells(table_id)`

Goal:

- return a flattened cell list for exact lookup, grounding, or export

Required output fields per cell:

- `table_id`
- `row_index`
- `cell_id`
- `col_index`
- `text`
- `row_span`
- `col_span`
- `bbox`
- `confidence`

Behavior:

- flatten the canonical row structure without losing row context
- preserve original `bbox` and `confidence`

## Resolution Rule For `table_id`

Current bounded phase0 artifacts use simple local IDs such as `t1`.

Therefore the wrapper must enforce one of these rules:

1. resolve `table_id` only when it is unique across the current normalized-manifest set
2. otherwise raise an ambiguity error

Do not silently merge tables with the same local `table_id`.

## Recommended Storage Assumption

The first implementation may read directly from:

- `control/project_domain/resources/manifests/*table*_normalized*.json`

If the normalized surface grows, add a lightweight table index later.

## Non-Goals

This wrapper does not own:

- parser execution
- OCR execution
- worksheet writing
- RAG indexing
- mutation of normalized source files

## Current Implementation

The read-only wrapper is now implemented at:

- `scripts/table_branch_wrapper_lib.py`

Current implementation characteristics:

- reads normalized manifests only
- exposes `get_tables`, `get_table_rows`, and `get_cells`
- includes a small CLI for bounded inspection
- fails on ambiguous `table_id`
- is verified by `scripts/test_table_branch_wrapper_lib.py`

## Immediate Implementation Hint

The first implementation can stay very small:

1. load normalized JSON files
2. build in-memory summaries
3. expose `get_tables`, `get_table_rows`, and `get_cells`
4. fail loudly on ambiguous `table_id`

That is enough for the next bounded phase.
