# Table Structure And Text Merge Policy

This document defines the bounded merge policy when two canonical normalized table outputs exist for the same source image:

- Apple helper normalized output
- PaddleOCR normalized output

## Purpose

The two parser families should not be treated as interchangeable truth.

The current workspace evidence supports this split:

- Apple helper is stronger for structure and clean cell grouping
- PaddleOCR remains the active parser path
- OCR text still needs explicit repair and review rules

## Current Evidence Base

- `control/project_domain/resources/manifests/phase0_paddleocr_table_parse_normalized_at2026_03_28.json`
- `control/project_domain/resources/manifests/phase0_apple_document_structure_normalized_at2026_03_28.json`
- `control/project_domain/resources/manifests/phase0_table_parser_comparison_at2026_03_28.json`

## Boundary

This is a bounded policy for:

- one shared source image
- one Apple normalized table
- one Paddle normalized table
- one later review or merge candidate

This is not yet a batch-wide auto-merge rule.

## Policy

### Structure Source

If both normalized outputs agree on:

- `document_id`
- `page`
- `table_id`
- row count
- column count
- cell count

then use the Apple helper as the preferred structure source for:

- grid skeleton
- row and column alignment
- span interpretation

If those fields drift, do not auto-merge. Send the table to review.

### Text Source

Text is handled per cell, not per table.

Use these ordered rules:

1. if one parser is empty and the other is non-empty, prefer the non-empty text
2. if both texts normalize to the same value after spacing or numeric formatting cleanup, prefer the cleaner normalized text
3. if both texts contain the same digits but only one preserves the decimal pattern, prefer the decimal-bearing candidate but keep it reviewable
4. if header labels or lexical tokens conflict materially, do not auto-merge; send the cell to review

### Review Priority

These cells remain review targets:

- numbers
- percentages
- scores
- identifiers
- header cells with alpha or alphanumeric substitution drift

## Current Practical Reading

On `image11.png`, the current comparison shows:

- shared structure compatibility
- one header conflict:
  - `65Q` vs `650`
- four repairable text differences:
  - `0.757` vs `0 757`
  - `0.622` vs `.622`
  - `0.670` vs `[blank]`
  - `0.554` vs `554`

This supports the current bounded interpretation:

- Apple helper is strong enough to guide structure
- PaddleOCR alone is not sufficient as text truth
- merged text still needs cell-level review gates

## Output Interpretation

Any future merged candidate should preserve:

- `structure_source`
- `text_source`
- `review_status`
- original Apple text candidate
- original Paddle text candidate

Do not discard source-specific evidence when creating a merged candidate.
