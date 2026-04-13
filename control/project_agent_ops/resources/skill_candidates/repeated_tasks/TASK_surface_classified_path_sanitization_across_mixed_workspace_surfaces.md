# Repeated Task: Surface-Classified Path Sanitization Across Mixed Workspace Surfaces

## Pattern Name

- path cleanup by surface class, not by string class alone

## Trigger

- the workspace contains machine-local absolute paths across docs, config snippets, runtime examples, scratch outputs, and external truth references
- the repo mixes control-plane and execution-plane artifacts
- a naive `replace all /Users/... with relative path` approach would destroy meaning

## Stable Steps

1. Scan for machine-local paths and group hits by artifact family before editing.
2. Classify each hit as one of: `repo-local doc`, `local-private`, `external workspace`, `scratch/tmp`, or `runtime/config surface`.
3. Apply the correct transformation:
   - repo-local docs -> repo-relative path
   - local-private references -> local placeholder
   - external workspace references -> external placeholder
   - scratch/tmp outputs -> `<TMP_DIR>`-style placeholder
   - runtime/config surfaces -> env or template placeholder
4. Validate the changed family with the smallest fitting check such as `rg`, `json.tool`, or `py_compile`.
5. Commit in small topical batches so rollback stays narrow.

## Candidate Promotion

- checklist: path-class decision table for mixed workspaces
- lint: artifact-family-specific path linting
- helper doc: `absolute-path cleanup playbook`

## Promotion Trigger

- another mixed repo needs machine-local path cleanup but contains both stable reusable docs and intentionally local or external references

## Current Proven Evidence

- on 2026-04-09, `my-image-parser` repeatedly used this pattern while sanitizing tracked docs and config surfaces
- the adopted rule was `docs -> relative`, `runtime -> dynamic/env-based`, `TOML/config snippets -> placeholder`, with multiple topical cleanup commits including `b13bab7`, `432db92`, `cfbeb21`, `cc309e2`, and `abab530`
