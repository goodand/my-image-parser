# Parser Sidecar To Canonical Schema Promotion Skill Smoke

## Purpose

Verify that the promoted skill-local wrapper can convert one bounded raw parser sidecar into the canonical `Table -> Row -> Cell` JSON shape without re-running the parser MCP.

## Command

```bash
python3 skills/parser-sidecar-to-canonical-schema-promotion/scripts/promote_parser_sidecar_to_canonical_schema.py \
  --raw-sidecar-json control/project_domain/resources/manifests/phase0_paddleocr_table_parse_raw_at2026_03_28.json \
  --normalized-output-json /tmp/phase0_paddleocr_table_parse_normalized_skill_smoke_at2026_03_28.json \
  --output-json /tmp/parser_sidecar_to_canonical_schema_skill_smoke_at2026_03_28.json
```

## Result

- status: success
- normalized_status: `completed`
- document_id: `01_full_presentation_2026-03-17`
- page: `24`
- table_id: `t1`
- row_count: `4`
- cell_count: `16`
- parser_backend: `paddleocr-mcp/pp_structurev3`

## Evidence

- raw sidecar input:
  - `control/project_domain/resources/manifests/phase0_paddleocr_table_parse_raw_at2026_03_28.json`
- normalized smoke output:
  - `/private/tmp/phase0_paddleocr_table_parse_normalized_skill_smoke_at2026_03_28.json`
- promotion result output:
  - `/private/tmp/parser_sidecar_to_canonical_schema_skill_smoke_at2026_03_28.json`

## Interpretation

The skill-local wrapper and shared promotion helper are sufficient for the current bounded PaddleOCR table sidecar case.

This smoke does not prove multi-table support.
It proves the current `first stable table payload -> canonical normalization` path is live and reusable.
