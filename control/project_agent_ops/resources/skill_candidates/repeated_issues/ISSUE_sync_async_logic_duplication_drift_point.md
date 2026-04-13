# Repeated Issue: Sync/Async Logic Duplication Drift Point

## Symptom

When adding an async variant of an existing sync function, the core logic (parsing, normalization, validation) is copy-pasted instead of extracted into a shared helper. The two copies drift independently — a validation rule change in one version is missed in the other.

## Current Proven Example

- `feedback-ledger.js` had `readFeedbackLedger` (sync) and `readFeedbackLedgerAsync` with identical `JSON.parse → normalizeFeedbackLedger → validateFeedbackLedger → error check` blocks
- Only the I/O call differed: `fs.readFileSync` vs `await fsp.readFile`
- Fixed 2026-04-07 by extracting `parsePersistedFeedbackLedger(raw, filePath)` — shared by both variants
- Bonus: the shared helper also added file-path-enriched error messages that neither original had

## Why This Is Dangerous

- Validation policy changes (e.g., new required field) are applied to one variant and missed in the other
- Tests may only exercise one variant, so the drift is invisible until production hits the untested path
- The duplication is initially small (5-6 lines), making it feel harmless, but each change compounds the drift risk

## Guardrail

When adding an async variant of a sync function:

- Extract the shared processing logic (parse, normalize, validate, transform) into a pure synchronous helper
- Sync and async variants should differ ONLY in the I/O call — everything after raw data acquisition uses the shared helper
- Test the shared helper independently to ensure both paths have identical behavior

## Escalation Trigger

Another async variant is added by copying the sync body instead of extracting a shared helper, creating a second drift point.

## Promotion Status

- absorbed on 2026-04-07 into `claude-gemini-communicator/skills/Skills-Create-Project/async-migration-verify/checklist-forconsistency-evaluation/async-migration-6-checkpoint.md` checkpoint 2
