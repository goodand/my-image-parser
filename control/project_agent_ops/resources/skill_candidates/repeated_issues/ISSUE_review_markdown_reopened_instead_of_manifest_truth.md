# Review Markdown Reopened Instead Of Manifest Truth

## Recurrence Signal

A review workflow emits both markdown and manifest outputs, but a downstream consumer starts reading the markdown again even though a machine-readable manifest already exists.

## Current Guardrail

If the review producer explicitly marks:

- `machine_truth_source = manifest`
- `markdown_human_facing_only = true`

then downstream machine consumers must read the manifest only and treat markdown as a human operator surface.

## Structural Fix Candidate

Manifest-first review-consumer contract plus lint or checklist rule that forbids markdown reparsing when machine truth was already emitted.

## Escalation Trigger

Another review-to-consumer bridge starts parsing prose markdown again or duplicates priority/default/winner logic that is already present in the review manifest.

## Current Proven Example

2026-03-30 `phase2` corpus review surface explicitly declared manifest-only machine truth so `Session B` could build retrieval and mapping preflight seeds without reading the markdown review.

