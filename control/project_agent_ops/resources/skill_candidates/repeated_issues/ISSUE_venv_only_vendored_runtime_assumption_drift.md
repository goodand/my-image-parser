# Repeated Issue: .venv-Only Vendored Runtime Assumption Drift

## Symptom

- a vendored local runtime works only when one exact `.venv/bin/python` layout exists
- moving to another machine, another venv layout, or an env-provided interpreter breaks the runtime surface
- code and skill docs quietly drift because both assumed the same too-narrow layout

## Scope

- vendored OCR, parser, and ML-adjacent tools
- repo-owned launchers and scripts that call local Python entrypoints
- `runtime.md` and troubleshooting pages that mirror those launch assumptions

## Guardrail

- forbid `.venv`-only assumptions for portable local runtimes
- add env override first, then add `.venv` / `venv` fallback where safe
- patch the matching skill docs in the same wave as the code change
- validate with a light direct check before claiming the portable surface is improved

## Follow-up

- centralize interpreter resolution logic for vendored runtimes
- add code review guidance that portable launcher surfaces must not hardcode one local interpreter layout
- keep future Docker or hosted-execution prep focused on boundaries, not on shipping model weights or cache

## Current Proven Evidence

- on 2026-04-09, `my-image-parser` patched `scripts/full_image_ocr_context_package_lib.py`, `scripts/run_phase0_imagesorcery_ocr_smoke.py`, and matching OCR skill docs so they now support env overrides and `.venv`/`venv` fallback instead of one fixed layout
