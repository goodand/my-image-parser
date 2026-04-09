#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOG_DIR="$ROOT_DIR/logs"
CACHE_DIR="$ROOT_DIR/.cache/uv"
mkdir -p "$LOG_DIR"
mkdir -p "$CACHE_DIR"

export UV_CACHE_DIR="$CACHE_DIR"

exec uvx --from context-portal-mcp conport-mcp \
  --mode stdio \
  --workspace_id "$ROOT_DIR" \
  --log-file "$LOG_DIR/conport.log" \
  --log-level INFO
