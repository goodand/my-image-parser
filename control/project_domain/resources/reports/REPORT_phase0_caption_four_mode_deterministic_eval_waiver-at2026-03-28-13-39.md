# Phase 0 Four-Mode Deterministic Eval Waiver

## Purpose

Record why Session A does not execute a deterministic 4-mode evaluation runner in this repo right now, even though the four-mode eval bundle is frozen and comparison-ready.

## Inputs Checked

- `control/project_domain/resources/manifests/phase0_caption_four_mode_eval_bundle_at2026_03_28.json`
- `control/project_domain/resources/reports/REPORT_phase0_caption_four_mode_eval_bundle-at2026-03-28-13-39.md`
- `control/project_domain/resources/manifests/phase0_caption_four_mode_comparison_at2026_03_28.json`
- repo-local search across `scripts/` and `control/` for deterministic four-mode evaluation harness candidates

## Result

- frozen eval bundle: `completed`
- deterministic four-mode runner in this repo: `not found`
- Session A verdict: `waiver`

## Evidence

Repo-local search found:

- comparison/readiness artifacts for four-mode execution
- evaluation plans and judge-oriented drafts
- no committed deterministic four-mode evaluator script in this repo that can consume the bundle and emit bounded results now

This means the current workspace is comparison-ready, but Session A cannot truthfully claim a deterministic evaluation execution without inventing a new harness.

## Boundary

This waiver does not mean:

- the 4-mode comparison is blocked
- Session B should stop
- the frozen bundle is insufficient

It does mean:

- Session A stops at `frozen eval bundle + deterministic waiver`
- Session B can continue with judge/qualitative evaluation from the same frozen bundle
- a later deterministic lane should either be imported intentionally or implemented as a separate bounded task

## Next One Step

Use `control/project_domain/resources/manifests/phase0_caption_four_mode_eval_bundle_at2026_03_28.json` as the shared input for Session B and any later deterministic harness work.
