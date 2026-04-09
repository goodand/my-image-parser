# Phase 1 Caption Four-Mode Corpus Experiment Summary

## Scope

- active corpus truth:
  - `phase1_caption_four_mode_corpus_ready_bundle_at2026_03_29.json`
- active consumer truth:
  - `phase1_caption_four_mode_corpus_auto_eval_true_batch_at2026_03_30.json`
- explicit excluded edge/manual lane:
  - `image4`

## Stable Cohort

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
- stable ready image count:
  - `9`

## Explicit Excludes

- `image1`: chart-dominant non-table
- `image2`: mixed chart-table composite
- `image3`: chart-dominant non-table
- `image4`: mixed chart-table edge case; deterministic re-entry failed in the bounded lane
- `image5`: diagram / non-table

## Current Outcome

- actual_input_mode:
  - `aggregate_bundle`
- batch winner frequency:
  - `reviewed_isolated_component_rerun = 8`
  - `full_image_ocr_context_rerun = 1`
- default baseline retained:
  - `yes`
- active default:
  - `full_image_baseline`
- semantic judge:
  - `waived`

## Interpretation

- `reviewed_isolated_component_rerun` is the dominant comparison winner in the current corpus cohort.
- `comparison winner` is still separate from `default replacement`.
- the current operational baseline remains `full_image_baseline`.
- `image4` should stay outside the automatic cohort and be treated as a manual/special-case lane until a new deterministic parser path exists.

## Canonical Reading Order

1. `REPORT_phase1_caption_four_mode_corpus_experiment_summary-at2026-03-30-22-39.md`
2. `REPORT_phase1_caption_four_mode_corpus_closure-at2026-03-30-22-19.md`
3. `phase1_caption_four_mode_corpus_auto_eval_true_batch_at2026_03_30.json`
4. `REPORT_phase1_caption_four_mode_corpus_semantic_judge_waiver-at2026-03-30-22-20.md`
