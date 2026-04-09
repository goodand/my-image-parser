# TASK: External Paper Cache For Edge-Case Solver Design

## Why this repeats

When the current codebase reaches a real edge case, the next useful step is often not immediate implementation but a bounded external research cache:
- save a small paper set locally
- map each paper to the open subproblem
- keep the result as reusable reference instead of re-searching from scratch next time

## Observed pattern

This is especially useful when:
- the codebase already has partial heuristics
- the remaining failure mode is architectural rather than just a bug
- the workspace needs stable external references before opening a new implementation slice

## Current proven handling

Create a bounded paper cache with:
- local PDFs
- one manifest
- one reference note that maps each paper to the open problem

## Promotion target

Reusable external-paper-cache workflow for bounded solver design.

## Promotion trigger

Trigger promotion when another edge case needs a small, stable paper set before implementation work should continue.
