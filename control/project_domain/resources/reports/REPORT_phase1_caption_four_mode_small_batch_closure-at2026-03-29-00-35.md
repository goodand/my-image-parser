# Phase 1 Caption Four-Mode Small-Batch Closure

## Purpose

Close the `phase1` small-batch extension of the bounded `4-mode` experiment and record the final producer truth, consumer truth, and promotion interpretation for downstream use.

## Canonical Inputs

- candidate selection:
  - `control/project_domain/resources/manifests/phase1_caption_four_mode_small_batch_candidates_at2026_03_28.json`
- readiness report:
  - `control/project_domain/resources/reports/REPORT_phase1_caption_four_mode_small_batch_readiness-at2026-03-28-14-10.md`
- canonical aggregate bundle:
  - `control/project_domain/resources/manifests/phase1_caption_four_mode_small_batch_bundle_at2026_03_28.json`
- aggregate bundle report:
  - `control/project_domain/resources/reports/REPORT_phase1_caption_four_mode_small_batch_bundle-at2026-03-28-23-54.md`
- canonical consumer manifest:
  - `control/project_domain/resources/manifests/phase1_caption_four_mode_small_batch_auto_eval_true_batch_at2026_03_28.json`
- consumer report:
  - `control/project_domain/resources/reports/REPORT_phase1_caption_four_mode_small_batch_auto_eval_true_batch-at2026-03-29-00-13.md`
- semantic judge waiver:
  - `control/project_domain/resources/reports/REPORT_phase1_caption_four_mode_small_batch_semantic_judge_waiver-at2026-03-29-00-13.md`

## Producer Closure

- aggregate stale drift:
  - `closed`
- canonical aggregate bundle image ids:
  - `image11`
  - `image7`
  - `image8`
  - `image10`
  - `image9`
- aggregate bundle status:
  - `image_count = 5`
  - `all_comparison_ready = true`
  - `default_anchor_consistent = true`

## Consumer Closure

- stale auto-eval drift:
  - `closed`
- actual consumed input mode:
  - `aggregate_bundle`
- aggregate input support:
  - `yes`
- per-image fallback support:
  - `yes`
- semantic judge harness:
  - `not present`
- semantic judge lane:
  - `waived`

## Batch Outcome

- winner frequency:
  - `reviewed_isolated_component_rerun = 4`
  - `full_image_ocr_context_rerun = 1`
- default baseline retained:
  - `yes`
- active default:
  - `full_image_baseline`

## Promotion Interpretation

- `comparison winner` is not treated as `default replacement`
- `image7`, `image9`, and `image10` derived non-baseline arms remain:
  - `comparison_only_pending_context_review`
- `image8` full-image OCR and parser arms remain:
  - `comparison_only_pending_context_review`
- `image8` reviewed isolated component arm is:
  - `comparison_ready_reviewed_branch`
- current policy reference:
  - `control/project_domain/resources/specs/prose/SPEC_caption_arm_promotion_policy.md`

## Current Closure Verdict

For the current scope, the workspace now has:

- a canonical `5-image` aggregate producer path
- a canonical consumer path
- fallback input support for future consumers
- an explicit semantic judge waiver
- an explicit promotion policy that keeps default replacement separate from comparison wins

What remains backlog, not blocker:

- repo-local semantic judge harness
- any later decision to replace `full_image_baseline` as the active default

## Canonical Consumer Order

1. Use `phase1_caption_four_mode_small_batch_bundle_at2026_03_28.json` as the canonical aggregate machine-readable input.
2. Use `phase1_caption_four_mode_small_batch_auto_eval_true_batch_at2026_03_28.json` as the current downstream consumer and proxy-eval input.
3. Use `REPORT_phase1_caption_four_mode_small_batch_semantic_judge_waiver-at2026-03-29-00-13.md` to interpret the absence of semantic judge automation.
4. Apply `SPEC_caption_arm_promotion_policy.md` before treating any comparison winner as a candidate default replacement.
