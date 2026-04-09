# Smoke Test: Object Isolation Correction Worker

## Purpose

Verify that the object-isolation correction skill no longer stops at packet creation.
The worker should:

1. load a packet JSON
2. try alpha connected-components first
3. fall back to ImageSorcery when alpha split is insufficient
4. emit a bounded imagegen request artifact when the route still needs model-assisted cleanup

## Scope

Validated files:

- `skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py`
- `skills/object-isolation-correction/scripts/prepare_object_isolation_correction_packet.py`
- `scripts/mcp/start-imagesorcery-mcp.sh`

## Commands

### Case A: Transparent PNG / split-oriented packet

```bash
python3 skills/object-isolation-correction/scripts/prepare_object_isolation_correction_packet.py \
  --source-image control/project_domain/resources/pptx_jobs/02_1/media/image10.png \
  --issue merged_objects \
  --issue split_decision_needed \
  --output-md <TMP_DIR>/object-isolation-worker-smoke-alpha/CORRECTION_packet.md \
  --output-json <TMP_DIR>/object-isolation-worker-smoke-alpha/CORRECTION_packet.json

vendor/mcp/imagesorcery-mcp/.venv/bin/python \
  skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py \
  --packet-json <TMP_DIR>/object-isolation-worker-smoke-alpha/CORRECTION_packet.json \
  --output-dir <TMP_DIR>/object-isolation-worker-smoke-alpha/run
```

### Case B: Hybrid photo / imagegen-request path

```bash
python3 skills/object-isolation-correction/scripts/prepare_object_isolation_correction_packet.py \
  --source-image control/project_domain/resources/pptx_jobs/02_1/media/image6.jpeg \
  --issue background_residue \
  --issue transparent_cutout_needed \
  --target-description "the person only" \
  --output-md <TMP_DIR>/object-isolation-worker-smoke-photo/CORRECTION_packet.md \
  --output-json <TMP_DIR>/object-isolation-worker-smoke-photo/CORRECTION_packet.json

vendor/mcp/imagesorcery-mcp/.venv/bin/python \
  skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py \
  --packet-json <TMP_DIR>/object-isolation-worker-smoke-photo/CORRECTION_packet.json \
  --output-dir <TMP_DIR>/object-isolation-worker-smoke-photo/run
```

## Observed Results

### Case A

- packet route: `imagesorcery-first`
- alpha split:
  - attempted: `true`
  - component_count: `1`
  - sufficient: `false`
- ImageSorcery fallback:
  - tool: `detect`
  - object_count: `2`
  - sufficient: `true`
- imagegen request:
  - written: `false`

Artifacts:

- `<TMP_DIR>/object-isolation-worker-smoke-alpha/run/worker_report.md`
- `<TMP_DIR>/object-isolation-worker-smoke-alpha/run/worker_result.json`
- `<TMP_DIR>/object-isolation-worker-smoke-alpha/run/alpha_components/alpha_component_01.png`
- `<TMP_DIR>/object-isolation-worker-smoke-alpha/run/imagesorcery/imagesorcery_crop_01.png`
- `<TMP_DIR>/object-isolation-worker-smoke-alpha/run/imagesorcery/imagesorcery_crop_02.png`

### Case B

- packet route: `hybrid`
- alpha split:
  - attempted: `true`
  - component_count: `1`
  - sufficient: `false`
- ImageSorcery fallback:
  - tool: `find`
  - object_count: `0`
  - sufficient: `false`
- imagegen request:
  - written: `true`

Artifacts:

- `<TMP_DIR>/object-isolation-worker-smoke-photo/run/worker_report.md`
- `<TMP_DIR>/object-isolation-worker-smoke-photo/run/worker_result.json`
- `<TMP_DIR>/object-isolation-worker-smoke-photo/run/imagesorcery/find_result.json`
- `<TMP_DIR>/object-isolation-worker-smoke-photo/run/imagegen/IMAGEGEN_REQUEST.md`
- `<TMP_DIR>/object-isolation-worker-smoke-photo/run/imagegen/IMAGEGEN_REQUEST.json`

## Troubleshooting Captured

The worker surfaced two workspace-relevant constraints and now accounts for both:

1. The ImageSorcery launcher should be invoked through `bash` because the shell script path itself is not executable in this workspace.
2. Text-prompted `find` currently behaves better as bbox-only retrieval in this workspace; geometry requests are not treated as reliable.

These constraints were folded back into:

- `skills/object-isolation-correction/references/troubleshooting.md`

## Conclusion

The worker is operational.

- It can consume a bounded correction packet.
- It can run deterministic alpha split without new dependency installation.
- It can contact ImageSorcery through stdio and produce fallback crops.
- It can emit a bounded imagegen request artifact when deterministic recovery is insufficient.
