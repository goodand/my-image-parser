# REFERENCE_multimodal_tool_examples_v0_1-at2026-04-13

## Purpose

This reference closes the gap between contract-only tool design and reusable example artifacts.

It links the first two concrete example surfaces:

- [multimodal_context_refinement_examples_v0_1_at2026_04_13.json](../manifests/multimodal_context_refinement_examples_v0_1_at2026_04_13.json)
- [multimodal_to_ppt_tool_example_io_v0_1_at2026_04_13.json](../manifests/multimodal_to_ppt_tool_example_io_v0_1_at2026_04_13.json)

## Why These Examples Exist

The tool specs were already closed at contract level:

- [SPEC_multimodal_context_refinement_tool.md](../specs/prose/SPEC_multimodal_context_refinement_tool.md)
- [multimodal_context_refinement_tool.contract.json](../specs/contracts/multimodal_context_refinement_tool.contract.json)
- [SPEC_multimodal_to_ppt_tool.md](../specs/prose/SPEC_multimodal_to_ppt_tool.md)
- [multimodal_to_ppt_tool.contract.json](../specs/contracts/multimodal_to_ppt_tool.contract.json)

What was missing was an example that another agent could read without guessing:

- what a generic multimodal bundle looks like
- how that bundle is consumed by the PPT-facing tool
- where manual gates remain honest and explicit

The thin runner that materializes the generic bundle shape is here:

- [REFERENCE_multimodal_context_refinement_tool_runner-at2026-04-13.md](./REFERENCE_multimodal_context_refinement_tool_runner-at2026-04-13.md)

The thin runner that turns bundle outputs into PPT-prep artifacts is here:

- [REFERENCE_multimodal_to_ppt_tool_runner-at2026-04-13.md](./REFERENCE_multimodal_to_ppt_tool_runner-at2026-04-13.md)

## Example 1. Generic Multimodal Tool

The first example bundle is intentionally mixed:

- `image27_system_diagram`
  - shows a case that is closed enough for downstream PPT support
- `image23_portfolio_table`
  - shows a case that is still honest about value-level uncertainty

This matters because the experiments proved that a reusable tool must support both:

- closed interpretation with preserved form
- explicit pending state when table or component grounding is still insufficient

## Example 2. PPT Consumer Tool

The second example shows how the generic bundle becomes PPT-facing output.

It does not invent a new deck lane.

It reuses current workspace truth:

- [ppt_page_link_matrix_v0_1.json](../manifests/ppt_page_link_matrix_v0_1.json)
- [ppt_regeneration_handoff_bundle_v0_1_at2026_04_13.json](../manifests/ppt_regeneration_handoff_bundle_v0_1_at2026_04_13.json)
- [lean_02_1_system_first_v2_image_role_matrix_at2026_04_13.json](../manifests/lean_02_1_system_first_v2_image_role_matrix_at2026_04_13.json)
- [lean_02_1_system_first_v2.pptx](../assets/portfolio_drafts/lean_02_1_system_first_v2/lean_02_1_system_first_v2.pptx)

## Ownership Boundary

- generic multimodal loop owner:
  - [`multimodal-evidence-refinement-loop`](<CLAUDE_SKILLS_ROOT>/Skills-Create-Project/multimodal-evidence-refinement-loop/SKILL.md)
- normalization specialist:
  - [`image-text-cot-review`](<CLAUDE_SKILLS_ROOT>/Skills-Create-Project/image-text-cot-review/SKILL.md)
- MCP lifecycle owner:
  - [`vendored-mcp-onboarding`](../../../../skills/vendored-mcp-onboarding/SKILL.md)
- PPT authoring surface:
  - [`pptx`](<CODEX_HOME>/skills/pptx/SKILL.md)

## Current Closure State

- specs exist: `yes`
- contracts exist: `yes`
- generic tool example exists: `yes`
- PPT consumer example exists: `yes`
- provider-executed OCR/component bundle exists: `no`
- standalone approved caption promotion exists: `no`

## One-Line Summary

These example artifacts are the first reusable bridge from experimental multimodal reading know-how into concrete tool-facing IO that another agent can consume without reconstructing the loop from prose alone.
