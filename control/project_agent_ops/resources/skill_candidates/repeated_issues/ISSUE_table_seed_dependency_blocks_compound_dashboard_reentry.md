# ISSUE: Table-Seed Dependency Blocks Compound Dashboard Reentry

## Summary

Some composite dashboard images cannot reach reviewed-component or parser-enriched reentry because the current downstream path requires a stable table-cell seed first. This turns a decomposition problem into a parser-seed bottleneck.

## Recurrence signal

This issue is present when:
- full-image OCR is usable
- parser-based table normalization returns `no_table_found` or no stable seed
- reviewed recrop cannot start because it depends on table-cell bbox seed data
- the image still appears visually decomposable into chart and lower-summary regions

## Current workaround

Run a bounded deterministic decomposition probe first. If title/chart/lower-summary regions can be surfaced, continue with typed regrouping instead of repeatedly retrying table-seeded reviewed recrop.

## Structural fix candidate

Add a decomposition stage that does not require a table seed to begin:
- proposal generation
- component typing
- regrouped candidate surfaces
- rule-based scoring

## Current proven example

- `image4`
- canonical evidence:
  - `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/reports/REPORT_phase1_image4_four_mode_reentry_waiver-at2026-03-30-21-27.md`
  - `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/reports/REPORT_phase1_image4_component_decomposition_probe-at2026-03-30-21-55.md`
