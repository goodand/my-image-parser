# Workspace Structure

## Structure Philosophy

이 workspace의 canonical 구조 철학은 다음으로 고정한다.

- `root > control > project meaning > action unit`
- root는 runtime plane이다
- `control/`은 canonical coordination / governance / decision-truth plane이다
  - 다시 읽어서 판단 기준으로 삼는 것
  - canonical source of truth로 삼는 것
  - 다른 주체와 상태를 맞출 때 참조하는 것
- project meaning은 4종으로 유지한다
  - `project_domain`
  - `project_agent_ops`
  - `user_decisions`
  - `team`
- action unit은 3종으로 축소한다
  - `resources`
  - `registry`
  - `archive`

키워드:

- 상태
- 조건
- 정합성
- 결정
- 동기화
- 정적
- 동적
- 재사용
- 다시 읽기

This workspace uses a split layout:

- workspace root for runtime assets and executable code
- `control/` for the Git-managed control plane

## Workspace Root Directories

- `analysis/`: extracted images and inspection artifacts
- `control/`: Git-managed control root for canonical coordination, registry, reusable bodies, and archives
- `context_portal/`: ConPort local database files
- `data/`: MCP runtime data such as SQLite files
- `input/`: incoming files such as PPTX inputs
- `logs/`: runtime logs
- `scripts/`: workspace executable scripts and launchers
- `scripts/mcp/`: MCP launcher wrappers
- `skills/`: workspace-local Agent Skills
- `vendor/`: vendored runtime dependencies and tool sources
- `.codex-tasks/`: Taskmaster recovery artifacts

## Control Root Layout

The canonical tree is ordered by:

1. project meaning
2. action unit

Project-meaning buckets:

- `control/user_decisions/`
- `control/project_domain/`
- `control/project_agent_ops/`
- `control/team/`

Action-unit buckets inside each project-meaning bucket:

- `resources/`
- `registry/`
- `archive/`

## Resource Secondary Kinds

`resources/` is the primary action unit for active rereadable bodies.

Inside `resources/`, use these secondary kinds as the placement rule:

- `reference`
- `evidence`
- `material`

These are not a second filesystem depth layer that must be inserted everywhere.

They are the interpretation rule for existing subdirectories and the naming rule for future subdirectories.

### Reference Resources

Use for stable guidance, rules, plans, reusable contracts, and rereadable normative content.

Typical examples:

- `rules/`
- `templates/`
- `specs/`
- `references/`
- `knowledge_bases/`
- `master_plans/`
- `checklists/`
- `contracts/`
- `task_packets/`
- `troubleshooting/`
- `adr/`
- `notes/`
- `closed_questions/`
- `experiment_plans/`

Placement boundary inside reference resources:

- `control/project_domain/resources/master_plans/`
  - canonical home for stable pipeline meaning, architecture, execution flow, phased rollout, and experiment framing
- `control/user_decisions/resources/notes/`
  - canonical home for user-facing decision-support overlays such as dashboards, scoreboards, task graphs, and current-state snapshots

Interpretation rule:

- if a document primarily defines how the system should work, it stays in `master_plans`
- if a document primarily helps the user understand current status, bottlenecks, or choice points, it belongs in `user_decisions/resources/notes`
- user-facing markdown notes under `control/user_decisions/resources/notes/` should prefer a minute-level timestamp suffix such as `-atYYYY-MM-DD-HH-MM`
- user-facing note overlays under `control/user_decisions/resources/notes/` are allowed to be dated even when they reuse prefixes like `REFERENCE_` or `CHECKLIST_`; they are treated as overlays, not stable canonical spec bodies
- symbolic-link export should be directory-first:
  - default shared views should prefer directory symlinks over many file-level symlinks
  - file-level symlinks should be created only when the user explicitly asks for them
- symlink alias names should include the workspace name when exported to shared Symbolic_links space
  - example: `my-image-parser__user_decisions__notes`
  - example: `my-image-parser__REFERENCE_surface_purpose_consumer_system_kind_model-at2026-04-05-09-17.md`
- when a user explicitly asks for a shared markdown shortcut or shared user-facing export, prefer the symbolic-link helper over ad-hoc manual linking:
  - default directories: `python3 control/team/resources/scripts/sync_symbolic_links.py sync-defaults`
  - explicit file: `python3 control/team/resources/scripts/sync_symbolic_links.py link-file <markdown-path>`
  - VS Code task labels:
    - `Control: Sync Default User-Facing Symbolic Links`
    - `Control: Create Symbolic Link For Current Markdown`

### Evidence Resources

Use for active result bodies that justify, compare, validate, or explain a state transition or judgment.

Typical examples:

- `reports/`
- `manifests/`
- `smoke/`
- `feedback/`
- `migration/`
- `cross_validation/`

### Material Resources

Use for active concrete payloads or bundled materials that are reread or reused downstream.

Typical examples:

- `assets/`
- `context_packages/`
- `pptx_jobs/`
- `imported_fourarm/`
- `external_repos/`
- `vendor_skills/`
- `codebase_graph/`

### Control-Maintenance Exception

Executable helpers should prefer root `scripts/`.

`control/*/resources/scripts/` is allowed only as a narrow exception for control-plane maintenance utilities.

Interpretation rule:

- Skills, MCP, CLI 같은 directory-unit runtime bodies는 root에 둔다
- `control/`에는 runtime body 자체를 넣지 않고, 그것에 대한:
  - 규칙
  - inventory
  - session path map
  - contracts
  - smoke/report
    를 둔다

Current example:

- `control/team/resources/scripts/lint_control_tree.py`

## Current Canonical Control Files

- `control/project_agent_ops/resources/tools_inventory/REFERENCE_mcp_setup.md`
- `control/team/resources/rules/RULES_development_team_operating_playbook.md`
- `control/team/resources/rules/RULES_workspace_structure.md`
- `control/project_domain/resources/references/REFERENCE_project_start_document_map.md`
- `control/project_agent_ops/resources/feedback/REFERENCE_feedback_filing_guide.md`
- `control/project_agent_ops/resources/skill_candidates/REFERENCE_repeated_pattern_triage.md`
- `control/project_domain/resources/references/REFERENCE_desktop_screenshot_agent_graph_ir.md`
- `control/project_agent_ops/resources/contracts/codex_mcp_snippet.toml`
- `control/project_agent_ops/registry/runtime/session_paths.json`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/`
- `control/project_domain/resources/specs/contracts/presentation_image_pipeline_spec.json`
- `control/team/resources/migration/REFERENCE_control_runs_immediate_migration_packet-at2026-03-30.md`
- `control/team/resources/reports/REPORT_registry_runs_residual_cleanup_execution-at2026-03-30-16-57.md`

## Notes

- Runtime databases are intentionally kept inside the workspace for inspection and portability.
- `control/project_agent_ops/registry/runtime/session_paths.json` is the canonical path map for future sessions.
- `control/project_agent_ops/registry/jobs/image_caption_jobs/` is the canonical registry home for image-caption job bodies and related execution-linked ledger files.
- root `scripts/` is the canonical executable script surface for workspace automation.
- MCP wrapper scripts in `scripts/mcp/` should be treated as the executable truth for workspace MCP startup behavior.
- `vendor/` stores vendored runtime dependencies and MCP/tool source trees, not control-plane truth bodies.
- root `skills/` stores skill package bodies; skill inventory and path synchronization belong in registry files such as `registry/tools/tool_inventory.json` and `registry/runtime/session_paths.json`, not in a separate `registry/skills/` namespace.
- agent and model feedback belongs under `control/project_agent_ops/resources/feedback/`
- repeated task and issue pattern documents belong under `control/project_agent_ops/resources/skill_candidates/`
- Artifact format is handled by filename rules and file extensions, not by top-level control buckets.
- Historical top-level shells such as `control/docs/`, `control/resources/`, `control/runs/`, `control/registry/`, `control/legacy/`, and `control/archive/` are not canonical and should not exist after migration cleanup.
- top-level `control/{project_meaning}/runs` directories are not canonical and should not exist after the completed 2026-03-30 migration.
- `control/project_agent_ops/registry/runs/` is no longer canonical after the completed residual cleanup on 2026-03-30 and should not exist.
- `control/project_agent_ops/registry/skills/` is not canonical and should not exist unless a real skill-registry body is introduced later.

## Project-Start Agent-Ops Documents

After project start, `project_agent_ops` should be treated as the canonical home for the ongoing agent-operation document set.

This set includes:

- provider and subagent feedback under `control/project_agent_ops/resources/feedback/`
- repeated task patterns under `control/project_agent_ops/resources/skill_candidates/repeated_tasks/`
- repeated issue patterns under `control/project_agent_ops/resources/skill_candidates/repeated_issues/`
- reusable packet forms under:
  - `control/project_agent_ops/resources/task_packets/standard/`
  - `control/project_agent_ops/resources/task_packets/canonical/`

Boundary rule:

- `feedback/` stores observed execution notes tied to a provider or worker role
- `repeated_tasks/` stores recurring execution recipes that may later become a skill, checklist, or script
- `repeated_issues/` stores recurring failure modes, coordination friction, or guardrail needs
