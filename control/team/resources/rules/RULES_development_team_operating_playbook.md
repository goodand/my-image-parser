# Development Team Operating Playbook

## Purpose

This document is the workspace-local team operating ruleset for `my-image-parser`.
It adapts the external development playbook good case into the actual structure, tools, and workflow used in this repository.

The goal is simple:

- keep workflow ordering stable
- keep TDD and smoke execution practical
- keep task-packet use bounded
- keep workspace and environment rules explicit

## Derived From

- External good case:
  - `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/claude-gemini-communicator/skills/Skills-Create-Project/codebase-analysis/references/codebase-analysis-development-playbook-at2026-03-23-03-36.md`

This local document is the active rule document for this workspace.
The external file remains a reference only.

## Source Of Truth

Primary local references:

- [RULES_workspace_structure.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/team/resources/rules/RULES_workspace_structure.md)
- [RULES_filename_and_linting.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/team/resources/rules/RULES_filename_and_linting.md)
- [REFERENCE_project_start_document_map.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/references/REFERENCE_project_start_document_map.md)
- [MASTER_PLAN_presentation_image_pipeline.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md)
- [presentation_image_pipeline_spec.json](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/specs/contracts/presentation_image_pipeline_spec.json)
- [SPEC_openai_image_caption_runner.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/specs/prose/SPEC_openai_image_caption_runner.md)
- [REFERENCE_mcp_setup.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_agent_ops/resources/tools_inventory/REFERENCE_mcp_setup.md)
- [REFERENCE_feedback_filing_guide.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_agent_ops/resources/feedback/REFERENCE_feedback_filing_guide.md)
- [REFERENCE_repeated_pattern_triage.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_agent_ops/resources/skill_candidates/REFERENCE_repeated_pattern_triage.md)
- [session_paths.json](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_agent_ops/registry/runtime/session_paths.json)

Important active experiment profile:

- [PLAN_codebase_per_image_caption_experiment_comparison-at2026-03-27-16-46.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/master_plans/drafts/PLAN_codebase_per_image_caption_experiment_comparison-at2026-03-27-16-46.md)

## Scope

This playbook governs:

1. workflow ordering for implementation and experiment work
2. TDD and validation ordering
3. smoke execution policy
4. task-packet usage
5. workspace and environment policy

This playbook does not replace:

- domain-specific pipeline specs
- filename or linting rule details
- import-boundary-specific rule docs

## Required Control Buckets

These buckets must be treated as canonical destinations when new reusable artifacts are created:

- `control/project_domain/resources/knowledge_bases/`
- `control/project_domain/resources/checklists/`
- `control/project_agent_ops/resources/task_packets/standard/`
- `control/project_agent_ops/resources/task_packets/canonical/`
- `control/project_agent_ops/resources/feedback/`
- `control/project_agent_ops/resources/skill_candidates/repeated_tasks/`
- `control/project_agent_ops/resources/skill_candidates/repeated_issues/`

Do not invent parallel ad hoc buckets when one of these already matches the artifact role.

Agent-ops sub-bucket rules:

- provider or agent feedback goes under `control/project_agent_ops/resources/feedback/`
- reusable subagent feedback goes under `control/project_agent_ops/resources/feedback/subagent/`
- repeated task patterns go under `control/project_agent_ops/resources/skill_candidates/repeated_tasks/`
- repeated issue patterns go under `control/project_agent_ops/resources/skill_candidates/repeated_issues/`

### Project-Start Ongoing Agent-Ops Documents

Treat these as the minimum ongoing document set that should keep growing after project start:

- `feedback/`
  - Claude, Gemini, Codex, and subagent-specific operating feedback
- `repeated_tasks/`
  - recurring bounded workflows and packetizable execution shapes
- `repeated_issues/`
  - recurring failure modes, friction patterns, and standing guardrail candidates

Filing rule:

- if the note is tied to one provider or one worker role, file it under `feedback/`
- if the same workflow keeps recurring across runs, promote it into `repeated_tasks/`
- if the same failure or coordination problem keeps recurring, promote it into `repeated_issues/`

## Progress Management

Use this order unless there is a strong reason not to:

1. source grounding
2. master plan and spec confirmation
3. bounded draft or experiment plan
4. task packet definition when handoff or bounded execution is needed
5. implementation with tests
6. smoke execution
7. artifact promotion into KB, checklist, report, or canonical packet

Rules:

- evidence before completion
- validation before mutation
- patch and append existing canonical docs before creating parallel canonical docs
- when a new canonical file is created, update `session_paths.json` if the file is likely to be reused in future sessions

## Workflow

### Step 1. Read Canonical Context First

Before changing code or control artifacts, read the minimum local context:

- workspace structure rules
- filename and linting rules
- active master plan
- relevant spec or contract
- `session_paths.json` for path lookup

### Step 2. Fix The Working Boundary

Decide whether the task is:

- a small bounded local change
- an experiment slice
- an MCP or skill operation change
- a broader pipeline extension

Then choose the smallest valid control artifact:

- patch active canonical doc
- or add a dated draft plan
- or create a bounded task packet

### Step 3. Freeze The Contract Before Implementation

For script or workflow work, define:

- input contract
- output contract
- done definition
- required checks

For experiment work, also define:

- dataset
- output location
- comparison surface
- evaluation dimensions

### Step 4. Implement Small Vertical Slices

Prefer slices that can be verified immediately.

Examples in this workspace:

- one-image caption run
- one dataset-jsonl smoke
- one screenshot capture smoke
- one MCP boot verification

### Step 5. Validate And Record Evidence

The result is not complete until:

- relevant tests pass
- relevant smoke passes
- artifacts are written to their canonical locations
- the report or plan reflects the actual state

## TDD Policy

### Contract First

Before changing behavior:

- restate the output contract
- identify the minimum failing case
- define the exact validation surface

### Preferred Test Order

1. syntax or compile check
2. unit or script-level test
3. one bounded smoke
4. wider batch or comparison run

### Workspace-Specific TDD Guidance

- for Python scripts, keep tests or smoke aligned with the actual CLI contract
- when changing `scripts/caption_images_openai.py`, start with one-image smoke or `--limit 1`
- when changing screenshot flow, keep capture and caption validation as separate boundaries
- when changing MCP orchestration, verify state persistence and completion rules before broad runs

## Smoke Test Policy

### Smoke Comes Before Broad Runs

Every new execution path should prove itself on the smallest practical case first.

Preferred smoke shapes in this workspace:

- one image from `control/project_domain/resources/assets/added_screenshots/`
- one row from a dataset JSONL with `--limit 1`
- one PPT slide screenshot capture fixture
- one MCP boot verification

### Smoke Report Requirements

A smoke report should record:

- purpose
- input artifact
- command
- output artifact paths
- pass or fail result
- notes about constraints or sandbox issues

Canonical smoke location:

- `control/project_agent_ops/resources/smoke/`
- or `control/project_domain/resources/smoke/` when the smoke is clearly domain-output specific

### Hard Rule

Do not scale to batch execution before the smallest smoke run is readable and reproducible.

## Task Packet Policy

### When Task Packets Are Required

Use a task packet when:

- work is handed to another agent or subagent
- the change must be bounded to certain paths
- done definition and checks must be fixed before execution
- more than one execution pass or role handoff is expected

### Canonical Locations

- reusable template or starter packet:
  - `control/project_agent_ops/resources/task_packets/standard/`
- reusable team-approved richer packet:
  - `control/project_agent_ops/resources/task_packets/canonical/`
- issued execution-bounded packet for a concrete pass:
  - `control/project_agent_ops/resources/task_packets/issued/`

### Minimum Packet Fields

- `goal`
- `allowed_paths`
- `context_files`
- `constraints`
- `done_definition`
- `required_checks`
- `deliverables`

Optional but recommended for parallel or role-separated work:

- `non_goals`
- `forbidden_paths`
- `depends_on`
- `parallel_group`
- `trace_id`

### Rule

Task packets are bounded execution contracts, not runtime state trackers.
Do not put heartbeat, PID, or live session state into canonical packets.
Use `issued/` for a concrete execution pass, and keep `canonical/` for reusable accepted packet forms.

## Workspace And Environment Policy

### Workspace Layout

Use the split layout already fixed in `RULES_workspace_structure.md`.

Canonical meanings:

- workspace root for executable code and runtime assets
- `control/` for Git-managed control artifacts

### Current Runtime Surface

- Python environment:
  - `.venv`
- MCP launchers:
  - `scripts/mcp/`
- local skills:
  - `skills/`
- runtime logs:
  - `logs/`
- runtime databases:
  - `data/agent-task-manager/`
  - `context_portal/`

### Environment Rules

- use `.env` for local API key configuration
- use `.env.example` only as a placeholder contract
- do not hardcode secrets into control artifacts or scripts
- treat wrapper scripts in `scripts/mcp/` as the executable truth for MCP startup behavior

### Path Registry Rule

If a new canonical file becomes operationally important, add it to:

- `control/project_agent_ops/registry/runtime/session_paths.json`

This keeps future sessions from re-discovering the same path structure manually.

## Tool Boundary Policy

### Skills

- skills are workflow and orchestration surfaces
- skills should not silently replace canonical specs or registries

### MCP

- MCP is the preferred control and data plane when orchestration or state tracking matters
- MCP output should not replace canonical local docs by default

### Scripts

- scripts are the executable truth for local repeatable behavior
- reports and plans should reference the script path rather than restating behavior loosely

### External References

- external good cases stay indexed-only unless promoted into a local artifact
- once a local adapted version exists, the local artifact becomes the active workspace rule

## Git And Parallel Work Policy

- small bounded changes may use the main working copy
- parallel or role-separated work may use worktrees
- do not spread one bounded implementation task across multiple writing roots without an explicit reason
- do not create or retain canonical artifacts under legacy control shells such as `control/docs/`, `control/resources/`, `control/runs/`, `control/registry/`, or `control/archive/`

## Completion Gate

Work is only complete when all of the following are true:

1. the contract is implemented or updated
2. the relevant validation has been rerun
3. the evidence is recorded in the proper control location
4. canonical references and registries are updated when needed
5. the result can be rediscovered by a future session without informal memory

## One-Line Summary

Read the local canonical rules first, freeze the contract, implement the smallest verifiable slice, run smoke before scale, and store every durable artifact in the existing canonical control buckets.
