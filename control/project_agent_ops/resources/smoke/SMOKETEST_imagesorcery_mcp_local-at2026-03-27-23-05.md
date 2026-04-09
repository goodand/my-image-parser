# Smoke Test: ImageSorcery MCP Local

## Date

- 2026-03-27 23:05 KST

## Purpose

Verify that the vendored `imagesorcery-mcp` launcher is not only registered, but also boots through stdio and can execute representative local tools.

## Surface Under Test

- launcher:
  - `scripts/mcp/start-imagesorcery-mcp.sh`
- vendored runtime:
  - `vendor/mcp/imagesorcery-mcp/.venv/bin/imagesorcery-mcp`
- sample image:
  - `control/project_domain/resources/pptx_jobs/02_1/media/image10.png`

## Verification Steps

1. Verified stdio boot through `FastMCP` subprocess client transport using the workspace launcher.
2. Verified tool listing succeeds.
3. Verified `detect` succeeds against a real PPT-extracted image.
4. Verified `find(description="table")` succeeds against the same image after local YOLOE and CLIP setup.

## Evidence Summary

- tool list returned: `17` tools
- representative tools observed:
  - `detect`
  - `find`
  - `ocr`
  - `crop`
  - `fill`
  - `get_metainfo`
- local model files present:
  - `models/yoloe-11l-seg-pf.pt`
  - `models/yoloe-11l-seg.pt`
  - `models/yoloe-11s-seg-pf.pt`
  - `models/yoloe-11s-seg.pt`
- local CLIP artifact present:
  - `mobileclip_blt.ts`

## Detect Result

- status: success
- image: `image10.png`
- result summary:
  - one detection returned
  - class: `sing`
  - confidence: `0.7621259689331055`

## Find Result

- status: success
- image: `image10.png`
- query: `table`
- result summary:
  - `found = false`
  - `found_objects = []`

This is still a successful smoke because the tool executed normally and returned structured output instead of failing on boot, model loading, or text-prompt setup.

## Notes

- `find` depends on local CLIP plus `mobileclip_blt.ts`; it does not use the OpenAI API.
- launcher-level cache redirection was needed so `YOLO_CONFIG_DIR` points to a workspace-writable path.
- stdio hygiene mattered: launcher and vendored runtime output had to stay off stdout so MCP transport remained machine-readable.

## Outcome

- `imagesorcery-mcp` is locally boot-verified in this workspace.
- canonical registry and setup references should reflect this smoke result.
