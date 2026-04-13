# REPORT_lean_02_1_system_first_portfolio_v2_visual_qa-at2026-04-13-15-37

## Scope

Visual QA for the regenerated lean `02_1` system-first portfolio v2 deck only.

Artifacts under review:

- `control/project_domain/resources/assets/portfolio_drafts/lean_02_1_system_first_v2/lean_02_1_system_first_v2.pptx`
- `control/project_domain/resources/assets/portfolio_drafts/lean_02_1_system_first_v2/render_sources`
- `control/project_domain/resources/assets/portfolio_drafts/lean_02_1_system_first_v2/renders`
- [lean_02_1_system_first_v2_image_role_matrix_at2026_04_13.json](../manifests/lean_02_1_system_first_v2_image_role_matrix_at2026_04_13.json)
- [ppt_regeneration_handoff_bundle_v0_1_at2026_04_13.json](../manifests/ppt_regeneration_handoff_bundle_v0_1_at2026_04_13.json)

Skill declaration used in this slice:

- `<CODEX_HOME>/skills/pptx/SKILL.md`
- `<CLAUDE_SKILLS_ROOT>/semantic-clarity-enhanced/SKILL.md`

## Initial QA Pass

Findings from the first v2 render pass:

1. Slide 5 still left the evidence table slightly smaller than desired for value-level reading.
2. Slide 6 used a note band that visually competed with the workflow screenshot, making the UI read smaller than necessary.

## Fixes Applied

Applied changes in [build_lean_02_1_system_first_portfolio_v2.py](../../../../scripts/build_lean_02_1_system_first_portfolio_v2.py):

1. Increased slide 5 image region width and height.
2. Reduced slide 5 note-band height so the table keeps more vertical room.
3. Increased slide 6 screenshot region height.
4. Reduced slide 6 note-band height to reduce competition with the screenshot.

## Reverify Pass

Reverification steps:

1. Rebuilt the deck with `.venv/bin/python`.
2. Re-rendered all six slide previews after the patch.
3. Rechecked slide 5 and slide 6 visually against the initial concerns.

## Verification Result

- deck exists: `yes`
- deck slide count = `6`: `yes`
- role matrix row count = `6`: `yes`
- rendered slide image count = `6`: `yes`
- one fix-and-reverify cycle completed: `yes`

## Residual Caveat

- Slide 6 remains a tall, narrow UI source image by nature.
- The slide now gives the screenshot more height, but the source aspect ratio still limits how wide it can read without cropping.
- This is acceptable for v2 because workflow integrity was prioritized over aggressive crop enlargement.

## Verdict

`pass_with_aspect_ratio_caveat`

The regenerated v2 deck is reviewable, image-led, and materially better aligned with the handoff bundle than v1.
