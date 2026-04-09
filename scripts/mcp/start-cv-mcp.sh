#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CACHE_DIR="$ROOT_DIR/.cache/uv"
cd "$ROOT_DIR"
mkdir -p "$CACHE_DIR"

export UV_CACHE_DIR="$CACHE_DIR"

if [ ! -f "$ROOT_DIR/.env" ]; then
  echo "Missing $ROOT_DIR/.env. Copy .env.example to .env and set OPENROUTER_API_KEY." >&2
  exit 1
fi

exec uvx --from git+https://github.com/samhains/cv-mcp cv-mcp-server
