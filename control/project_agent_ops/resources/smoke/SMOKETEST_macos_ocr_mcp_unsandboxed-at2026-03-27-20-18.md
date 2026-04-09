# macOS OCR MCP Unsandboxed Smoke

## Purpose

Verify whether the vendored `macos-ocr-mcp` is usable in this workspace and clarify the fallback status.

## Inputs

- synthetic sample:
  - `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_agent_ops/resources/smoke/macos_ocr_smoke_sample.png`
- project screenshot sample:
  - `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/cross_validation/02_1/slide_screenshots_simctl/slide-0001.png`

## Observed Results

### Sandboxed path

- `ocrmac` path raised `TypeError: 'NoneType' object is not iterable`
- local Swift Vision fallback also failed in sandbox with a Foundation generic ObjC error

Interpretation:

- OCR is not reliable inside the current sandboxed execution surface

### Unsandboxed path

- direct Swift fallback smoke on synthetic sample succeeded
- vendored `macos-ocr-mcp` wrapper succeeded on:
  - synthetic sample
  - real slide screenshot

Observed synthetic sample result:

- engine: `ocrmac`
- annotation_count: `1`
- full_text: `HELLOOR 123`

Observed project screenshot result:

- engine: `ocrmac`
- annotation_count: `13`
- OCR evidence extracted from slide text

## Conclusion

- `macos-ocr-mcp` is a valid OCR tool for this workspace
- it should be treated as **unsandboxed-only for reliable execution**
- `macOCR` remains **reference-only** in the current workspace because:
  - `ocr` binary is not installed globally
  - local vendored Xcode build is not yet clean

## Operational Rule

1. Prefer `macos-ocr-mcp` first.
2. If OCR is needed during a constrained execution surface, rerun unsandboxed before concluding the image contains no text.
3. Treat `macOCR` as a future fallback or debugging path, not an active production path yet.
