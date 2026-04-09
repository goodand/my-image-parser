#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DATA_DIR="$ROOT_DIR/data/agent-task-manager"
CACHE_DIR="$ROOT_DIR/.cache/npm"
mkdir -p "$DATA_DIR"
mkdir -p "$CACHE_DIR"

export STORAGE="sqlite"
export SQLITE_PATH="$DATA_DIR/agent-tasks.db"
export NPM_CONFIG_CACHE="$CACHE_DIR"
export npm_config_cache="$CACHE_DIR"

# The published npm bin points directly at dist/index.js without a shebang.
# Find the temporary npx .bin directory from PATH and launch the JS entry with node.
exec npx -y -p agent-task-manager-mcp node -e '
const path = require("path");
const binDir = process.env.PATH.split(path.delimiter).find((segment) => {
  return segment.includes(`${path.sep}_npx${path.sep}`) && segment.endsWith(`${path.sep}node_modules${path.sep}.bin`);
});
if (!binDir) {
  console.error("Unable to locate the npx install bin directory for agent-task-manager-mcp.");
  process.exit(1);
}
const entry = path.resolve(binDir, "../agent-task-manager-mcp/dist/index.js");
require("child_process")
  .spawn(process.execPath, [entry], { stdio: "inherit", env: process.env })
  .on("exit", (code) => process.exit(code ?? 0));
'
