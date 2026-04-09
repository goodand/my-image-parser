# Phase 0 Four-Mode Qualitative Summary

## Purpose

Provide a manual-ready qualitative comparison of the current bounded `4-mode` caption set for `image11.png` when a repo-local semantic judge harness is not yet present.

## Input Paths Used

- comparison manifest:
  - `control/project_domain/resources/manifests/phase0_caption_four_mode_comparison_at2026_03_28.json`
- judge input:
  - `control/project_domain/resources/manifests/phase0_caption_four_mode_judge_input_at2026_03_28.json`
- frozen eval bundle:
  - `control/project_domain/resources/manifests/phase0_caption_four_mode_eval_bundle_at2026_03_28.json`
- readiness report:
  - `control/project_domain/resources/reports/REPORT_phase0_four_mode_caption_readiness-at2026-03-28-11-36.md`
- supporting arm evidence:
  - `control/project_domain/resources/reports/REPORT_phase0_full_image_context_rerun_smoke-at2026-03-28-09-19.md`
  - `control/project_domain/resources/reports/REPORT_phase0_parser_enriched_caption_rerun_smoke-at2026-03-28-11-08.md`
  - `control/project_domain/resources/reports/REPORT_phase0_reviewed_isolated_component_caption_rerun_smoke-at2026-03-28-11-36.md`

## Rubric

- `table relation signal`
- `metric mention coverage`
- `caption completeness`
- `grounded comparative takeaway`
- `non-table noise suppression`

Important gate:

- qualitative strength may choose a comparison winner
- it must not override `default-ready` versus `comparison-ready` status

## Per-Arm Findings

### full_image_baseline

- strengths:
  - clean and concise
  - retains the strongest title/context fidelity with `Two-Phase Hyde-PC (65Q, 오류 5건 제외)`
  - mentions the key metric set and the `70Q` versus `65Q` table frame
- limitations:
  - does not say which side is higher
  - reads as a table summary, not as an explicit comparative takeaway

### full_image_ocr_context_rerun

- strengths:
  - adds the most explicit relational signal among the full-image surfaces
  - says `65Q` is generally higher than `70Q`
  - keeps all metric mentions
- limitations:
  - loses some title fidelity
  - adds mild generic noise such as `This image shows` and `scenarios`
  - remains `comparison_only_pending_context_review`

### parser_table_enriched_rerun

- strengths:
  - preserves table scope tightly
  - keeps `Two-Phase Hyde-PC` condition context
  - covers all core metric names and delta framing
- limitations:
  - does not add an explicit directional takeaway
  - remains `comparison_only_pending_context_review`
  - still behaves more like a structure-aware summary than a table-reading winner

### reviewed_isolated_component_rerun

- strengths:
  - strongest non-table noise suppression
  - keeps all three metric names plus `70Q`, `65Q`, and `Delta`
  - explicitly says `65Q` is higher for all metrics
  - evidence-backed crop preserved expected table tokens while removing `7` extraneous full-image OCR tokens
- limitations:
  - less title/context fidelity than baseline or parser-enriched rerun
  - still a `reviewed branch only`, not a default path

## Qualitative Winner Candidate

- winner candidate: `reviewed_isolated_component_rerun`

Reason:

- it preserves the same table-focused metric coverage as the other enriched arms
- it gives the clearest bounded comparative takeaway
- it is the only arm with explicit evidence that the input surface removed non-table OCR noise without losing expected table tokens

Runner-up interpretation:

- `parser_table_enriched_rerun` is the strongest title/context-preserving alternative
- `full_image_ocr_context_rerun` is the strongest full-image alternative because it adds relation wording

## Baseline Retention

- keep baseline as default: `yes`
- current default arm:
  - `full_image_baseline`

Reason:

- `full_image_baseline` remains the default-ready anchor
- `full_image_ocr_context_rerun` and `parser_table_enriched_rerun` are still `comparison_only_pending_context_review`
- `reviewed_isolated_component_rerun` is `comparison_ready_reviewed_branch`, not default-ready

## Judge Possible 여부

- repo-local semantic judge harness available: `no`
- current lane closure:
  - `manual qualitative summary + frozen eval bundle + judge waiver`

## Fields Needed To Merge With Session A Deterministic Lane Later

- `execution_arm`
- `ledger_path`
- `source_image_path`
- `input_surface`
- `prompt_version`
- `caption`
- `alt_text`
- `context_variant`
- `context_review_status`
- `ocr_status`
- `recommended_current_default`
- `comparison_ready`
- `parity_audit.ready_for_side_by_side_read`
- `qualitative_winner_candidate`
- `baseline_retained`

## Next One Step

Feed the frozen eval bundle into a future judge consumer when one exists, while preserving the current deterministic `4-mode` comparison as the canonical bounded input surface.
