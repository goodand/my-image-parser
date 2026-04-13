# Repeated Task: Binary Evidence Batch Packaging With Scope Guard

## Pattern Name

- binary evidence batch packaging with scope guard

## Trigger

- a review-facing slice includes binary deliverables such as PPTX, JPG renders, and screenshots
- the artifacts are small enough to keep in Git, but only if their scope stays bounded
- the packaging pass must avoid accidentally pulling in unrelated binaries or tool caches

## Stable Steps

1. Measure the size of the binary artifact set before staging it.
2. Enumerate the exact files that belong to the bounded evidence set.
3. Confirm the artifacts are review-facing outputs rather than runtime caches, vendor payloads, or local scratch.
4. Stage only the bounded binary set plus any tiny companion state files needed for review context.
5. Verify the staged list before commit so no adjacent bulky directory leaked in.
6. Commit the evidence batch separately from text-only docs and separately from vendor absorption decisions.

## Candidate Promotion

- checklist: bounded binary packaging preflight
- review rule: size and scope must both be checked before staging binary evidence
- helper: directory inventory + size summary before binary evidence commit

## Promotion Trigger

- another presentation or review slice needs to commit a small binary proof set without opening the door to large runtime payloads

## Current Proven Evidence

- on 2026-04-13, `my-image-parser` measured the lean `02_1` portfolio draft set, confirmed it was bounded review evidence, and committed the PPTX, six render-source decks, six rendered JPGs, three screenshots, and one `.surface.json` in `999e72b`

## Step-By-Step Evidence Trace

1. The binary set was read from the lean execution contract before staging.
   - plan evidence: `control/project_domain/resources/master_plans/drafts/PLAN_lean_ppt_image_character_portfolio_slice-at2026-04-11.md`
   - review index evidence: `control/project_domain/resources/references/REFERENCE_lean_02_1_system_first_portfolio_review_index-at2026-04-13.md`
2. The exact bounded binary inventory was enumerated.
   - one final deck PPTX
   - six `render_sources/slide-*-source.pptx`
   - six `renders/slide-*.jpg`
   - three review screenshots
   - one `.surface.json`
3. Size was measured before staging.
   - `portfolio_drafts`: about `4.6M`
   - screenshots: about `1.3M` each
4. The set was then classified as review evidence, not runtime residue.
   - supporting QA evidence: `control/project_domain/resources/reports/REPORT_lean_02_1_system_first_portfolio_visual_qa-at2026-04-13-13-30.md`
5. Only the bounded binary set plus the tiny review-surface state file were staged.
6. The batch was committed separately from text docs and separately from vendor decisions in `999e72b`.
