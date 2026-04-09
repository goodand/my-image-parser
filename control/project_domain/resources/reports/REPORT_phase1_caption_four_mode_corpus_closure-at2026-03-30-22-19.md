# Phase 1 Caption Four-Mode Corpus Closure

## Purpose

Close the current corpus-wide `4-mode` expansion after the non-edge-case table-centric images were frozen and record the canonical producer truth, consumer truth, and explicit exclusion set for downstream use.

## Canonical Inputs

- candidates:
  - `control/project_domain/resources/manifests/phase1_caption_four_mode_corpus_candidates_at2026_03_29.json`
- ready bundle:
  - `control/project_domain/resources/manifests/phase1_caption_four_mode_corpus_ready_bundle_at2026_03_29.json`
- excluded set:
  - `control/project_domain/resources/manifests/phase1_caption_four_mode_corpus_excluded_at2026_03_29.json`
- corpus scan report:
  - `control/project_domain/resources/reports/REPORT_phase1_caption_four_mode_corpus_scan-at2026-03-29-00-55.md`
- corpus auto-eval manifest:
  - `control/project_domain/resources/manifests/phase1_caption_four_mode_corpus_auto_eval_true_batch_at2026_03_30.json`
- corpus auto-eval report:
  - `control/project_domain/resources/reports/REPORT_phase1_caption_four_mode_corpus_auto_eval_true_batch-at2026-03-30-22-20.md`
- semantic judge waiver:
  - `control/project_domain/resources/reports/REPORT_phase1_caption_four_mode_corpus_semantic_judge_waiver-at2026-03-30-22-20.md`
- image4 re-entry waiver:
  - `control/project_domain/resources/reports/REPORT_phase1_image4_four_mode_reentry_waiver-at2026-03-30-21-27.md`

## Producer Closure

- stable ready image ids:
  - `image7`
  - `image8`
  - `image9`
  - `image10`
  - `image11`
  - `image12`
  - `image13`
  - `image14`
  - `image15`
- excluded image ids:
  - `image1`
  - `image2`
  - `image3`
  - `image4`
  - `image5`
- aggregate bundle status:
  - `image_count = 9`
  - `all_comparison_ready = true`
  - `default_anchor_consistent = true`
- requested target:
  - `20`
- available corpus images:
  - `14`
- requested target met:
  - `false`

## Consumer Closure

- actual consumed input mode:
  - `aggregate_bundle`
- semantic judge harness:
  - `not present`
- semantic judge lane:
  - `waived`
- batch winner frequency:
  - `reviewed_isolated_component_rerun = 8`
  - `full_image_ocr_context_rerun = 1`
- default baseline retained:
  - `yes`
- active default:
  - `full_image_baseline`

## Exclusion Interpretation

- `image1`:
  - confirmed exclude as chart-dominant non-table surface
- `image2`:
  - confirmed exclude as mixed chart-table composite where table-focused reruns would under-represent the full image
- `image3`:
  - confirmed exclude as chart-dominant non-table surface
- `image4`:
  - confirmed exclude as the only remaining mixed chart-table edge case
  - bounded deterministic re-entry failed because no stable parser seed or fallback sidecar closed inside the slice
  - treat this as a manual/special-case lane until a new deterministic parser path exists
- `image5`:
  - confirmed exclude as diagram / non-table image

## Current Closure Verdict

For the current scope, the workspace now has:

- a canonical `9-image` corpus aggregate producer path
- a canonical corpus-level auto-eval path
- an explicit semantic judge waiver for the expanded cohort
- explicit GPT-confirmed excludes for the non-table and composite out-of-scope images
- an explicit waiver path for `image4` without reopening the shared cohort truth

What remains backlog, not blocker:

- a repo-local semantic judge harness
- any later decision to replace `full_image_baseline` as the active default
- any future deterministic parser path that could reopen `image4`

## Canonical Consumer Order

1. Use `phase1_caption_four_mode_corpus_ready_bundle_at2026_03_29.json` as the canonical aggregate machine-readable corpus input.
2. Use `phase1_caption_four_mode_corpus_auto_eval_true_batch_at2026_03_30.json` as the current downstream consumer and proxy-eval input.
3. Use `REPORT_phase1_caption_four_mode_corpus_semantic_judge_waiver-at2026-03-30-22-20.md` to interpret the absence of semantic judge automation.
4. Use `REPORT_phase1_image4_four_mode_reentry_waiver-at2026-03-30-21-27.md` when discussing why `image4` remains outside the canonical cohort.
5. Apply `SPEC_caption_arm_promotion_policy.md` before treating any comparison winner as a candidate default replacement.
