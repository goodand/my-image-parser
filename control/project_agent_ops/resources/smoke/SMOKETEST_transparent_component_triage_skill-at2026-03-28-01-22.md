# Smoke Test: Transparent Component Triage Skill

## Command

```bash
<REPO_ROOT>/vendor/mcp/imagesorcery-mcp/.venv/bin/python -B \
  skills/transparent-component-triage/scripts/classify_alpha_split_batch.py \
  --limit 2 \
  --output-root <TMP_DIR>/transparent_component_triage_smoke/output \
  --manifest-jsonl <TMP_DIR>/transparent_component_triage_smoke/manifest.jsonl \
  --summary-json <TMP_DIR>/transparent_component_triage_smoke/summary.json \
  --report-md <TMP_DIR>/transparent_component_triage_smoke/report.md
```

## Expected

- skill-local wrapper should resolve the existing alpha-only batch classifier
- the run should produce a bounded report, summary JSON, manifest JSONL, and per-image worker outputs
- the result should remain a review-gated candidate subset, not an automatic promotion surface

## Observed

- wrapper `--help`: `0`
- live smoke exit: `0`
- total_images: `2`
- alpha_split_sufficient: `1`
- single_component_only: `1`
- candidate image:
  - `01_full_presentation_2026-03-17:image1.png`
  - `alpha_component_count = 82`
- baseline-retained image:
  - `01_full_presentation_2026-03-17:image10.png`
  - `classification = single_component_only`

## Output Paths

- report: `<TMP_DIR>/transparent_component_triage_smoke/report.md`
- summary: `<TMP_DIR>/transparent_component_triage_smoke/summary.json`
- manifest: `<TMP_DIR>/transparent_component_triage_smoke/manifest.jsonl`
- output_root: `<TMP_DIR>/transparent_component_triage_smoke/output/2026-03-27-16-22`
- skill: `skills/transparent-component-triage`

## Interpretation

- the repo-specific skill wrapper works and reuses the existing alpha-only batch classifier correctly
- the skill is suitable for conservative transparent-image triage
- the candidate subset still requires reviewed selection because high component counts can be fragment-heavy rather than semantically meaningful
