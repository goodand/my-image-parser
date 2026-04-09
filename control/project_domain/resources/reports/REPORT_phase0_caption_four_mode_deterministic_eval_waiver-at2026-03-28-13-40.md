# Phase 0 Four-Mode Deterministic Eval Waiver

## Purpose

Close the Session A deterministic-evaluation lane explicitly after freezing the current four-arm comparison bundle.

## Inputs

- four-mode readiness:
  - `control/project_domain/resources/reports/REPORT_phase0_four_mode_caption_readiness-at2026-03-28-11-36.md`
- frozen eval bundle:
  - `control/project_domain/resources/manifests/phase0_caption_four_mode_eval_bundle_at2026_03_28.json`
- current four-mode comparison:
  - `control/project_domain/resources/manifests/phase0_caption_four_mode_comparison_at2026_03_28.json`

## Harness Discovery Evidence

Repo-wide search was run against `scripts/`, `control/`, and adjacent project files for:

- `hitk`
- `judge`
- `deterministic`
- `four_mode`
- `4-mode`
- `eval_`

What exists:

- deterministic preprocessing and review surfaces
- master-plan and draft references to future evaluation paths
- optional judge-oriented draft planning documents

What was **not** found in this workspace:

- a concrete runnable `4-mode` deterministic evaluation runner that directly consumes the frozen caption comparison bundle
- a stable local `hitk`-style script under this repo for the current caption-arm surface

## Waiver Decision

Final answer:

- `waive deterministic lane in this repo for now`

Reason:

- Session A successfully froze the four-arm comparison bundle.
- The current workspace does not yet contain a concrete deterministic evaluator that consumes that bundle directly.
- Forcing a new deterministic evaluator in this turn would create a new evaluation surface instead of closing the existing Session A lane cleanly.

## Boundaries

This waiver does **not** mean:

- the four-arm bundle is incomplete
- the four-mode comparison is not ready
- Session B judge/qualitative work should stop

It **does** mean:

- Session A ends with a reusable frozen bundle and an explicit deterministic-eval gap report
- any future deterministic scorer should consume the frozen bundle rather than rebuilding arm extraction logic

## Next One Step

Let Session B consume:

- `control/project_domain/resources/manifests/phase0_caption_four_mode_eval_bundle_at2026_03_28.json`

for judge or qualitative evaluation, while any later deterministic lane is added as a separate bounded harness that reads the same bundle.
