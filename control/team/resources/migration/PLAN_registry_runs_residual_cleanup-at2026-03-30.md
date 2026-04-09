# Plan Registry Runs Residual Cleanup

## Status

completed

## Date

2026-03-30

## Goal

Remove the residual `registry/runs` naming under:

- `control/project_agent_ops/registry/runs/`

without breaking current path consumers.

## Why This Needs Cleanup

The control-tree migration removed `runs` as a primary action unit.

However, `project_agent_ops/registry/runs/` still remains as an internal namespace.

That leaves an avoidable naming drift:

- the primary model says `resources / registry / archive`
- the remaining registry subtree still says `runs`

## Current Scope

The residual subtree currently contains two different semantic groups:

1. runtime/session path map

- `control/project_agent_ops/registry/runs/session_paths.json`

2. job registry bodies

- `control/project_agent_ops/registry/runs/image_caption_jobs/`

These should not remain under the same `runs` label forever.

## Target Split

Preferred future target namespaces:

1. runtime path registry

- `control/project_agent_ops/registry/runtime/session_paths.json`

2. job registry bodies

- `control/project_agent_ops/registry/jobs/image_caption_jobs/`

This split is preferred because:

- `session_paths.json` is a runtime path map, not a run report
- `image_caption_jobs/` stores job registry bodies, not a generic run bucket
- the names `runtime` and `jobs` match the actual reread purpose better than `runs`

## Migration Strategy

### Phase 1: Preparation

- keep existing paths canonical for now
- document the target split
- update structure rules so the remaining `registry/runs` naming is explicitly treated as residual

### Phase 2: Controlled Move

- move `session_paths.json` to `registry/runtime/`
- move `image_caption_jobs/` to `registry/jobs/`
- patch all control references, scripts, task packets, and rules
- regenerate inventories that embed the old paths

### Phase 3: Residual Removal

- verify no active references remain to `control/project_agent_ops/registry/runs/`
- remove the empty residual `registry/runs/` directory

## Verification Checklist

- `rg` finds no active references to `control/project_agent_ops/registry/runs/` outside migration/history files
- `session_paths.json` remains the canonical path map after relocation
- image-caption job ledgers remain readable at the new registry path
- tool/rule documents no longer describe `registry/runs` as canonical

## Execution Note

This cleanup was executed on 2026-03-30.

See:

- `control/team/resources/reports/REPORT_registry_runs_residual_cleanup_execution-at2026-03-30-16-57.md`
