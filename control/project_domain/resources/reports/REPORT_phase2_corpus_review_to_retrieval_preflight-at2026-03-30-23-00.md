# Phase 2 Corpus Review To Retrieval Preflight

## Purpose

Bridge the human-facing corpus review surface into machine-readable decision, retrieval, and mapping seeds without regenerating any caption arms.

## Used Truth Source

- review surface manifest: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase2_caption_four_mode_corpus_review_surface_at2026_03_30.json`
- machine truth mode: `manifest`
- manifest-only consumer: `true`

## Corpus Summary

- image_count: `9`
- image_ids: `image11, image7, image8, image10, image12, image13, image14, image9, image15`
- active default baseline: `full_image_baseline`

## Human Review Carry-Over

- highest priority: `image11, image7, image8`
- high priority: `image10, image12, image13, image14, image9`

## Output Seeds

- decision seed: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase2_caption_review_decision_seed_at2026_03_30.jsonl`
- retrieval input seed: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase2_retrieval_input_seed_at2026_03_30.jsonl`
- mapping review seed: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase2_mapping_review_seed_at2026_03_30.jsonl`

## Guardrails

- keep `full_image_baseline` as the active default until a later explicit promotion decision closes
- do not treat comparison winners as default replacements
- treat reviewed or parser reruns in pending-review state as comparison-only inputs
- do not run retrieval or mapping in this slice; only prepare seeds

## Required Human Decision Fields

- `selected_caption_arm`
- `approved_caption`
- `approved_alt_text`
- `use_for_retrieval`
- `mapping_review_required`
- `outlier_candidate`
- `reviewer_notes`

## Current Downstream Status

- retrieval_ready: `false`
- mapping_ready: `false`
- regeneration_ready: `false`
