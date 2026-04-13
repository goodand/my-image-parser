# Repeated Task: Runtime Portability Hardening Across Code And Skill Docs

## Pattern Name

- vendored runtime portability hardening

## Trigger

- local OCR, parser, or ML-adjacent runtimes should remain in the repo
- the runtime currently assumes one machine layout such as one fixed `.venv/bin/python` path or one fixed vendored root
- later execution is expected to move toward Docker or hosted-agent environments

## Stable Steps

1. Identify the over-constrained assumption in runtime code first: fixed interpreter path, one venv layout, or one launcher root.
2. Add env override support for the bounded runtime entrypoints.
3. Add `.venv` / `venv` fallback or equivalent dual-layout support where safe.
4. Patch `runtime.md` and troubleshooting pages so the documented launch path matches the new code behavior.
5. Validate the runtime surface with the lightest direct check available, such as `py_compile`, `--help`, or a bounded smoke.
6. Leave heavy model weights or caches out of scope; harden the runtime boundary without pretending the full remote-execution migration is already done.

## Candidate Promotion

- checklist: vendored runtime portability hardening
- helper: shared interpreter/launcher resolution utility
- review rule: code + skill runtime docs must evolve together for portable runtime surfaces

## Promotion Trigger

- another local tool should stay available in the repo while becoming less tied to one workstation layout

## Current Proven Evidence

- on 2026-04-09, `my-image-parser` first relaxed vendored launcher assumptions in `92f444c`
- it then hardened OCR-oriented runtime code and matching skill docs in `09cfec6`
- the affected surfaces included `scripts/full_image_ocr_context_package_lib.py`, `scripts/run_phase0_imagesorcery_ocr_smoke.py`, and related `skills/*/references/runtime.md` and `troubleshooting.md`
