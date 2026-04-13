# NOTE_review_surface_cross_validation_scope_freeze-at2026-04-09-19-03

## Intent

Freeze the current scope interpretation for the `my-image-parser` review-surface lane after the user clarified that image captioning itself is the main test and the review-surface work is cross-validation only.

## Frozen Decision

The current review-surface lane in `my-image-parser` is **not** the main product-under-test. It is a bounded cross-validation lane for the extracted-image caption experiment.

Therefore:

1. the primary test remains image caption quality on extracted presentation images
2. the review surface is a cross-check tool for that caption test
3. the current bootstrap session may close this workspace slice even if some images end in explicit `manual_lane` deferral rather than uniform comparison-ready approval
4. remaining UX work in `vscode-markdown-review-surface` does not block closure of the current `my-image-parser` cross-validation slice

## Effective Closure Boundary

For the current slice, closure requires:

1. source markdown remains read-only
2. session-local writeback works
3. one accepted evaluation cohort is frozen
4. every row in that cohort reaches a terminal state
5. comparison-ready images receive approved caption and alt text
6. non-ready images are explicitly deferred instead of left pending
7. table-heavy comparison-ready images are checked for table-internal value coverage

The current first-10 bootstrap session satisfies that boundary.

## Non-Blocking Follow-Up

The following remain useful but are no longer closure blockers for this workspace slice:

- refreshed comparison-ready cohort selection
- candidate-text comparison section completion in the external review-surface app
- label/readability refinement in the external review-surface app
- broader surface UX completion for mixed readiness image types

## Related Artifacts

- [Bootstrap gate verdict before scope freeze](../../../../project_domain/resources/reports/REPORT_phase2_review_surface_current_evaluation_gate_verdict-at2026-04-09-18-37.md)
- [Bootstrap evaluation with terminal row states](../../../../project_domain/resources/reports/REPORT_phase2_review_surface_10_image_human_evaluation-at2026-04-09-18-56.md)
- [Cross-validation slice closure report](../../../../project_domain/resources/reports/REPORT_phase2_review_surface_cross_validation_slice_closure-at2026-04-09-19-03.md)
- [10-image evaluation runbook](../../../../project_domain/resources/master_plans/MASTER_PLAN_10_image_evaluation_runbook-at2026-04-09.md)
- [Presentation image pipeline master plan](../../../../project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md)
