# Phase0 Alpha Split Batch Classification Report

## Purpose

Classify which PPT-extracted images are already good enough for deterministic alpha split without ImageSorcery fallback.

## Batch Surface

- input_root: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs`
- worker_script: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py`
- worker_python: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/vendor/mcp/imagesorcery-mcp/.venv/bin/python`
- alpha_threshold: `1`
- min_pixels: `32`
- padding: `4`
- min_components_for_success: `2`

## Summary

- total_images: `61`
- alpha_split_sufficient: `9`
- non_alpha_source_or_opaque_surface: `1`
- single_component_only: `50`
- unsupported_source_format: `1`

## Alpha-Split-Sufficient Candidates

- `01_full_presentation_2026-03-17:image1.png` components=`82` manifest=`/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/archive/object_isolation/alpha_split_batch/2026-03-27-15-05/01_full_presentation_2026-03-17/image1/alpha_components/alpha_components.json`
- `01_full_presentation_2026-03-17:image2.png` components=`139` manifest=`/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/archive/object_isolation/alpha_split_batch/2026-03-27-15-05/01_full_presentation_2026-03-17/image2/alpha_components/alpha_components.json`
- `01_full_presentation_2026-03-17:image3.png` components=`85` manifest=`/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/archive/object_isolation/alpha_split_batch/2026-03-27-15-05/01_full_presentation_2026-03-17/image3/alpha_components/alpha_components.json`
- `01_full_presentation_2026-03-17:image4.png` components=`140` manifest=`/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/archive/object_isolation/alpha_split_batch/2026-03-27-15-05/01_full_presentation_2026-03-17/image4/alpha_components/alpha_components.json`
- `02_1:image11.png` components=`3` manifest=`/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/archive/object_isolation/alpha_split_batch/2026-03-27-15-05/02_1/image11/alpha_components/alpha_components.json`
- `02_1:image12.png` components=`4` manifest=`/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/archive/object_isolation/alpha_split_batch/2026-03-27-15-05/02_1/image12/alpha_components/alpha_components.json`
- `02_1:image17.png` components=`9` manifest=`/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/archive/object_isolation/alpha_split_batch/2026-03-27-15-05/02_1/image17/alpha_components/alpha_components.json`
- `02_1:image7.png` components=`26` manifest=`/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/archive/object_isolation/alpha_split_batch/2026-03-27-15-05/02_1/image7/alpha_components/alpha_components.json`
- `02_1:image8.png` components=`7` manifest=`/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/archive/object_isolation/alpha_split_batch/2026-03-27-15-05/02_1/image8/alpha_components/alpha_components.json`

## Single-Component-Only Cases

- `01_full_presentation_2026-03-17:image10.png` reason: Alpha split found 1 component(s) at or above the pixel threshold.
- `01_full_presentation_2026-03-17:image11.png` reason: Alpha split found 1 component(s) at or above the pixel threshold.
- `01_full_presentation_2026-03-17:image12.png` reason: Alpha split found 1 component(s) at or above the pixel threshold.
- `01_full_presentation_2026-03-17:image13.png` reason: Alpha split found 1 component(s) at or above the pixel threshold.
- `01_full_presentation_2026-03-17:image14.png` reason: Alpha split found 1 component(s) at or above the pixel threshold.
- `01_full_presentation_2026-03-17:image15.png` reason: Alpha split found 1 component(s) at or above the pixel threshold.
- `01_full_presentation_2026-03-17:image5.png` reason: Alpha split found 1 component(s) at or above the pixel threshold.
- `01_full_presentation_2026-03-17:image7.png` reason: Alpha split found 1 component(s) at or above the pixel threshold.
- `01_full_presentation_2026-03-17:image8.png` reason: Alpha split found 1 component(s) at or above the pixel threshold.
- `01_full_presentation_2026-03-17:image9.png` reason: Alpha split found 1 component(s) at or above the pixel threshold.
- `02_1:image1.png` reason: Alpha split found 1 component(s) at or above the pixel threshold.
- `02_1:image10.png` reason: Alpha split found 1 component(s) at or above the pixel threshold.
- `02_1:image13.png` reason: Alpha split found 1 component(s) at or above the pixel threshold.
- `02_1:image14.png` reason: Alpha split found 1 component(s) at or above the pixel threshold.
- `02_1:image15.png` reason: Alpha split found 1 component(s) at or above the pixel threshold.
- `02_1:image16.png` reason: Alpha split found 1 component(s) at or above the pixel threshold.
- `02_1:image18.png` reason: Alpha split found 1 component(s) at or above the pixel threshold.
- `02_1:image19.png` reason: Alpha split found 1 component(s) at or above the pixel threshold.
- `02_1:image2.png` reason: Alpha split found 1 component(s) at or above the pixel threshold.
- `02_1:image20.png` reason: Alpha split found 1 component(s) at or above the pixel threshold.

## Non-Alpha Or Opaque-Surface Cases

- `02_1:image6.jpeg` extension=`.jpeg` reason: Alpha split found 1 component(s) at or above the pixel threshold.

## No-Component Cases

- none

## Worker Errors

- none

## Recommendation

- only the `alpha_split_sufficient` subset should move forward as deterministic split candidates
- keep all other images on the full-image + standalone OCR baseline
- do not turn on automatic object-isolation batch fanout for the insufficient subset yet
