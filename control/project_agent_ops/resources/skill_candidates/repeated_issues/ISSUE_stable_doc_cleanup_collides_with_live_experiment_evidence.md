# Repeated Issue: Stable-Doc Cleanup Collides With Live Experiment Evidence

## Symptom

- a cleanup wave starts on the reasonable goal of removing machine-local drift
- but some nearby reports, manifests, or specs are still live experiment evidence or are being actively edited
- the same cleanup motion now risks changing current experiment truth instead of only cleaning reusable surfaces

## Scope

- mixed workspaces where reusable docs live next to active reports, manifests, and truth-source specs
- repos where the experiment loop is still running while GitHub-prep or portability work has already started

## Guardrail

- classify candidate files as `stable reusable surface` vs `live evidence surface` before editing
- sanitize stable docs, skills, scripts, and reusable references first
- do not normalize active reports/manifests/specs until they are frozen or the user explicitly asks
- if a file is actively user-modified, treat it as blocked unless the user asks to merge into that edit

## Follow-up

- add explicit labeling or lint support that can mark live evidence surfaces as cleanup-protected
- keep future cleanup packets explicit about `safe to sanitize` vs `truth-bearing / live-edit` classes

## Current Proven Evidence

- on 2026-04-09, `my-image-parser` left ongoing experiment surfaces such as `SPEC_corpus_review_decision_capture.md` and current review/evidence files untouched while surrounding tracked reusable docs were sanitized
