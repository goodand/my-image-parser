#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SERVER_DIR="${MACOS_OCR_MCP_SERVER_DIR:-$ROOT_DIR/vendor/mcp/macos-ocr-mcp}"
ENTRYPOINT="${MACOS_OCR_ENTRYPOINT:-$SERVER_DIR/main.py}"
if [ -n "${MACOS_OCR_PYTHON:-}" ]; then
  PYTHON_BIN="$MACOS_OCR_PYTHON"
elif [ -x "$SERVER_DIR/.venv/bin/python" ]; then
  PYTHON_BIN="$SERVER_DIR/.venv/bin/python"
else
  PYTHON_BIN="$SERVER_DIR/venv/bin/python"
fi

if [ ! -f "$ENTRYPOINT" ]; then
  echo "Missing MCP source entrypoint at $ENTRYPOINT. Set MACOS_OCR_ENTRYPOINT or clone whiteking64/macos-ocr-mcp first." >&2
  exit 1
fi

if [ ! -x "$PYTHON_BIN" ]; then
  echo "Missing Python runtime at $PYTHON_BIN. Set MACOS_OCR_PYTHON or run 'uv sync' in $SERVER_DIR first." >&2
  exit 1
fi

cd "$SERVER_DIR"
exec "$PYTHON_BIN" "$ENTRYPOINT" "$@"
