# TASK: Objective-Profile Scoring For Regrouped Component Candidates

## Summary

After a bounded decomposition probe surfaces regrouped candidates, score those candidates against explicit objective profiles before attempting re-entry or promotion.

## Repeat signal

Use this task when:
- decomposition proposals already exist
- regrouped candidates are visible
- the main question is no longer "can we decompose?" but "which regrouped surface fits the current experiment objective?"

## Current proven example

- `image4`
- canonical evidence:
  - `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase1_image4_component_decomposition_candidate_scoring_at2026_03_30.json`
  - `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/reports/REPORT_phase1_image4_component_decomposition_candidate_scoring-at2026-03-30-22-05.md`

## Standard bounded flow

1. read the decomposition probe manifest
2. define one current objective profile and one contrast profile
3. score regrouped candidates deterministically
4. record the winner under each profile
5. decide whether the current mainline should:
   - keep full-dashboard path
   - try a narrower crop
   - or stay excluded
