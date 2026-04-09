# Repeated Task: Model-Backed MCP Activation And Smoke

## Purpose

Capture the recurring workflow for turning a vendored, model-backed MCP into an actually usable local tool surface.

## Recurrence Signal

This task shape recurs when:

- an MCP depends on local model downloads or post-install setup
- the server boots before inference tools are truly usable
- launcher, cache path, and runtime smoke all need to be verified together

## Canonical Flow

1. vendor and isolate the MCP runtime under `vendor/mcp/`
2. create a thin launcher under `scripts/mcp/`
3. redirect logs and writable caches into workspace-owned paths
4. run upstream post-install or model download steps
5. verify light surface first:
   - executable exists
   - stdio boot or tool listing works
6. verify heavy surface second:
   - one metadata or config tool
   - one actual inference tool
7. register the MCP only after both light and heavy smokes succeed

## Why This Pattern Matters

- prevents false positives where the server boots but core tools still fail
- keeps model cache writes out of source-controlled vendor paths
- makes community MCP adoption less fragile in sandboxed environments

## Promotion Target

- model-backed MCP activation checklist
- launcher helper template
- troubleshooting reference for post-install and smoke order

## Current Promotion Status

- partially promoted into repo-local skill: `skills/vendored-mcp-onboarding`
- the skill now captures the light-smoke then heavy-smoke activation order for model-backed MCPs

## Related Evidence

- `scripts/mcp/start-imagesorcery-mcp.sh`
- `vendor/mcp/imagesorcery-mcp/`
- `control/project_agent_ops/resources/skill_candidates/repeated_tasks/KB_repeated_task_patterns.md`
