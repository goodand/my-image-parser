# REPORT_multimodal_tool_split_decision-at2026-04-13-16-59

## Decision

The experimental results are now promoted into two tool contracts, not one:

1. `multimodal_context_refinement_tool`
2. `multimodal_to_ppt_tool`

## Why The Split Is Correct

The experiment proved two different kinds of value:

- generic multimodal understanding value
- PPT-specific consumption and regeneration value

If they stay fused, the result becomes too large, less reusable, and harder to verify.

If they are split:

- the first tool becomes broadly reusable
- the second tool becomes a focused consumer tool
- verification boundaries become clearer

## What The Experiment Directly Proved

- whole-image plus component evidence is stronger than one-shot captioning
- OCR must be layered, not single-pass
- table-heavy images need value-level coverage checks
- multimodal form sometimes carries meaning and must not be flattened into noise
- PPT generation should remain image-led and consumer-facing, not absorbed into the generic image-understanding loop

## Current Promotion Outputs

- [SPEC_multimodal_context_refinement_tool.md](../specs/prose/SPEC_multimodal_context_refinement_tool.md)
- [multimodal_context_refinement_tool.contract.json](../specs/contracts/multimodal_context_refinement_tool.contract.json)
- [SPEC_multimodal_to_ppt_tool.md](../specs/prose/SPEC_multimodal_to_ppt_tool.md)
- [multimodal_to_ppt_tool.contract.json](../specs/contracts/multimodal_to_ppt_tool.contract.json)

## Immediate Next Step

The next implementation slice should build only the first runnable contract surface:

- emit one `multimodal_context_bundle_atYYYY_MM_DD.json`
- verify that later PPT-facing work can consume it without reopening OCR/provider logic

## One-Line Summary

The experiment result is promoted as two separate tools: one generic multimodal understanding tool and one PPT consumer tool that uses the first tool's outputs without absorbing its responsibilities.
