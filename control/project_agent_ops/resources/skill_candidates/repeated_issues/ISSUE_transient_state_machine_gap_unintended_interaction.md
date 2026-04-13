# Repeated Issue: Transient State Machine Gap Allowing Unintended Interaction

## Symptom

A state machine has a transient state (auto-transitions after a timer or event) where UI affordances are left in their default configuration instead of being deliberately designed. During the transient window, the user can trigger actions that lead to error paths or unexpected behavior.

## Current Proven Example

- `slide-view-model.js` save state machine: `idle → dirty → saving → saved → idle`
- The `saved` state auto-resets to `idle` after 2 seconds via `scheduleDecisionSlidesSavedReset()`
- During those 2 seconds, the button shows "Saved" but was NOT disabled (`saveDisabled` was false)
- If the user clicked "Saved", the submit function ran, found no dirty payload, and showed an error: "Enter a feedback comment or change at least one decision field before saving."
- The `saveDisabled` condition had `(!isDirty && saveState !== 'saved')` — the `saveState !== 'saved'` exception was specifically added to keep the button enabled during `saved` state, but this created the gap
- Fixed 2026-04-08 by simplifying to `!isDirty` — button is disabled whenever there are no changes, regardless of whether the state is `saved` or `idle`

## Why This Matters

- Users see "Saved" and expect the button to be inert — clicking it and seeing an error is confusing
- Transient states are often added last as polish, and their UI affordances are under-specified because the state lasts only 1-2 seconds
- The pattern compounds with different transient durations: a 5-second "saved" window gives the user more time to accidentally trigger the unintended path

## Guardrail

When adding a transient state to a state machine:
- Explicitly design the UI affordances for that state (button enabled/disabled, clickable areas, keyboard shortcuts)
- Ask: "what happens if the user interacts with the UI during this transient state?"
- Default to disabling interactive elements during transient states unless there is a specific reason to keep them active

## Escalation Trigger

Another transient auto-reset state is added to a state machine without explicitly deciding whether interactive elements should be enabled or disabled during the transient window.

## Promotion Status

- standalone issue, not yet absorbed into a skill
