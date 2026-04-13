# NOTE_skill_first_platform_evolution_direction-at2026-04-09-19-32

## Intent

Freeze the next productization direction after the current caption-experiment cycle closure.

## Frozen Direction

The next evolution path should begin with `Agent Skills`, not a new monolithic `MCP` and not a full `Docker-first platform`.

The recommended order is:

1. extend and compose existing skills first
2. freeze provider-agnostic contracts for image context, caption output, evaluation output, and PPT regeneration handoff
3. keep existing MCPs and scripts as underlying providers
4. promote only the most stable and repeated provider path into a dedicated MCP later
5. open broader platform packaging only after the skill and contract layer proves stable

## Why This Direction

- the current workspace already has reusable skills and provider paths
- some lower providers depend on ML-backed runtimes, so turning everything into a new MCP too early would expand scope from workflow packaging into platform engineering
- the immediate product goal is not just caption generation but `context-aware image use inside PPT workflows`
- downstream workspaces such as `my-second-identity` need multimodal form preservation, so the orchestration layer must keep provider choice flexible while the contract hardens

## Product Goal

The target system should help produce PPT workflows where images are not treated as passive decoration.

The system should:

- parse images with context sensitivity
- preserve meaningful multimodal form when needed
- generate and evaluate captions and alt text
- support bounded human or agent cross-validation
- feed approved image understanding back into PPT regeneration or PPT authoring workflows

## Near-Term Ownership Model

Use `existing skills + stable contracts + provider matrix` as the canonical near-term ownership model.

That means:

- orchestration belongs to skills
- heavy OCR/parser/vision execution may remain in existing MCPs or scripts
- only repeated stable provider paths should later be promoted into narrower MCP surfaces

## Canonical Companion

- [PLAN_skill_first_multimodal_ppt_platform_evolution-at2026-04-09.md](../../../../project_domain/resources/master_plans/drafts/PLAN_skill_first_multimodal_ppt_platform_evolution-at2026-04-09.md)

## One-Line Summary

The next program should start as a `skill-first, provider-backed, platform-later` evolution path for context-aware PPT image understanding and regeneration.
