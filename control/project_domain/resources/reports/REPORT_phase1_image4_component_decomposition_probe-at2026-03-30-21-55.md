# Phase1 Image4 Component Decomposition Probe

## Input

- source_image_path: `<LOCAL_PPTX_JOBS_ROOT>/01_full_presentation_2026-03-17/media/image4.png`
- image_size: `1280x820`

## Summary

- found_title_block: `True`
- found_chart_region: `True`
- chart_panel_count: `3`
- found_lower_region: `True`
- found_table_like_region: `True`
- image_kind_guess: `compound_dashboard_like`
- decomposition_ready_for_regrouping: `True`
- selection_recommendation: `decomposition_stage_candidate_available`

## Candidate Surfaces

### full_dashboard

- bbox: `[0, 0, 1280, 820]`
- component_ids: `['full_dashboard']`
- rationale: Keep the full dashboard as the no-loss baseline candidate.

### title_plus_chart_set

- bbox: `[23, 12, 1225, 341]`
- component_ids: `['title_block', 'chart_region']`
- rationale: Preserve title context together with the upper chart set.

### chart_set

- bbox: `[23, 59, 1225, 341]`
- component_ids: `['chart_region']`
- rationale: Preserve the chart-heavy analytical surface without the full dashboard.

### title_plus_table

- bbox: `[23, 12, 984, 691]`
- component_ids: `['title_block', 'table_like_region']`
- rationale: Preserve title context together with the lower summary/table region.

### table_only

- bbox: `[23, 409, 984, 691]`
- component_ids: `['table_like_region']`
- rationale: Isolate the lower dense region as a possible metrics table or summary crop.

## Interpretation

- This probe does not decide re-entry by itself.
- It tests whether deterministic proposal generation can expose title/chart/lower-summary regions before a stronger decomposition slice exists.
- If the chart region and lower region both appear, the next bounded step should be typed regrouping plus rule-based scoring rather than more ad-hoc recrop tweaks.
