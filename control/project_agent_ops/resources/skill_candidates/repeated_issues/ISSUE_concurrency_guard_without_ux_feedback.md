# Repeated Issue: Concurrency Guard Without UX Feedback

## Symptom

A technical concurrency guard (in-flight flag, mutex, semaphore) is added to prevent race conditions, but the guard silently drops the blocked action without informing the user. The user believes their action was accepted when it was actually ignored.

## Current Proven Example

- `extension.js` `onSaveDecisionFeedback` had `feedbackSaveInFlight` flag that silently returned on concurrent saves
- User clicks Save twice quickly — second save is dropped with no visible indication
- User believes both saves succeeded, but only the first was persisted
- Fixed 2026-04-07 by adding `statusMessage: "Save already in progress"` + `pushDocumentState()` before returning

## Why This Is Dangerous

- Silent data loss is worse than an explicit error — the user doesn't know to retry
- In feedback/evaluation workflows, a lost decision entry can mean re-doing manual review work
- The guard correctly prevents the race condition, but trades a technical bug for a UX bug
- The pattern compounds: if the user retries and hits the guard again, they may give up entirely

## Guardrail

When adding a concurrency guard:

- Always provide visible feedback when an action is blocked ("Save already in progress", "Please wait", spinner)
- Prefer latest-wins queue over drop-on-busy when possible — queue the last request and replay after completion
- If using drop policy, at minimum surface a status message explaining why the action was not performed
- Consider disabling the triggering UI element (button, input) while the guard is active

## Escalation Trigger

Another concurrency guard (debounce, in-flight flag, lock) is added that silently drops user actions without providing feedback.

## Recurrence On 2026-04-08 (Client-Side Layer)

- `decision-slides.js` `submitDecisionSlidesFeedback()` had a client-side `saveState === 'saving'` guard that silently returned on double-click
- This was distinct from the host-side guard in `extension.js` — the client guard fires first, so the host guard (which does provide feedback) was unreachable
- Demonstrates that the same pattern recurs at different architectural layers: host-side was fixed in round 1, but client-side was introduced by Codex in round 2 with the same silent-return anti-pattern
- Fixed by adding `setDecisionSlidesUiState({ statusMessage: 'Save already in progress.' })` before the client-side return

## Promotion Status

- absorbed on 2026-04-07 into `claude-gemini-communicator/skills/Skills-Create-Project/async-migration-verify/checklist-forconsistency-evaluation/async-migration-6-checkpoint.md` checkpoint 3
- recurred on 2026-04-08 at the client-side layer (different guard, same anti-pattern)
