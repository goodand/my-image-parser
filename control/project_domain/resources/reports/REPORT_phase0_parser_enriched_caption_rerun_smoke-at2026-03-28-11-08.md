# Phase 0 Parser-Enriched Caption Rerun Smoke

## Purpose

Run one bounded parser-enriched caption rerun on top of the existing `full-image + standalone OCR` context package surface and verify that the parser/table branch is now mechanically comparison-ready on one real PPT-derived image.

## Inputs

- source image:
  - `control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image11.png`
- bounded OCR baseline package:
  - `control/project_domain/resources/context_packages/full_image_ocr_baseline/01_full_presentation_2026-03-17/image11/CONTEXT_PACKAGE.json`
- merged table candidate:
  - `control/project_domain/resources/manifests/phase0_table_merge_candidate_at2026_03_28.json`
- parser-enriched adapter:
  - `scripts/parser_enriched_context_package_lib.py`
  - `scripts/build_parser_enriched_context_package.py`
- caption runner:
  - `scripts/caption_images_openai.py`
  - `scripts/caption_runner_lib.py`

## Produced Artifacts

- parser-enriched context package:
  - `control/project_domain/resources/context_packages/parser_enriched_table_baseline/01_full_presentation_2026-03-17/image11/CONTEXT_PACKAGE.json`
- parser-enriched context markdown:
  - `control/project_domain/resources/context_packages/parser_enriched_table_baseline/01_full_presentation_2026-03-17/image11/CONTEXT_PACKAGE.md`
- parser-enriched context manifest:
  - `control/project_domain/resources/manifests/phase0_parser_enriched_context_manifest_at2026_03_28.json`
- bounded rerun ledger:
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase0_parser_enriched_rerun_image11_at2026_03_28.json`
- execution sidecar:
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase0_parser_enriched_rerun_image11_at2026_03_28_execution_records.jsonl`
- evaluation sidecar:
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase0_parser_enriched_rerun_image11_at2026_03_28_evaluation_decisions.jsonl`

## Result

- rerun status: `completed`
- model: `gpt-4.1`
- prompt_version: `openai-gpt-4.1-caption-context-v1`
- context_variant: `parser_table_enriched`
- context review_status: `pending_review`
- source_image_path preserved: `true`
- parser document_id: `01_full_presentation_2026-03-17`
- parser table_id: `t1`
- parser page: `24`
- parser pending_review_count: `10`

Observed caption:

- `A table compares DH@10, MRR, and CR@10 metrics for 70Q and 65Q under the Two-Phase Hyde-PC condition, showing the delta for each metric.`

Observed alt text:

- `Table comparing DH@10, MRR, CR@10 metrics for 70Q and 65Q with deltas.`

## Shape Comparability

The parser-enriched rerun is shape-compatible with the already-closed arms.

- same source image as the phase1 baseline:
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w1.json`
- same source image as the OCR-enriched rerun:
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase0_full_image_context_rerun_image11_at2026_03_28.json`
- same top-level ledger family:
  - `job_id`
  - `created_at`
  - `updated_at`
  - `model`
  - `prompt_version`
  - `records`
- same per-record contract as the OCR-enriched rerun:
  - `source_context`
  - `context_package`
  - `caption`
  - `alt_text`
  - `structured_metadata`
  - `raw_response_path`
- bounded parser-specific additions stayed inside `context_package`:
  - `context_variant`
  - `table_summary`
  - `selected_text_evidence`
  - `parser_enrichment`

This means the parser/table branch is now mechanically usable as a comparison arm without changing the caption runner contract.

## Interpretation

- parser/table structure evidence can be adapted into the existing `context_package` surface
- the runner accepts that surface end to end on `image11.png`
- this arm is comparison-ready as bounded evidence
- this arm is not yet default-ready because the parser-enriched context package remains `pending_review`

## Boundary

This smoke does not mean:

- raw parser output should be injected directly into captioning
- numeric or header-sensitive cells may bypass review
- parser-enriched reruns should replace the OCR baseline automatically

It does mean:

- the parser-enriched caption arm is now closed at bounded smoke level
- it can be compared against the full-image baseline and OCR-enriched rerun on one shared image

