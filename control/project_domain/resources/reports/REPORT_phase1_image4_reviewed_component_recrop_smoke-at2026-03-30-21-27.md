# Phase1 Image4 Reviewed Component Recrop Smoke

## Scope

- packet: `TASK_PACKET_phase1_image4_multi_component_recrop_reentry_slice-at2026-03-30.md`
- source image: `control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image4.png`
- bounded goal: determine whether the new multi-component recrop path can reopen `image4` for a stable per-image `4-mode` bundle

## Deterministic Attempts

### 1. Full-image OCR context

- command surface: `python3 scripts/build_full_image_ocr_context_package.py`
- scratch output root: `/private/tmp/image4_full_image_ocr_context`
- result:
  - `ocr_status = usable`
  - `review_status = pending_review`
  - `ocr_engine = ocrmac`
  - `ocr_annotation_count = 73`

Interpretation:

- the image is readable enough for OCR-backed context
- this closes only the `full_image_ocr_context_rerun` prerequisite, not the parser/reviewed prerequisites

### 2. Paddle parser single-source probe

- command surface: `vendor/mcp/paddleocr-mcp/.venv/bin/python scripts/run_paddleocr_mcp_boot_smoke.py`
- output json: `/private/tmp/image4_paddle_smoke.json`
- normalized output: `/private/tmp/image4_paddle_normalized.json`
- result:
  - `status = completed`
  - `tool_names = [pp_structurev3]`
  - `normalized_status = no_table_found`
  - `slide = 18`

Interpretation:

- the bounded parser path did not yield a stable table-normalized surface for `image4`
- this blocks single-source candidate creation for `parser_table_enriched_rerun`

### 3. Reviewed multi-component recrop entry

- current recrop logic requires a merged candidate seed bbox from table cells
- no stable parser-normalized table was produced in step 2
- therefore reviewed recrop could not enter its bounded crop-selection phase

Interpretation:

- the new recrop logic itself was not disproven
- `image4` is blocked earlier because no stable table seed exists for the reviewed branch

### 4. Apple document-structure helper fallback

- command surface: `xcrun swift skills/parser-sidecar-to-canonical-schema-promotion/scripts/macos_table_structure_helper.swift`
- expected raw output: `/tmp/image4_apple_helper_raw.json`
- observed result:
  - no helper JSON emitted within the bounded observation window
  - no `/tmp/image4_apple_helper_raw.json` was produced in that window
  - the helper left long-lived `swift-frontend` and `vision_document_runner` processes until manual cleanup

Interpretation:

- the Apple helper did not provide a stable fallback sidecar for `image4`
- this means there is still no deterministic Apple-normalized route that can unlock parser-enriched or reviewed-component closure in this slice

## Outcome

- `image4` remains blocked for:
  - `parser_table_enriched_rerun`
  - `reviewed_isolated_component_rerun`
- no new GPT tie-break was needed because deterministic evidence was sufficient to preserve exclusion

## Next One Step

- only revisit `image4` if a new deterministic parser path can first produce a stable table seed bbox
