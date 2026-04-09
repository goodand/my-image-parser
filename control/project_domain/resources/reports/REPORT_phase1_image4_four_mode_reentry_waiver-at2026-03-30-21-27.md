# Phase1 Image4 Four-Mode Reentry Waiver

## Decision

`image4` remains `excluded`.

## Used Truth Sources

- `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_phase1_image4_multi_component_recrop_reentry_slice-at2026-03-30.md`
- `control/project_domain/resources/manifests/phase1_caption_four_mode_small_batch_bundle_at2026_03_28.json`
- `control/project_domain/resources/reports/REPORT_phase1_caption_four_mode_small_batch_readiness-at2026-03-28-14-10.md`
- `control/project_domain/resources/manifests/phase1_caption_four_mode_small_batch_candidates_at2026_03_28.json`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_caption_10w_01_full_presentation_2026-03-17_w02.json`
- `control/project_domain/resources/manifests/phase1_caption_four_mode_corpus_excluded_at2026_03_29.json`
- `control/project_domain/resources/manifests/phase1_image4_reentry_attempt_summary_at2026_03_30.json`

## Deterministic Path Attempted

1. Verified the current excluded state and existing baseline ledger.
2. Built a bounded full-image OCR context package in `/private/tmp`.
3. Ran a bounded PaddleOCR PP-StructureV3 parse attempt against `image4`.
4. Probed the Apple Vision document-structure helper as a bounded single-source fallback.
5. Checked whether the new reviewed multi-component recrop logic could enter from a stable merged-candidate seed.

## Result

- `full_image_baseline`: already present
- `full_image_ocr_context_rerun`: feasible in bounded scratch, `ocr_status = usable`
- `parser_table_enriched_rerun`: not closable in this slice because the parser attempt returned `normalized_status = no_table_found`
- `apple document-structure fallback`: not closable in this slice because the helper did not emit a stable sidecar JSON within the bounded observation window
- `reviewed_isolated_component_rerun`: not closable in this slice because reviewed recrop requires table-cell bbox seed data from a stable merged candidate

## Why Exclusion Remains Correct

- `image4` is still the chart-table composite edge case described by the current canonical exclusion set
- the new recrop logic did not unlock a safe reviewed branch because no stable parser-derived seed was available
- the bounded Apple helper fallback also failed to yield a promotable raw sidecar for `image4`
- without stable parser and reviewed surfaces, a bounded per-image frozen `4-mode` bundle cannot be emitted

## GPT Direct Confirmation

- used: `no`
- reason: deterministic evidence was sufficient to preserve exclusion, so a new tie-break was unnecessary

## Final Inclusion Or Exclusion Decision

- final decision: `excluded`
- reason: `no_stable_parser_or_reviewed_surface_after_bounded_recrop_slice`

## Next One Step

- keep `image4` outside the current canonical cohort unless a future deterministic parser path produces a stable normalized table or reviewed seed bbox without helper non-termination
