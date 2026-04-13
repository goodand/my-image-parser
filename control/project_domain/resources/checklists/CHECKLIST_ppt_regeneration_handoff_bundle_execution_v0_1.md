# CHECKLIST_ppt_regeneration_handoff_bundle_execution_v0_1

## Purpose

Use this checklist when a later lane consumes:

- [ppt_regeneration_handoff_bundle_v0_1_at2026_04_13.json](../manifests/ppt_regeneration_handoff_bundle_v0_1_at2026_04_13.json)

and must regenerate or safely edit the lean `02_1` portfolio deck.

## Required Skill Surfaces

- `<CODEX_HOME>/skills/pptx/SKILL.md`
- `<CLAUDE_SKILLS_ROOT>/semantic-clarity-enhanced/SKILL.md`

## Before Starting

- [ ] Open [ppt_regeneration_handoff_bundle_v0_1_at2026_04_13.json](../manifests/ppt_regeneration_handoff_bundle_v0_1_at2026_04_13.json)
- [ ] Open [ppt_page_link_matrix_v0_1.json](../manifests/ppt_page_link_matrix_v0_1.json)
- [ ] Open [REFERENCE_ppt_regeneration_handoff_bundle_v0_1-at2026-04-13.md](../references/REFERENCE_ppt_regeneration_handoff_bundle_v0_1-at2026-04-13.md)
- [ ] Open [REFERENCE_lean_02_1_system_first_portfolio_review_index-at2026-04-13.md](../references/REFERENCE_lean_02_1_system_first_portfolio_review_index-at2026-04-13.md)
- [ ] Confirm the current deck exists: `control/project_domain/resources/assets/portfolio_drafts/lean_02_1_system_first_v1/lean_02_1_system_first_v1.pptx`
- [ ] Confirm the current render set contains exactly `6` slide images
- [ ] Confirm the handoff bundle still says `ready_for_manual_regeneration_with_text_promotion_pending`
- [ ] Confirm no deletion is planned in this slice

## Ownership Boundary

- [ ] Treat Band 8 image understanding as upstream evidence, not as PPT ownership
- [ ] Treat `pptx` as the only PPT authoring owner surface
- [ ] Treat `semantic-clarity-enhanced` as copy support only
- [ ] Do not create a new owner skill while executing this checklist
- [ ] Do not reopen MCP onboarding, launcher, inventory, or activation work

## Per Slide

- [ ] Read `source_images`
- [ ] Read `current_pages`
- [ ] Read `text_promotion_state`
- [ ] Read `regeneration_handoff`
- [ ] Keep the declared `presentation_role`
- [ ] Keep the declared `visual_type`
- [ ] Keep the declared `supporting_text_goal`
- [ ] Keep the declared `layout_role`
- [ ] Preserve the dominant visual block before rewriting copy
- [ ] Preserve form-bearing details that make the image useful, not generic
- [ ] If the slide is table-heavy, preserve value-level readability
- [ ] If the slide is UI-heavy, preserve before/after or flow readability
- [ ] If the slide is code/problem-heavy, preserve problem/solution pairing
- [ ] Do not claim standalone approved caption or alt-text promotion unless it was separately created

## Regeneration Checks

- [ ] Deck still contains exactly `6` slides after regeneration
- [ ] Each regenerated slide still maps to the same `target_slide_no`
- [ ] Slide 1 still reads as `architecture_hero`
- [ ] Slide 2 still reads as a paired product experience flow
- [ ] Slide 3 still reads as profile credibility, not portrait-first
- [ ] Slide 4 still reads as problem-and-code proof
- [ ] Slide 5 still reads as evidence table with readable values
- [ ] Slide 6 still reads as applied AI workflow closure

## QA

- [ ] Re-render slide previews after regeneration
- [ ] Re-run one visual QA pass
- [ ] Complete at least one fix-and-reverify cycle if any issue is found
- [ ] If Quick Look preview and deck disagree, trust the `.pptx` deck first
- [ ] If `markitdown` is available, verify the regenerated deck text once

## Stop Conditions

- [ ] Stop if the handoff requires new MCP/provider setup
- [ ] Stop if the handoff requires deleting current portfolio artifacts
- [ ] Stop if the handoff requires inventing missing approved-caption truth
- [ ] Stop if the handoff would break the system-first narrative
- [ ] Stop if any slide loses its dominant image role during regeneration
