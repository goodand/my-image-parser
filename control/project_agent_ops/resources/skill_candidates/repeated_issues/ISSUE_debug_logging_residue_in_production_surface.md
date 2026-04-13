# Repeated Issue: Debug Logging Residue In Production Surface

## Symptom

`console.log` debug statements remain in production code paths after development. They produce noise in extension host output, leak internal state, and signal incomplete cleanup.

## Current Proven Example

- `extension.js:125,127` had `console.log('[wikilink-debug]...')` in the host message handler
- `webview-wikilinks.js` had multiple `console.log` calls for suggestion request/response debugging
- discovered during 2026-04-07 product review, removed by Codex in same session
- post-fix grep confirms zero `console.log` in `src/`

## Why This Is Dangerous

- in stdio-based protocols (MCP), stdout pollution can corrupt transport
- in extension hosts, debug logs slow output and confuse users
- indicates the review/lint gate does not catch log residue

## Guardrail

- add an eslint rule or lint check that flags `console.log` in `src/` (allow `console.error` and `console.warn`)
- during code review, grep for `console.log` before merge
- if debug logging is needed in production, use a gated logger that can be disabled

## Escalation Trigger

Another `console.log` debug statement is found in committed production code in `src/`.

## Linked Pattern

- `ISSUE_stdio_stdout_pollution_in_machine_readable_mcp.md` (same class of issue in MCP context)
