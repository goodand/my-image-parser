# Repeated Issue: Sandboxed macOS OCR Context Builder Drift

## Issue Name

- full-image OCR context-package builders can complete structurally in sandbox while returning unusable OCR due to macOS Vision fallback failure

## Symptom

- the builder writes markdown, JSON, and manifest artifacts successfully
- OCR payload still comes back with Foundation or fallback errors in sandbox
- the same image returns `ocr_status=usable` when rerun unsandboxed

## Scope

- `macos-ocr-mcp`
- full-image OCR context-package builders
- any workflow that tries to treat sandbox OCR failure as a final no-text verdict

## Guardrail

- do not treat sandbox OCR failure as final on macOS-native OCR paths
- rerun unsandboxed before promoting `no_text`, `weak_text`, or `error` outcomes into the next baseline decision
- keep smoke evidence that distinguishes structural builder success from OCR-runtime success

## Follow-up

- preserve both sandbox and unsandboxed smoke artifacts for the same image when this drift is observed
- keep the unsandboxed execution rule visible in OCR references, task packets, and runner docs
