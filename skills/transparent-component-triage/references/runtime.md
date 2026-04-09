# Runtime

## Canonical Command

```bash
python3 skills/transparent-component-triage/scripts/classify_alpha_split_batch.py
```

## Recommended Runtime

If the underlying worker needs the vendored ImageSorcery runtime, use:

```bash
vendor/mcp/imagesorcery-mcp/.venv/bin/python -B \
  skills/transparent-component-triage/scripts/classify_alpha_split_batch.py
```

## Useful Narrow Smoke

```bash
vendor/mcp/imagesorcery-mcp/.venv/bin/python -B \
  skills/transparent-component-triage/scripts/classify_alpha_split_batch.py \
  --limit 3
```

## Input Notes

- `--input-root` defaults to `control/project_domain/resources/pptx_jobs/`
- `--limit` is useful for smoke runs only
- tuning knobs like `--alpha-threshold`, `--min-pixels`, and `--min-components-for-success` are passthrough classifier settings

## Output Interpretation

- `alpha_split_sufficient` means mechanically sufficient for alpha-only splitting
- it does **not** mean semantically safe for automatic downstream promotion
- `single_component_only` means keep the file on the full-image baseline
- use the report and summary as triage evidence, not as a final approval record
