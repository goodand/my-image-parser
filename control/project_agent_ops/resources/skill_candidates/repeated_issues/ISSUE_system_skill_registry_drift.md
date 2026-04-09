# Repeated Issue: System Skill Registry Drift

## Purpose

Record the recurring gap where built-in Codex system skills are usable in practice but absent from workspace-local inventory and setup references.

## Recurrence Signal

This issue appears when:

- a system skill is used in planning or implementation
- the workspace inventory only lists MCP launchers and custom skills
- later operators cannot see that the skill is already available
- adjacent registry surfaces such as `.vscode/mcp.json` and `tool_inventory.json` drift apart from the actual workspace state
- newly promoted repo-local skills exist under `skills/*` but are absent from the inventory snapshot
- a registry bucket such as `global_codex_skills_confirmed` accidentally mixes system/global skills with repo-local custom skills

## Current Workaround

- append the system skill to the workspace inventory
- add a short usage reference under `control/project_agent_ops/resources/tools_inventory/`
- cross-link it from the main MCP or tooling setup reference
- when drift is discovered, diff these three surfaces together:
  - `.codex/config.toml`
  - `.vscode/mcp.json`
  - `control/project_agent_ops/registry/tools/tool_inventory.json`
- also compare `tool_inventory.json` against `skills/*/SKILL.md` before treating the registry as current
- keep global/system skill lists separate from workspace custom skill paths or names
- when possible, use a subagent as a secondary read-only auditor, but keep the main agent's direct file diff as the canonical verdict if the subagent times out

## Structural Fix Candidate

- maintain a dedicated `system_skill_notes` section in tool inventory
- review system-skill coverage whenever a new workflow depends on one
- add a lightweight registry-audit pass whenever a new MCP or workspace skill is promoted

## Escalation Trigger

- another built-in skill becomes operationally important but is missing from workspace-local docs
- another workspace-local MCP or promoted skill is present in config or on disk but absent from the canonical tool list
- a global/system registry bucket starts to overclaim repo-local custom skills as if they were built-in runtime skills

## Related Evidence

- `control/project_agent_ops/resources/skill_candidates/repeated_issues/KB_repeated_issue_patterns.md`
