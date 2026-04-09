# Repeated Task: Vendored Python MCP Bootstrap

## Purpose

Capture the recurring workflow for onboarding a Python-based MCP into this workspace without touching the main workspace runtime.

## Recurrence Signal

This task shape recurs when:

- a new Python MCP is vendored under `vendor/mcp/`
- the MCP should stay isolated from `.venv`
- the server needs a dedicated launcher and workspace registration

## Canonical Flow

1. vendor the upstream source under `vendor/mcp/`
2. create a dedicated venv inside the vendored directory
3. install the package into that venv
4. create a thin wrapper under `scripts/mcp/`
5. register the server in `.codex/config.toml`
6. register the server in `.vscode/mcp.json` if VS Code MCP use matters
7. update tool inventory and session registry
8. run a bounded boot or help smoke before treating the server as active

## Why This Pattern Matters

- avoids contaminating the main workspace runtime
- keeps removal and rebuild bounded to the vendored MCP
- fits the patch philosophy better than rewriting stable workspace scripts

## Promotion Target

- bootstrap checklist
- helper script
- MCP onboarding skill or packet template

## Current Promotion Status

- promoted into repo-local skill: `skills/vendored-mcp-onboarding`
- use the skill to standardize onboarding order before touching launcher, config, inventory, or smoke evidence

## Related Evidence

- `control/project_agent_ops/resources/skill_candidates/repeated_tasks/KB_repeated_task_patterns.md`
