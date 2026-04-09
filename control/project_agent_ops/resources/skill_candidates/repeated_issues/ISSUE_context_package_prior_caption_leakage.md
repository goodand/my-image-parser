# Repeated Issue: Context Package Prior Caption Leakage

## Issue Name

- review-oriented context packages can accidentally carry prior baseline captions back into the next generation prompt

## Symptom

- a context package contains fields such as `Existing phase-1 caption` or prior caption text in a summary field
- the later caption rerun appears overly anchored to the earlier caption instead of the image plus OCR evidence
- baseline comparison becomes less trustworthy because the rerun is partially self-conditioned

## Scope

- reviewed context-package builders
- caption rerun prompts that consume OCR evidence plus PPT-local summary
- any workflow where human-readable review summaries and model-input summaries share the same field

## Guardrail

- never inject prior baseline caption or alt-text fields into the new caption prompt by default
- sanitize mixed review summaries before prompt use
- prefer OCR excerpt, slide numbers, and PPT-local provenance as the prompt-safe context surface

## Follow-up

- keep a separate prompt-safe context view or sanitize the existing package before model injection
- add fixture tests that confirm review-only text is not present in the injected prompt
