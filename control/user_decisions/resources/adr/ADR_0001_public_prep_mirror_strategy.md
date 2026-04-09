# ADR 0001 Public Prep Mirror Strategy

## Status

accepted

## Date

2026-03-30

## Decision

Do not publish the current workspace as a raw repository snapshot.

Prepare a curated public-prep mirror first, then publish that mirror or a dedicated public-prep branch. The public surface must expose reusable code, reusable skills, and frozen documentation, while excluding local runtime state, run artifacts, registry outputs, machine-local configuration, and private raw assets.

## Context

The current workspace mixes:

- experiment workspace state
- operational state
- reusable code
- reusable skills
- local MCP setup and machine-local paths

That mixed state is useful for local execution, but it is not a safe or clean public repository boundary.

## Include In Public Prep

- `scripts/`
- `skills/`
- `control/project_domain/resources/` specs, references, and master plans
- vendored wrapper or launcher code only when it is necessary to understand or run the public slice

## Exclude Or Template In Public Prep

- run outputs and registries already covered by repo ignore policy
- local-only directories such as `.codex/`, `.claude/`, `.history/`
- most machine-local `.vscode/` settings
- MCP configuration that contains absolute paths
- private or raw assets

## Required Public Prep Additions

- root `README.md`
- `docs/START_HERE.md` or `docs/AGENT_ONBOARDING.md`
- vendor license and origin audit when vendored code is included

## Delegation Rule

Do not hand the full repository to a fresh agent by default.

Use frozen truth sources plus a fixed interpretation packet instead. The goal is to prevent re-deriving experiment history from noisy workspace state.

## Local Truth Sources For Public Prep Handoff

- `control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md`
- `control/project_domain/resources/specs/prose/SPEC_full_image_standalone_ocr_context_package_baseline.md`
- `control/project_domain/resources/manifests/phase1_caption_four_mode_small_batch_bundle_at2026_03_28.json`
- `control/project_domain/resources/reports/REPORT_phase1_caption_four_mode_small_batch_auto_eval_true_batch-at2026-03-29-00-13.md`
- `skills/image-result-auditor/SKILL.md`

## Fixed Interpretation For Handoff

- default baseline = `full_image_baseline`
- comparison winner != default replacement
- `image7` and `image9` parser or reviewed arms = `comparison_only_pending_context_review`

## Non Goals For Public Prep Workers

- do not regenerate run artifacts
- do not rewrite the master plan
- do not rewrite the context package
- do not reinterpret experiment history

## Consequences

- GitHub publication is treated as a curation step, not a direct push step
- public onboarding must be intentionally written
- future worker handoff should prefer an immutable packet over open-ended repo exploration
