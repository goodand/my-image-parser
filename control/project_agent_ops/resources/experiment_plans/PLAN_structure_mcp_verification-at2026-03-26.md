# Goal

Stabilize the workspace directory structure, update canonical path records, and verify that local Agent Skills and registered MCP wrappers are usable or clearly blocked.

## Deliverables

- Fixed workspace directory layout
- Updated path registry
- Usable local Agent Skill docs
- MCP verification results with restart notes

## Acceptance

- Core workspace artifacts live under stable top-level directories.
- `registry/session_paths.json` matches actual file locations.
- Local skills under `skills/` no longer contain placeholder template text.
- MCP status can be reported per wrapper as working, blocked, or restart-needed.
