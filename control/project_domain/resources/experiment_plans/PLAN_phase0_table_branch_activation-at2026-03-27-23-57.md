# Phase 0 Table Branch Activation Plan

## Purpose

Define the immediate experiment sequence required before the project treats the table branch as an active runnable path.

This plan starts from the current state:

- `imagesorcery-mcp` is usable for bounded component selection
- `macos-ocr-mcp` is usable as OCR evidence
- `paddleocr-mcp` is now boot-verified for bounded local `PP-StructureV3` parsing
- the canonical `Table -> Row -> Cell` schema now has one bounded normalized real-image artifact

## Current Progress

The first bounded activation slice has now produced:

- Step 0 complete:
  - triage selected `image11.png` as `use_full_image`
- Step 1 complete:
  - `paddleocr-mcp` full boot smoke succeeded
- Step 2 complete:
  - `PP-StructureV3` real-image smoke succeeded on `image11.png`
- Step 3 complete:
  - one canonical `Table -> Row -> Cell` normalization was written for the same image
- Step 5 complete:
  - the implemented read-only wrapper served a bounded downstream consumer smoke on the normalized table

The bounded sequence now includes an implemented Step 4 read-only wrapper.

## Current Reviewed Skill Supports

The current workspace now has explicit reviewed or reusable skill surfaces around the table branch:

- `transparent-component-triage`
- `parser-sidecar-to-canonical-schema-promotion`
- `table-branch-activation-slice`
- `vendored-mcp-onboarding`

These skills support bounded activation, but they do not replace canonical smoke evidence.

## Required Execution Order

The next table-branch activation sequence is:

0. design and use an `xhigh` triage-worker selection gate instead of automatic component-isolation fanout
1. complete `paddleocr-mcp` full boot smoke
2. run `PP-StructureV3` smoke on `1` to `2` real PPT-extracted table images
3. normalize the parser output into the canonical `Table -> Row -> Cell` schema
4. only then implement the local wrapper surface for `get_tables`, `get_table_rows`, and `get_cells`
5. use the wrapper against the normalized output for a bounded downstream consumer smoke

This order is mandatory.

Do not implement the wrapper first.
Do not promote `paddleocr-mcp` to canonical parser status before Step 3 succeeds.

## Why Step 0 Comes First

The current phase0 object-isolation smoke showed that automatic crop selection can be mechanically valid while still semantically wrong.

Therefore the project should not fan out automatic component isolation for table candidates.

Instead, the first gate is a bounded triage-worker design that decides:

- whether the full image should be used directly
- whether a reviewed crop is needed
- whether a candidate image should be excluded from the table-parser smoke set

## Step 0. XHigh Triage Worker Selection Gate

### Goal

Use `gpt-5.4 xhigh` workers to classify candidate PPT-extracted images before any table-parser smoke is run.

### Worker Decision Space

Each triage worker should output exactly one of:

- `use_full_image`
- `use_reviewed_crop`
- `not_a_table_candidate`
- `needs_manual_audit`

### Minimum Inputs Per Worker

- source image path
- source slide number or ppt provenance
- existing OCR evidence if available
- object-isolation smoke evidence if available
- the user-facing goal:
  - `table parse readiness`

### Output Artifact

- `control/project_domain/resources/manifests/phase0_table_triage_selection.jsonl`

Minimum row fields:

- `source_image_id`
- `source_image_path`
- `source_slide_numbers`
- `selection_decision`
- `selected_surface_path`
- `selection_rationale`
- `worker_id`
- `audit_required`

### Success Gate

- at least `1` and at most `2` candidate images are promoted into the parser smoke set
- every selected surface has a clear provenance path
- no automatic crop is promoted without explicit triage acceptance

## Step 1. PaddleOCR MCP Full Boot Smoke

### Goal

Move `paddleocr-mcp` from `installed_pending_full_smoke` to a true boot-verified state.

### Required Checks

- launcher starts without falling back to home-scoped cache paths
- local `PP-StructureV3` mode is selected
- stdio boot remains machine-readable
- one bounded command completes without hanging indefinitely

### Output Artifact

- `control/project_agent_ops/resources/smoke/SMOKETEST_paddleocr_mcp_boot-atYYYY-MM-DD-HH-MM.md`

### Success Gate

- `tool_inventory.json` may be updated from `boot_verified: false` to `boot_verified: true` only after this smoke exists

## Step 2. PP-StructureV3 Real-Image Table Parse Smoke

### Goal

Run the installed parser on `1` to `2` real PPT-extracted images that passed Step 0.

### Input Policy

- use only triage-approved images
- prefer the full image unless triage explicitly selected a reviewed crop
- do not exceed `2` images in this bounded smoke

### Output Artifact Family

- `control/project_domain/resources/manifests/phase0_table_parser_smoke_inputs.jsonl`
- `control/project_domain/resources/manifests/phase0_table_parser_raw_outputs.jsonl`
- `control/project_domain/resources/reports/REPORT_phase0_table_parser_smoke-atYYYY-MM-DD-HH-MM.md`

### Success Questions

- does `PP-StructureV3` detect the table region correctly?
- are rows and cells materially recoverable?
- is the raw output stable enough to normalize?
- does parser output outperform the current OCR-only fallback for table structure?

## Step 3. Canonical Schema Normalization

### Goal

Map raw parser output into the project’s canonical `Table -> Row -> Cell` structure.

### Minimum Canonical Fields

- `document_id`
- `page`
- `table_id`
- `rows`
  - `row_index`
  - `cells`
    - `col_index`
    - `text`
    - `row_span`
    - `col_span`
    - `bbox`
    - `confidence`

### Output Artifact

- `control/project_domain/resources/manifests/phase0_table_parser_normalized_outputs.jsonl`

### Success Gate

- at least one real PPT-derived table image is normalized without schema drift
- every normalized row can be traced back to the original image path and parser raw output

## Step 4. Wrapper Surface Implementation

### Goal

Implement the local wrapper surface only after normalization succeeds.

### Deferred Tool Family

- `get_tables(document_id)`
- `get_table_rows(table_id)`
- `get_cells(table_id)`

### Design Constraint

The wrapper must read normalized records, not raw parser responses.

### Current Status

Completed.

Implemented files:

- `scripts/table_branch_wrapper_lib.py`
- `scripts/test_table_branch_wrapper_lib.py`

## Parallelism Policy

Parallelism is bounded and stage-specific.

- Step 0 may use `xhigh` triage workers
- Steps 1 and 2 should stay narrow and evidence-heavy
- do not run Step 4 in parallel with Step 2 or Step 3

Recommended ceiling:

- triage workers: up to `6`
- parser smoke workers: up to `2`
- normalization worker: `1`
- wrapper implementation worker: `1`

## Non-Goals

- no batch-wide table parser rollout
- no worksheet export promotion
- no row-level RAG activation
- no `get_tables/get_table_rows/get_cells` implementation before normalization success

## One-Line Summary

The bounded table-branch activation slice now reaches consumer-ready read-only lookup: `xhigh triage selection -> PaddleOCR boot smoke -> PP-StructureV3 smoke on 1-2 real PPT images -> canonical normalization -> read-only wrapper implementation -> downstream consumer smoke`.

## Step 5. Downstream Consumer Smoke

### Goal

Use the implemented wrapper against the normalized manifest and confirm that one bounded downstream consumer slice is already viable.

### Required Checks

- `get_tables(document_id)` returns one table summary
- `get_table_rows(table_id)` returns ordered rows
- `get_cells(table_id)` returns flattened lookup cells
- row-chunk projection is derivable from wrapper output
- worksheet-style preview is derivable from wrapper output

### Current Status

Completed.

Artifacts:

- `control/project_domain/resources/manifests/phase0_table_wrapper_consumer_smoke_at2026_03_28.json`
- `control/project_domain/resources/reports/REPORT_phase0_table_wrapper_consumer_smoke-at2026-03-28-09-13.md`
