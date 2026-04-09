#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SERVER_DIR="${IMAGESORCERY_SERVER_DIR:-$ROOT_DIR/vendor/mcp/imagesorcery-mcp}"
if [ -n "${IMAGESORCERY_MCP_BIN:-}" ]; then
  MCP_BIN="$IMAGESORCERY_MCP_BIN"
elif [ -x "$SERVER_DIR/.venv/bin/imagesorcery-mcp" ]; then
  MCP_BIN="$SERVER_DIR/.venv/bin/imagesorcery-mcp"
else
  MCP_BIN="$SERVER_DIR/venv/bin/imagesorcery-mcp"
fi
LOG_DIR="$ROOT_DIR/logs/imagesorcery"
YOLO_CACHE_DIR="$LOG_DIR/ultralytics"
SOURCE_LOG_DIR="$SERVER_DIR/src/imagesorcery_mcp/logs"
SOURCE_LOG_FILE="$SOURCE_LOG_DIR/imagesorcery.log"

if [ ! -x "$MCP_BIN" ]; then
  echo "Missing ImageSorcery executable at $MCP_BIN. Set IMAGESORCERY_MCP_BIN or install the vendored MCP runtime." >&2
  exit 1
fi

if [ ! -f "$SERVER_DIR/config.toml" ]; then
  echo "Missing ImageSorcery config at $SERVER_DIR/config.toml." >&2
  exit 1
fi

if [ ! -d "$LOG_DIR" ]; then
  echo "Missing workspace log directory at $LOG_DIR." >&2
  exit 1
fi

mkdir -p "$YOLO_CACHE_DIR"

if [ ! -L "$SOURCE_LOG_FILE" ] && [ ! -f "$SOURCE_LOG_FILE" ]; then
  echo "Missing ImageSorcery log file bridge at $SOURCE_LOG_FILE. Run the setup step first." >&2
  exit 1
fi

cd "$SERVER_DIR"
export YOLO_CONFIG_DIR="$YOLO_CACHE_DIR"
exec "$MCP_BIN" --transport stdio
