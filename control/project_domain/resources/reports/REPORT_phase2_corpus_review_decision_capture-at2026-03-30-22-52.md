# Report: Phase 2 Corpus Review Decision Capture

## Purpose

Create the bounded bridge between the existing corpus review surface and the later retrieval or mapping preflight consumers.

## Produced Artifacts

- prose spec:
  - [SPEC_corpus_review_decision_capture.md](../specs/prose/SPEC_corpus_review_decision_capture.md)
- machine-readable contract:
  - [corpus_review_decision_capture.contract.json](../specs/contracts/corpus_review_decision_capture.contract.json)
- prefilled review seed:
  - [phase2_caption_review_decision_seed_at2026_03_30.jsonl](../manifests/phase2_caption_review_decision_seed_at2026_03_30.jsonl)

## Canonical Inputs

- review surface manifest:
  - [phase2_caption_four_mode_corpus_review_surface_at2026_03_30.json](../manifests/phase2_caption_four_mode_corpus_review_surface_at2026_03_30.json)
- review markdown:
  - [REVIEW_phase2_caption_four_mode_corpus_review-at2026-03-30-22-45.md](./REVIEW_phase2_caption_four_mode_corpus_review-at2026-03-30-22-45.md)
- promotion policy:
  - [SPEC_caption_arm_promotion_policy.md](../specs/prose/SPEC_caption_arm_promotion_policy.md)

## Design Summary

- one JSON object per image
- seed rows are machine-prefilled from the existing review surface
- reviewer fills the decision fields after reading the review markdown
- downstream retrieval preflight reads only approved rows

## Schema Shape

The contract captures three layers:

1. machine-prefilled review context
   - image id
   - source image path
   - bundle path
   - active default arm
   - comparison winner
   - comparison winner promotion state
   - pending context review arms

2. human decision fields
   - selected caption arm
   - selected caption promotion state
   - caption decision
   - caption edit required
   - approved caption
   - approved alt text
   - retrieval toggle
   - optional mapping preflight hint
   - outlier candidate flag
   - rationale and notes

3. review status fields
   - review status
   - reviewer id
   - reviewed at

## Ingestion Rules

- retrieval preflight may read only rows with:
  - `review_status = completed`
  - `use_for_retrieval = true`
  - non-empty `approved_caption`
- `mapping_review_required` is kept as an optional downstream hint, not the primary gate
- `outlier_candidate` is a preflight suspicion field and not a final mapping label

## Seed Coverage

- image count: `9`
- seeded image ids:
  - `image11`
  - `image7`
  - `image8`
  - `image10`
  - `image12`
  - `image13`
  - `image14`
  - `image9`
  - `image15`

## Boundaries Preserved

This Session C bridge did not:

- regenerate any caption arm
- modify any per-image or corpus bundle
- execute retrieval
- finalize mapping
- modify the master plan

## Verification

- contract JSON parses
- seed file contains one row per active corpus review image
- every seed row points back to the current review surface and review markdown
- required cross-field rules are written into the prose spec and machine-readable contract metadata

## Readiness Result

The workspace now has a human decision capture bridge that can:

- receive Session A review outcomes
- preserve approved caption text without reopening arm bundles
- feed Session B retrieval or mapping preflight once review is completed
