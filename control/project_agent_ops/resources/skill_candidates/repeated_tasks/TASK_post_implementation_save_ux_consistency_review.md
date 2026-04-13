# Repeated Task: Post-Implementation Save-UX Consistency Review

## Recurrence Signal

Repeated whenever a Codex or subagent implements a save-UX plan for a bounded review surface. The implementation passes all tests but contains subtle consistency issues that only surface during manual code review.

## Current Manual Handling

After Codex delivers a save-UX implementation, review each file for the following 5-point checklist:

1. **Indentation consistency**: verify that all new/modified lines match the surrounding indentation (tabs vs spaces, indent depth)
2. **Guard-without-feedback**: every early-return guard that blocks a user action must provide visible UX feedback (statusMessage, error note, disabled state) before returning
3. **Cascaded DOM double-update**: if a state-mutation helper is called before a broader state mutation, verify the helper's fields are not immediately overwritten by the subsequent call
4. **Transient state affordances**: for every transient state in the state machine (auto-reset states like `saved`), verify that interactive elements are explicitly enabled or disabled — not left at defaults
5. **Dead code after consolidation**: when a call site is removed, verify the function definition is also removed if no other call sites remain

## Repeated Invariant

- Save-UX implementations consistently pass automated tests but fail on these 5 patterns because tests verify state transitions and output, not code quality or UX edge cases
- The patterns are orthogonal to each other — fixing one does not prevent the others

## Current Proven Evidence

- On 2026-04-08, Codex delivered save-UX + validation-preview for `vscode-markdown-review-surface` with 96 tests passing
- Post-implementation review found all 5 patterns:
  - (1) `decision-slides.js:108` had 6-space indent instead of 4
  - (2) `decision-slides.js:250` client-side saving guard silently returned
  - (3) `decision-slides.js:291` `clearDecisionSlidesFeedbackNotes()` → `setDecisionSlidesUiState()` double DOM update
  - (4) `slide-view-model.js:66` `saved` state left button clickable during 2-second transient window
  - (5) `decision-slides.js:170` `clearDecisionSlidesFeedbackNotes` function remained after call site removal
- All 5 fixed in the same review pass; tests still 96 passing after patches

## Promotion Target

Reusable 5-point post-implementation review checklist for any save-UX delivery on bounded review surfaces.

## Promotion Trigger

Another save-UX implementation is delivered by Codex/subagent and the same 5-point review reveals 2+ of these patterns again.
