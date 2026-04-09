#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SERVER_DIR="$ROOT_DIR/vendor/mcp/tigaweb-image-edit-sample-mcp"
IMAGE_DIR="$ROOT_DIR/control/project_domain/resources/assets/image_edit_sample_mcp/images"
CACHE_DIR="$ROOT_DIR/.cache/npm"

mkdir -p "$CACHE_DIR"
mkdir -p "$IMAGE_DIR"

export NPM_CONFIG_CACHE="$CACHE_DIR"
export npm_config_cache="$CACHE_DIR"

if [ ! -f "$SERVER_DIR/src/server.ts" ]; then
  echo "Missing MCP source at $SERVER_DIR. Clone tigaweb/image-edit-sample-mcp first." >&2
  exit 1
fi

if [ ! -f "$SERVER_DIR/dist/server.js" ]; then
  echo "Missing compiled server at $SERVER_DIR/dist/server.js. Run the local TypeScript build first." >&2
  exit 1
fi

cd "$SERVER_DIR"
exec node "$SERVER_DIR/dist/server.js" "$IMAGE_DIR"
