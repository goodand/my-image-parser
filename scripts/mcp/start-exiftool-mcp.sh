#!/usr/bin/env bash
set -euo pipefail

CACHE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/.cache/uv"
mkdir -p "$CACHE_DIR"
export UV_CACHE_DIR="$CACHE_DIR"

if ! command -v exiftool >/dev/null 2>&1; then
  echo "ExifTool is not installed. Install it first, for example: brew install exiftool" >&2
  exit 1
fi

exec uvx --from exiftool-mcp python -m exiftool_mcp.server
