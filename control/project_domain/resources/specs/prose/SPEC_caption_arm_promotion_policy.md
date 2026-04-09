# Caption Arm Promotion Policy

## Purpose

Define the current promotion rules for `4-mode` caption comparison outputs so that `comparison winner`, `comparison-ready`, and `default replacement` are not conflated.

## Scope

This policy applies to:

- bounded `phase0` single-image `4-mode` comparison outputs
- `phase1` small-batch `4-mode` aggregate and auto-eval outputs
- `phase1` corpus `4-mode` aggregate and auto-eval outputs
- downstream consumers that read:
  - frozen eval bundles
  - aggregate bundles
  - proxy auto-eval manifests

## Source Of Truth

- comparison surface:
  - [SPEC_caption_arm_comparison_surface.md](./SPEC_caption_arm_comparison_surface.md)
- phase1 aggregate bundle:
  - [phase1_caption_four_mode_small_batch_bundle_at2026_03_28.json](../../manifests/phase1_caption_four_mode_small_batch_bundle_at2026_03_28.json)
- phase1 auto-eval:
  - [phase1_caption_four_mode_small_batch_auto_eval_true_batch_at2026_03_28.json](../../manifests/phase1_caption_four_mode_small_batch_auto_eval_true_batch_at2026_03_28.json)
- phase1 corpus aggregate bundle:
  - [phase1_caption_four_mode_corpus_ready_bundle_at2026_03_29.json](../../manifests/phase1_caption_four_mode_corpus_ready_bundle_at2026_03_29.json)
- phase1 corpus auto-eval:
  - [phase1_caption_four_mode_corpus_auto_eval_true_batch_at2026_03_30.json](../../manifests/phase1_caption_four_mode_corpus_auto_eval_true_batch_at2026_03_30.json)
- phase1 corpus closure:
  - [REPORT_phase1_caption_four_mode_corpus_closure-at2026-03-30-22-19.md](../../reports/REPORT_phase1_caption_four_mode_corpus_closure-at2026-03-30-22-19.md)

## Promotion States

- `default_ready_anchor`
  - Meaning:
    - arm is currently allowed to remain the active default output
  - Current holder:
    - `full_image_baseline`

- `comparison_only_pending_context_review`
  - Meaning:
    - arm may participate in comparison and batch evaluation
    - arm must not replace the default while context review is still pending
  - Current examples:
    - `full_image_ocr_context_rerun`
    - `parser_table_enriched_rerun`
    - `image7` and `image9` reviewed isolated reruns

- `comparison_ready_reviewed_branch`
  - Meaning:
    - arm is usable as a reviewed comparison branch
    - arm is still not the default without an explicit promotion decision
  - Current example:
    - `image11` reviewed isolated rerun

## Current Default Rule

- Keep `full_image_baseline` as the active default baseline.
- A non-baseline arm may win a bounded comparison or proxy auto-eval without changing the active default.
- Default replacement requires a separate promotion decision after the comparison phase.

## Current Batch Interpretation

The historical `phase1` small-batch closure remains valid for the original `5-image` slice.

For the current active `phase1` corpus cohort:

- included images:
  - `image7`
  - `image8`
  - `image9`
  - `image10`
  - `image11`
  - `image12`
  - `image13`
  - `image14`
  - `image15`
- explicit excludes:
  - `image1`
  - `image2`
  - `image3`
  - `image4`
  - `image5`
- qualitative or proxy winners may vary by image
- batch-level winner frequency is currently:
  - `reviewed_isolated_component_rerun = 8`
  - `full_image_ocr_context_rerun = 1`
- despite that, `full_image_baseline` remains the active default

## Required Guardrails

- Do not treat `qualitative_winner_candidate` as a default replacement signal.
- Do not promote any arm solely because it improves `noise suppression` or `relation wording`.
- Do not collapse `comparison-ready` and `default-ready` into one field.
- Preserve promotion-state penalties inside proxy auto-eval and future judge lanes.

## Promotion Preconditions

An arm can only be considered for default replacement if all of the following hold:

1. its context package or reviewed branch is no longer pending
2. it remains stable across more than one image
3. its comparison benefit is not only stylistic, but operationally useful
4. the promotion is recorded explicitly in a later policy or closure artifact

## Operational Result

The current pipeline supports:

- comparison winner selection
- proxy batch ranking
- downstream consumer input

It does not yet support:

- automatic default replacement by proxy score
- automatic replacement driven by reviewed-branch wins alone
