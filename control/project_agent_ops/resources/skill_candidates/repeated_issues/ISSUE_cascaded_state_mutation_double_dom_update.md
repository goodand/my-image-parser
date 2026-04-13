# Repeated Issue: Cascaded State Mutation Double DOM Update

## Symptom

A helper function wraps a state mutation and triggers a DOM update as a side effect. The caller invokes the helper, then immediately calls another state mutation that also triggers a DOM update. The first DOM update is rendered for zero frames before being overwritten by the second, wasting a paint cycle and adding unnecessary complexity.

## Current Proven Example

- `decision-slides.js` `submitDecisionSlidesFeedback()` called `clearDecisionSlidesFeedbackNotes()` on line 291
- `clearDecisionSlidesFeedbackNotes()` internally called `setDecisionSlidesUiState({ statusMessage: '', errorMessage: '' })` which calls `updateDecisionSlidesSaveUi()`
- Immediately after, `setDecisionSlidesUiState({ saveState: 'saving', statusMessage: 'Saving feedback...', errorMessage: '' })` was called on line 292
- The second call overwrites the exact same nodes (statusMessage, errorMessage) the first call just wrote
- Fixed 2026-04-08 by removing the `clearDecisionSlidesFeedbackNotes()` call, since the subsequent `setDecisionSlidesUiState()` already sets both statusMessage and errorMessage explicitly

## Why This Matters

- Wasted DOM mutation increases paint jank, especially in webview-hosted surfaces where each paint is more expensive
- Creates a false dependency on the helper function's internal behavior — if someone changes the helper, the caller still works, but the implicit "clear then set" contract is fragile
- Makes the code harder to reason about: a reader must trace through the helper to realize the first update is immediately overwritten

## Guardrail

When calling a state-mutation helper before another state mutation:
- Check whether the subsequent mutation already covers the fields the helper sets
- If so, remove the helper call and let the subsequent mutation handle everything
- If the helper has additional side effects beyond the overlapping fields, extract only those side effects

## Escalation Trigger

Another state-change helper is called immediately before a broader state mutation that overwrites all fields the helper just set.

## Promotion Status

- standalone issue, not yet absorbed into a skill
