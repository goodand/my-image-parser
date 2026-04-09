# Phase 0 Reviewed Isolated-Component Caption Rerun Smoke

## Purpose

Re-open the isolated-component arm on `image11.png`, create a reviewed component surface that is actually better than the full image for table-focused caption input, and verify one bounded rerun end to end.

## Inputs

- source image:
  - `control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image11.png`
- bounded full-image context package:
  - `control/project_domain/resources/context_packages/full_image_ocr_baseline/01_full_presentation_2026-03-17/image11/CONTEXT_PACKAGE.json`
- merged reviewed table candidate:
  - `control/project_domain/resources/manifests/phase0_table_merge_candidate_at2026_03_28.json`
- reviewed component builder:
  - `scripts/reviewed_component_context_package_lib.py`
  - `scripts/build_reviewed_component_context_package.py`
- caption runner:
  - `scripts/caption_images_openai.py`
  - `scripts/caption_runner_lib.py`

## Produced Artifacts

- reviewed component image:
  - `control/project_domain/resources/context_packages/reviewed_isolated_component/01_full_presentation_2026-03-17/image11/REVIEWED_COMPONENT.png`
- reviewed component context package:
  - `control/project_domain/resources/context_packages/reviewed_isolated_component/01_full_presentation_2026-03-17/image11/CONTEXT_PACKAGE.json`
- reviewed component context markdown:
  - `control/project_domain/resources/context_packages/reviewed_isolated_component/01_full_presentation_2026-03-17/image11/CONTEXT_PACKAGE.md`
- reviewed component manifest:
  - `control/project_domain/resources/manifests/phase0_reviewed_isolated_component_context_manifest_at2026_03_28.json`
- reviewed component dataset row:
  - `control/project_domain/resources/manifests/phase0_reviewed_isolated_component_dataset_image11_at2026_03_28.jsonl`
- bounded rerun ledger:
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase0_reviewed_isolated_component_rerun_image11_at2026_03_28.json`

## Reviewed Component Evidence

- component kind: `reviewed_table_component`
- component bbox: `[6, 64, 511, 307]`
- crop OCR status: `usable`
- crop OCR annotation_count: `16`
- context review_status: `reviewed_candidate`
- context_variant: `reviewed_isolated_component`

Comparison against the full-image OCR evidence:

- expected table-token coverage:
  - full image: `16 / 16`
  - reviewed component: `16 / 16`
- extraneous token count:
  - full image: `7`
  - reviewed component: `0`
- reviewed component better for caption input: `true`

Extraneous full-image OCR tokens removed by the reviewed component surface:

- `Two-Phase`
- `Hyde-PC`
- `fr`
- `52`
- `00`
- `9`
- `0`

This means the reviewed component preserves the same table coverage while removing non-table noise from the OCR evidence.

## Result

- rerun status: `completed`
- model: `gpt-4.1`
- prompt_version: `openai-gpt-4.1-caption-context-v1`
- context_variant: `reviewed_isolated_component`
- source image for rerun:
  - `control/project_domain/resources/context_packages/reviewed_isolated_component/01_full_presentation_2026-03-17/image11/REVIEWED_COMPONENT.png`

Observed caption:

- `A table compares three metrics (DH@10, MRR, CR@10) across two columns (70Q and 65Q) and shows the differences (Delta). The 65Q column has higher values for all metrics.`

Observed alt text:

- `Table of DH@10, MRR, and CR@10 for 70Q and 65Q with corresponding Delta values.`

## Interpretation

- this is not a raw alpha component
- this is a reviewed table crop derived from merged table structure evidence
- the crop OCR is cleaner than the full-image OCR for the table-only reading task
- the caption rerun succeeds on the reviewed component surface without changing the caption runner contract

## Boundary

This smoke does not mean:

- isolated components become the default baseline
- unattended object isolation is now allowed
- every reviewed crop will outperform the full image

It does mean:

- the isolated-component arm is now closed at bounded smoke level on one shared image
- the previous waiver is superseded for `image11.png`
- this arm is comparison-ready as a reviewed branch
