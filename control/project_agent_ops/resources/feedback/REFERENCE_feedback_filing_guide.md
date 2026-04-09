# Feedback Filing Guide

## Purpose

Standardize how provider and subagent feedback is recorded in this workspace.

## Canonical buckets

- Claude: `control/project_agent_ops/resources/feedback/claude/`
- Gemini: `control/project_agent_ops/resources/feedback/gemini/`
- Codex: `control/project_agent_ops/resources/feedback/codex/`
- Subagent: `control/project_agent_ops/resources/feedback/subagent/`

## What belongs in feedback

- what worked well
- what created friction
- what context was missing
- what should be adjusted next time
- provider-specific strengths or weaknesses observed in this workspace

## Canonical use after project start

Use feedback when the main value is an observed execution note tied to a provider or agent role.

Treat `feedback/` as one of the ongoing project-start document buckets, not as a temporary scratch area.

Typical buckets:

- `feedback/claude/` for Claude-specific behavior notes
- `feedback/gemini/` for Gemini-specific behavior notes
- `feedback/codex/` for Codex-specific behavior notes
- `feedback/subagent/` for worker or delegated-agent operating notes

Keep feedback entries concise and evidence-oriented.
If the same lesson appears across multiple runs, do not keep rewriting it as raw feedback forever.

Project-start interpretation:

- `feedback/` is where provider and subagent observations accumulate first
- promotion happens later only when a note becomes reusable beyond one actor-specific observation

## What does not belong in feedback

- repeated operational failure patterns that are broader than one provider
- generalized task recipes
- domain-level experiment conclusions

Those belong in:

- repeated issues:
  - `control/project_agent_ops/resources/skill_candidates/repeated_issues/`
- repeated tasks:
  - `control/project_agent_ops/resources/skill_candidates/repeated_tasks/`
- domain plans or KBs:
  - `control/project_domain/resources/`

## Promotion rule

Promote a feedback insight out of `feedback/` when one of these becomes true:

- the same workflow keeps recurring and should become a reusable task pattern
- the same failure or friction keeps recurring and should become a reusable issue pattern
- the note has become a standing operating rule rather than a one-run observation

Promotion destinations:

- reusable workflow shape -> `skill_candidates/repeated_tasks/`
- reusable failure or guardrail -> `skill_candidates/repeated_issues/`
- domain conclusion -> `project_domain/resources/`

## Minimum entry fields

- date
- context
- positive signal
- friction or risk
- follow-up action

## Recommended filename pattern

- `FEEDBACK_<topic>-atYYYY-MM-DD.md`

For provider-specific files, keep them in the provider bucket instead of flattening them at the root.

## Cross-link rule

When a feedback entry causes a repeated-task or repeated-issue file to be created:

- keep the original feedback file
- add a link from the new repeated-pattern file back to the originating feedback evidence
- do not move the original feedback note into the repeated-pattern bucket
