# REFERENCE_multimodal_context_refinement_tool_runner-at2026-04-13

## Purpose

This reference explains the thin runner for `multimodal_context_refinement_tool`.

- runner: [`scripts/run_multimodal_context_refinement_tool.py`](../../../../scripts/run_multimodal_context_refinement_tool.py)
- lib: [`scripts/multimodal_context_refinement_tool_lib.py`](../../../../scripts/multimodal_context_refinement_tool_lib.py)

The runner is intentionally thin.

It does not own OCR providers or component extraction.

It assembles, validates, and emits the stable bundle shape so that other agents can reuse the experiment result without reconstructing the contract from prose.

## Modes

### 1. `emit-example`

Use a stored example record and materialize a full bundle.

```bash
python3 scripts/run_multimodal_context_refinement_tool.py emit-example \
  --example-id image27_system_diagram \
  --output-json /tmp/multimodal_context_bundle_image27.json \
  --output-report /tmp/multimodal_context_bundle_image27.md
```

### 2. `emit-bundle`

Use explicit JSON inputs to assemble a bundle from current evidence.

Required inputs:

- `--source-image-path`
- `--task-intent`
- `--provider-policy-json`
- `--loop-budget-json`
- `--output-json`

Optional JSON inputs:

- `--baseline-context-json`
- `--evidence-bundle-json`
- `--normalized-interpretation-json`
- `--form-preservation-json`
- `--loop-state-json`

## Boundary

- allowed:
  - bundle assembly
  - contract validation
  - markdown report emission
- not allowed:
  - provider onboarding
  - OCR runtime ownership
  - PPT authoring
  - human approval finalization

## Current Examples

- [multimodal_context_refinement_examples_v0_1_at2026_04_13.json](../manifests/multimodal_context_refinement_examples_v0_1_at2026_04_13.json)
- [REFERENCE_multimodal_tool_examples_v0_1-at2026-04-13.md](./REFERENCE_multimodal_tool_examples_v0_1-at2026-04-13.md)

## One-Line Summary

The thin runner makes the multimodal tool contract executable enough for reuse without pretending that provider execution or PPT authoring now belong to the same tool.
