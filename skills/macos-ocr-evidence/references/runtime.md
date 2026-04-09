# Runtime Notes

## Preferred MCP Path

- Launcher:
  - `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/scripts/mcp/start-macos-ocr-mcp.sh`
- Vendored source:
  - `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/vendor/mcp/macos-ocr-mcp`
- Tool:
  - `ocr_image(file_path)`

This path is macOS-only.
In this workspace it is also **unsandboxed-preferred**.

Observed behavior:

- sandboxed execution can fail with `NoneType` iteration errors inside `ocrmac`
- unsandboxed execution has been smoke-verified on:
  - a synthetic text image
  - a real slide screenshot

## Fallback Path

- local fallback script:
  - `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/scripts/ocr/macos_vision_ocr.swift`

The vendored MCP wrapper can call this script when `ocrmac` throws a `NoneType`-style failure.

## Complementary CLI Path

- Vendored source:
  - `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/vendor/ocr/macOCR`

The repo documents:

- `ocr --input <file>`
- `ocr --rect <x,y,w,h>`
- `ocr --language <code>`

Treat `macOCR` as a fallback or comparison surface.
In the current workspace, treat it as **reference-only** for now.

Observed activation status:

- `ocr` binary is not installed globally
- local vendored build is not yet clean enough to treat as an active runtime path

## Good Fits

- extracted PPT media with visible labels or UI text
- isolated object cutouts that still contain readable text
- chart and table screenshots where OCR can validate caption grounding

## Known Limits

- `macos-ocr-mcp` returns annotation-level results, not a polished paragraph summary
- `macos-ocr-mcp` may need an unsandboxed rerun for reliable OCR execution
- `macOCR` may require a local install or build cleanup before the CLI is usable
- neither surface replaces structured table parsing
