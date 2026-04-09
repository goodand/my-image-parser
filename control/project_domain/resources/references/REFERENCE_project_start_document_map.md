# Project Start Document Map

## Purpose

Define the canonical document split between `project_domain`, `user_decisions`, and `project_agent_ops` after project start.

This file is the routing reference for new reusable documents.

## Core split

Use `control/project_domain/` when the document is about:

- product or pipeline meaning
- experiment design or evaluation framing
- domain resources and datasets
- canonical specs, master plans, knowledge bases, and checklists

Use `control/user_decisions/` when the document is about:

- user-facing decision support
- closed questions and choice framing
- progress dashboards and scoreboards
- task graphs and current-state snapshots that help the user understand bottlenecks or tradeoffs

Use `control/project_agent_ops/` when the document is about:

- agent execution
- MCP setup and operational constraints
- feedback about Claude, Gemini, Codex, or subagents
- repeated task patterns and repeated issue patterns
- task packets, handoffs, and runtime coordination

## Canonical destinations after project start

### Project domain documents

- master plans:
  - `control/project_domain/resources/master_plans/`
- knowledge bases:
  - `control/project_domain/resources/knowledge_bases/`
- checklists:
  - `control/project_domain/resources/checklists/`
- specs and contracts:
  - `control/project_domain/resources/specs/`
- references:
  - `control/project_domain/resources/references/`

### User decision documents

- closed questions:
  - `control/user_decisions/resources/closed_questions/`
- decision-support notes:
  - `control/user_decisions/resources/notes/`
- decision-facing reports:
  - `control/user_decisions/resources/reports/`

### Agent-ops documents

- feedback root:
  - `control/project_agent_ops/resources/feedback/`
- provider feedback:
  - `control/project_agent_ops/resources/feedback/claude/`
  - `control/project_agent_ops/resources/feedback/gemini/`
  - `control/project_agent_ops/resources/feedback/codex/`
- subagent feedback:
  - `control/project_agent_ops/resources/feedback/subagent/`
- repeated task patterns:
  - `control/project_agent_ops/resources/skill_candidates/repeated_tasks/`
- repeated issue patterns:
  - `control/project_agent_ops/resources/skill_candidates/repeated_issues/`
- task packets:
  - `control/project_agent_ops/resources/task_packets/`

## Minimum post-start document set

After project start, the workspace should maintain at least these reusable document buckets.

### Project domain minimum set

- one active master plan under `control/project_domain/resources/master_plans/`
- one or more domain references under `control/project_domain/resources/references/`
- knowledge bases under `control/project_domain/resources/knowledge_bases/`
- checklists under `control/project_domain/resources/checklists/`
- specs or contracts under `control/project_domain/resources/specs/`

### User decisions minimum set

- one or more closed-question or decision-support notes under `control/user_decisions/resources/`
- dashboards, scoreboards, or task-graph overlays under `control/user_decisions/resources/notes/`

### Agent-ops minimum set

- provider and subagent feedback under `control/project_agent_ops/resources/feedback/`
- repeated task patterns under `control/project_agent_ops/resources/skill_candidates/repeated_tasks/`
- repeated issue patterns under `control/project_agent_ops/resources/skill_candidates/repeated_issues/`
- standard and canonical task packets under `control/project_agent_ops/resources/task_packets/`

## Canonical meaning of the agent-ops buckets

- `feedback/` stores observed model or agent behavior and operating notes.
- `repeated_tasks/` stores recurring workflow shapes that may deserve a skill, checklist, or script.
- `repeated_issues/` stores recurring failure modes or friction patterns that need guardrails.
- `task_packets/` stores bounded execution handoff artifacts for main-agent or subagent work.

## Project-Start Ongoing Documents

After project start, the following should be treated as the ongoing `project_agent_ops` document surface:

- `feedback/`
  - provider-specific notes for Claude, Gemini, and Codex
  - delegated-worker notes under `feedback/subagent/`
- `repeated_tasks/`
  - recurring execution recipes, packetizable workflows, and future skill candidates
- `repeated_issues/`
  - recurring failure modes, naming friction, context gaps, and coordination guardrails

Operational distinction:

- `feedback/` is evidence-first and actor-specific
- `repeated_tasks/` is recipe-first and reuse-oriented
- `repeated_issues/` is guardrail-first and diagnosis-oriented

## Filing rules

1. If the document explains the pipeline itself, file it under `project_domain`.
2. If the document helps the user understand current status, bottlenecks, or decision tradeoffs, file it under `user_decisions`.
3. If the document explains how agents operate on the pipeline, file it under `project_agent_ops`.
4. If the same insight has both domain meaning and agent-ops meaning, keep the canonical version in one place and cross-reference it from the other.
5. Do not put repeated task or repeated issue notes under `feedback/`.
6. Do not put provider feedback under `project_domain`.
7. Do not keep decision-support overlays such as dashboards or task graphs in `master_plans`; move them to `control/user_decisions/resources/notes/` and leave a redirect stub if needed.
8. If a feedback note keeps recurring, promote it into `repeated_tasks/` or `repeated_issues/` and leave the feedback file as evidence, not as the canonical rule.

## Examples

- "which caption path should be the default?" -> `project_domain/resources/master_plans/`
- "what is blocked right now and what can I decide next?" -> `user_decisions/resources/notes/`
- "Subagent thread cap changes only apply after a new session" -> `project_agent_ops/resources/skill_candidates/repeated_issues/`
- "Codex was effective for packetized caption shards but packet naming caused lint friction" -> `project_agent_ops/resources/feedback/codex/`
