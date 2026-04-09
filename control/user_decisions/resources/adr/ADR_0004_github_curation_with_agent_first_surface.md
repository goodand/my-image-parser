# ADR 0004 GitHub Curation With Agent-First Surface

## Status

accepted

## Date

2026-04-05

## Decision

Curate `my-image-parser` for GitHub now as a clean repository first, while reducing future portability blockers for Docker or hosted agent execution.

The GitHub target is not a raw workspace snapshot.

The repository should preserve agent-facing execution and reasoning surfaces as broadly as practical, while excluding machine-local settings and nonessential local state.

## Primary Goal

Make the repository clean enough to upload to GitHub now.

Do not treat Docker enablement as the current primary objective.

Instead, prevent known blockers early:

- machine-local agent settings
- absolute paths
- model cache coupling
- local-only state that would make later hosted execution harder

## Visibility And Audience

- first upload mode: `private-first but publicable`
- primary readers: both humans and agents

## Include

- `scripts/`
- `skills/`
- broad portions of `project_agent_ops/resources/`
- launcher surfaces
- contracts
- install documentation
- runtime code
- selected vendored source when needed for agent execution or understanding

## Exclude

- `.codex/`
- `.claude/`
- `.vscode/`
- `tool_inventory`
- handoff documents intended for local or merge-time agent exchange
- model weights
- cache directories
- machine-local runtime state

## Vendor Policy

Do not use a wrapper-only public surface.

Preferred policy:

- include launcher surfaces
- include runtime code
- include selected vendored source when needed
- exclude model weights and cache material

This preserves agent-usable execution context without forcing the public repository to carry heavyweight model artifacts.

## Agent-First Surface Rule

When there is a trade-off between simplifying user-facing surface and preserving agent-facing execution context, prefer preserving the agent-facing surface unless it leaks machine-local or private state.

However, do not preserve local handoff files as repository artifacts for this purpose.

Agent-to-agent exchange should instead happen through:

- commit messages
- merge flow communication

## Runs And Registry Rule

- do not keep `runs/` wholesale
- keep only a few explanatory `manifest` or `report` files when they materially help agents understand the repository
- do not keep `tool_inventory` in the public repository

## Path Sanitization Rule

Replace absolute local paths with environment-variable placeholders.

Chosen style:

- prefer env-var placeholders over markdown-only removal
- do not keep machine-specific absolute launcher paths in public-facing TOML, JSON, or Markdown examples

## Cleanup Order

1. ignore and scope cleanup
2. TOML and path sanitization
3. documentation cleanup

## Allowed Refactoring Scope

File moves and structural cleanup are allowed when they better reflect the codebase rules and intended public shape.

This is not limited to comment-only or path-only edits.

## Consequences

- the repository can be prepared for GitHub without waiting for Docker implementation
- later Docker or hosted-agent work should face fewer machine-local blockers
- agent-facing runtime understanding remains stronger than in a wrapper-only or docs-only public mirror
