# TASK: Multi-Component Reviewed Crop Recrop Candidate Selection

## Why this repeats

The current reviewed-component flow often starts from a parser-derived seed bbox such as a table-cell union. On composite slides or multi-component transparent images, that seed bbox can be structurally correct but still too narrow for captioning because nearby title/context components are excluded.

This repeats whenever:
- a reviewed branch needs a semantically tighter crop than the full image
- a single seed bbox exists, but nearby disconnected alpha components still belong to the same useful caption surface
- raw alpha split is too fragmented to promote directly, but a bounded union recrop is still feasible

## Observed pattern

In the current codebase:
- alpha components can already be enumerated and exported
- parser or merged-candidate logic can already produce a seed bbox
- the missing step was selecting a better reviewed crop candidate when more than one nearby component exists

## Current proven handling

The bounded fix that worked here was:
1. start from the existing reviewed seed bbox
2. enumerate alpha components without promoting them directly
3. build a bounded `alpha_nearby_union` candidate only from nearby external components
4. evaluate `seed_bbox` versus union candidates with the same OCR-proxy evidence surface
5. keep provenance and candidate-selection metadata inside the reviewed-component context package

## Promotion target

Reusable reviewed-component recrop candidate selection for multi-component images.

## Promotion trigger

Trigger promotion again when another reviewed branch:
- is blocked because the seed bbox is too narrow
- still has a bounded nearby-component recrop option
- should be improved without opening a new semantic object-selection lane

## Current proven example

`scripts/reviewed_component_context_package_lib.py` now supports bounded candidate generation and selection between:
- `seed_bbox`
- `alpha_nearby_union`

for reviewed-component context-package generation.
