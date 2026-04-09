#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CACHE_DIR="$ROOT_DIR/.cache/npm"
mkdir -p "$CACHE_DIR"

export NPM_CONFIG_CACHE="$CACHE_DIR"
export npm_config_cache="$CACHE_DIR"

SERVER_ROOTS=("$ROOT_DIR")

if [[ -n "${FILESYSTEM_EXTRA_ROOT:-}" ]]; then
  SERVER_ROOTS+=("${FILESYSTEM_EXTRA_ROOT}")
fi

exec npx -y @modelcontextprotocol/server-filesystem "${SERVER_ROOTS[@]}"
