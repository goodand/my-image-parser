# TASK: Fast-Start Packet For Parallel Experiment Session Split

## Why this repeats

Parallel experiment work often slows down because every new session re-reads the master plan and re-derives the same interpretation before doing any bounded work.

## Observed pattern

The faster path is:
1. freeze the current canonical truth for the specific slice
2. define fixed interpretation rules explicitly
3. split owned paths between producer and consumer sessions
4. let each session start from a task packet instead of from the full plan corpus

## Current proven handling

For parallel experiment slices:
- one session owns the producer lane
- another session owns the consumer lane
- each session receives a `fast-start packet` with only:
  - goal
  - truth sources
  - fixed interpretation
  - owned paths
  - non-goals
  - deliverables
  - validation

## Promotion target

Reusable fast-start packet template for bounded parallel experiment sessions.

## Promotion trigger

Trigger promotion when another experiment should start in parallel without paying repeated master-plan reread cost.
