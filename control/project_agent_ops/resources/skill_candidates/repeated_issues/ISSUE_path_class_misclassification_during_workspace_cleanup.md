# Repeated Issue: Path-Class Misclassification During Workspace Cleanup

## Symptom

- the same absolute-path pattern appears across many artifact families
- cleanup pressure encourages one universal replacement rule
- but docs, runtime snippets, external references, and scratch outputs each need different treatment

## Scope

- control-plane plus execution-plane repositories
- GitHub-prep, portability, or repo-root migration waves
- docs and config surfaces that still carry machine-local paths

## Guardrail

- do not decide from string shape alone
- classify the path by artifact class first:
  - repo-local doc
  - local-private reference
  - external workspace reference
  - scratch/tmp path
  - runtime/config surface
- only then apply the matching rewrite rule

## Follow-up

- maintain a shared path-class decision table
- add lint support or review checklist items that ask `what kind of path is this?` before rewriting
- keep docs-relative, runtime-dynamic, and config-placeholder strategies separate

## Current Proven Evidence

- on 2026-04-09, `my-image-parser` explicitly adopted the rule `docs -> relative`, `runtime -> dynamic/env-based`, `TOML/config snippets -> placeholder`, preventing blanket relative-path rewrites across mixed surfaces
