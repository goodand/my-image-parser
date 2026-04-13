# NOTE_presentation_image_pipeline_active_scope_freeze-at2026-04-09-19-11

## Intent

Freeze what `MASTER_PLAN_presentation_image_pipeline.md` currently means operationally inside `my-image-parser`, so the master plan can be closed without pretending that every originally listed long-range phase was executed in this cycle.

## Frozen Active Scope

For the current `my-image-parser` cycle, the active executable scope of the presentation image pipeline is:

1. extract and organize presentation images as experiment inputs
2. build and freeze canonical caption-comparison truth for the current stable corpus
3. close the current corpus-level consumer truth for that caption experiment
4. run bounded human cross-validation on the caption truth through the review-surface lane
5. record explicit excludes and manual lanes instead of leaving unresolved edge cases open

In this frozen scope, the following artifacts are the primary closure evidence:

- [Phase1 corpus closure](../../../../project_domain/resources/reports/REPORT_phase1_caption_four_mode_corpus_closure-at2026-03-30-22-19.md)
- [Phase1 corpus experiment summary](../../../../project_domain/resources/reports/REPORT_phase1_caption_four_mode_corpus_experiment_summary-at2026-03-30-22-39.md)
- [Corpus auto-eval manifest](../../../../project_domain/resources/manifests/phase1_caption_four_mode_corpus_auto_eval_true_batch_at2026_03_30.json)
- [Review-surface cross-validation scope freeze](./NOTE_review_surface_cross_validation_scope_freeze-at2026-04-09-19-03.md)
- [Review-surface cross-validation closure](../../../../project_domain/resources/reports/REPORT_phase2_review_surface_cross_validation_slice_closure-at2026-04-09-19-03.md)

## Explicitly Out Of Current Active Scope

The following remain valid future or backlog directions, but they are **not required** to close the current master-plan cycle:

- downstream retrieval execution
- final document mapping confirmation
- filename/metadata commit wave
- presentation regeneration from approved text
- full UX completion of the external `vscode-markdown-review-surface` application

## Required Next Measurement

Although live downstream execution is out of scope, the next downstream **measurement** is required.

That required next measurement is:

- retrieval dry-run / preflight measurement

This means the workspace should measure readiness and blocked reasons for retrieval without requiring live retrieval execution in the current cycle.

For downstream consumers such as `my-second-identity`, this measurement must also check whether reviewed captions preserve meaningful multimodal form when that form is part of the document's content contract. The downstream gate must not assume that all non-text structure can be treated as noise.

See:

- [Retrieval measurement without execution policy](./NOTE_retrieval_measurement_without_execution_policy-at2026-04-09-19-19.md)

## Closure Rule

The master plan may now be treated as closed for the current active scope if:

1. stable caption truth is frozen
2. corpus-level consumer truth is frozen
3. excluded/manual lanes are explicit
4. bounded human cross-validation is closed
5. no current active-scope blocker remains

Those conditions are satisfied in the current workspace state.

## One-Line Summary

`MASTER_PLAN_presentation_image_pipeline.md` should now be read as **closed for the current caption-experiment cycle**, while broader retrieval/mapping/regeneration ambitions stay as future extensions rather than active blockers.
