# Repeated Issue: Vendored Runtime Bootstrap Permission Drift

## Purpose

Capture the recurring risk that vendored MCP bootstrapping can fail or look incomplete because sandbox permissions and long-running installs obscure the real status.

## Recurrence Signal

This issue appears when:

- a venv is created under `vendor/mcp/`
- package installation requires escalated execution
- the install session runs long enough that intermediate output is misleading

## Current Workaround

- rerun blocked steps with explicit escalation
- verify completion using concrete checks:
  - executable exists
  - import succeeds
  - `--help` or boot smoke succeeds
- when the launcher is a shell script under workspace control, invoke it through `bash` instead of assuming the path itself is executable

## Structural Fix Candidate

- standard bootstrap checklist for vendored Python MCPs
- always verify by artifact state, not only by intermediate process output

## Escalation Trigger

- the same permission or ambiguous-install-state pattern appears on another vendored MCP integration

## Related Evidence

- `control/project_agent_ops/resources/skill_candidates/repeated_issues/KB_repeated_issue_patterns.md`
