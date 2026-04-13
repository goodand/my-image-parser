# Review Surface Requirement Response By Control-Plane Program Steward

## Purpose

Freeze the Steward response to the review-surface requirement refresh submission so the next implementation slice can proceed without ambiguity.

This response is grounded in the current `my-image-parser` phase2 review contract and the submitted `vscode-markdown-review-surface` status packet.

## Direct Inputs

- [Submission packet](../../../../project_domain/resources/master_plans/SUBMISSION_review_surface_requirement_refresh_and_status_packet-for-control-plane-program-steward-at2026-04-09.md)
- review surface progress packet: `<VSCODE_REVIEW_SURFACE_ROOT>/control/project_domain/resources/references/REFERENCE_review_surface_progress_and_expert_evaluation_packet-at2026-04-08.md`
- slide preview evaluation packet: `<VSCODE_REVIEW_SURFACE_ROOT>/control/project_domain/resources/references/REFERENCE_slide_preview_writeback_evaluation_packet-at2026-04-08.md`
- [Bootstrap source review markdown](../../../../project_domain/resources/reports/REVIEW_phase1_caption_10w_obsidian_caption_review-at2026-03-27-19-08.md)
- [Phase2 decision capture spec](../../../../project_domain/resources/specs/prose/SPEC_corpus_review_decision_capture.md)
- [Phase2 operator policy](NOTE_phase2_caption_review_operator_policy-at2026-04-05-11-30.md)

## Steward Decision

### 1. Evaluation Body

- fixed decision:
  - `arm-by-arm candidate comparison`

Interpretation:

- the human evaluator must be able to compare actual candidate caption and alt-text outputs for the relevant arms inside the review workflow
- source markdown remains useful supporting context, but it is not the primary evaluation body for this phase
- a metadata-only decision form is not enough to justify `selected_caption_arm`, `approved_caption`, and `approved_alt_text`

### 2. Required UX

- fixed decision:
  - `candidate text comparison included`

Interpretation:

- the review surface must include a read-only candidate-text comparison section
- the decision form remains necessary, but it is not sufficient by itself
- the comparison section does not need to live entirely inside the right panel
- prefer a vertical split for wide slides:
  - top: slide preview (wide)
  - bottom: candidate comparison + decision entry
- preferred split:
  - main body: image and arm-by-arm candidate caption/alt text comparison
  - right panel: decision entry, status, and compact summary

### 3. Master Plan Completion Criterion

- fixed decision:
  - `comparison UX completion included`

Interpretation:

- `10-image bootstrap/open works` is only an intermediate readiness proof
- this slice is not considered complete merely because a session can be opened
- the completion bar for the human evaluation surface is:
  - 10-image session bootstrap/open works
  - candidate text comparison is available in-surface
  - a reviewer can make bounded decisions without reopening external artifact chains

### 4. Lane Boundary

- fixed decision:
  - `decision-slides` and `slide-preview` stay split

Interpretation:

- `decision-slides` remains the human evaluation lane
- `slide-preview` remains the source-grounded selection/writeback proof lane
- do not collapse them into one surface in this slice
- reuse bridge seams where helpful, but preserve the lane boundary

### 5. Candidate Text Source Of Truth

- fixed decision:
  - `artifact contract extension required`

Interpretation:

- candidate texts must come from explicit session/bootstrap artifacts
- do not rely on ad hoc reparsing of human-facing markdown as the canonical source of arm text comparison
- the session artifact contract should explicitly carry per-arm caption and alt-text payloads for the evaluation surface

## Ordered Next Priority

Freeze the next implementation order as:

1. `artifact contract extension`
2. `candidate-text comparison section`
3. `label readability / operator clarity`
4. `actual 10-image evaluation run on the refreshed surface`
5. `cross-mode consolidation` only after the above

This means the correct path is:

- not `current contract + immediate evaluation`
- instead `contract extension + comparison UI + then human evaluation`

## Why This Decision Was Chosen

The current phase2 decision model in `my-image-parser` already assumes a reviewer will choose among arm outputs and possibly approve an edited final caption.

That decision cannot be made cleanly from:

- image preview alone
- metadata such as `active default`, `comparison winner`, and `promotion state`
- source markdown that does not expose the candidate comparison payload in the evaluation surface itself

Therefore the surface must expose the candidate texts directly if it is to serve as the canonical human evaluation lane.

## Explicit Non-Goals For This Slice

- no collapse of `decision-slides` and `slide-preview` into one mode
- no generic WYSIWYG expansion
- no requirement to make the right panel hold all comparison content
- no reliance on external markdown reading as the sole evaluation method

## Operational Effect

After this note:

- the open/bootstrap path remains valid but incomplete for final acceptance
- metadata-only review UX is treated as insufficient for phase completion
- the next accepted implementation slice must extend the session artifact contract and surface the candidate texts
- only after that should the 10-image evaluation be treated as the main execution task
