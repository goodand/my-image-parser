# Phase 1 Caption Four-Mode Small-Batch Auto Eval

## Input

- `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase0_caption_four_mode_eval_bundle_at2026_03_28.json`
- `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase1_image10_caption_four_mode_eval_bundle_at2026_03_28.json`

## Semantic Judge Availability

- semantic_judge_available: `False`

## Batch Summary

- image_count: `2`
- batch_level_winner_frequency: `{'reviewed_isolated_component_rerun': 2}`
- default_baseline_retained: `True`

## Per-Image Results

### /Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image11.png

- bundle_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase0_caption_four_mode_eval_bundle_at2026_03_28.json`
- comparison_ready: `True`
- default_ready_arm: `full_image_baseline`
- qualitative_winner_candidate: `reviewed_isolated_component_rerun`
- baseline_retained: `True`
- edge_case_review_recommended: `True`

| arm | total | promotion | strengths | weaknesses |
| --- | ---: | --- | --- | --- |
| `full_image_baseline` | `12.50` | `default_ready_anchor` | `all_core_metrics_present, title_or_condition_context_present, default_ready_anchor` | `none` |
| `full_image_ocr_context_rerun` | `11.75` | `comparison_only_pending_context_review` | `all_core_metrics_present, explicit_relation_signal, title_or_condition_context_present, ocr_evidence_support` | `generic_image_framing_noise, promotion_penalty:comparison_only_pending_context_review` |
| `parser_table_enriched_rerun` | `12.25` | `comparison_only_pending_context_review` | `all_core_metrics_present, title_or_condition_context_present, parser_structure_support, ocr_evidence_support` | `promotion_penalty:comparison_only_pending_context_review` |
| `reviewed_isolated_component_rerun` | `12.50` | `comparison_ready_reviewed_branch` | `all_core_metrics_present, explicit_relation_signal, ocr_evidence_support, strong_noise_suppression_proxy` | `weak_title_context_fidelity, promotion_penalty:comparison_ready_reviewed_branch` |

### /Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image10.png

- bundle_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase1_image10_caption_four_mode_eval_bundle_at2026_03_28.json`
- comparison_ready: `True`
- default_ready_arm: `full_image_baseline`
- qualitative_winner_candidate: `reviewed_isolated_component_rerun`
- baseline_retained: `True`
- edge_case_review_recommended: `True`

| arm | total | promotion | strengths | weaknesses |
| --- | ---: | --- | --- | --- |
| `full_image_baseline` | `3.50` | `default_ready_anchor` | `default_ready_anchor` | `missing_metric_mentions, weak_relation_signal, weak_title_context_fidelity` |
| `full_image_ocr_context_rerun` | `2.75` | `comparison_only_pending_context_review` | `ocr_evidence_support` | `missing_metric_mentions, weak_relation_signal, weak_title_context_fidelity, promotion_penalty:comparison_only_pending_context_review` |
| `parser_table_enriched_rerun` | `4.25` | `comparison_only_pending_context_review` | `parser_structure_support, ocr_evidence_support` | `missing_metric_mentions, weak_relation_signal, weak_title_context_fidelity, promotion_penalty:comparison_only_pending_context_review` |
| `reviewed_isolated_component_rerun` | `4.50` | `comparison_ready_reviewed_branch` | `ocr_evidence_support, strong_noise_suppression_proxy` | `missing_metric_mentions, weak_relation_signal, weak_title_context_fidelity, promotion_penalty:comparison_ready_reviewed_branch` |

## Baseline Retention

- qualitative winner and default-ready arm are tracked separately
- keep `full_image_baseline` as the active default unless a later promotion gate changes that status

## Edge-Case Handling

- when top proxy scores remain close, prefer GPT direct image verification over human pixel review
- keep that escalation as an evidence-seeking tie-break, not as a default replacement rule
