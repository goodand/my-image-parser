# Control Tree Lint Baseline Split

## Purpose

Record a baseline that separates current `lint_control_tree.py` findings into:

- legacy debt
- active structural violations
- active contract drift

This baseline is intended to keep future cleanup work bounded and machine-rereadable.

## Baseline Source

- lint script:
  - [lint_control_tree.py](../scripts/lint_control_tree.py)
- structure rule:
  - [RULES_workspace_structure.md](../rules/RULES_workspace_structure.md)
- captured on:
  - `2026-03-30`

## Current Snapshot

- total errors: `77`
- total warnings: `240`
- total findings: `317`

Most frequent codes:

- `DOC002`: `119`
- `DOC001`: `114`
- `NAME020`: `70`
- `NAME011`: `5`

## Classification Rule

### Legacy Debt

Treat as legacy debt when the finding lives under one of these areas:

- `control/*/archive/`
- `control/project_domain/resources/assets/`
- `control/project_domain/resources/context_packages/`
- `control/project_domain/resources/imported_fourarm/`

Interpretation:

- these findings are real, but they mostly belong to inherited material, preserved payloads, or archived bundles
- they should not block active structure decisions in the same way as current coordination-surface drift

### Active Structural Violation

Treat as active structural violation when the finding indicates the control-plane layout itself is misaligned with the current structure philosophy.

Current examples:

- `TREE002`
- `TREE003`
- `DOC003`
- unexpected `control/*/resources/scripts/`
- `.obsidian` living directly under a project-meaning bucket

Interpretation:

- this category is the shortest path to structure correctness
- these should be reviewed before broad naming cleanup

### Evidence Naming Or Placement Debt

Treat as evidence naming or placement debt when findings live under:

- `control/*/resources/reports/`
- `control/*/resources/manifests/`

Interpretation:

- these are active rereadable bodies, but many are dated operational artifacts still living under `resources/`
- this is important, but it is a placement/naming cleanup lane rather than a root-structure blocker

### Other Active Contract Drift

Everything else is treated as active contract drift.

Typical examples:

- canonical docs with dated filenames
- title/filename drift on active notes or checklists
- operational plans living in `resources/experiment_plans/`

Interpretation:

- this lane is active and should eventually be cleaned
- but it is broader than the immediate structure-boundary problems

## Current Split

- active structural violation: `2`
- evidence naming or placement debt: `154`
- legacy material or archive debt: `77`
- other active contract drift: `84`

Note:

- this split is a triage baseline, not a replacement for the raw lint result
- counts are derived from the current path-based classification pass and may shift when lint contracts evolve

## Current Active Structural Violations

1. `control/user_decisions/.obsidian`
   - `TREE002`
   - non-canonical action-unit directory under a project-meaning bucket
2. `control/user_decisions/.obsidian/core-plugins.json`
   - `NAME020`
   - machine-readable filename rule does not currently exempt the `.obsidian` runtime subtree

## Immediate Cleanup Priority

1. Separate runtime-local Obsidian state from active control-tree action units.
2. Decide whether `.obsidian` is:
   - an allowed runtime exception under `user_decisions/`
   - or something that should move behind a clearer exception contract
3. Keep legacy debt and evidence-placement debt out of the first cleanup pass.
4. Use this baseline when deciding whether a new lint finding is:
   - a real structure regression
   - or previously known inherited debt

## Recommended Next Lane

### Lane A. Active Structure First

- resolve `.obsidian` exception handling
- verify `control/*/resources/scripts/` remains exception-only
- keep `root > control > project meaning > action unit` readable in both rules and lint

### Lane B. Evidence Placement Cleanup

- review `resources/reports/` and `resources/manifests/` for operational dated artifacts
- move only when the move improves rereadability and canonical placement

### Lane C. Legacy Debt Freeze

- do not let archive/material payload debt dominate current structural decisions
- treat it as inventory debt unless an active consumer depends on those filenames

## Decision Use

This baseline should be used as the answer to:

- "is the structure currently broken, or just noisy?"
- "what is inherited debt versus active violation?"
- "which lint findings should block a new canonical decision?"

Current answer:

- the workspace is noisy
- but the truly active structure violations are narrow
- the main current blocker is not broad archive debt, but boundary handling for runtime-local exceptions such as `.obsidian`
