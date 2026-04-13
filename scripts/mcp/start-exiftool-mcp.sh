#!/usr/bin/env bash
set -euo pipefail

CACHE_ROOT="${MCP_CACHE_DIR:-${XDG_CACHE_HOME:-$HOME/.cache}/my-image-parser/mcp}"
CACHE_DIR="${EXIFTOOL_MCP_UV_CACHE_DIR:-$CACHE_ROOT/uv}"
EXIFTOOL_INSTALL_HINT="${EXIFTOOL_INSTALL_HINT:-Install ExifTool and set EXIFTOOL_BIN if it is not on PATH.}"
mkdir -p "$CACHE_DIR"
export UV_CACHE_DIR="$CACHE_DIR"
EXIFTOOL_BIN="${EXIFTOOL_BIN:-$(command -v exiftool || true)}"

if [ -z "$EXIFTOOL_BIN" ] || [ ! -x "$EXIFTOOL_BIN" ]; then
  echo "ExifTool is not available. $EXIFTOOL_INSTALL_HINT" >&2
  exit 1
fi

export EXIFTOOL_BIN
exec uvx --from "${EXIFTOOL_MCP_PACKAGE:-exiftool-mcp}" python -m exiftool_mcp.server
