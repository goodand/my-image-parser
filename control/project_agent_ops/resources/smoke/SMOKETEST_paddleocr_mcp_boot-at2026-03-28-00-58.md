# Smoke Test: PaddleOCR MCP Boot

## Purpose

Verify that the uv-managed local `paddleocr-mcp` server boots over stdio and can execute one bounded `pp_structurev3` call on a real PPT-extracted table image.

## Input

- server launcher:
  - `scripts/mcp/start-paddleocr-mcp.sh`
- smoke runner:
  - `scripts/run_paddleocr_mcp_boot_smoke.py`
- real smoke image:
  - `control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image11.png`

## Verified

- stdio client initialization succeeded
- `list_tools` succeeded
- advertised tool list contained:
  - `pp_structurev3`
- bounded `pp_structurev3` call succeeded on the real PPT image
- the returned preview contained structured HTML table output

## Runtime Notes

- first boot required heavyweight model downloads into workspace-managed caches under:
  - `logs/paddleocr/paddlex_cache`
  - `logs/paddleocr/modelscope_cache`
  - `logs/paddleocr/huggingface_cache`
- launcher-level cache and home redirection prevented writes into user-global cache paths
- the canonical machine-readable artifact is:
  - `control/project_agent_ops/resources/smoke/artifacts/paddleocr_mcp_boot_smoke_at2026_03_28.json`

## Result

- status: `completed`
- boot verification: `passed`
- practical interpretation:
  - `PaddleOCR MCP` is now boot-verified for local `PP-StructureV3` table parsing in this workspace
  - the next bounded step can move on to `image11.png` table parsing normalization into the canonical `Table -> Row -> Cell` schema
