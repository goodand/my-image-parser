# Multimodal Context Refinement Tool

## Purpose

Define a high-reuse tool contract for iterative multimodal understanding.

This tool is the direct promotion target of the image-caption experiments.

It exists to turn the proven loop:

- whole-image read
- whole-image OCR
- component split
- per-component OCR
- table or structure extraction when needed
- context reinjection
- repeated LLM interpretation

into one reusable tool-facing contract.

The output is not a deck.

The output is a machine-usable multimodal understanding bundle that later tools can consume.

## Why This Tool Is Generic

This tool should be usable outside `my-image-parser`.

It is useful whenever an image or slide-derived image carries meaning in:

- layout
- table structure
- chart labels
- UI controls
- code blocks
- multimodal form

and cannot be safely flattened into one-shot caption text.

## Design Rule

The tool must preserve the distinction between:

- raw image evidence
- OCR evidence
- component evidence
- reinjected context
- normalized judgment
- unresolved pending reasons

It must not blend these into one paragraph.

## Canonical Inputs

- `source_image_path`
- `task_intent`
  - examples: `caption`, `review`, `form_preservation`, `ppt_support`
- `baseline_context`
  - existing caption
  - existing OCR
  - source slide metadata
  - prior human review if available
- `provider_policy`
  - which OCR/table/component providers are allowed
- `loop_budget`
  - max passes
  - stop conditions

## Canonical Loop

1. Read the full image first.
2. Produce the first image-type judgment.
3. Run whole-image OCR.
4. Decide whether component split is needed.
5. If needed, produce component crops.
6. Run per-component OCR.
7. If the image is table-heavy or chart-heavy, request structure-aware extraction.
8. Reinject the current evidence stack into the next LLM pass.
9. Compare the new pass with the baseline and prior pass.
10. Either:
   - close to a normalized state
   - or leave an explicit `pending` reason with next-pass focus

## Required Output Layers

- evidence bundle
  - source image
  - whole-image OCR
  - component crops
  - component OCR
  - structure-aware extraction if present
- normalized interpretation
  - image type
  - form-bearing summary
  - candidate caption
  - candidate alt text
- form-preservation assessment
  - enough for downstream
  - underspecified
  - blocked
- loop state
  - pass count
  - closure state
  - pending reasons
  - unresolved fields

## Output Quality Rules

- Table-heavy images must not stop at `a table is shown`.
- If value-level reading matters, the tool must say whether value coverage was achieved.
- UI images must keep interaction-region meaning, not only surface appearance.
- Code/problem images must keep problem-solution pairing if both are visible.
- Layout or form meaning must be explicitly called out when later consumers depend on it.

## Non-Goals

- do not author PPT directly
- do not commit image metadata
- do not finalize human approval
- do not treat downstream deck layout as part of this tool

## Owner/Family Boundary

- owner-family anchor:
  - `multimodal-evidence-refinement-loop`
- specialist normalization:
  - `image-text-cot-review`
- provider lifecycle remains separate:
  - `vendored-mcp-onboarding`

## One-Line Summary

The `multimodal_context_refinement_tool` is the generic reusable tool contract that turns iterative whole-image, OCR, component, and reinjected-context reading into one stable multimodal understanding bundle.
