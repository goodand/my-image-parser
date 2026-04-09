#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SERVER_DIR="${PADDLEOCR_MCP_SERVER_DIR:-$ROOT_DIR/vendor/mcp/paddleocr-mcp}"
if [ -n "${PADDLEOCR_MCP_BIN:-}" ]; then
  MCP_BIN="$PADDLEOCR_MCP_BIN"
elif [ -x "$SERVER_DIR/.venv/bin/paddleocr_mcp" ]; then
  MCP_BIN="$SERVER_DIR/.venv/bin/paddleocr_mcp"
else
  MCP_BIN="$SERVER_DIR/venv/bin/paddleocr_mcp"
fi
LOG_DIR="$ROOT_DIR/logs/paddleocr"
MCP_HOME_DIR="$LOG_DIR/home"
PADDLE_HOME_DIR="$LOG_DIR/paddle_home"
XDG_CACHE_DIR="$LOG_DIR/xdg_cache"
PADDLEX_CACHE_DIR="$LOG_DIR/paddlex_cache"
MODELSCOPE_CACHE_DIR="$LOG_DIR/modelscope_cache"
HF_CACHE_DIR="$LOG_DIR/huggingface_cache"

if [ ! -f "$SERVER_DIR/pyproject.toml" ]; then
  echo "Missing PaddleOCR MCP project file at $SERVER_DIR/pyproject.toml." >&2
  exit 1
fi

if [ ! -x "$MCP_BIN" ]; then
  echo "Missing PaddleOCR MCP executable at $MCP_BIN. Set PADDLEOCR_MCP_BIN or run 'uv sync --directory $SERVER_DIR' first." >&2
  exit 1
fi

mkdir -p "$LOG_DIR" "$MCP_HOME_DIR" "$PADDLE_HOME_DIR" "$XDG_CACHE_DIR" "$PADDLEX_CACHE_DIR" "$MODELSCOPE_CACHE_DIR" "$HF_CACHE_DIR"

export PADDLEOCR_MCP_PIPELINE="${PADDLEOCR_MCP_PIPELINE:-PP-StructureV3}"
export PADDLEOCR_MCP_PPOCR_SOURCE="${PADDLEOCR_MCP_PPOCR_SOURCE:-local}"
export PADDLEOCR_MCP_DEVICE="${PADDLEOCR_MCP_DEVICE:-cpu}"
export HOME="${PADDLEOCR_MCP_HOME:-$MCP_HOME_DIR}"
export PADDLE_HOME="${PADDLE_HOME:-$PADDLE_HOME_DIR}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$XDG_CACHE_DIR}"
export PADDLE_PDX_CACHE_HOME="${PADDLE_PDX_CACHE_HOME:-$PADDLEX_CACHE_DIR}"
export PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK="${PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK:-True}"
export MODELSCOPE_CACHE="${MODELSCOPE_CACHE:-$MODELSCOPE_CACHE_DIR}"
export HF_HOME="${HF_HOME:-$HF_CACHE_DIR}"
export HUGGINGFACE_HUB_CACHE="${HUGGINGFACE_HUB_CACHE:-$HF_CACHE_DIR/hub}"

cd "$SERVER_DIR"
exec "$MCP_BIN" "$@"
