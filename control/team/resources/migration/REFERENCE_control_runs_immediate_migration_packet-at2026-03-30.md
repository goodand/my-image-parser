# Control Runs Immediate Migration Packet

## Purpose

Prepare an immediate migration from the transitional top-level `control/*/runs`
layout into the accepted `project meaning -> action unit` control tree with
three action units:

- `resources`
- `registry`
- `archive`

## Governing Decision

- ADR:
  - `control/user_decisions/resources/adr/ADR_0002_workspace_plane_and_control_action_units.md`

## Immediate Scope

This packet prepares migration for the following transitional buckets:

- `control/project_domain/runs`
- `control/project_agent_ops/runs`
- `control/user_decisions/runs`
- `control/team/runs`

It does **not** cover nested `registry/runs` directories, because those already
live under the `registry` action unit and do not violate the new top-level
action-unit rule.

## Canonical Migration Model

- depth sequence:
  - `control -> project meaning -> action unit`
- action units:
  - `resources`
  - `registry`
  - `archive`

Interpretation rule:

- active reread bodies move to `resources`
- current index and status surfaces stay in `registry`
- historical or superseded material moves to `archive`

## Machine-Readable Inventory

- generated inventory:
  - `control/team/resources/migration/control_runs_migration_inventory_at2026_03_30.json`
- generator:
  - `scripts/build_control_runs_migration_inventory.py`
- parallel execution plan:
  - `control/team/resources/migration/control_runs_migration_parallel_plan_at2026_03_30.json`

## Immediate Migration Targets

High-priority active-resource moves:

- `control/project_domain/runs/manifests -> control/project_domain/resources/manifests`
- `control/project_domain/runs/reports -> control/project_domain/resources/reports`
- `control/project_domain/runs/context_packages -> control/project_domain/resources/context_packages`
- `control/project_domain/runs/pptx_jobs -> control/project_domain/resources/pptx_jobs`
- `control/project_agent_ops/runs/manifests -> control/project_agent_ops/resources/manifests`
- `control/project_agent_ops/runs/reports -> control/project_agent_ops/resources/reports`
- `control/project_agent_ops/runs/smoke -> control/project_agent_ops/resources/smoke`
- `control/user_decisions/runs/*.md -> control/user_decisions/resources/reports/`
- `control/team/runs/*.md -> control/team/resources/reports/`

Archive-first moves:

- `control/project_domain/runs/component_split_ocr -> control/project_domain/archive/component_split_ocr`
- `control/project_domain/runs/intermediates -> control/project_domain/archive/intermediates`
- `control/project_domain/runs/logs -> control/project_domain/archive/logs`
- `control/project_domain/runs/object_isolation -> control/project_domain/archive/object_isolation`
- `control/project_domain/runs/pptx_extract -> control/project_domain/archive/pptx_extract`
- `control/project_agent_ops/runs/logs -> control/project_agent_ops/archive/logs`

## Validation Expectations

After migration:

- there should be no top-level:
  - `control/project_domain/runs`
  - `control/project_agent_ops/runs`
  - `control/user_decisions/runs`
  - `control/team/runs`
- nested `control/project_agent_ops/registry/runs` may remain
- path references in rules, reports, indexes, and handoffs must be updated

## Parallel Execution Design

Recommended implementation mode:

- `10` workers
- model:
  - `gpt-5.4`
- reasoning effort:
  - `xhigh`

Execution rule:

- each worker owns a disjoint write scope
- registry synchronization is deferred to the final registry owner lane
- final removal of empty top-level `runs` directories is coordinator-only

Worker lanes:

1. `W01` — `project_domain/runs/manifests`
2. `W02` — `project_domain/runs/reports`
3. `W03` — `project_domain/runs/context_packages`
4. `W04` — `project_domain` active resource bundle:
   - `added_screenshots`
   - `cross_validation`
   - `experiment_plans`
   - `imported_fourarm`
   - `pptx_jobs`
   - `smoke`
5. `W05` — `project_domain` archive bundle:
   - `component_split_ocr`
   - `intermediates`
   - `logs`
   - `object_isolation`
   - `pptx_extract`
6. `W06` — `project_agent_ops` manifests and plans
7. `W07` — `project_agent_ops` reports, smoke, and logs
8. `W08` — `user_decisions/runs`
9. `W09` — `team/runs` plus team migration-doc sync
10. `W10` — registry and path-index synchronization

Coordinator responsibilities:

- dispatch the 10 worker lanes
- merge in dependency order
- run final validation
- remove empty top-level `control/*/runs` directories

## Execution Companion

Use this packet together with:

- `control/team/resources/migration/CHECKLIST_control_runs_immediate_migration.md`
