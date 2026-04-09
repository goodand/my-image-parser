# Phase1 Image4 Apple Document Structure Probe

## Scope

- source image: `control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image4.png`
- bounded goal: determine whether the Apple Vision document-structure helper can yield a stable sidecar for downstream canonical promotion

## Command

```bash
xcrun swift skills/parser-sidecar-to-canonical-schema-promotion/scripts/macos_table_structure_helper.swift \
  --input /Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image4.png \
  --output /tmp/image4_apple_helper_raw.json
```

## Observed Result

- the helper did not emit JSON to stdout within the bounded observation window
- `/tmp/image4_apple_helper_raw.json` was not created during that window
- process inspection showed both of the following remained alive after the command should have completed:
  - `swift-frontend ... macos_table_structure_helper.swift`
  - `/tmp/.../vision_document_runner`
- the lingering helper runner was manually cleaned up after the bounded probe

## Interpretation

- this probe did not produce a stable raw Apple helper sidecar for `image4`
- because no helper-sidecar JSON was emitted, canonical promotion could not begin
- in this slice, the Apple helper path does not close the missing parser seed requirement for reviewed recrop

## Result

- decision impact: `image4` exclusion remains correct
- downstream effect: `parser_table_enriched_rerun` and `reviewed_isolated_component_rerun` remain blocked

## Next One Step

- only reopen `image4` if a future deterministic parser path produces a stable normalized table or reviewed seed bbox without helper non-termination
