# Zero-Ready State Hidden Without Dry-Run Manifest

## Recurrence Signal

All review rows are still pending, but the workspace has no explicit downstream artifact saying that retrieval or mapping are blocked only because no completed rows exist.

## Current Guardrail

When decision ingestion produces zero ready rows, emit explicit dry-run manifests with:

- `ready_to_execute = false`
- a stable `blocked_reason`
- planned downstream outputs

This prevents later sessions from guessing whether the pipeline is broken or simply waiting on human review.

## Structural Fix Candidate

Mandatory dry-run reporting stage after review-decision ingestion whenever ready count is zero.

## Escalation Trigger

Another phase or corpus reaches decision ingestion and downstream consumers still have to infer the blocked state from empty JSONL files alone.

## Current Proven Example

2026-03-30 `phase2` needed explicit retrieval and mapping dry-run manifests because the canonical ready-row JSONLs were empty while all decision rows were still pending.

