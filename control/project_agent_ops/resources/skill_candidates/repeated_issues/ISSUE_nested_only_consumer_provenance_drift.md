# ISSUE: Nested-Only Consumer Provenance Drift

## Summary

A consumer manifest can be semantically correct but still hard to use when the real truth-source details only exist in nested objects instead of stable top-level fields.

## Recurrence signal

This issue is present when:
- the artifact already records input resolution correctly
- downstream readers still need to reopen nested structures for basic questions
- report text is clear, but the canonical JSON is awkward to consume programmatically

## Current workaround

Project the most important consumer-facing provenance and summary fields to top-level keys while keeping the nested detail for full fidelity.

## Structural fix candidate

Explicit `top-level consumer projection` rule for eval manifests.

## Escalation trigger

Escalate when another downstream artifact is nominally correct but forces consumers to traverse nested helper objects just to discover input mode, resolved sources, or winner frequency.
