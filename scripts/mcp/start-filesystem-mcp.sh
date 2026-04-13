#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CACHE_ROOT="${MCP_CACHE_DIR:-${XDG_CACHE_HOME:-$HOME/.cache}/my-image-parser/mcp}"
CACHE_DIR="${FILESYSTEM_MCP_NPM_CACHE:-$CACHE_ROOT/npm}"
mkdir -p "$CACHE_DIR"

export NPM_CONFIG_CACHE="$CACHE_DIR"
export npm_config_cache="$CACHE_DIR"

SERVER_ROOTS=("$ROOT_DIR")

if [[ -n "${FILESYSTEM_EXTRA_ROOT:-}" ]]; then
  SERVER_ROOTS+=("${FILESYSTEM_EXTRA_ROOT}")
fi

if [[ -n "${FILESYSTEM_EXTRA_ROOTS:-}" ]]; then
  IFS=':' read -r -a EXTRA_ROOTS <<< "${FILESYSTEM_EXTRA_ROOTS}"
  for extra_root in "${EXTRA_ROOTS[@]}"; do
    if [[ -n "${extra_root}" ]]; then
      SERVER_ROOTS+=("${extra_root}")
    fi
  done
fi

exec npx -y @modelcontextprotocol/server-filesystem "${SERVER_ROOTS[@]}"
