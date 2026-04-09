# ADR 0003 Resource Secondary Kinds Inside Resources

## Status

accepted

## Date

2026-03-30

## Decision

Keep the primary `control/` structure unchanged:

- `control/`
- project meaning column
- action unit

Keep the primary control action units unchanged:

- `resources`
- `registry`
- `archive`

Do not add a fourth action unit such as `evidence`.

Instead, treat `resources/` as having three secondary resource kinds:

- `reference`
- `evidence`
- `material`

These secondary kinds are not a new top-level filesystem axis.

They are a placement and naming rule used inside each `resources/` bucket to reduce drift.

## Working Definitions

- `reference`:
  - long-lived rereadable bodies used as rules, plans, specs, templates, contracts, or reusable guidance
- `evidence`:
  - rereadable result bodies that justify, compare, verify, or explain a state transition or judgment
- `material`:
  - rereadable resource bodies that carry execution-linked payloads such as assets, context packages, extracted jobs, imported bundles, or similar concrete materials

## Context

`control/` was reduced to three primary action units:

- `resources`
- `registry`
- `archive`

That solved the instability caused by `runs` as a primary action unit.

However, `resources/` still collects several different reread patterns under one bucket.

Examples already present in the workspace include:

- rules, specs, templates, ADRs, references, task packets, master plans
- reports, manifests, smoke outputs, migration packets, cross-validation outputs
- assets, context packages, extracted PPT jobs, imported bundles, external repo mirrors

All of these are active readable bodies, so they belong in `resources/`.

But they are not the same kind of resource.

If that difference is not named, three operational problems appear:

- search cost rises because readers do not know whether they are looking for guidance, judgment, or concrete payloads
- new artifact placement drifts because `resources/` becomes a catch-all bucket
- the boundary between `resources/` and `registry/` becomes less clear when structured JSON bodies are mixed with index-like materials

## Rationale

The stronger distinction inside `resources/` is not who owns the artifact.

That is already handled by the project-meaning column:

- `project_domain`
- `project_agent_ops`
- `user_decisions`
- `team`

The remaining distinction is how the resource is reread.

`reference` resources answer:

- what rules apply
- what should be reused
- what stable guidance exists

`evidence` resources answer:

- why a decision or status should be believed
- what comparison or verification result was observed
- what result body should be audited later

`material` resources answer:

- what concrete payload is being carried for reread or downstream reuse
- what extracted or imported body is part of the active workspace truth

This keeps the primary tree simple while still giving `resources/` an internal navigation model.

## Consequences

- `resources/` remains the correct primary action unit for active rereadable bodies.
- `registry/` remains reserved for canonical path, active selection, id mapping, and status synchronization.
- `archive/` remains reserved for superseded or historical bodies.
- teams may keep existing subdirectory names, but each resource subdirectory should be interpretable as one of:
  - `reference`
  - `evidence`
  - `material`
- executable helpers should not spread inside `control/*/resources/`.
  - if a helper is primarily executable, prefer root `scripts/`
  - a control-local script is allowed only as a narrow maintenance exception for the control plane itself

## Example Mappings

Typical `reference` resource directories:

- `rules`
- `templates`
- `specs`
- `references`
- `knowledge_bases`
- `master_plans`
- `checklists`
- `contracts`
- `task_packets`
- `troubleshooting`
- `adr`
- `notes`
- `closed_questions`

Typical `evidence` resource directories:

- `reports`
- `manifests`
- `smoke`
- `feedback`
- `migration`
- `cross_validation`

Typical `material` resource directories:

- `assets`
- `context_packages`
- `pptx_jobs`
- `imported_fourarm`
- `external_repos`
- `vendor_skills`
- `codebase_graph`

Borderline rule:

- if a directory mainly stores a body to be reread for explanation or verification, prefer `evidence`
- if it mainly stores reusable guidance or normative content, prefer `reference`
- if it mainly stores concrete payloads or bundled materials, prefer `material`

## Notes

This decision does not require an immediate second migration.

It establishes the interpretation rule for existing `resources/` directories and the placement rule for future ones.
