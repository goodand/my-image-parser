# Repeated Issue: Partial Structural Fix — Same Class, Different Fields

## Symptom

A structural fix (e.g., reordering object spread, adding validation, adjusting precedence) is applied only to the fields explicitly named in a review finding. Other fields that belong to the same structural class remain unprotected, carrying the identical vulnerability. A second review round is required to catch the same fix pattern on the sibling fields.

## Current Proven Example

- `slide-session.js` `createSlideDescriptors()` had spread collision: `decisionRow`/`feedbackSlide` could overwrite descriptor-owned fields
- Codex 2nd patch: moved `ordinal` and `title` after spread — protected those two
- `slide_id` and `image_id` left before spread — same collision class, same vulnerability, not fixed
- Codex 3rd patch: moved all 4 fields after spread — fully resolved
- Each partial fix round cost a full review-handoff-verify cycle

## Why This Is Dangerous

- The fix appears complete because the specific reported fields are addressed
- The reviewer validated the named fields and declared "collision is closed" prematurely
- Each incomplete round costs a full review-handoff-verify cycle (reading, critique, Codex patch, re-build, re-test)
- The pattern compounds: if the fix class has N members and only K are addressed each round, convergence takes ceil(N/K) rounds

## Guardrail

When applying a structural fix:

- Identify all fields/entities that belong to the same structural class as the reported ones
- Apply the fix to the entire class, not just the explicitly named members
- In the fix description, enumerate which class members were addressed and confirm no siblings remain
- Reviewer should ask: "are there other fields/entities that have the same relationship to this structure?"

## Escalation Trigger

Another structural fix (spread reordering, validation addition, precedence adjustment, null guard) addresses only the named fields while leaving structurally identical siblings unprotected, requiring a follow-up round.

## Promotion Status

- absorbed on 2026-04-07 into `claude-gemini-communicator/skills/Skills-Create-Project/cross-repo-product-review/checklist-forconsistency-evaluation/review-convergence-consistency-checklist.md`
