# TASK: Projection-Profile Component Decomposition Probe For Compound Dashboards

## Summary

When a composite dashboard image is excluded because table-seeded parser/reviewed paths cannot close, run a bounded deterministic decomposition probe before attempting a heavier semantic solution.

## Repeat signal

Use this task when:
- the image is a chart-table or dashboard-style composite
- recrop logic exists but still depends on a missing parser seed
- the next useful question is whether the image can be decomposed into title/chart/lower-summary regions at all

## Current proven example

- `image4`
- canonical evidence:
  - `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase1_image4_component_decomposition_probe_at2026_03_30.json`
  - `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/reports/REPORT_phase1_image4_component_decomposition_probe-at2026-03-30-21-55.md`

## Standard bounded flow

1. run a deterministic decomposition probe
2. emit a decomposition manifest with typed proposals and regrouped candidates
3. inspect whether title/chart/lower-summary blocks were surfaced
4. decide whether the next slice should be:
   - typed regrouping + scoring
   - stronger proposal generation
   - continued exclusion

## Expected outputs

- decomposition manifest JSON
- short markdown report
- explicit recommendation:
  - `decomposition_stage_candidate_available`
  - or `needs_stronger_proposal_generation`
