# Backlog: REFERENCE_mcp_setup.md system_skill_notes cross-link

## Canonical Name

`BACKLOG_setup_ref_system_skill_cross_link`

## Owner

`vendored-mcp-onboarding` (owner-family entrypoint)

## Status

Open — contained via documentation but not structurally resolved.

## Problem

`tool_inventory.json` carries `workspace_skills.system_skill_notes` (e.g., `imagegen`), but `REFERENCE_mcp_setup.md` does not cross-link or reference that section. This means one canonical owner output knows about system skills while the other does not.

## Structural Fix

Add a `System Skills` section to `REFERENCE_mcp_setup.md` that points to `tool_inventory.json` `workspace_skills.system_skill_notes` and lists the currently tracked system skills with their status.

## Blocked By

Original task non-goal: direct modification of `REFERENCE_mcp_setup.md` was out of scope for the 2026-04-01 owner-family hardening pass.

## Closure Condition

- `REFERENCE_mcp_setup.md` has a section that references `system_skill_notes`
- At least `imagegen` is listed with its current status
- The `mcp_inventory_sync_checklist.md` system-skill gate no longer flags partial coverage for known system skills

## References

- `control/project_agent_ops/resources/skill_candidates/repeated_issues/ISSUE_system_skill_registry_drift.md`
- `skills/vendored-mcp-onboarding/references/tool-owner-family-map.md` (Open issue note)
- `skills/vendored-mcp-onboarding/checklists/mcp_inventory_sync_checklist.md` (Section 8 system-skill gate)
