# Repeated Task: Parallel Subagent Packetized Caption Execution

## Pattern

Run one-image or one-shard caption workers in parallel with non-overlapping outputs.

## Stable recipe

1. materialize shard inputs first
2. publish issued task-packets per worker
3. include `allowed_paths` and `locked_paths`
4. run one-image smoke gate
5. execute workers against the packet command only
6. aggregate from worker ledgers and sidecars

## Why this may deserve a dedicated skill

- the same packetized worker pattern is likely reusable across caption runs, screenshot caption runs, and MCP-backed image worker orchestration

## Current promoted surface

- `skills/image-job-dispatcher`
  - thin `SKILL.md`
  - `references/runtime.md`
  - `references/shard-strategy.md`
  - `references/task-packet-contract.md`
  - `checklists/parallel-preflight.md`
