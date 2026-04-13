# Repeated Task: Git-Safety Snapshot Before Boundary Cleanup

## Pattern Name

- local safety bootstrap before cleanup

## Trigger

- a workspace needs aggressive cleanup, scope reduction, or public-prep work
- Git recovery is missing or too weak to safely survive accidental deletion or broad restructuring
- the cost of losing local state has already been demonstrated by a deletion or missing-backup incident

## Stable Steps

1. Freeze the immediate goal as `recoverability first`, not `perfect public surface first`.
2. Add or tighten the smallest ignore boundary that blocks obvious local-only or machine-only state.
3. Sanitize one config surface if needed so the first commit does not immediately preserve a known machine-local leak.
4. `git init` and make a narrow boundary commit first.
5. Add a second broader snapshot commit that captures stable agent-facing surfaces such as `scripts/`, `skills/`, and reusable `control/resources`.
6. Only after those two safety commits exist, start wider cleanup such as path sanitization or portability hardening.

## Candidate Promotion

- checklist: local-safety bootstrap before cleanup
- packet: `cleanup safety bootstrap` packet for volatile workspaces
- script: optional repo preflight that checks whether a recoverable Git baseline exists before bulk cleanup

## Promotion Trigger

- another repo needs GitHub-prep, portability cleanup, or broad document/path normalization before a trustworthy Git baseline exists

## Current Proven Evidence

- on 2026-04-09, `my-image-parser` first landed `1825804` (`chore(init): add ignore boundaries and sanitized mcp snippet`)
- it then landed `495f295` (`chore(snapshot): add broad agent-facing workspace surface`)
- broader path and runtime cleanup only continued after those two recovery anchors existed
