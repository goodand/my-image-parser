# Phase 0 Four-Mode Caption Readiness

## Purpose

Record whether the current workspace is ready to start the intended core 4-mode caption comparison.

## Truth Sources

- `control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md`
- `control/project_domain/resources/master_plans/drafts/PLAN_codebase_per_image_caption_experiment_comparison-at2026-03-27-16-46.md`
- `control/project_domain/resources/specs/prose/SPEC_full_image_standalone_ocr_context_package_baseline.md`
- `control/project_domain/resources/reports/REPORT_phase0_imagesorcery_ocr_smoke-at2026-03-27-23-30.md`
- `control/project_domain/resources/reports/REPORT_phase0_full_image_context_rerun_smoke-at2026-03-28-09-19.md`
- `control/project_domain/resources/reports/REPORT_phase0_parser_enriched_caption_rerun_smoke-at2026-03-28-11-08.md`
- `control/project_domain/resources/reports/REPORT_phase0_isolated_component_caption_arm_waiver-at2026-03-28-11-08.md`

## Ready Count

- ready arms: `3 / 4`

## Immediately Runnable Arms

1. `full_image_baseline`
   - status: `ready`
   - evidence:
     - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w1.json`
2. `full_image_ocr_context_rerun`
   - status: `ready_for_comparison`
   - evidence:
     - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase0_full_image_context_rerun_image11_at2026_03_28.json`
   - note:
     - still `pending_review`, so comparison-ready but not default-ready
3. `parser_table_enriched_rerun`
   - status: `ready_for_comparison`
   - evidence:
     - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase0_parser_enriched_rerun_image11_at2026_03_28.json`
   - note:
     - still `pending_review`, so comparison-ready but not default-ready

## Blocked Arms

1. `reviewed_isolated_component_caption_arm`
   - status: `blocked_by_explicit_waiver`
   - evidence:
     - `control/project_domain/resources/reports/REPORT_phase0_isolated_component_caption_arm_waiver-at2026-03-28-11-08.md`
   - block reason:
     - current isolated component surfaces are not better than the full original image on the target image

## Readiness Verdict

Final answer:

- `No`

The workspace is **not** ready to start the intended 4-mode comparison immediately because one of the four intended arms is still blocked and has been waived rather than implemented.

## Interpretation

What *is* ready right now:

- a bounded `3-mode` comparison on the shared source image
  - full image baseline
  - OCR-enriched rerun
  - parser-enriched rerun

What is *not* ready right now:

- the isolated-component arm as a fair comparison peer

## Next One Step

Choose one of the following:

1. start a bounded `3-mode` comparison now using the three ready arms
2. keep the `4-mode` framing, but do not execute it until a reviewed isolated-component candidate proves better than the full-image baseline on one shared image

