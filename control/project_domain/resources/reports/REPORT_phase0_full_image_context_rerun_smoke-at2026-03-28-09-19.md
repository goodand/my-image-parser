# Phase 0 Full-Image Context Rerun Smoke

## Purpose

Run one bounded caption rerun on top of the `full-image + standalone OCR` context baseline and record whether the runner accepts the injected context package end to end.

This is a smoke, not a promotion decision.

## Inputs

- source image:
  - `control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image11.png`
- context package manifest:
  - `control/project_domain/resources/manifests/phase0_full_image_ocr_context_package_manifest.jsonl`
- context package:
  - `control/project_domain/resources/context_packages/full_image_ocr_baseline/01_full_presentation_2026-03-17/image11/CONTEXT_PACKAGE.json`
- rerun ledger:
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase0_full_image_context_rerun_image11_at2026_03_28.json`

## Baseline Versus Rerun

Baseline phase1 caption:

- `A table shows the performance metrics DH@10, MRR, and CR@10 for 70Q and 65Q in the Two-Phase Hyde-PC test, including delta comparisons.`

Context-injected rerun caption:

- `This image shows a table comparing metrics for 'Two-Phase Hyde-PC' on '70Q' and '65Q' scenarios, with delta values for each metric. The metrics include DH@10, MRR, and CR@10, with 65Q values generally higher than 70Q.`

## Result

- rerun status: `completed`
- model: `gpt-4.1`
- context package `review_status`: `pending_review`
- OCR status inside package: `usable`
- OCR annotation count: `18`

## Interpretation

The context-injection path is mechanically valid:

- the runner loaded the context package
- the request completed successfully
- the ledger persisted the embedded `context_package`

The semantic change is modest but directionally useful:

- the rerun makes the `65Q > 70Q` relationship explicit
- the visible title and table role remain preserved

## Boundary

This rerun should not yet be treated as the new canonical caption baseline because the context package is still `pending_review`.

It is only bounded evidence that:

- the current context-package contract is compatible with the caption runner
- the rerun path can complete on a real PPT-derived table image

## Next Step

The next correct action is:

1. review and accept or revise the current context package
2. only then decide whether the context-enriched rerun should replace the phase1 baseline for this image class

