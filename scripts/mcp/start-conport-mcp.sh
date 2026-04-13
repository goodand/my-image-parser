#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STATE_ROOT="${MCP_STATE_DIR:-${XDG_STATE_HOME:-$HOME/.local/state}/my-image-parser/mcp}"
CACHE_ROOT="${MCP_CACHE_DIR:-${XDG_CACHE_HOME:-$HOME/.cache}/my-image-parser/mcp}"
CACHE_DIR="${CONPORT_UV_CACHE_DIR:-$CACHE_ROOT/uv}"
WORKSPACE_ID="${CONPORT_WORKSPACE_ID:-$ROOT_DIR}"
LOG_FILE="${CONPORT_LOG_FILE:-$STATE_ROOT/logs/conport.log}"

mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$CACHE_DIR"

export UV_CACHE_DIR="$CACHE_DIR"

exec uvx --from "${CONPORT_MCP_PACKAGE:-context-portal-mcp}" conport-mcp \
  --mode stdio \
  --workspace_id "$WORKSPACE_ID" \
  --log-file "$LOG_FILE" \
  --log-level INFO
