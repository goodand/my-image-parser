# REFERENCE_multimodal_to_ppt_tool_runner-at2026-04-13

## Purpose

This reference explains the thin runner for:

- [`multimodal_to_ppt_tool`](../specs/prose/SPEC_multimodal_to_ppt_tool.md)

The runner does not author a `.pptx` deck directly.

It emits a PPT-prep package that other agents can pass to the global [`pptx`](<CODEX_HOME>/skills/pptx/SKILL.md) surface.

## Files

- runner lib:
  - [`scripts/multimodal_to_ppt_tool_lib.py`](../../../../scripts/multimodal_to_ppt_tool_lib.py)
- CLI:
  - [`scripts/run_multimodal_to_ppt_tool.py`](../../../../scripts/run_multimodal_to_ppt_tool.py)
- tests:
  - [`scripts/test_multimodal_to_ppt_tool_lib.py`](../../../../scripts/test_multimodal_to_ppt_tool_lib.py)

## Output Boundary

The runner emits:

- `ppt_prep_package_manifest.json`
- `ppt_story_plan.json`
- `ppt_slide_role_matrix.json`
- `ppt_regeneration_handoff_bundle.json`

It does not emit a final deck.

PPT authoring remains a downstream step owned by [`pptx`](<CODEX_HOME>/skills/pptx/SKILL.md).

## Commands

### 1. Emit the stored example package

```bash
python3 scripts/run_multimodal_to_ppt_tool.py \
  emit-example \
  --output-dir /tmp/multimodal_to_ppt_example \
  --output-report /tmp/multimodal_to_ppt_example/report.md
```

### 2. Emit a package from explicit multimodal context bundles

Prepare an input JSON object that contains:

- `multimodal_context_bundles` or `multimodal_context_bundle_refs`
- `presentation_intent`
- `story_intent`
- `slide_plan`
- `ppt_authoring_policy`

Then run:

```bash
python3 scripts/run_multimodal_to_ppt_tool.py \
  emit-package \
  --input-json /tmp/multimodal_to_ppt_input.json \
  --output-dir /tmp/multimodal_to_ppt_explicit \
  --output-report /tmp/multimodal_to_ppt_explicit/report.md
```

## Step By Step

1. Build or load `multimodal_context_bundle` inputs first.
2. Decide slide-worthy scope before calling the runner.
3. Use this runner to emit a PPT-prep package.
4. Hand the emitted package to a later agent that uses [`pptx`](<CODEX_HOME>/skills/pptx/SKILL.md).
5. Treat the emitted handoff bundle as consumer-ready input, not as proof that the deck was already regenerated.

## Manual Gates That Remain

- table-heavy slides still need value-level readability judgment
- the emitted package does not human-approve text promotion
- donor tools such as `slides-grab` remain reference-only

## One-Line Summary

`run_multimodal_to_ppt_tool.py` gives other agents a reusable thin CLI that turns multimodal understanding outputs into PPT-prep artifacts without collapsing the `pptx` authoring boundary.
