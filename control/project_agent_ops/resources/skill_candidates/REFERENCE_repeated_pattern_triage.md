# Repeated Pattern Triage

## Purpose

Decide whether a recurring observation belongs under repeated tasks or repeated issues.

## Use repeated tasks when

- the same bounded workflow is executed again and again
- a packet recipe or execution sequence keeps repeating
- a future skill, script, or checklist could absorb the pattern

Canonical bucket:

- `control/project_agent_ops/resources/skill_candidates/repeated_tasks/`

## Use repeated issues when

- the same failure mode or coordination problem keeps returning
- the problem affects multiple runs or providers
- the main value is guardrail or diagnosis, not execution recipe

Canonical bucket:

- `control/project_agent_ops/resources/skill_candidates/repeated_issues/`

## Quick test

- "Should we automate this repeated workflow?" -> repeated task
- "Should we guard against this repeated failure?" -> repeated issue

## Promotion sources

Repeated patterns commonly originate from:

- `feedback/claude/`
- `feedback/gemini/`
- `feedback/codex/`
- `feedback/subagent/`
- smoke reports
- run reports
- task-packet retrospectives

The source evidence should remain where it was first recorded.
The repeated-pattern file becomes the canonical reusable summary.

## Naming guidance

- repeated task:
  - `TASK_<topic>.md`
- repeated issue:
  - `ISSUE_<topic>.md`

Use `KB_*.md` only when a directory-level summary of multiple repeated entries is needed.

## Escalation heuristic

Create a repeated-pattern file when:

- the same thing has already happened more than once, or
- the next run is likely to hit the same pattern again, or
- the pattern is important enough that future agents should discover it without rereading old feedback logs

## Project-Start Interpretation

These buckets are part of the ongoing `project_agent_ops` document surface after project start.

- `repeated_tasks/` grows from recurring execution evidence
- `repeated_issues/` grows from recurring failure or friction evidence

Promotion rule:

- actor-specific note first appears in `feedback/`
- once the same pattern repeats, promote it into `repeated_tasks/` or `repeated_issues/`
