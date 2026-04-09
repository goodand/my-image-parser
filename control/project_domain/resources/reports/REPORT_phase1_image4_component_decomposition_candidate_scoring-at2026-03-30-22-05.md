# Phase1 Image4 Component Decomposition Candidate Scoring

## Input

- source_image_path: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image4.png`
- image_kind_guess: `compound_dashboard_like`
- current_experiment_objective: `dashboard_overview_caption_input`

## Winners

- dashboard_overview_caption_input winner: `full_dashboard`
- embedded_table_focus winner: `title_plus_table`

## Dashboard Overview Scores

| candidate | total | strengths | weaknesses |
| --- | ---: | --- | --- |
| `full_dashboard` | `10.00` | `preserves_title_context, preserves_chart_region, preserves_lower_summary_or_table, preserves_dashboard_semantics, no_loss_anchor` | `none` |
| `title_plus_chart_set` | `3.00` | `preserves_title_context, preserves_chart_region` | `drops_lower_summary_or_table, partial_dashboard_semantics_only` |
| `title_plus_table` | `2.50` | `preserves_title_context, preserves_lower_summary_or_table` | `drops_chart_region, partial_dashboard_semantics_only` |
| `chart_set` | `0.50` | `preserves_chart_region` | `drops_title_context, drops_lower_summary_or_table, partial_dashboard_semantics_only` |
| `table_only` | `-0.50` | `preserves_lower_summary_or_table` | `drops_title_context, drops_chart_region, partial_dashboard_semantics_only` |

## Embedded Table Focus Scores

| candidate | total | strengths | weaknesses |
| --- | ---: | --- | --- |
| `title_plus_table` | `5.00` | `preserves_table_region, keeps_title_context, focused_crop` | `none` |
| `table_only` | `4.00` | `preserves_table_region, focused_crop` | `none` |
| `full_dashboard` | `2.00` | `preserves_table_region, keeps_title_context` | `keeps_chart_noise_for_table_focus` |
| `title_plus_chart_set` | `-1.00` | `keeps_title_context, focused_crop` | `drops_table_region, keeps_chart_noise_for_table_focus` |
| `chart_set` | `-2.00` | `focused_crop` | `drops_table_region, keeps_chart_noise_for_table_focus` |

## Current Interpretation

- mainline_recommendation: `keep_full_dashboard_or_full_image_path`
- reentry_ready: `False`
- reason: deterministic scoring says dashboard semantics are best preserved by full_dashboard; derived-arm reentry still requires typed regrouping and stronger evidence

## Summary

- This experiment does not reopen `image4` by itself.
- It shows that deterministic regrouping candidates are now scoreable.
- For the current dashboard-level objective, `full_dashboard` still beats narrower crops.
- Therefore the decomposition bottleneck has narrowed from `no component view at all` to `typed regrouping plus stronger promotion evidence`.
