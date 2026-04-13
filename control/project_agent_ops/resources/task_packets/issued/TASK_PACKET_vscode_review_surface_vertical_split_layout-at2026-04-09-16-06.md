# Task Packet: VS Code Review Surface Vertical Split Layout

## Goal

Update the `decision-slides` lane UI layout so wide PPT-style slides are evaluated in a top/bottom split (vertical split), not a left/right split.

The expected operator experience is:

- top: wide slide preview (primary attention surface)
- bottom: candidate comparison + decision entry (operator controls)
- advanced metadata is not the primary body and must be collapsible

This is a UX/layout slice only. It must not change evaluation semantics, contracts, or writeback behavior.

## Fixed Truth Inputs

- Steward requirement response:
  - `control/user_decisions/resources/notes/NOTE_review_surface_requirement_response_by_control-plane-program-steward-at2026-04-09-14-17.md`
- Submission packet:
  - `control/project_domain/resources/master_plans/SUBMISSION_review_surface_requirement_refresh_and_status_packet-for-control-plane-program-steward-at2026-04-09.md`
- Bootstrap source review markdown (evidence only):
  - `control/project_domain/resources/reports/REVIEW_phase1_caption_10w_obsidian_caption_review-at2026-03-27-19-08.md`
- Bootstrap session evidence (do not regenerate in this slice):
  - `control/project_domain/resources/reports/REVIEW_phase1_caption_10w_obsidian_caption_review-at2026-03-27-19-08.review-surface-session/phase2-caption-decision-slides-first-10`
- Reference packets:
  - `<VSCODE_REVIEW_SURFACE_ROOT>/control/project_domain/resources/references/REFERENCE_review_surface_progress_and_expert_evaluation_packet-at2026-04-08.md`
  - `<VSCODE_REVIEW_SURFACE_ROOT>/control/project_domain/resources/references/REFERENCE_slide_preview_writeback_evaluation_packet-at2026-04-08.md`

## Scope

- only `vscode-markdown-review-surface` UI layout for `decision-slides`
- restructure view composition into a vertical split optimized for wide slides
- keep navigation (`Prev/Next`) behavior intact
- keep decision entry form behavior intact
- keep session summary/feedback summary intact

## Non-Goals

- do not change session bootstrap logic
- do not change artifact contracts or payload shape
- do not add candidate text comparison content (this is a separate contract slice)
- do not touch `slide-preview` lane
- do not implement retrieval/mapping coupling

## Implementation Notes

- the current pain is that wide slides get visually compressed under left/right layouts
- the right panel is currently metadata-heavy; after this slice it should feel like an operator control panel, not the evaluation body
- prefer progressive disclosure:
  - show minimal decision controls by default
  - hide derived metadata behind a toggle (e.g. "Advanced")

## Suggested Edit Targets (vscode-markdown-review-surface)

- `src/decision/slide-shell.js`
- `src/decision/webview-html.js`
- `src/decision/slide-decision-form.js`
- `src/decision/slide-session-summary.js`
- related CSS/layout in the webview (wherever the lane styles live)

## Done Definition

- in `decision-slides`, the slide preview is full-width in a top region and is not horizontally squeezed by a right-side panel
- decision entry remains usable without scrolling the slide out of view
- advanced metadata is collapsible and not dominant on first view
- no contract, bootstrap, or writeback changes were required

## Verification

- `npm test` in `vscode-markdown-review-surface` still passes
- manually open the existing bootstrap session and confirm:
  - slide is full-width and readable
  - decision entry is visible and usable
  - the layout matches top/bottom split

## Handoff Note

This slice intentionally does not solve the missing `candidate text comparison` requirement. It only makes the evaluation surface readable and operator-friendly for wide PPT-style slides.
