# Codex Feedback

## Purpose

Store project-start and ongoing feedback specific to Codex for this workspace.

## Source Of Truth

- This file is the canonical Codex feedback surface under `project_agent_ops/resources/feedback/codex/`.
- Append new entries instead of rewriting prior entries unless an entry is clearly invalid.

## Entry Format

For each entry, record:

- date
- context
- positive signal
- problem or friction
- follow-up action

## Current Entries

- 2026-03-27
  - context: control taxonomy migration and phase-1 caption experiment execution
  - positive signal: control tree, master plan, packet surface, and phase-1 OpenAI baseline were aligned and runnable inside the local workspace
  - problem or friction: repeated packet JSON filenames from the older `10w` set still trigger linter hard errors because machine-readable names are not lowercase snake_case
  - follow-up action: normalize or reclassify the legacy `10w` packet JSON files before the next experiment phase
- 2026-03-27
  - context: phase-1 caption quality sample review
  - positive signal: chart, UI screenshot, code screenshot, and popup samples were mostly described accurately enough for baseline comparison
  - problem or friction: at least one completed caption was semantically truncated while still passing the structured output contract
  - follow-up action: add a caption completeness guard before phase-2 evaluation overlay or any commit-oriented flow
