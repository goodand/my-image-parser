# Review Decision Ingestion To Ready Subsets

## Recurrence Signal

A structured human review decision seed already exists, but downstream retrieval and mapping work still needs a deterministic ingestion pass that materializes only the completed and eligible rows.

## Current Manual Handling

Read the decision JSONL, filter:

- retrieval-ready rows:
  - `review_status = completed`
  - `use_for_retrieval = true`
  - non-empty `approved_caption`
- mapping-ready rows:
  - retrieval-ready plus mapping still in scope

Then emit one ingestion manifest, one retrieval-ready JSONL, one mapping-ready JSONL, and one report.

## Promotion Target

Reusable review-decision ingestion stage between human decision capture and downstream retrieval or mapping execution.

## Promotion Trigger

Another review-driven workflow needs to hold downstream execution until completed rows exist, while still preserving a machine-readable empty-ready state when everything is pending.

## Current Proven Example

2026-03-30 `phase2` corpus review decision ingestion emitted zero ready rows from the all-pending seed and recorded the explicit next action to fill the decision rows and rerun ingestion.

