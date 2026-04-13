# REFERENCE_multimodal_tools_start_here-at2026-04-13

## Purpose

This is the fastest entry surface for another agent that needs to use the current multimodal tool chain.

Use this when the goal is:

- turn image understanding evidence into a reusable machine bundle
- turn that bundle into PPT-prep artifacts
- hand the result to the global [`pptx`](<CODEX_HOME>/skills/pptx/SKILL.md) surface without rebuilding the tool chain from prose

## Tool Split

### 1. Generic image-understanding tool

- spec:
  - [SPEC_multimodal_context_refinement_tool.md](../specs/prose/SPEC_multimodal_context_refinement_tool.md)
- contract:
  - [multimodal_context_refinement_tool.contract.json](../specs/contracts/multimodal_context_refinement_tool.contract.json)
- runner:
  - [REFERENCE_multimodal_context_refinement_tool_runner-at2026-04-13.md](./REFERENCE_multimodal_context_refinement_tool_runner-at2026-04-13.md)

Use this first.

Its output is a `multimodal_context_bundle`.

### 2. PPT-facing consumer tool

- spec:
  - [SPEC_multimodal_to_ppt_tool.md](../specs/prose/SPEC_multimodal_to_ppt_tool.md)
- contract:
  - [multimodal_to_ppt_tool.contract.json](../specs/contracts/multimodal_to_ppt_tool.contract.json)
- runner:
  - [REFERENCE_multimodal_to_ppt_tool_runner-at2026-04-13.md](./REFERENCE_multimodal_to_ppt_tool_runner-at2026-04-13.md)

Use this second.

Its output is a PPT-prep package:

- `ppt_prep_package_manifest.json`
- `ppt_story_plan.json`
- `ppt_slide_role_matrix.json`
- `ppt_regeneration_handoff_bundle.json`

### 3. PPT authoring owner surface

- [`pptx`](<CODEX_HOME>/skills/pptx/SKILL.md)

Use this last.

It remains the authoring owner surface.

The multimodal tools do not replace it.

## Fastest Path

### Path A. Reuse the stored examples

1. Emit a generic multimodal bundle example.
2. Emit a PPT-prep package example.
3. Read the emitted package and hand it to `pptx`.

Commands:

```bash
python3 scripts/run_multimodal_context_refinement_tool.py \
  emit-example \
  --example-id image27_system_diagram \
  --output-json /tmp/multimodal_context_bundle.json \
  --output-report /tmp/multimodal_context_bundle.md

python3 scripts/run_multimodal_to_ppt_tool.py \
  emit-example \
  --output-dir /tmp/multimodal_to_ppt_package \
  --output-report /tmp/multimodal_to_ppt_package/report.md
```

### Path B. Build from explicit bundle inputs

1. Produce one or more `multimodal_context_bundle` JSON files.
2. Prepare one input JSON for `multimodal_to_ppt_tool`.
3. Emit the PPT-prep package.

Command:

```bash
python3 scripts/run_multimodal_to_ppt_tool.py \
  emit-package \
  --input-json /tmp/multimodal_to_ppt_input.json \
  --output-dir /tmp/multimodal_to_ppt_package \
  --output-report /tmp/multimodal_to_ppt_package/report.md
```

## Current Example Truth

- generic bundle examples:
  - [multimodal_context_refinement_examples_v0_1_at2026_04_13.json](../manifests/multimodal_context_refinement_examples_v0_1_at2026_04_13.json)
- PPT example IO:
  - [multimodal_to_ppt_tool_example_io_v0_1_at2026_04_13.json](../manifests/multimodal_to_ppt_tool_example_io_v0_1_at2026_04_13.json)
- bridge reference:
  - [REFERENCE_multimodal_tool_examples_v0_1-at2026-04-13.md](./REFERENCE_multimodal_tool_examples_v0_1-at2026-04-13.md)

## Boundary

- The generic tool preserves image evidence, OCR evidence, component evidence, reinjected context, normalized judgment, and pending reasons.
- The PPT tool consumes that output and emits PPT-prep artifacts only.
- `slides-grab` remains donor/reference only.
- `.pptx` generation or editing remains owned by [`pptx`](<CODEX_HOME>/skills/pptx/SKILL.md).

## Verification

Minimum checks:

```bash
python3 scripts/test_multimodal_context_refinement_tool_lib.py
python3 scripts/test_multimodal_to_ppt_tool_lib.py
```

## One-Line Summary

If another agent needs the current multimodal tool chain, the order is: `multimodal_context_refinement_tool -> multimodal_to_ppt_tool -> pptx`.
