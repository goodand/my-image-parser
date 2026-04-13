# REPORT_lean_02_1_system_first_portfolio_visual_qa-at2026-04-13-13-30

## Scope

Visual QA for the lean `02_1` system-first portfolio v1 deck only.

Artifacts under review:

- `control/project_domain/resources/assets/portfolio_drafts/lean_02_1_system_first_v1/lean_02_1_system_first_v1.pptx`
- `control/project_domain/resources/assets/portfolio_drafts/lean_02_1_system_first_v1/render_sources`
- `control/project_domain/resources/assets/portfolio_drafts/lean_02_1_system_first_v1/renders`
- [lean_02_1_system_first_v1_image_role_matrix_at2026_04_11.json](../manifests/lean_02_1_system_first_v1_image_role_matrix_at2026_04_11.json)

Skill declaration used in this slice:

- `<CODEX_HOME>/skills/pptx/SKILL.md`
- `<CLAUDE_SKILLS_ROOT>/semantic-clarity-enhanced/SKILL.md`

## Initial QA Pass

Findings from the first render pass:

1. Slide 2 headline wrapped too aggressively and crowded the subtitle.
2. Slide 3 bullet block overflowed at the bottom edge.
3. Slide 4 bullet block overflowed into the footer area.
4. Slide 5 right-column copy was denser than needed for an image-led evidence slide.

## Fixes Applied

Applied changes in [build_lean_02_1_system_first_portfolio.py](../../../../scripts/build_lean_02_1_system_first_portfolio.py):

1. Compressed slide 2 title and subtitle copy to reduce wrap pressure.
2. Tightened slide 2 supporting explanation copy.
3. Reduced slide 3 bullet count from three to two and kept the slide image-led.
4. Reduced slide 4 bullet count from three to two so the footer would clear the content block.
5. Compressed slide 5 evidence copy while keeping the table as the dominant visual block.

## Reverify Pass

Reverification steps:

1. Rebuilt the deck and six single-slide render-source decks.
2. Re-rendered all slide previews with `qlmanage -t`.
3. Verified the final deck text with `markitdown`.

Evidence:

- [PLAN_lean_ppt_image_character_portfolio_slice-at2026-04-11.md](../master_plans/drafts/PLAN_lean_ppt_image_character_portfolio_slice-at2026-04-11.md)
- [build_lean_02_1_system_first_portfolio.py](../../../../scripts/build_lean_02_1_system_first_portfolio.py)
- [REFERENCE_lean_02_1_system_first_portfolio_review_index-at2026-04-13.md](../references/REFERENCE_lean_02_1_system_first_portfolio_review_index-at2026-04-13.md)

## Verification Result

- deck exists: `yes`
- deck slide count = `6`: `yes`
- role matrix row count = `6`: `yes`
- rendered slide image count = `6`: `yes`
- one fix-and-reverify cycle completed: `yes`

## Residual Caveat

Quick Look can keep stale same-filename preview cache during repeated QA passes.

Practical rule for this slice:

- the `.pptx` deck is the source of truth
- repeated preview drift should be checked against `markitdown` before assuming the deck itself is stale

This caveat affects preview confidence, not the saved deck artifact.

## Verdict

`pass_with_preview_cache_caveat`

The lean portfolio slice is reviewable and the deck artifact is valid.
