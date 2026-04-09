# Decision Seed Contract And Seed Row Shape Drift

## Recurrence Signal

A prose spec and machine-readable contract describe one review decision row shape, but the actual generated seed JSONL still follows an older nested-template structure.

## Current Guardrail

If a review decision contract is introduced or revised, regenerate the seed JSONL immediately and verify:

- required flat fields exist on every row
- machine-prefilled paths are present
- downstream consumers no longer depend on legacy nested templates

## Structural Fix Candidate

Contract-first regeneration check for review decision seeds plus one bounded ingestion smoke after every schema change.

## Escalation Trigger

Another decision-capture workflow updates the contract or report vocabulary without regenerating the canonical seed rows.

## Current Proven Example

2026-03-30 `phase2` corpus review decision capture briefly described a flat row contract while the actual seed still used a nested `human_decision_template` structure until the Session B bridge regenerated it.

