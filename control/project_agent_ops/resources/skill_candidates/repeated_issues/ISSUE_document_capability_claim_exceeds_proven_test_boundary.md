# Repeated Issue: Document Capability Claim Exceeds Proven Test Boundary

## Symptom

A reference or evaluation document claims a capability is "closed", "sufficient", or "stable", but the actual test suite only proves a narrower subset of that claim. The document language implies a stronger guarantee than the evidence supports.

## Current Proven Examples (2026-04-08)

All from `REFERENCE_slide_preview_writeback_evaluation_packet-at2026-04-08.md`:

1. **"source mapping is sufficient for writeback"** — contract-level algorithmic intersection is tested (`slide-selection-contract.test.js`, `slide-renderer.test.js`), but visual hit accuracy in the real webview layout (CSS, font metrics, viewport) is unproven.

2. **"stable region_id"** — `region_id` is line-number based (`{slide_id}.lines-{start}-{end}`), usable within current slide context, but not durable across source mutations. No `documentVersion` or `source_hash` invalidation exists. Document used "stable" without qualifying scope.

3. **"writeback path closed"** — `replaceDocument` is tested via mock callback only. Actual VS Code `WorkspaceEdit` semantics (undo stack, dirty state, concurrent edit, encoding) are not exercised.

4. **"178 passing" as evidence** — presented alongside a 12-module path list, but `slide-preview-runtime.js` (the largest orchestration file) has no independent test. Readers infer comprehensive coverage from the pass count.

## Later Session Extension (2026-04-09)

The same issue reappeared while patching the upper progress packet and then reconciling the progress packet with the detailed writeback packet:

1. **"10-image readiness is almost closed"** — `evaluation-session-bootstrap.js` existed, but command wiring, helper tests, and smoke were still absent. The document language initially implied near-readiness before the entry path was actually verified.

2. **paired reference packets drifted away from code truth** — the upper progress packet reflected later implementation and test closure, but the detailed writeback packet still described visual-hit proof, runtime interaction proof, and `WorkspaceEdit` last-mile as unproven. Readers comparing the two packets would infer contradictory capability boundaries unless the stale packet was reconciled.

3. **hardcoded pass counts reappeared as capability shorthand** — exact totals such as `178 passing` or `222 passing` were read as readiness evidence, even when the real question was whether the cited runtime seam or command path had direct proof.

## Why This Matters

- Reviewers who trust document claims without checking test boundaries may approve a slice that has unproven gaps
- "Closed" language closes the door on further verification work that is actually still needed
- The gap between claim and evidence grows silently as the document is reused as a reference

## Guardrail

When writing evaluation or reference documents that claim a capability is proven:

- Split every claim into **proven** (with specific test file citations) and **not yet proven** (with specific gap description)
- Never use "stable", "sufficient", or "closed" without qualifying the scope (contract-level, session-scoped, etc.)
- If a test uses mocks or fakes for a critical dependency (e.g., `getBoundingClientRect`, `replaceDocument`), disclose the mock boundary explicitly
- If two related packets exist, treat code and tests as the source of truth and either reconcile or explicitly deprecate the stale packet before sharing both

## Escalation Trigger

Another evaluation or reference document claims a capability is closed while the test suite only proves a subset, and the gap is discovered during expert review rather than at document creation time.

## Promotion Status

- standalone issue, not yet absorbed into a skill
