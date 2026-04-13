# Repeated Issue: Guard Filter Set Missing Alias Forms

## Symptom

A programmatic guard constructs a blocklist or allowlist from a canonical source, but the runtime accepts multiple naming conventions for the same entity. The guard covers only one naming form, leaving alias forms unblocked.

## Current Proven Example

- `webpack.config.js` `RejectNodeBuiltinImportsPlugin` built `NODE_BUILTIN_MODULES` from `builtinModules` (which returns bare names: `fs`, `path`, ...)
- Used `.replace(/^node:/, '')` to normalize — a no-op since the source already lacks `node:` prefix
- Result: `require('fs')` blocked, `require('node:fs')` not blocked — guard was half-effective
- Fixed 2026-04-07 by generating both `bare` and `node:${bare}` forms for each entry

## Why This Is Dangerous

- The guard gives false confidence that all forms are covered
- Alias forms are often preferred by newer code, linters, or style guides (e.g., `node:` prefix is recommended in modern Node.js)
- The gap is invisible in testing unless tests specifically try the alias form
- The original implementation looked plausible — `.replace()` suggested the author was thinking about normalization, but the direction was wrong

## Guardrail

When building a filter set from a canonical source:

- Enumerate all accepted naming conventions for the target domain (e.g., `fs` and `node:fs` for Node.js builtins)
- Generate entries for every convention, not just the canonical form
- Add at least one test that uses the alias form to verify the guard catches it
- When using normalization (`.replace()`), verify the direction: are you stripping to normalize, or do you need to generate the variant?

## Escalation Trigger

Another guard or blocklist is built from a single naming convention while the runtime or consumer accepts multiple forms of the same identifier.

## Linked Pattern

- `ISSUE_timestamp_syntax_variant_*` — similar class: near-match variants that bypass a gate designed to enforce a single form

## Promotion Status

- absorbed on 2026-04-07 into `claude-gemini-communicator/skills/Skills-Create-Project/async-migration-verify/checklist-forconsistency-evaluation/async-migration-6-checkpoint.md` checkpoint 1 variant
