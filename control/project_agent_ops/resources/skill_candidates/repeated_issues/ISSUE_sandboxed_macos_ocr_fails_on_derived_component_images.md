# Repeated Issue: Sandboxed macOS OCR Fails On Derived Component Images

## Symptom

A derived crop or reviewed component image is structurally valid, but macOS OCR fails in sandbox while the same image succeeds when rerun unsandboxed.

## Current Proven Example

- reviewed isolated-component crop on `image11.png`
- sandboxed OCR failed on the derived crop surface
- unsandboxed OCR returned `usable` with the expected table-token set
- the bounded rerun only became valid after the unsandboxed OCR evidence was used

## Why This Is Dangerous

- it can make a strong reviewed component look worse than the full image
- it can push the workflow toward a premature waiver
- it hides a runtime boundary problem as if it were an OCR-quality problem

## Guardrail

Always rerun macOS OCR unsandboxed before waiving a reviewed component branch when:

- the image is a newly derived crop or component image
- sandbox OCR fails with generic Foundation or fallback errors
- the source image already suggests the crop should improve semantic focus

## Linked Pattern

- `Sandboxed macOS OCR Context Builder Drift`
