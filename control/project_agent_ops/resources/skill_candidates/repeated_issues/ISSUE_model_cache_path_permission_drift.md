# Repeated Issue: Model Cache Path Permission Drift

## Purpose

Capture the recurring risk that model-backed tools try to write settings, caches, or persistent metadata into source-tree paths that are not reliable under the active runtime.

## Recurrence Signal

This issue appears when:

- an MCP uses ML libraries that auto-create cache or settings files
- the upstream default path points into the vendored source tree
- sandboxed or restricted runs fail on cache writes while the same tool works after path override

## Current Workaround

- redirect model and settings cache paths into workspace-owned writable directories
- prefer launcher-exported env vars over in-tool hardcoded defaults
- rerun the same tool after path override to confirm the failure was environmental, not model-related

## Structural Fix Candidate

- standard cache-path override block for model-backed MCP launchers
- dedicated checklist item for writable cache and settings paths before heavy smoke
- inventory note recording which env vars stabilize the runtime

## Escalation Trigger

- another vendored ML tool fails because it tries to write caches or settings under vendor source paths
- inference succeeds only after a launcher-level cache override

## Related Evidence

- `scripts/mcp/start-imagesorcery-mcp.sh`
- `vendor/mcp/imagesorcery-mcp/src/imagesorcery_mcp/tools/detect.py`
- `vendor/mcp/imagesorcery-mcp/src/imagesorcery_mcp/tools/find.py`
- `control/project_agent_ops/resources/skill_candidates/repeated_issues/KB_repeated_issue_patterns.md`
