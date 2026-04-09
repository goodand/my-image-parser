# Phase 0 Table Parser Smoke Report

## Purpose

Record the first bounded `PP-StructureV3` real-image table parse smoke and the first successful normalization into the canonical `Table -> Row -> Cell` schema.

## Inputs

- parser launcher:
  - `scripts/mcp/start-paddleocr-mcp.sh`
- bounded runner:
  - `scripts/run_paddleocr_mcp_boot_smoke.py`
- triage-approved image:
  - `control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image11.png`

## Produced Artifacts

- smoke result:
  - `control/project_domain/resources/manifests/phase0_paddleocr_table_parse_smoke_at2026_03_28.json`
- raw parser sidecar:
  - `control/project_domain/resources/manifests/phase0_paddleocr_table_parse_raw_at2026_03_28.json`
- normalized canonical table:
  - `control/project_domain/resources/manifests/phase0_paddleocr_table_parse_normalized_at2026_03_28.json`

## Verified

- `pp_structurev3` succeeded on a real PPT-extracted image
- the selected image was traced back to:
  - `document_id = 01_full_presentation_2026-03-17`
  - `slide = 24`
- the parser returned one recoverable HTML table
- the first normalization produced a canonical `Table -> Row -> Cell` record with:
  - `table_id = t1`
  - `row_count = 4`
  - `column_count = 4`
  - non-zero `bbox` values derived from `table_res_list[0].cell_box_list`
  - per-cell confidence values derived from `table_ocr_pred.rec_scores`

## Practical Reading

The parser captured a compact metric table with this shape:

- header row:
  - `Metric | 70Q | 650 | Delta`
- data rows:
  - `DH@10 | 0 757 | 815 | +0.058`
  - `MRR | .622 | [blank] | +0.048`
  - `CR@10 | 0.514 | 554 | +0.040`

This is sufficient evidence that the current workspace now has:

- one boot-verified `PaddleOCR MCP`
- one real PPT-derived table parse smoke
- one first successful canonical normalization

## Boundary

- this report does not yet expose a local wrapper surface
- this report does not yet activate worksheet export or row-level RAG
- this report closes Steps `1`, `2`, and `3` of the bounded table-branch activation plan for `image11.png`

## Next Step

Design the local wrapper surface that reads normalized outputs only:

- `get_tables(document_id)`
- `get_table_rows(table_id)`
- `get_cells(table_id)`
