# Task Packet: Phase1 Image4 Multi-Component Recrop Reentry Slice

## Goal

Determine whether `image4.png` can re-enter the current `phase1 small-batch 4-mode` experiment after the new multi-component reviewed-crop recrop logic. Close this bounded producer slice with either:

1. an `image4` frozen `4-mode` bundle, or
2. an explicit waiver that preserves exclusion.

Do not re-read or reinterpret the full master plan. Use only the truth sources below.

## Current Canonical Truth

- current stable `phase1` aggregate bundle already exists and is `5-image`
- `image4` is the only excluded image
- exclusion rationale is still `mixed_chart_table_edge_case_and_no_frozen_derived_arms`
- default baseline remains `full_image_baseline`
- manual human image review is forbidden
- GPT direct image confirmation is allowed only if deterministic evidence leaves an unresolved edge case

## Required Inputs

- [phase1_caption_four_mode_small_batch_bundle_at2026_03_28.json](../../../../project_domain/resources/manifests/phase1_caption_four_mode_small_batch_bundle_at2026_03_28.json)
- [REPORT_phase1_caption_four_mode_small_batch_readiness-at2026-03-28-14-10.md](../../../../project_domain/resources/reports/REPORT_phase1_caption_four_mode_small_batch_readiness-at2026-03-28-14-10.md)
- [phase1_caption_four_mode_small_batch_candidates_at2026_03_28.json](../../../../project_domain/resources/manifests/phase1_caption_four_mode_small_batch_candidates_at2026_03_28.json)
- [image4.png](../../../../project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image4.png)
- [build_reviewed_component_context_package.py](../../../../../scripts/build_reviewed_component_context_package.py)
- [reviewed_component_context_package_lib.py](../../../../../scripts/reviewed_component_context_package_lib.py)
- [alpha_component_lib.py](../../../../../scripts/alpha_component_lib.py)

## Fixed Interpretation

1. `image4` is currently excluded, not pending inclusion.
2. `image4` is a composite `chart + table` edge case, not a normal table-only image.
3. `comparison winner != default replacement`.
4. `full_image_baseline` remains the default baseline regardless of any bounded derived-arm success.
5. Do not patch shared aggregate truth, shared auto-eval truth, shared registry, or master plan in this slice.
6. If deterministic evidence is insufficient but the image still looks plausibly recoverable, GPT direct image confirmation is allowed as a bounded tie-break only after deterministic attempts.

## Scope

- Use the new reviewed-component recrop logic on `image4`
- Prefer existing builders and existing context-package flows
- Try to close only the missing derived-arm path(s) needed for `image4`
- If `image4` still cannot safely produce a stable reviewed/parser surface, write an explicit waiver and keep it excluded

## Non-Goals

- Do not modify the current `phase1` canonical aggregate bundle
- Do not modify `phase1` consumer auto-eval outputs
- Do not change shared registry or master plan
- Do not regenerate already-stable `image7/image8/image9/image10/image11` artifacts
- Do not promote object isolation to unattended default behavior

## Allowed Write Surfaces

- `scripts/` only if a bounded bug fix is required for this slice
- `control/project_domain/resources/manifests/` for new `image4`-specific artifacts
- `control/project_domain/resources/reports/` for new bounded reports
- `<TMP_DIR>/` for scratch outputs

## Expected Outputs

### Success path

- one `image4` reviewed-component bounded smoke report
- one `image4` parser/reviewed closure report or combined `4-mode` closure report
- one `image4` frozen `4-mode` eval bundle
- one `image4` inclusion decision report

### Failure-safe path

- one explicit waiver report that states why `image4` remains excluded after the new recrop logic

## Preferred Filenames

- `control/project_domain/resources/reports/REPORT_phase1_image4_reviewed_component_recrop_smoke-atYYYY-MM-DD-HH-MM.md`
- `control/project_domain/resources/manifests/phase1_image4_caption_four_mode_eval_bundle_atYYYY_MM_DD.json`
- `control/project_domain/resources/reports/REPORT_phase1_image4_four_mode_reentry_decision-atYYYY-MM-DD-HH-MM.md`
- `control/project_domain/resources/reports/REPORT_phase1_image4_four_mode_reentry_waiver-atYYYY-MM-DD-HH-MM.md`

## Done Definition

- `image4` is closed by exactly one of:
  - `included` through a bounded frozen `4-mode` bundle
  - `excluded` through explicit waiver
- all new JSON passes `python3 -m json.tool`
- modified Python passes `py_compile` or an existing test
- final report states:
  - used truth sources
  - deterministic path attempted
  - whether GPT direct confirmation was needed
  - final inclusion or exclusion decision
  - next one step

## Verification

1. Re-read the truth-source files listed above and do not use the full master plan as primary context.
2. Verify `image4` still starts from excluded status before patching.
3. Verify any reviewed crop uses bounded recrop candidate logic rather than raw alpha component promotion.
4. If GPT direct confirmation is used, keep it as tie-break evidence rather than default promotion logic.
5. Validate all new JSON with `python3 -m json.tool`.
6. Validate modified Python with `py_compile` or existing tests.

## Handoff Note

This is a bounded producer slice only. Do not mutate shared `phase1` aggregate truth inside this task. If `image4` becomes viable, emit stable per-image artifacts and a clear inclusion recommendation so a later synchronization slice can decide whether to expand the cohort.
