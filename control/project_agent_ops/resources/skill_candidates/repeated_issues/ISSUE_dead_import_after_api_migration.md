# Repeated Issue: Dead Import After API Migration

## Symptom

After migrating all call sites from one API surface to another (sync→async, old library→new library, callback→promise), the original import survives even though no call site uses it. The dead import gives the false impression that the old API is still in use.

## Current Proven Example

- `decision-session-artifacts.js` had `const fs = require('fs'); const fsp = fs.promises;` after all sync calls were converted to `fsp.*`
- `fs` was only used to derive `fsp` — no `fs.readFileSync`, `fs.writeFileSync`, or `fs.existsSync` remained
- Readers seeing `const fs = require('fs')` assumed sync methods were still in use
- Fixed 2026-04-07 by changing to `const fsp = require('fs').promises;`

## Why This Is Dangerous

- Gives a false signal that the old API surface is still active
- Reviewers skip the module during "are we fully async?" audits because they see the old import
- Linters don't always catch unused intermediate derivations (`fs` is "used" to produce `fsp`)
- Can block tree-shaking or bundler optimizations in environments that support them

## Guardrail

After any API migration:

- Grep for the old module/import across all migrated files
- For each hit, verify at least one direct call site remains — derivation-only usage is a dead import
- If the old import is only needed to access a sub-property (e.g., `fs.promises`), destructure directly

## Escalation Trigger

Another API migration (sync→async, old SDK→new SDK, require→import) leaves the old import in place with no direct call sites.

## Linked Pattern

- `Runtime Bundle Migration Can Leave Source-Level Generator Debt Behind` — same class: migration leaves structural residue even when runtime behavior is correct

## Promotion Status

- absorbed on 2026-04-07 into `claude-gemini-communicator/skills/Skills-Create-Project/async-migration-verify/checklist-forconsistency-evaluation/async-migration-6-checkpoint.md` checkpoint 1
