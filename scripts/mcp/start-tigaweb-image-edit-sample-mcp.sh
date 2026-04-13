#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STATE_ROOT="${MCP_STATE_DIR:-${XDG_STATE_HOME:-$HOME/.local/state}/my-image-parser/mcp}"
CACHE_ROOT="${MCP_CACHE_DIR:-${XDG_CACHE_HOME:-$HOME/.cache}/my-image-parser/mcp}"
SERVER_DIR="${TIGAWEB_IMAGE_EDIT_SAMPLE_MCP_SERVER_DIR:-$ROOT_DIR/vendor/mcp/tigaweb-image-edit-sample-mcp}"
IMAGE_DIR="${TIGAWEB_IMAGE_EDIT_SAMPLE_IMAGE_DIR:-$STATE_ROOT/tigaweb-image-edit-sample/images}"
CACHE_DIR="${TIGAWEB_IMAGE_EDIT_SAMPLE_NPM_CACHE:-$CACHE_ROOT/npm}"
NODE_BIN="${TIGAWEB_IMAGE_EDIT_SAMPLE_NODE_BIN:-node}"
ENTRYPOINT="${TIGAWEB_IMAGE_EDIT_SAMPLE_ENTRYPOINT:-$SERVER_DIR/dist/server.js}"

mkdir -p "$CACHE_DIR"
mkdir -p "$IMAGE_DIR"

export NPM_CONFIG_CACHE="$CACHE_DIR"
export npm_config_cache="$CACHE_DIR"

if [ ! -f "$SERVER_DIR/src/server.ts" ]; then
  echo "Missing MCP source at $SERVER_DIR. Clone tigaweb/image-edit-sample-mcp first." >&2
  exit 1
fi

if [ ! -f "$ENTRYPOINT" ]; then
  echo "Missing compiled server at $ENTRYPOINT. Set TIGAWEB_IMAGE_EDIT_SAMPLE_ENTRYPOINT or run the local TypeScript build first." >&2
  exit 1
fi

cd "$SERVER_DIR"
exec "$NODE_BIN" "$ENTRYPOINT" "$IMAGE_DIR"
