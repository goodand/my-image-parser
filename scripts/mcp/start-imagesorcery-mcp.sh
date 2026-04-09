#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SERVER_DIR="$ROOT_DIR/vendor/mcp/imagesorcery-mcp"
VENV_BIN="$SERVER_DIR/.venv/bin"
LOG_DIR="$ROOT_DIR/logs/imagesorcery"
YOLO_CACHE_DIR="$LOG_DIR/ultralytics"
SOURCE_LOG_DIR="$SERVER_DIR/src/imagesorcery_mcp/logs"
SOURCE_LOG_FILE="$SOURCE_LOG_DIR/imagesorcery.log"

if [ ! -x "$VENV_BIN/imagesorcery-mcp" ]; then
  echo "Missing ImageSorcery executable at $VENV_BIN/imagesorcery-mcp. Install the vendored MCP first." >&2
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
exec "$VENV_BIN/imagesorcery-mcp" --transport stdio
