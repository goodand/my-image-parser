# Repeated Task: Post-Critique Evaluation Document Precision Calibration

## Symptom

An agent critiques an evaluation/reference document, patches it, but the first patch is directionally correct yet imprecise. Multiple calibration rounds are needed before the document reaches expert-ready precision.

## Current Proven Example (2026-04-08)

`REFERENCE_slide_preview_writeback_evaluation_packet-at2026-04-08.md` required 2 calibration rounds after initial critique patch (6 items × 2 rounds = 12 corrections total):

### Round 1 corrections (direction → precision):
- Hardcoded line count ("877줄") → structural description ("largest single-orchestration runtime")
- Blended limitation note → separated "proven" vs "not yet proven" lists
- "session-scoped stability" (still too broad) → "current slide context" scope
- Isolation caveat buried in Why This Matters → separate `## Current Isolation Boundary` section
- "모두 unit level" (factually wrong — smoke/acceptance exist) → Proven Evidence + Unproven Boundaries split
- Flat Open Scope list → 3 buckets with priority order

### Round 2 corrections (precision → calibrated):
- "refactor target" → "main obstacle to runtime-level verification and modular reuse" (병목 framing)
- Single test file citation → 3 test file chain across mapping pipeline (근거 분산)
- "session-scoped" → "current slide context, not durable across source mutations" (한 단계 더 보수적)
- "acceptance" in Proven Evidence → "adjacent acceptance (decision-slides lane)" label (direct vs adjacent 분리)
- Isolation rationale → added "keeps writeback proof independent from decision workflow coupling" (bounded slice 전략 고정)
- Integration/Verification flat 1-2-3-4 → UI/Runtime Proof + Host Mutation Proof sub-buckets (겹침 해소)

## Later Session Extension (2026-04-09)

The same calibration task repeated on the upper progress packet and then once more during cross-document reconciliation:

### Progress packet calibration

`REFERENCE_review_surface_progress_and_expert_evaluation_packet-at2026-04-08.md` needed another 2 calibration rounds with the same structural categories:

- flat file list → 4 grouped workstream blocks
- vague bootstrap risk notes → concrete failure scenarios with expected outcomes
- stale runtime metric framing → structural description only
- direct and adjacent evidence mixed together → explicit evidence split
- proof-role duplication (`flow`, `host`, `acceptance`) → distinct semantic roles
- pass count removed in favor of stale-safe verification wording

### Cross-document consistency calibration

After both packets were individually patched, a third pass was still needed because the detailed writeback packet had become stale relative to the progress packet and current code/tests:

- items still listed as unproven had already been closed by later tests
- invalidation wording still described stale-guard absence after `slide-source-snapshot.js` and host-side stale rejection landed
- exact pass count had staled again
- open-scope items still contained already-closed proof work
- bridge / linked-state / binder extraction evolution was missing

## Recurring Calibration Categories

1. **Hardcoded metrics → structural descriptions**: exact numbers stale immediately; structural risk message survives
2. **Blended claims → proven/unproven separation**: every capability claim must cite specific test files for the proven part and name the specific gap for the unproven part
3. **Scope overstatement → conservative qualification**: "stable" → "session-scoped" → "current slide context, not durable" — each round narrows
4. **Misplaced disclosure → structural position**: disclosures buried in value sections must become independent sections
5. **Flat mixed lists → typed/prioritized buckets**: items of different concern types need grouping before readers can evaluate
6. **Direct vs adjacent evidence → label separation**: evidence from a different lane must be labeled as adjacent, not direct proof

## Repeated Invariant

The first critique patch captures the right issues but tends to:
- Use the document's own language (which is what was wrong)
- Blend proven and unproven in one sentence
- Place disclosures where they're structurally convenient rather than where readers need them
- Leave metrics that stale immediately

## Promotion Target

Reusable post-critique precision checklist applied after the first patch round, before presenting to the user.

## Promotion Trigger

Another evaluation document is patched and requires 2+ correction rounds on the same structural issues (metric staleness, proven/unproven blending, scope overstatement, misplaced disclosure, flat mixing).

## Detail

- `TASK_post_critique_evaluation_document_precision_calibration.md` (this file)
