#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STATE_ROOT="${MCP_STATE_DIR:-${XDG_STATE_HOME:-$HOME/.local/state}/my-image-parser/mcp}"
CACHE_ROOT="${MCP_CACHE_DIR:-${XDG_CACHE_HOME:-$HOME/.cache}/my-image-parser/mcp}"
SERVER_DIR="${IMAGESORCERY_SERVER_DIR:-${IMAGESORCERY_MCP_SERVER_DIR:-$ROOT_DIR/vendor/mcp/imagesorcery-mcp}}"
if [ -n "${IMAGESORCERY_MCP_ENTRYPOINT:-}" ]; then
  MCP_BIN="$IMAGESORCERY_MCP_ENTRYPOINT"
elif [ -n "${IMAGESORCERY_MCP_BIN:-}" ]; then
  MCP_BIN="$IMAGESORCERY_MCP_BIN"
elif [ -x "$SERVER_DIR/.venv/bin/imagesorcery-mcp" ]; then
  MCP_BIN="$SERVER_DIR/.venv/bin/imagesorcery-mcp"
else
  MCP_BIN="$SERVER_DIR/venv/bin/imagesorcery-mcp"
fi
LOG_DIR="${IMAGESORCERY_LOG_DIR:-$STATE_ROOT/logs/imagesorcery}"
LOG_FILE="${IMAGESORCERY_LOG_FILE:-$LOG_DIR/imagesorcery.log}"
YOLO_CACHE_DIR="${IMAGESORCERY_YOLO_CACHE_DIR:-$CACHE_ROOT/imagesorcery/ultralytics}"
CONFIG_FILE="${IMAGESORCERY_CONFIG_FILE:-$SERVER_DIR/config.toml}"

if [ ! -x "$MCP_BIN" ]; then
  echo "Missing ImageSorcery executable at $MCP_BIN. Set IMAGESORCERY_MCP_BIN or install the vendored MCP runtime." >&2
  exit 1
fi

if [ ! -f "$CONFIG_FILE" ]; then
  echo "Missing ImageSorcery config at $CONFIG_FILE." >&2
  exit 1
fi

mkdir -p "$LOG_DIR" "$YOLO_CACHE_DIR"

cd "$SERVER_DIR"
export IMAGESORCERY_CONFIG_FILE="$CONFIG_FILE"
export IMAGESORCERY_LOG_FILE="$LOG_FILE"
export YOLO_CONFIG_DIR="$YOLO_CACHE_DIR"
exec "$MCP_BIN" --transport stdio "$@"
