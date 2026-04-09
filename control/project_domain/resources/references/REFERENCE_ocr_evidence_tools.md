# OCR Evidence Tool Reference

## Purpose

Summarize the OCR surfaces that complement object isolation and caption review in this workspace.

This document is reference-only.

## Preferred MCP Surface: macos-ocr-mcp

Workspace-local source:

- `vendor/mcp/macos-ocr-mcp`

Launcher:

- `scripts/mcp/start-macos-ocr-mcp.sh`

Surface:

- `ocr_image(file_path)`

Observed utility:

- runs OCR on a local image file
- returns per-annotation text
- returns confidence
- returns bounding boxes

Practical fit:

- OCR evidence on PPT-extracted media assets
- OCR evidence on isolated-object cutouts
- text grounding for charts, UI screenshots, and table-like images

Observed activation status in this workspace:

- usable when executed unsandboxed
- sandboxed execution can fail in the `ocrmac` path and should not be treated as a final no-text verdict
- the vendored wrapper now includes a local Swift Vision fallback path for `ocrmac` failure cases
- current phase0 smoke indicates that full-image standalone OCR is more reliable than OCR on automatically isolated crops for the tested PPT assets

## Complementary CLI Surface: macOCR

Workspace-local source:

- `vendor/ocr/macOCR`

Upstream:

- <https://github.com/schappim/macOCR>

Observed utility from the upstream README:

- interactive region OCR on screen
- `--input <file>` OCR on an existing image file
- `--rect <x,y,w,h>` for scripting a screen region
- `--language` and `--list-languages` for OCR language control

Practical fit:

- fallback when MCP is unavailable
- manual debugging for OCR disagreements
- quick comparison between file OCR and screen-region OCR

Current workspace status:

- reference-only
- global `ocr` binary is not installed
- vendored Xcode project build is not yet clean enough to treat as an active runtime path

## Planned Helper Surface: Apple Vision Document Structure

Decision:

- do not introduce a separate workspace MCP for this path first
- treat Apple Vision document recognition as a local helper script invoked from existing agent skills

Intended role:

- recover table skeleton hints
- recover table bbox, row count, column count, and span hints
- provide per-cell transcript or line candidates when available

Boundary:

- helper sidecar only
- not a final canonical table artifact
- must still flow through canonical normalization before any `get_tables`, `get_table_rows`, or `get_cells` consumer reads it

Preferred integration points:

- `skills/macos-ocr-evidence`
- `skills/parser-sidecar-to-canonical-schema-promotion`

## Recommended Order

1. Use `macos-ocr-mcp` first on the full original PPT-extracted image.
2. If object isolation is attempted, treat OCR on the isolated crop as a secondary comparison surface, not the new default truth source.
3. If OCR is required inside a constrained run surface, rerun unsandboxed before concluding there is no usable text.
4. For table-like images where structure matters more than raw OCR text, prefer `paddleocr-mcp` as the active parser and treat Apple Vision document recognition as a helper-script sidecar only.
5. Use `macOCR` only as a reference or future comparison path until the CLI is explicitly activated in this workspace.

## Current Workspace Decision

The current decision after phase0 smoke is:

- `full image + standalone OCR` is the immediate baseline for the next caption-context package
- automatically isolated crops are not yet trustworthy enough to replace the full-image baseline
- object-level OCR should be used only on reviewed or obviously well-bounded candidates
- Apple Vision document recognition, if added, should be integrated into existing skills as a helper script rather than as a first-class MCP

## Not Owned Here

- object isolation preprocessing
- caption generation
- caption approval
- metadata write-back
