# Phase 0 Apple Document Structure Helper Smoke Report

## Purpose

Record the first bounded `RecognizeDocumentsRequest` helper execution on a real PPT-extracted image and the first successful promotion of that helper-sidecar into the canonical `Table -> Row -> Cell` schema.

## Inputs

- helper script:
  - `skills/parser-sidecar-to-canonical-schema-promotion/scripts/macos_table_structure_helper.swift`
- promotion entrypoint:
  - `scripts/promote_parser_sidecar_to_canonical_schema.py`
- selected image:
  - `control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image11.png`

## Produced Artifacts

- smoke summary:
  - `control/project_domain/resources/manifests/phase0_apple_document_structure_smoke_at2026_03_28.json`
- raw Apple helper sidecar:
  - `control/project_domain/resources/manifests/phase0_apple_document_structure_raw_at2026_03_28.json`
- promotion result:
  - `control/project_domain/resources/manifests/phase0_apple_document_structure_promotion_at2026_03_28.json`
- normalized canonical table:
  - `control/project_domain/resources/manifests/phase0_apple_document_structure_normalized_at2026_03_28.json`

## Verified

- the helper compiled and executed under local Xcode and Swift
- `RecognizeDocumentsRequest` returned:
  - `table_count = 1`
  - `cell_count = 16`
- the same promotion entrypoint used for parser sidecars also accepted the Apple helper output
- provenance was recovered through the PPT extraction manifest:
  - `document_id = 01_full_presentation_2026-03-17`
  - `slide = 24`
- the normalized output produced:
  - `table_id = t1`
  - `row_count = 4`
  - `column_count = 4`
  - `parser_backend = apple_vision_recognize_documents_request`

## Practical Reading

The promoted table grid is:

- `Metric | 70Q | 65Q | Delta`
- `DH@10 | 0.757 | 0.815 | +0.058`
- `MRR | 0.622 | 0.670 | +0.048`
- `CR@10 | 0.514 | 0.554 | +0.040`

## Interpretation

This closes the gap between:

- Apple Vision as a local table-structure helper
- the existing parser-sidecar promotion pipeline
- the current read-only wrapper surface

The helper is now runnable and promotable, but it remains a helper-sidecar path.

This does not mean:

- Apple helper replaces `paddleocr-mcp` as the primary parser
- Apple helper text should be treated as final cell truth
- the helper is exposed as a standalone MCP

It does mean:

- Apple structure hints can be generated locally
- they can be lifted into the same canonical schema used by downstream consumers
- future comparison or merge logic can treat Apple as `structure-first`, Paddle as `parser-first`, and OCR as `text-evidence`

## Next Step

The next bounded Apple-side action is one of:

1. compare Apple helper normalized output against the existing Paddle normalized output for the same image
2. add a merge policy that prefers Apple for grid skeleton and OCR/Paddle for cell text repair
3. run one more bounded smoke on a second triage-approved table image before any wider rollout
