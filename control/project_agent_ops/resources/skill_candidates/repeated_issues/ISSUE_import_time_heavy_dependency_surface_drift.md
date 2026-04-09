# Repeated Issue Candidate: Import-Time Heavy Dependency Surface Drift

## Why This Repeats

A script can have a valid runtime implementation but still expose a broken operational surface if heavyweight libraries are imported at module import time.

This usually shows up when:

- `--help` should work in a lighter interpreter
- only a subset of commands need the heavy dependency
- vendored runtimes and system runtimes coexist in the same workspace

## Observed Workspace Case

- `scripts/build_component_split_ocr_report.py --help` initially failed
- root cause: `scripts/alpha_component_lib.py` imported `numpy` at import time
- effect: even surface-only inspection needed the vendored runtime, although the heavy dependency was only required inside actual alpha split execution

## Current Workaround

- move heavy imports such as `numpy`, `PIL`, or model-backed libraries into the narrowest runtime function that actually needs them
- keep CLI parsing and `--help` paths import-light
- verify both:
  - the lightweight surface (`--help`)
  - the real execution path under the intended runtime

## Structural Fix Candidate

- add a review rule for local tools: import-time dependencies must stay minimal unless the tool is intentionally single-runtime only
- prefer a service/config wrapper over module-top side effects when the same core will be consumed by multiple entrypoints

## Escalation Trigger

Escalate if another local script or skill surface:

- fails on `--help`
- requires a vendored interpreter just to inspect the surface
- or starts importing ML/image libraries before argument parsing
