# Control Runs Immediate Migration Checklist

## Preconditions

- [ ] Confirm ADR 0002 is accepted:
  - `control/user_decisions/resources/adr/ADR_0002_workspace_plane_and_control_action_units.md`
- [ ] Regenerate migration inventory:
  - `python3 scripts/build_control_runs_migration_inventory.py`
- [ ] Verify inventory has zero unresolved top-level entries
- [ ] Confirm parallel worker plan:
  - `control/team/resources/migration/control_runs_migration_parallel_plan_at2026_03_30.json`
- [ ] Freeze current git status before moving files

## Directory Creation

- [ ] Create missing target directories under:
  - `control/project_domain/resources/`
  - `control/project_domain/archive/`
  - `control/project_agent_ops/resources/`
  - `control/project_agent_ops/archive/`
  - `control/user_decisions/resources/`
  - `control/team/resources/`

## Move Order

- [ ] Dispatch `10` workers on `gpt-5.4 xhigh` with disjoint write scopes
- [ ] Move `project_domain` active resources first
- [ ] Move `project_agent_ops` active resources second
- [ ] Move `user_decisions` and `team` reports third
- [ ] Move archive-classified material last
- [ ] Run registry synchronization after all move lanes complete

## Post-Move Sync

- [ ] Update path references in:
  - rules
  - reports
  - registries
  - handoffs
  - specs
- [ ] Regenerate any path-based inventory files that changed

## Validation

- [ ] `python3 -m json.tool` on changed JSON registries
- [ ] `rg -n "control/.*/runs" control` only matches allowed nested registry paths or historical references intentionally retained
- [ ] No top-level `control/*/runs` directories remain
- [ ] Canonical packet paths in migration inventory still resolve

## Done Definition

- [ ] top-level `runs` buckets under the four control columns are removed
- [ ] moved artifacts resolve under `resources` or `archive`
- [ ] nested `registry/runs` remains intact where still semantically correct
- [ ] rules and indexes no longer describe `runs` as a primary action unit
- [ ] worker plan and actual migration result agree on ownership boundaries
