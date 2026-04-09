# Smoke Test: Object Isolation Correction Skill

## Date

- 2026-03-27 23:10 KST

## Purpose

Verify that the workspace skill can build a bounded correction packet for object-isolation retries.

## Surface Under Test

- skill:
  - `skills/object-isolation-correction`
- script:
  - `skills/object-isolation-correction/scripts/prepare_object_isolation_correction_packet.py`
- sample image:
  - `control/project_domain/resources/pptx_jobs/02_1/media/image10.png`

## Verification Steps

1. Verified `--help` for the skill-local packet builder.
2. Generated a markdown correction packet.
3. Generated a JSON sidecar with the same route decision.

## Smoke Inputs

- source image:
  - `control/project_domain/resources/pptx_jobs/02_1/media/image10.png`
- issues:
  - `merged_objects`
  - `split_decision_needed`
- target description:
  - `the table only`

## Smoke Outputs

- markdown packet:
  - `/tmp/object-isolation-correction-smoke/CORRECTION_smoke.md`
- json packet:
  - `/tmp/object-isolation-correction-smoke/CORRECTION_smoke.json`

## Result Summary

- chosen route: `imagesorcery-first`
- recommended next tools:
  - `imagesorcery-mcp.detect/find`
  - `imagesorcery-mcp.fill`
  - `imagesorcery-mcp.crop`

## Outcome

- the skill structure is present
- the helper script is executable
- the route-selection packet is generated successfully for a real local image
