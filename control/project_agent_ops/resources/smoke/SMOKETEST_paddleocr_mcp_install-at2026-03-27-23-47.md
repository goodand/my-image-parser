# Smoke Test: PaddleOCR MCP Install

## Purpose

Record the current installation state of the uv-managed local `paddleocr-mcp` vendor project.

## Verified

- `vendor/mcp/paddleocr-mcp/pyproject.toml` exists
- `vendor/mcp/paddleocr-mcp/uv.lock` exists
- `vendor/mcp/paddleocr-mcp/.venv/bin/paddleocr_mcp` exists
- workspace launcher exists:
  - `scripts/mcp/start-paddleocr-mcp.sh`
- project-local host config exists:
  - `.codex/config.toml`
  - `.vscode/mcp.json`

## Runtime Notes

- The launcher redirects cache-related paths through:
  - `PADDLE_PDX_CACHE_HOME`
  - `PADDLE_HOME`
  - `XDG_CACHE_HOME`
- The launcher disables the initial model-source connectivity check through:
  - `PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK=True`

## Current Boundary

- installation and launcher wiring are complete
- binary presence is verified
- full stdio boot verification is still pending
- reason:
  - first-run model initialization remains heavyweight and may require a bounded dedicated smoke

## Next Check

1. run a bounded stdio smoke with the launcher
2. confirm that `PP-StructureV3` local mode boots cleanly
3. store one canonical smoke artifact before switching `boot_verified` to `true`
