#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CACHE_ROOT="${MCP_CACHE_DIR:-${XDG_CACHE_HOME:-$HOME/.cache}/my-image-parser/mcp}"
CACHE_DIR="${CV_MCP_UV_CACHE_DIR:-$CACHE_ROOT/uv}"
ENV_FILE="${CV_MCP_ENV_FILE:-$ROOT_DIR/.env}"
mkdir -p "$CACHE_DIR"

export UV_CACHE_DIR="$CACHE_DIR"

if [ -z "${OPENROUTER_API_KEY:-}" ] && [ -z "${OPENAI_API_KEY:-}" ] && [ -f "$ENV_FILE" ]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

if [ -z "${OPENROUTER_API_KEY:-}" ] && [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "Missing OPENROUTER_API_KEY or OPENAI_API_KEY. Set one in the environment or provide CV_MCP_ENV_FILE." >&2
  exit 1
fi

cd "$ROOT_DIR"
exec uvx --from "${CV_MCP_PACKAGE:-git+https://github.com/samhains/cv-mcp}" "${CV_MCP_COMMAND:-cv-mcp-server}"
