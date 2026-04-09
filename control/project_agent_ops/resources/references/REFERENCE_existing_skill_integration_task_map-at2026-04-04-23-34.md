# Existing Skill Integration Task Map

## Purpose

Translate current promotion-worthy repeated patterns into concrete integration tasks for existing skills, instead of creating new standalone skills too early.

## Integration Rule

- extend an existing skill first when the repeated pattern fits its current ownership rule
- create a new skill only when the pattern defines a stable workflow that does not already have a strong owner
- keep integration write-sets disjoint so the tasks can run in parallel

## Priority Integrations

### `image-result-auditor`

- issued task packet:
  - [TASK_PACKET_image_result_auditor_review_bridge_integration-at2026-04-04-23-34.md](../task_packets/issued/TASK_PACKET_image_result_auditor_review_bridge_integration-at2026-04-04-23-34.md)
- absorbs:
  - aggregate bundle to human review surface flattening
  - review surface manifest to retrieval preflight bridge
  - review decision ingestion to ready subsets
  - zero-ready downstream dry-run contract
  - machine-prefilled review-seed drift validation
  - single-writer canonical JSONL review entry
  - human-edited caption arm exception normalization

### `image-job-dispatcher`

- issued task packet:
  - [TASK_PACKET_image_job_dispatcher_fast_start_packet_integration-at2026-04-04-23-34.md](../task_packets/issued/TASK_PACKET_image_job_dispatcher_fast_start_packet_integration-at2026-04-04-23-34.md)
- absorbs:
  - fast-start packet for parallel experiment session split
  - packet-first bounded session startup
  - owned-path and non-goal discipline for narrow experiment slices

### `parser-sidecar-to-canonical-schema-promotion`

- issued task packet:
  - [TASK_PACKET_parser_sidecar_compound_edgecase_integration-at2026-04-04-23-34.md](../task_packets/issued/TASK_PACKET_parser_sidecar_compound_edgecase_integration-at2026-04-04-23-34.md)
- absorbs:
  - projection-profile component decomposition probe for compound dashboards
  - objective-profile scoring for regrouped component candidates
  - table-seed dependency blocks compound dashboard reentry

## Deferred For Now

These stay as KB candidates for now because they fit a broader control-plane maintenance workflow more than any current runtime skill:

- control action-unit migration with inventory-led execution
- residual registry namespace decomposition
- post-migration active path repair and revalidation

## Parallelism

The three issued integration packets above can run in parallel because their preferred write-sets are disjoint:

- `skills/image-result-auditor/*`
- `skills/image-job-dispatcher/*`
- `skills/parser-sidecar-to-canonical-schema-promotion/*`

## Expected Outcome

If these packets are completed, the workspace will absorb the strongest recent repeated patterns into existing skills without fragmenting the skill surface prematurely.
