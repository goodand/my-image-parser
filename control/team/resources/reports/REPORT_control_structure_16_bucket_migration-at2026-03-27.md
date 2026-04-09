# Control Structure 16-Bucket Migration Report

## Purpose

Record the migration of the current workspace control artifacts into the `project meaning -> action unit` model.

## Model

- project meaning:
  - `user_decisions`
  - `project_domain`
  - `project_agent_ops`
  - `team`
- action unit:
  - `resources`
  - `runs`
  - `registry`
  - `archive`

## Current Workspace Sources Classified In This Step

- `.codex-tasks/20260326-structure-mcp-verification/SPEC.md`
- `.codex-tasks/20260326-structure-mcp-verification/PROGRESS.md`
- `control/project_domain/runs/manifests/added_screenshots_manifest_at2026_03_27.json`
- `control/project_domain/runs/cross_validation/index.json`

## Result

- task-structure spec moved into `control/project_agent_ops/runs/experiment_plans/`
- task progress moved into `control/project_agent_ops/runs/reports/`
- domain manifests moved into `control/project_domain/runs/manifests/`
- team rule registry added at `control/team/registry/rule_index.json`

## Scope

This report classifies only current workspace artifacts. External workspaces remain out of scope and should be referenced through registries rather than imported into the active control tree.
