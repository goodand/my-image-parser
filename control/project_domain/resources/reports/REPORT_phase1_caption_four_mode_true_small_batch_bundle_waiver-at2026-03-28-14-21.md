# Phase 1 Caption Four-Mode True Small-Batch Bundle Waiver

## Purpose

Record why the current `phase1` auto-eval lane is still consuming a `1-image` frozen bundle template rather than a true multi-image small-batch bundle.

## Input Evidence

- auto-eval input used:
  - `../manifests/phase0_caption_four_mode_eval_bundle_at2026_03_28.json`
- auto-eval output:
  - `../manifests/phase1_caption_four_mode_small_batch_auto_eval_at2026_03_28.json`
- readiness closure:
  - `./REPORT_phase0_four_mode_caption_readiness-at2026-03-28-11-36.md`

## Findings

1. No true `phase1_caption_four_mode_small_batch_bundle_at*.json` exists in `control/project_domain/resources/manifests/`.
2. Only one shared image currently has all four arm surfaces closed under the current bounded evidence set.
3. The shared image is `image11.png`, and each non-baseline arm currently exposes only one matching context package:
   - `full_image_ocr_baseline/.../image11/CONTEXT_PACKAGE.json`
   - `parser_enriched_table_baseline/.../image11/CONTEXT_PACKAGE.json`
   - `reviewed_isolated_component/.../image11/CONTEXT_PACKAGE.json`
4. Under the current lane constraints, arm regeneration and bundle regeneration are out of scope.

## Waiver Decision

- current `phase1` auto-eval is accepted as a `1-image small-batch template consumer`
- current `phase1` auto-eval is **not** accepted as a true multi-image small-batch evaluation
- expanding to a true small-batch requires additional images with all four arms already closed before bundle assembly

## Why This Matters

- it prevents overstating `1-image template consumption` as `small-batch coverage`
- it keeps deterministic lane closure separate from batch-generalization claims
- it avoids regenerating caption arms just to satisfy a later consumer lane

## Next Step

Assemble a true `phase1` small-batch bundle only after additional shared images reach `4-arm closed` status through the normal deterministic lane. Then rerun the same auto-eval consumer without changing its scoring contract.
