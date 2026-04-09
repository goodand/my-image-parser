# PPTX Slide Screenshot Capture Smoke Test

## Scope

Validate the local skill `pptx-slide-screenshot-capture` on a minimal simulator-visible fixture.

## Fixture

- Viewer page: [index.html](./fixtures/pptx-slide-screenshot-capture-fixture/index.html)
- Source image: [image1.png](../../../project_domain/resources/pptx_jobs/02_1/media/image1.png)
- Job manifest: [cross_validation_manifest.json](../../../project_domain/resources/cross_validation/02_1/cross_validation_manifest.json)
- Simulator: `iPhone 17` `890CC53F-E0E3-4559-AA1B-0764B0369851`

## Result

- Viewer surface load: passed
- `simctl screenshot` direct shell call: passed
- helper script in sandboxed Python process: failed
- helper script outside sandbox: passed

## Commands Used

```bash
python3 -m http.server 8000 --bind 127.0.0.1
xcrun simctl boot 890CC53F-E0E3-4559-AA1B-0764B0369851
xcrun simctl bootstatus 890CC53F-E0E3-4559-AA1B-0764B0369851 -b
xcrun simctl openurl 890CC53F-E0E3-4559-AA1B-0764B0369851 \
  "http://127.0.0.1:8000/control/project_agent_ops/resources/smoke/fixtures/pptx-slide-screenshot-capture-fixture/index.html"
python3 skills/pptx-slide-screenshot-capture/scripts/capture_simctl_slide_screenshots.py \
  --job-manifest control/project_domain/resources/cross_validation/02_1/cross_validation_manifest.json \
  --udid 890CC53F-E0E3-4559-AA1B-0764B0369851 \
  --slide-count 1 \
  --manual-advance \
  --overwrite
```

## Output Artifacts

- Screenshot: [slide-0001.png](../../../project_domain/resources/cross_validation/02_1/slide_screenshots_simctl/slide-0001.png)
- Dataset: [slide_screenshots_simctl_dataset.jsonl](../../../project_domain/resources/cross_validation/02_1/slide_screenshots_simctl_dataset.jsonl)

## Observed Failure

The sandboxed Python run failed with `CoreSimulatorService connection invalid` while the direct shell `simctl` call worked.

## Conclusion

The skill workflow and helper script are valid.
For Codex-driven smoke runs, the helper should be executed outside the sandbox when it needs to call `xcrun simctl` through Python.
