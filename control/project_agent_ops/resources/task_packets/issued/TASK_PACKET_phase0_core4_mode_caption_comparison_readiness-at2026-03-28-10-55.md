# Task Packet: Phase0 Core 4-Mode Caption Comparison Readiness

## Goal

Make the current master-plan-level `core 4-mode caption comparison` comparison-ready through bounded implementation and smoke evidence.

## Canonical Targets

- [MASTER_PLAN_presentation_image_pipeline.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md)
- [PLAN_codebase_per_image_caption_experiment_comparison-at2026-03-27-16-46.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/master_plans/drafts/PLAN_codebase_per_image_caption_experiment_comparison-at2026-03-27-16-46.md)

## Current State Summary

Already possible:

1. full image baseline
2. OCR-evidence-enriched input

Still incomplete:

3. reviewed isolated-component caption arm
4. parser/table-structure-enriched caption arm

## Required Inputs

- [MASTER_PLAN_presentation_image_pipeline.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md)
- [PLAN_codebase_per_image_caption_experiment_comparison-at2026-03-27-16-46.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/master_plans/drafts/PLAN_codebase_per_image_caption_experiment_comparison-at2026-03-27-16-46.md)
- [SPEC_full_image_standalone_ocr_context_package_baseline.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/specs/prose/SPEC_full_image_standalone_ocr_context_package_baseline.md)
- [REPORT_phase0_imagesorcery_ocr_smoke-at2026-03-27-23-30.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/reports/REPORT_phase0_imagesorcery_ocr_smoke-at2026-03-27-23-30.md)
- [REPORT_phase0_full_image_context_rerun_smoke-at2026-03-28-09-19.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/reports/REPORT_phase0_full_image_context_rerun_smoke-at2026-03-28-09-19.md)
- [REPORT_phase0_table_parser_smoke-at2026-03-28-01-19.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/reports/REPORT_phase0_table_parser_smoke-at2026-03-28-01-19.md)
- [REPORT_phase0_table_parser_comparison-at2026-03-28-10-20.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/reports/REPORT_phase0_table_parser_comparison-at2026-03-28-10-20.md)
- [table_branch_wrapper_lib.py](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/scripts/table_branch_wrapper_lib.py)
- [table_merge_candidate_lib.py](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/scripts/table_merge_candidate_lib.py)

## Required Rules

1. Keep full-image + standalone OCR as the active default baseline.
2. Implement the parser-enriched arm first.
3. Restrict the bounded target to `image11.png`.
4. Do not feed raw parser response directly to caption input. Use normalized or merged candidate artifacts.
5. Parser-enriched context must show:
   - `source_image_path`
   - document or slide provenance
   - table or row/column summary
   - selected text evidence
   - `review_status`
6. Isolated-component arm must use a reviewed component surface only.
7. If isolated-component arm is not clearly better than the original for caption input, close it with explicit waiver instead of forcing implementation.
8. Master plan changes must be append-only.

## Non-Goals

- Do not promote object isolation to unattended default.
- Do not implement the screenshot arm.
- Do not do metadata write-back or rename commit.
- Do not rewrite the master plan broadly.

## Expected Outputs

### Required

- parser-enriched arm smoke report
- parser-enriched manifest or context artifact
- parser-enriched ledger
- isolated-component arm smoke report or waiver report
- 4-mode readiness summary report

### Preferred Filenames

- `control/project_domain/resources/reports/REPORT_phase0_parser_enriched_caption_rerun_smoke-atYYYY-MM-DD-HH-MM.md`
- `control/project_domain/resources/manifests/phase0_parser_enriched_context_manifest_atYYYY_MM_DD.json`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase0_parser_enriched_rerun_image11_atYYYY_MM_DD.json`
- `control/project_domain/resources/reports/REPORT_phase0_isolated_component_caption_arm_waiver-atYYYY-MM-DD-HH-MM.md`
- `control/project_domain/resources/reports/REPORT_phase0_four_mode_caption_readiness-atYYYY-MM-DD-HH-MM.md`

## Allowed Write Surfaces

- `scripts/` bounded helper, adapter, runner, test changes
- `control/project_domain/resources/manifests/`
- `control/project_domain/resources/reports/`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/`
- `domain_artifact_index.json`
- `session_paths.json`

## Done Definition

- parser-enriched arm bounded smoke succeeds on one image.
- isolated-component arm is closed by either success or explicit waiver.
- new JSON passes `json.tool`.
- modified Python passes `py_compile` or tests.
- final report states:
  - ready arm count
  - immediately runnable arms
  - blocked arms
  - block reasons
  - next one step

## Verification

1. Re-read the current truth sources before patching.
2. Verify parser-enriched arm uses normalized or merged artifacts, not raw parser payload.
3. Verify the parser-enriched rerun is comparable in shape to the full-image baseline and OCR-enriched rerun.
4. Verify the isolated-component arm is closed by bounded smoke or waiver.
5. Validate all new JSON with `python3 -m json.tool`.
6. Validate modified Python with `py_compile` or tests.

## Handoff Note

If either remaining arm cannot be promoted safely, close it with explicit waiver evidence rather than leaving the readiness state ambiguous.
