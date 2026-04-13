# Repeated Issue: Checklist Template/Instance Duplication Without Convention

## Pattern

A skill's checklist directory contains both a non-timestamp file (`checklist-name.md`) and a timestamp file (`checklist-name-at2026-04-08-00-16.md`) with identical content. No convention explains which is the template and which is the instance.

## Recurrence Signal

- a newly created skill has paired files in `checklist-forconsistency-evaluation/` or `checklist-forimplementation/` where one has a timestamp suffix and one does not
- the workspace's existing convention (visible in all other skills) uses timestamp-only files

## Failure Signature

- edits applied to one copy are not applied to the other, causing silent drift
- `SKILL.md` Read Order references only the timestamp file, making the non-timestamp copy orphaned
- `verify_artifact_order.py` may count the duplicate as an extra artifact

## Current Workaround

- delete the non-timestamp duplicate when confirmed identical to the timestamp file
- retain only the timestamp file as the canonical instance (matches workspace convention)

## Structural Fix Candidate

- skill creation workflow explicitly produces only timestamp files for checklist artifacts
- if a "stable name" alias is needed, use a symlink or a redirect note, not a full copy

## Escalation Trigger

- another skill is created with the same paired-file pattern causing drift or validator confusion

## Current Proven Evidence

- on 2026-04-08, both `cross-repo-product-review` and `async-migration-verify` had 3 pairs of identical timestamp/non-timestamp checklist files; 3 non-timestamp duplicates were deleted after diff confirmed identity
