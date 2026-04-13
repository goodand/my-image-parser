#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STATE_ROOT="${MCP_STATE_DIR:-${XDG_STATE_HOME:-$HOME/.local/state}/my-image-parser/mcp}"
CACHE_ROOT="${MCP_CACHE_DIR:-${XDG_CACHE_HOME:-$HOME/.cache}/my-image-parser/mcp}"
DATA_DIR="${AGENT_TASK_MANAGER_STATE_DIR:-$STATE_ROOT/agent-task-manager}"
CACHE_DIR="${AGENT_TASK_MANAGER_NPM_CACHE:-$CACHE_ROOT/npm}"
mkdir -p "$DATA_DIR"
mkdir -p "$CACHE_DIR"

export STORAGE="${AGENT_TASK_MANAGER_STORAGE:-sqlite}"
export SQLITE_PATH="${AGENT_TASK_MANAGER_SQLITE_PATH:-$DATA_DIR/agent-tasks.db}"
export NPM_CONFIG_CACHE="$CACHE_DIR"
export npm_config_cache="$CACHE_DIR"

if [ -n "${AGENT_TASK_MANAGER_ENTRYPOINT:-}" ]; then
  exec node "$AGENT_TASK_MANAGER_ENTRYPOINT" "$@"
fi

if [ -n "${AGENT_TASK_MANAGER_BIN:-}" ]; then
  exec "$AGENT_TASK_MANAGER_BIN" "$@"
fi

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
