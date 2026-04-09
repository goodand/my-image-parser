# Repeated Task Candidate: Alpha-Split-Only Candidate Batch Classification

## Why This Repeats

When object-isolation work should stay conservative, the workspace still needs a bounded batch pass that answers a narrower question:

- which files are already good enough for deterministic alpha split only
- which files should remain on the full-image baseline

This comes up before any automatic ImageSorcery or imagegen fanout is allowed.

## Current Manual Handling

1. discover extracted PPT media under `control/project_domain/resources/pptx_jobs/*/media/*`
2. run the object-isolation correction worker in `--skip-imagesorcery-fallback` mode
3. collect per-image `worker_result.json` and alpha component manifests
4. write a batch manifest JSONL, summary JSON, and markdown report
5. treat only the `alpha_split_sufficient` subset as review-gated deterministic candidates

## Current Workspace Surface

- script: `skills/object-isolation-correction/scripts/classify_alpha_split_batch.py`
- report example: `control/project_domain/resources/reports/REPORT_phase0_alpha_split_batch_classification-at2026-03-27-15-05.md`
- summary example: `control/project_domain/resources/manifests/phase0_alpha_split_batch_classification_summary.json`

## Promotion Target

- reusable preflight checklist or skill wrapper for deterministic alpha-split candidate discovery
- optional later promotion into a reviewed-selection gate before object-level caption reruns

## Promotion Trigger

Promote this pattern if another experiment needs the same:

- transparent-image triage
- worker-in-batch execution
- deterministic candidate subset extraction
- baseline-retention decision

## Current Promotion Status

- promoted into repo-local skill: `skills/transparent-component-triage`
- root implementation remains `skills/object-isolation-correction/scripts/classify_alpha_split_batch.py`
- skill-local wrapper exists to keep the conservative batch triage contract explicit
