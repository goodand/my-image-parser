#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SERVER_DIR="$ROOT_DIR/vendor/mcp/macos-ocr-mcp"
PYTHON_BIN="$SERVER_DIR/.venv/bin/python"

if [ ! -f "$SERVER_DIR/main.py" ]; then
  echo "Missing MCP source at $SERVER_DIR. Clone whiteking64/macos-ocr-mcp first." >&2
  exit 1
fi

if [ ! -x "$PYTHON_BIN" ]; then
  echo "Missing Python runtime at $PYTHON_BIN. Run 'uv sync' in $SERVER_DIR first." >&2
  exit 1
fi

cd "$SERVER_DIR"
exec "$PYTHON_BIN" "$SERVER_DIR/main.py"
