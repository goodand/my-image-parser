# Phase 1 Image4 Edge-Case Direct Read And Recrop Status

## Purpose

Record a direct visual read of `image4.png` after the new multi-component reviewed-crop recrop logic was added, and restate the current bounded interpretation without reopening the full experiment plan.

## Input

- source image:
  - `<LOCAL_PPTX_JOBS_ROOT>/01_full_presentation_2026-03-17/media/image4.png`
- current small-batch readiness:
  - `./REPORT_phase1_caption_four_mode_small_batch_readiness-at2026-03-28-14-10.md`
- current candidate manifest:
  - `../manifests/phase1_caption_four_mode_small_batch_candidates_at2026_03_28.json`
- reviewed recrop implementation:
  - `../../../../scripts/reviewed_component_context_package_lib.py`

## Direct Read

`image4.png` is not a simple table image.

It is a composite overview slide with:
- four bar-chart panels
  - `DocHit@10`
  - `MRR`
  - `ChunkRecall@10`
  - `ChunkF1@10`
- one smaller embedded structure metrics table
- a title-level summary surface: `Answerable-45 Merged Metrics Overview`

## Current Interpretation

- The existing exclusion reason `mixed_chart_table_edge_case_and_no_frozen_derived_arms` remains semantically correct.
- The new reviewed-component recrop logic improves one specific failure mode:
  - seed bbox too narrow
  - nearby disconnected alpha components should stay with the main crop
- But this does **not** by itself prove that `image4` should immediately re-enter the stable `phase1` cohort.

Why not:
- `image4` is a multi-panel analytical figure, not a table-only figure
- a bounded recrop may improve the embedded table crop, while still losing the whole-dashboard meaning
- the correct comparison surface may still depend on whether the experiment wants:
  - the whole overview
  - the embedded metrics table
  - or one chart-table mixed subregion

## Recrop Status

The codebase now has bounded reviewed-component candidate selection for multi-component images:
- `seed_bbox`
- `alpha_nearby_union`

That means the workspace can now test whether a reviewed crop was under-cropped because nearby alpha components were omitted.

What is still unresolved for `image4`:
- whether a better reviewed crop is sufficient for the experiment goal
- whether parser/reviewed derived arms still preserve the dashboard-level semantics
- whether `image4` should stay excluded even after recrop because the image is structurally multi-panel

## Current Decision

- direct visual read performed: `yes`
- current exclusion immediately overturned: `no`
- current safe interpretation: keep `image4` excluded until the bounded re-entry slice runs
- current operational rule: treat `image4` decomposition as a research-lane slice, not as a blocker for the current stable phase1 mainline
- recommended next step: use the issued packet
  - `../../../project_agent_ops/resources/task_packets/issued/TASK_PACKET_phase1_image4_multi_component_recrop_reentry_slice-at2026-03-30.md`

## Recording Status

Experiment evidence is being recorded.

Current recording surfaces include:
- canonical reports under `control/project_domain/resources/reports/`
- canonical manifests under `control/project_domain/resources/manifests/`
- repeated task/issue promotion under `control/project_agent_ops/resources/skill_candidates/`

The recrop reinforcement work for this edge case has also been logged into repeated-pattern buckets:
- `TASK_multi_component_reviewed_crop_recrop_candidate_selection.md`
- `ISSUE_seed_bbox_only_reviewed_crop_truncation_on_multi_component_images.md`

## One-Line Summary

`image4` was directly re-read and remains a real composite edge case; the new recrop logic is now available for a bounded re-entry test, but the direct read alone is not enough to promote it back into the stable cohort.
