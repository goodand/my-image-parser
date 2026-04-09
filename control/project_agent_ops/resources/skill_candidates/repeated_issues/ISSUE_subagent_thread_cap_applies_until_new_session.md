# Repeated Issue: Subagent Thread Cap Applies Until New Session

## Pattern

When `.codex/config.toml` is added or changed during an already-running Codex session, the current live thread cap may not expand immediately.

## Observed effect

- repo-local config pinned `max_threads = 10`
- the current live session still rejected the 7th concurrent worker with `agent thread limit reached (max 6)`

## Guardrail

- treat thread-cap changes as next-session settings
- if a larger fan-out is needed immediately, either restart Codex or run workers in waves
- close completed workers before attempting to spawn more in the same live session
