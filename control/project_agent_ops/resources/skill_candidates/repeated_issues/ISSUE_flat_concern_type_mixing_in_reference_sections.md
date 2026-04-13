# Repeated Issue: Flat Concern-Type Mixing In Reference Document Sections

## Symptom

A reference document section lists items of fundamentally different concern types (product expansion, integration debt, architecture debt, verification debt) in a single flat list without grouping or priority. Readers cannot distinguish urgency or ownership.

## Current Proven Examples (2026-04-08)

From `REFERENCE_slide_preview_writeback_evaluation_packet-at2026-04-08.md`:

1. **Open Scope** — original flat list mixed `style/layout/asset` expansion, `mode linkage`, `runtime refactor`, `integration/e2e test`, `WorkspaceEdit verification` in one bullet list. Fixed by splitting into 3 buckets: Integration/Verification → Product Expansion → Architecture/Maintainability, with priority order.

2. **Why This Matters** — original section mixed the value statement ("critique가 지적했던 render only를 넘어섰다") with an isolation disclosure ("feedbackLedger 미연결"). Fixed by extracting isolation disclosure into a separate `## Current Isolation Boundary` section.

## Later Session Extension (2026-04-09)

The same structural mixing reappeared while patching the upper progress packet:

1. **10-Image Evaluation Readiness** — product/tool readiness and cross-repo coordination status were initially described together. Fixed by renaming the section to `10-Image Evaluation Readiness (Cross-Repo Coordination)` and explicitly noting that this is coordination readiness, not proven product readiness.

2. **Proven Evidence list** — direct `slide-preview` slice proof and adjacent/shared evidence from `decision-slides` were initially presented together. Fixed by splitting the section into `Direct slice evidence` and `Adjacent / shared infrastructure evidence`.

## Why This Matters

- Flat mixed lists hide priority — a reader cannot tell which items block the next step
- Items of different concern types have different owners and timelines
- Without grouping, review discussions waste time classifying before evaluating

## Guardrail

When writing Open Scope, Next Steps, or similar sections:

- Group by concern type (product, integration/verification, architecture)
- Within each group, state priority order explicitly
- If a section mixes a value claim with a boundary disclosure, separate them into distinct subsections
- If evidence comes from different ownership or proof lanes, separate direct evidence from adjacent/shared evidence instead of listing them in one flat proof block

## Escalation Trigger

Another reference document's Open Scope or equivalent section contains 5+ items of mixed concern types in a flat list, and a reviewer has to re-sort them before they can prioritize.

## Promotion Status

- standalone issue, confirmed across the detail packet and the upper progress packet
