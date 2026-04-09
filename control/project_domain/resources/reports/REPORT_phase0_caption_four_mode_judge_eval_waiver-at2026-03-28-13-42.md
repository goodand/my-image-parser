# Phase 0 Four-Mode Caption Judge Eval Waiver

## Purpose

Close the qualitative/judge evaluation lane for the current bounded `4-mode` comparison by recording whether a repo-local judge harness exists and, if not, what frozen consumer surface is now available instead.

## Input Paths Used

- comparison manifest:
  - `control/project_domain/resources/manifests/phase0_caption_four_mode_comparison_at2026_03_28.json`
- readiness report:
  - `control/project_domain/resources/reports/REPORT_phase0_four_mode_caption_readiness-at2026-03-28-11-36.md`
- comparison surface spec:
  - `control/project_domain/resources/specs/prose/SPEC_caption_arm_comparison_surface.md`
- comparison surface contract:
  - `control/project_domain/resources/specs/contracts/caption_arm_comparison_surface.contract.json`
- generated judge input:
  - `control/project_domain/resources/manifests/phase0_caption_four_mode_judge_input_at2026_03_28.json`
- generated frozen eval bundle:
  - `control/project_domain/resources/manifests/phase0_caption_four_mode_eval_bundle_at2026_03_28.json`

## Judge Capability Verdict

- repo-local judge harness available: `false`
- bounded LLM/judge execution performed: `no`
- waiver scope:
  - current `1-image`, `4-arm`, qualitative caption comparison on `image11.png`

## Waiver Rationale

1. The implemented comparison surface is explicitly `read_only` and contractually framed as a comparison builder, not as a semantic judge runner.
2. The current repo-local proven surface is:
   - ledger-backed arm extraction
   - parity audit
   - promotion-gate handling
   - frozen eval-bundle generation
3. The repo contains planning material for a later evaluation overlay, but the current workspace does not expose a first-party bounded judge runner for this exact `4-mode` qualitative comparison.
4. The caption runner's built-in evaluation sidecar is default bookkeeping, not a semantic judge lane.

## Closest Reusable Surface

The closest reusable surface is the existing comparison runner:

- `scripts/run_caption_arm_comparison.py`

It now produced two bounded consumer artifacts for this session:

- judge input:
  - `control/project_domain/resources/manifests/phase0_caption_four_mode_judge_input_at2026_03_28.json`
- frozen eval bundle:
  - `control/project_domain/resources/manifests/phase0_caption_four_mode_eval_bundle_at2026_03_28.json`

These are suitable as downstream inputs for a later deterministic or LLM-judge lane, but they are not themselves a judge verdict.

## What This Waiver Does Not Mean

- it does not reopen blocked comparison arms
- it does not invalidate the current `4 / 4 ready` comparison verdict
- it does not demote the frozen bundle surface

## Next One Step

Use the frozen eval bundle as the canonical input for a later judge consumer, or continue with the manual qualitative summary for the current bounded `image11.png` comparison.
