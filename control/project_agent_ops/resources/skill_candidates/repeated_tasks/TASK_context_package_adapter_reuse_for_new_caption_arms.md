# Repeated Task: Context Package Adapter Reuse For New Caption Arms

## Recurrence Signal

A new caption arm needs extra evidence, but the existing caption runner contract is already stable and should not be widened just to support one bounded experiment slice.

## Current Proven Example

- parser/table-structure-enriched caption rerun on `image11.png`
- preserved the existing `context_package` ingestion path
- attached parser evidence through a bounded adapter instead of raw parser payload injection

## Repeatable Pattern

1. keep the runner contract stable
2. build a bounded context adapter artifact
3. preserve:
   - `source_image_path`
   - provenance
   - review status
4. keep arm-specific enrichment nested inside `context_package`
5. run one bounded rerun before considering broader rollout

## Promotion Candidate

- reusable adapter helper or checklist for adding new caption arms through existing context-package surfaces

## Why It Matters

This pattern avoids avoidable drift in:

- prompt surface
- ledger schema
- comparison parity across arms

