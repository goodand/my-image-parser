# Bounded Table-Branch Activation Slice Closure

## Pattern

Close a dormant or candidate table-parser branch through one bounded, ordered evidence slice before treating the branch as active.

## Why It Repeats

- parser backends can be installed and partially verified long before the branch is trustworthy
- plans repeatedly need the same closure sequence:
  - triage
  - boot smoke
  - real parse smoke
  - canonical normalization
  - wrapper or consumer confirmation
- without a fixed activation slice, branch status drifts between "installed", "candidate", and "active"

## Current Promoted Surface

- `skills/table-branch-activation-slice`

## Boundary

This pattern owns:

- bounded branch activation
- evidence ordering
- stop conditions before rollout

It does not own:

- parser implementation
- batch rollout
- worksheet export
- row-level RAG activation
