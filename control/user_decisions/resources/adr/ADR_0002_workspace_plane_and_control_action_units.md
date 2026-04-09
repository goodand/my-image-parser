# ADR 0002 Workspace Plane And Control Action Units

## Status

accepted

## Date

2026-03-30

## Decision

Adopt a two-plane workspace model at the top level:

- `runtime`
- `control`

Within `control/`, keep the existing project-meaning columns:

- `project_domain`
- `project_agent_ops`
- `user_decisions`
- `team`

Within those `control` columns, reduce the primary action-unit filesystem axis to three categories:

- `resources`
- `registry`
- `archive`

Adopt the control-tree depth sequence as:

- root
- `control/`
- project meaning column
- action unit

In concrete form:

- `control/project_domain/{resources,registry,archive}`
- `control/project_agent_ops/{resources,registry,archive}`
- `control/user_decisions/{resources,registry,archive}`
- `control/team/{resources,registry,archive}`

Do not treat `runs` as a primary action unit going forward.

## Working Definitions

- `control`: `결정`, `조건`, `상태`의 `정적/동적` `다시 읽기`와 `동기화`
- `registry`: `상태`, `결정`의 `동적` `동기화`
- `resources`: `조건`, `결정`의 `정적` `다시 읽기`와 `재사용`
- `archive`: `결정`, `상태`의 `정적` `다시 읽기`

## Context

The earlier control-tree model used:

- project meaning columns:
  - `project_domain`
  - `project_agent_ops`
  - `user_decisions`
  - `team`
- action units:
  - `archive`
  - `registry`
  - `resources`
  - `runs`

That 4x4 structure worked as an internal control-plane scaffold, but the `runs` axis became conceptually unstable.

The main problem is that `runs` mixes multiple meanings:

- how an artifact was produced
- how often it is reread
- whether it is canonical or ephemeral
- whether it is runtime state, governance material, or reusable reference

Those concerns are not the same kind of classification as `resources`, `registry`, or `archive`.

Separately, the workspace root already contains executable and tool-owned surfaces such as:

- `scripts/`
- `skills/`
- `logs/`
- `data/`
- `context_portal/`

Those directories should not be forced into the same filesystem axis as control artifacts.

## Rationale

The stronger distinction is:

- top-level workspace plane
- control-internal semantic classification

At the top level, the workspace is divided into:

- `runtime`
- `control`

Inside `control/`, the stronger long-lived classification remains the project-meaning columns, because they answer who rereads and reuses the artifact:

- domain truth
- agent operational truth
- user decision truth
- team-wide governance truth

Inside each control column, the action-unit layer should describe long-lived artifact role:

- `resources`
- `registry`
- `archive`

That role-based split is more stable than `runs`.

The depth order should place project meaning before action unit.

That ordering is preferred because:

- project meaning answers the stronger semantic question: who rereads, governs, and reuses the artifact
- action unit answers the secondary role question: what kind of canonical artifact it is inside that semantic column
- `team` rules, `project_domain` specs, and `user_decisions` ADRs are easier to navigate when semantic ownership is resolved before artifact role
- the existing control tree already follows this direction, so the choice minimizes migration churn

## Consequences

- `control/` remains the canonical governance and coordination plane.
- root-level execution surfaces stay outside `control/`.
- `team` remains one control-plane semantic column, not a root-level super-category.
- the preferred depth order is `control -> project meaning -> action unit`, not the inverse.
- future `control/*/runs` material should be interpreted as transitional structure rather than a preferred end state.
- when reorganizing existing control artifacts, prefer role-based placement into:
  - `resources`
  - `registry`
  - `archive`

## Notes

This decision does not require an immediate full migration of every existing `runs/` directory.

It establishes the preferred conceptual model for future organization and for incremental restructuring work.
