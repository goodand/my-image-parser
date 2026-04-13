# Multimodal To PPT Tool

## Purpose

Define the consumer tool that takes multimodal understanding output and turns it into PPT-ready slide input.

This tool is not the generic image-understanding tool.

It is the downstream specialization that uses:

- multimodal understanding bundles
- page intent
- story intent
- publication intent

to create PPT-facing outputs.

## Tool Split

The split is intentional:

1. `multimodal_context_refinement_tool`
   - generic
   - reusable
   - image understanding only
2. `multimodal_to_ppt_tool`
   - consumer-specific
   - PPT-facing
   - turns understanding into slides, role matrices, and deck outputs

## Canonical Inputs

- one or more `multimodal_context_bundle` inputs
  - thin runner surface: `multimodal_context_bundles` or `multimodal_context_bundle_refs`
- `presentation_intent`
  - examples: `portfolio`, `review_deck`, `evidence_deck`, `client_summary`
- `slide_plan`
  - target slide count
  - ordering
  - one dominant visual block rule
- `page_link_matrix` if available
- `ppt_authoring_policy`
  - current owner surface is `pptx`

## Canonical Responsibilities

This tool may:

- choose which multimodal outputs are slide-worthy
- map images to slide roles
- derive supporting text goals
- prepare deck-facing structured input
- call or hand off to the PPT authoring surface

This tool must not:

- re-run the full multimodal understanding loop as its default behavior
- pretend PPT is a new owner family
- flatten form-bearing evidence into generic marketing bullets

## Output Layers

- story plan
- slide role matrix
- PPT regeneration handoff bundle
- optional regenerated deck
- review index
- visual QA evidence

## Thin Runner Surface

The current thin runner emits fixed filenames inside a caller-provided output directory:

- `ppt_prep_package_manifest.json`
- `ppt_story_plan.json`
- `ppt_slide_role_matrix.json`
- `ppt_regeneration_handoff_bundle.json`

These are the runnable surface names.

The dated artifact names in higher-level planning language still describe the canonical artifact classes, not a required on-disk filename contract for the thin runner.

## PPT Boundary

PPT authoring remains a separate surface:

- `pptx` is the authoring owner surface

This tool may prepare structured deck input and invoke that surface, but does not absorb it into a new owner family.

## External Tool Donor Boundary

Adjacent tooling such as local `slides-grab` clones may be referenced for:

- export ideas
- review surface ideas
- adjacent workflow patterns

but they remain donor/reference surfaces.

They are not the source of truth for current workspace deck outputs.

## Quality Rules

- one dominant visual block per slide
- preserve form when the source image itself is evidence
- keep table-heavy slides readable at value level, not just table presence level
- support top-bottom layouts when wide slide geometry makes that more legible
- do not let supporting text outrun the image evidence

## Non-Goals

- do not own provider onboarding
- do not replace the generic multimodal tool
- do not change image metadata or approval records
- do not force every workflow into PPT

## One-Line Summary

The `multimodal_to_ppt_tool` is the consumer tool that converts multimodal understanding bundles into story- and deck-ready PPT artifacts while keeping `pptx` as the authoring owner surface.
