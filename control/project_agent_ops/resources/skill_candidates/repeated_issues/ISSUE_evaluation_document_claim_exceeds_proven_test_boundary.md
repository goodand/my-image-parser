# Repeated Issue: Evaluation Document Claim Exceeds Proven Test Boundary

## Symptom

An evaluation or reference document asserts that a capability is "closed", "sufficient", or "stable", but the actual test evidence only proves a narrower subset of that claim. The document reads as if the full path is verified, while in reality only the contract/algorithm layer is covered.

## Sub-Types

1. **Algorithmic proof claimed as visual proof** — contract test uses fake geometry (e.g., fake `getBoundingClientRect`), but document claims mapping "works" without qualifying the boundary
2. **Session-scoped identity described as "stable"** — line-number-based ID is called stable without disclosing vulnerability to source mutation
3. **Mock injection claimed as host integration** — `replaceDocument` callback mock passes, but document claims the writeback path is "closed" without disclosing the last-mile gap (undo stack, dirty state, encoding)
4. **Pass count cited without coverage gap disclosure** — "178 passing" is cited as evidence but the largest orchestration module has no dedicated test file

## Current Proven Examples (2026-04-08)

All 4 sub-types appeared in a single document review of `REFERENCE_slide_preview_writeback_evaluation_packet-at2026-04-08.md`:

- Review Focus #1: "source mapping sufficient" → only contract-level fake-rect tests exist
- Review Focus #2: "stable region_id" → line-number based, no `documentVersion` or hash invalidation
- Evidence: "writeback closed" → `replaceDocument` is a callback mock, VS Code WorkspaceEdit not tested
- Evidence: "178 passing" → `slide-preview-runtime.js` (largest single file) has no test file

## Why This Matters

Evaluation packets are read by expert reviewers who rely on them to scope their review. If claims exceed the proven boundary, reviewers either:
- Over-trust the slice and skip edge cases that are actually unverified
- Discover the gap late and lose confidence in the entire document

## Guardrail

When writing evaluation documents:
- Split every capability claim into **proven** (what tests actually cover) and **not yet proven** (what remains outside test boundary)
- Never cite pass counts without disclosing which modules or paths lack coverage
- Qualify identity/stability claims with the actual scope (current slide context, session, durable)
- Qualify integration claims with the actual injection boundary (mock, fake, real API)

## Escalation Trigger

Another evaluation document claims a vertical slice is "closed" or "proven" and a later reviewer discovers that the claim only holds at contract level, not at the integration or runtime level the document implies.

## Promotion Status

- standalone issue, not yet absorbed into a skill
