# Repeated Issue: Stdio Stdout Pollution In Machine-Readable MCP

## Purpose

Capture the recurring risk that a stdio MCP emits human-readable text on stdout and interferes with machine-readable transport.

## Recurrence Signal

This issue appears when:

- a vendored MCP uses stdio transport
- startup code contains `print(...)` or default stdout logging
- third-party libraries emit banners or status lines during import or first inference

## Current Workaround

- move launcher and server diagnostics to stderr
- patch vendored logging handlers away from stdout
- redirect noisy library stdout to stderr during import or model load
- verify with a real MCP client transport instead of assuming raw shell output is authoritative

## Structural Fix Candidate

- add a standard stdio hygiene review to vendored MCP onboarding
- keep a launcher rule that reserves stdout strictly for MCP transport
- require one client-based tool-call smoke before marking stdio boot as verified

## Escalation Trigger

- another vendored MCP shows mixed human-readable stdout and MCP traffic
- a tool call succeeds only after stderr redirection or launcher patching

## Related Evidence

- `vendor/mcp/imagesorcery-mcp/src/imagesorcery_mcp/logging_config.py`
- `vendor/mcp/imagesorcery-mcp/src/imagesorcery_mcp/server.py`
- `control/project_agent_ops/resources/skill_candidates/repeated_issues/KB_repeated_issue_patterns.md`
