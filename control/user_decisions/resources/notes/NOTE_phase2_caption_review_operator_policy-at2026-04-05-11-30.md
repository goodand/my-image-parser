# Phase 2 Caption Review Operator Policy

## Purpose

Freeze the current operator policy for the `phase2` caption review decision stage so one human reviewer can convert the 9-image corpus review into canonical human decision rows.

This stage exists to finalize caption decisions for the active 9-image corpus so the reviewed rows can later move into retrieval or mapping preflight without reopening the full comparison workflow.

## Fixed Truth Inputs

Treat these as fixed truth while entering decisions:

- [Corpus closure report](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/reports/REPORT_phase1_caption_four_mode_corpus_closure-at2026-03-30-22-19.md)
- [Corpus review surface](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/reports/REVIEW_phase2_caption_four_mode_corpus_review-at2026-03-30-22-45.md)
- [Decision capture spec](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/specs/prose/SPEC_corpus_review_decision_capture.md)
- [Operator entry guide](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/reports/REVIEW_phase2_caption_review_decision_entry-at2026-03-30-23-23.md)
- [Operator checklist](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/checklists/CHECKLIST_phase2_caption_review_decision_entry.md)
- [Editable decision seed JSONL](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase2_caption_review_decision_seed_at2026_03_30.jsonl)

Do not modify corpus truth, bundle truth, or auto-eval truth during this stage.

## Current Global Policy Decisions

### 1. Reviewer Count

- fixed value:
  - `1 reviewer`

Interpretation:

- one human reviewer edits the canonical decision seed JSONL
- no concurrent editing of the canonical seed is allowed
- if multiple reviewers are needed later, split owned image ids ahead of time or use reviewer-local copies before merge

### 2. `approved_alt_text` Policy

- fixed value:
  - `required for completed rows`

Interpretation:

- every completed row must include `approved_alt_text`
- completion is not allowed with `approved_alt_text = null`
- this stage does not treat alt text as a follow-up cleanup item

### 3. Edit Path Policy

- fixed value:
  - `bounded edit path allowed`

Interpretation:

- prefer selecting one of the existing arms first
- if no existing arm text is good enough, use the contract-defined edit path
- the current contract expresses this as `selected_caption_arm = llm_edited_caption`
- do not introduce a separate `human_edited_caption` value at this stage

Required consequences:

- `selected_caption_arm = llm_edited_caption`
- `selected_caption_promotion_state = null`
- `caption_edit_required = true`
- `caption_decision = approve_edited_caption`

### 4. Retrieval Strictness

- fixed value:
  - `aggressive`

Interpretation:

- if the reviewer can produce a stable final caption, prefer `use_for_retrieval = true`
- only block retrieval when the row clearly belongs to a deferred lane, manual lane, or rejection lane

## Required Per-Row Decisions

Each image row must end with explicit values for:

- `selected_caption_arm`
- `selected_caption_promotion_state`
- `caption_decision`
- `caption_edit_required`
- `approved_caption`
- `approved_alt_text` or intentional `null` only while not completed
- `use_for_retrieval`
- `mapping_review_required`
- `outlier_candidate`
- `review_status`
- `reviewer_id`
- `reviewed_at`
- `decision_rationale`
- `retrieval_block_reason` if needed
- `outlier_reason` if needed
- `reviewer_notes`

Machine-prefilled fields remain fixed and must not be edited during ordinary review.

## Review Order

Review the current corpus in this order:

1. `image11`
2. `image7`
3. `image8`
4. `image10`
5. `image12`
6. `image13`
7. `image14`
8. `image9`
9. `image15`

This preserves the current priority order from the review surface.

## Per-Row Decision Questions

For each image, answer these questions explicitly:

1. Should the current default stay, should the comparison winner be chosen, should another arm be selected, or is the edit path needed?
2. Is the final caption stable enough for retrieval?
3. Does this image require additional mapping review?
4. Does this image look like an outlier candidate?
5. What final `approved_caption` should downstream consumers treat as canonical?

## Review Heuristic

Use this order when deciding a row:

1. Can one existing arm be approved as-is?
2. If not, can one existing arm be lightly edited into a stable final caption?
3. If yes, use `llm_edited_caption` and record the edit path explicitly.
4. Write both `approved_caption` and `approved_alt_text`.
5. If the final caption is stable enough to represent the image for retrieval, set `use_for_retrieval = true`.

## Operational Constraints

- the canonical seed JSONL has one active writer at a time
- machine-prefilled fields are not editable during ordinary review
- corpus truth, bundle truth, and auto-eval truth are fixed during decision entry
- retrieval execution is out of scope for this stage
- mapping execution is out of scope for this stage

## Done Condition

This stage is complete only when:

- all 9 rows are no longer `pending`
- each completed row satisfies the decision capture contract
- the ingestion validator passes
- `retrieval_ready_count` is explicit
- blocked rows carry explicit `retrieval_block_reason`
- outlier rows carry explicit `outlier_reason`

## Operational Effect

Under this policy:

- the canonical seed has one active editor
- `approved_caption` is the primary completion target
- `approved_alt_text` blocks completion until filled
- `llm_edited_caption` is the only bounded edit-path escape hatch
- retrieval opens by default once the reviewer has confidence in the final caption
- mapping and retrieval execution remain downstream phases, not part of this policy stage

## Directly Related Files

- [Decision capture spec](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/specs/prose/SPEC_corpus_review_decision_capture.md)
- [Decision capture contract](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/specs/contracts/corpus_review_decision_capture.contract.json)
- [Operator entry guide](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/reports/REVIEW_phase2_caption_review_decision_entry-at2026-03-30-23-23.md)
- [Operator checklist](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/checklists/CHECKLIST_phase2_caption_review_decision_entry.md)
- [Seed editing reference](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/references/REFERENCE_phase2_caption_review_decision_seed_editing.md)
- [Editable decision seed JSONL](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase2_caption_review_decision_seed_at2026_03_30.jsonl)
- [Review surface manifest](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase2_caption_four_mode_corpus_review_surface_at2026_03_30.json)
- [Corpus review markdown](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/reports/REVIEW_phase2_caption_four_mode_corpus_review-at2026-03-30-22-45.md)
- [Decision ingestion manifest](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase2_caption_review_decision_ingestion_at2026_03_30.json)
