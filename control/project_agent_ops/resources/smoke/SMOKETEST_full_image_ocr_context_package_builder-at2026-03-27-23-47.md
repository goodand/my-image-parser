# Full-Image OCR Context Package Builder Smoke

## Purpose

Verify that the new full-image standalone OCR context-package builder can:

- resolve PPT extraction metadata for one real image
- generate markdown and JSON context-package artifacts
- maintain a manifest row
- confirm the already-known sandbox versus unsandboxed OCR behavior

## Script Surface

- script:
  - `scripts/build_full_image_ocr_context_package.py`
- helper library:
  - `scripts/full_image_ocr_context_package_lib.py`
- fixture test:
  - `scripts/test_full_image_ocr_context_package_lib.py`

## Static Verification

- fixture test command:
  - `python3 scripts/test_full_image_ocr_context_package_lib.py`
- result:
  - `OK`
- builder `--help` command:
  - `python3 scripts/build_full_image_ocr_context_package.py --help`
- result:
  - argument surface printed successfully

## Live Smoke Input

- image:
  - `control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image11.png`
- expected semantic type:
  - full-image table OCR candidate

## Sandboxed Run

- output root:
  - `/private/tmp/full-image-ocr-context-smoke`
- observed result:
  - builder completed structurally
  - `ocr_status = error`
  - `review_status = rejected`
- OCR failure:
  - `Fallback OCR failed: {"error":"The operation couldn’t be completed. (Foundation._GenericObjCError error 0.)"}`

Interpretation:

- this reproduces the already-known sandbox OCR failure pattern
- the builder is still useful because it preserves the failed package surface and notes, but the OCR result itself should not be treated as final in sandbox

## Unsandboxed Run

- output root:
  - `/private/tmp/full-image-ocr-context-smoke-unsandboxed`
- manifest:
  - `/private/tmp/full-image-ocr-context-smoke-unsandboxed/manifest.jsonl`
- context package:
  - `/private/tmp/full-image-ocr-context-smoke-unsandboxed/01_full_presentation_2026-03-17/image11/CONTEXT_PACKAGE.md`
- OCR result:
  - `/private/tmp/full-image-ocr-context-smoke-unsandboxed/01_full_presentation_2026-03-17/image11/OCR_RESULT.json`

Observed result:

- `image_id = 01_full_presentation_2026-03-17:image11.png`
- `ocr_status = usable`
- `review_status = pending_review`
- `ocr_engine = ocrmac`
- `ocr_annotation_count = 18`

Observed package qualities:

- PPT extraction manifest was resolved correctly
- source slide number `24` was carried into the package
- existing phase-1 caption and alt text were carried into the summary surface
- markdown, JSON, OCR raw JSON, OCR full text, and manifest row were all written

## Conclusion

- the new builder is structurally valid and reusable
- reliable OCR execution still requires the known unsandboxed path
- the script is suitable for the `full-image + standalone OCR` baseline workflow
- object isolation remains separate and review-gated; this builder should be used on the full original PPT-extracted image first
