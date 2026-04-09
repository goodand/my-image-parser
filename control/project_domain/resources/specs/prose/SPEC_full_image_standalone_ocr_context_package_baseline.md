# Full-Image Standalone OCR Context Package Baseline

This document defines the current next-step baseline for caption-context preparation after the phase0 ImageSorcery + OCR smoke.

It is a baseline spec, not a completed run report.

This workspace now includes a builder script at:

- `scripts/build_full_image_ocr_context_package.py`

It writes one context package per image and maintains a manifest row for later caption reruns.

## Current Decision

The current workspace decision is:

- use the full original PPT-extracted image as the primary image surface
- use standalone OCR on that full image as the primary text-evidence surface
- build one reviewed context package per image from OCR evidence plus PPT-local summary
- do not promote automatic object isolation into unattended batch preprocessing yet

This decision is grounded in:

- `REPORT_phase0_imagesorcery_ocr_smoke-at2026-03-27-23-30.md`
- `phase0_imagesorcery_ocr_smoke_summary_at2026_03_27.json`

## Why This Baseline Exists

Phase0 smoke showed that:

- promptable `find()` did not return usable semantic matches on the tested PPT assets
- generic `detect()` fallback could produce semantically wrong crops
- full-image standalone OCR produced more useful text evidence than OCR on automatically isolated outputs

Therefore the workspace should treat `full-image + standalone OCR` as the immediate context baseline for the next caption rerun.

## Baseline Flow

The baseline flow is:

1. start from one PPT-extracted image
2. run standalone OCR on the full original image
3. collect OCR evidence and a no-text or weak-text decision when needed
4. merge OCR evidence with PPT-local summary or nearby slide context
5. produce one reviewed context package artifact for later caption injection
6. rerun caption generation only after the context package is accepted

## Canonical Inputs

- extracted image set:
  - `control/project_domain/resources/assets/caption_experiment/extracted_media/01_full_presentation_2026-03-17`
  - `control/project_domain/resources/assets/caption_experiment/extracted_media/02_1`
- extracted-image run artifacts:
  - `control/project_domain/resources/pptx_jobs/`
- OCR runtime reference:
  - `control/project_domain/resources/references/REFERENCE_ocr_evidence_tools.md`
- experiment foundation:
  - `control/project_domain/resources/knowledge_bases/KB_caption_experiment_foundation.md`

## Primary OCR Surface

Preferred OCR surface:

- `macos-ocr-mcp`

Current interpretation:

- run OCR on the full original image first
- treat isolated-object OCR as a comparison-only or review-gated branch
- rerun unsandboxed before concluding that a full image has no usable text

## Context Package Purpose

The context package is the bounded text-and-source bundle that will later be injected into a caption rerun or caption review surface.

Its job is to preserve useful text evidence without forcing the next stage to re-open all OCR artifacts manually.

## Required Output Fields

Each context-package row should carry at least:

- `image_id`
- `source_image_path`
- `source_dataset`
- `source_pptx`
- `source_slide_numbers`
- `image_surface`
- `ocr_surface`
- `ocr_status`
- `ocr_engine`
- `ocr_annotation_count`
- `ocr_text_excerpt`
- `ocr_text_full_path`
- `ppt_local_summary`
- `context_package_markdown_path`
- `context_package_json_path`
- `review_status`
- `notes`

## Field Meaning

- `image_surface`
  - expected current value: `full_image_original`
- `ocr_surface`
  - expected current value: `full_image_standalone_ocr`
- `ocr_status`
  - `usable`, `weak_text`, `no_text`, or `error`
- `ppt_local_summary`
  - short summary from slide-local or PPT-local context that helps caption rerun interpret the image
- `review_status`
  - `pending_review`, `accepted`, `needs_more_context`, or `rejected`

## Recommended Output Layout

Raw baseline outputs should stay under `runs/`.

Recommended layout:

- `control/project_domain/resources/context_packages/full_image_ocr_baseline/`
- `control/project_domain/resources/context_packages/full_image_ocr_baseline/<dataset>/<image_id>/CONTEXT_PACKAGE.md`
- `control/project_domain/resources/context_packages/full_image_ocr_baseline/<dataset>/<image_id>/CONTEXT_PACKAGE.json`
- `control/project_domain/resources/manifests/phase0_full_image_ocr_context_package_manifest.jsonl`
- `control/project_domain/resources/reports/REPORT_phase0_full_image_ocr_context_package_baseline-atYYYY-MM-DD-HH-MM.md`

If a later experiment promotes this baseline into an active reusable asset family, only then should a promoted derivative move into `resources/`.

## Review Rules

The context package should be reviewed before caption rerun when:

- OCR output is long, noisy, or obviously duplicated
- OCR text conflicts with the visible chart, table, or UI semantics
- the image appears to contain multiple semantic regions
- surrounding PPT-local context is required to interpret abbreviations or metric names

The context package can move forward faster when:

- OCR is short and clearly aligned with the visible image
- slide context is obvious from the extracted image itself
- there is no unresolved ambiguity about what the image depicts

## Non-Goals

This baseline does not own:

- automatic object isolation fanout
- crop or mask promotion as the new default image surface
- metadata write-back
- rename commit
- final multi-arm comparison

## Promotion Gate

Use this baseline as the next caption-context source unless a later reviewed branch can show all of the following:

1. isolated crops are semantically aligned with the intended object
2. isolated or cropped OCR is at least neutral relative to full-image OCR on the promoted cases
3. the reviewed isolated surface is easier to caption than the full-image baseline
4. promotion criteria are recorded in a bounded report or manifest

Until then, `full-image + standalone OCR` remains the safer default baseline.

## Example Operational Ordering

The current preferred ordering is:

1. PPT-extracted image
2. full-image standalone OCR
3. reviewed context package
4. caption rerun with context injection
5. optional evaluation overlay

Object isolation remains available only as a reviewed branch after this baseline, not before it.

## Source Basis

- `control/project_domain/resources/reports/REPORT_phase0_imagesorcery_ocr_smoke-at2026-03-27-23-30.md`
- `control/project_domain/resources/manifests/phase0_imagesorcery_ocr_smoke_summary_at2026_03_27.json`
- `control/project_domain/resources/references/REFERENCE_object_isolation_tools.md`
- `control/project_domain/resources/references/REFERENCE_ocr_evidence_tools.md`
- `control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md`
