# Repeated Task Patterns

## Purpose

Track repeated project-agent operational tasks that may later be promoted into a reusable skill, helper script, or standard packet.

## Source Of Truth

- This file is the canonical repeated-task pattern log under `project_agent_ops/resources/skill_candidates/repeated_tasks/`.
- Keep the list concise and only promote patterns that recur across sessions or runs.

## Candidate Pattern Format

For each candidate, record:

- task name
- recurrence signal
- current manual handling
- promotion target
- promotion trigger

## Current Repeated Task Patterns

### Parallel Caption Shard Preparation

- recurrence signal: repeated whenever one-image or bounded-batch caption jobs are run in parallel
- current manual handling: main agent splits dataset JSONL into shard JSONL files and assigns one shard per worker
- promotion target: script or skill wrapper
- promotion trigger: a second multi-arm experiment that requires the same shard production and packet emission path
- current promoted surface: `skills/image-job-dispatcher` with page-split sidecars for runtime, shard strategy, task-packet contract, and parallel preflight

### Master Plan Consolidation

- recurrence signal: repeated whenever new drafts or implementation profiles are merged into the canonical pipeline narrative
- current manual handling: manual draft triage plus append-only patching into the single active master plan
- promotion target: standard consolidation packet or dedicated consolidation skill
- promotion trigger: another merge cycle involving three or more active drafts

### External MCP And Skill Onboarding

- recurrence signal: repeated whenever a new external capability is brought into the workspace through a vendored MCP, local launcher, inventory update, and skill wrapper
- current manual handling: clone or vendor the upstream source, prepare the runtime, add a launcher under `scripts/mcp/`, register it in `.codex/config.toml`, update tool inventory and path registry, then add a local skill and smoke evidence
- promotion target: reusable onboarding checklist, script bundle, or dedicated MCP-onboarding skill
- promotion trigger: a second or third new MCP integration that follows the same vendor -> launcher -> config -> inventory -> skill -> smoke sequence

### Project-Start Agent-Ops Document Promotion

- recurrence signal: repeated whenever raw provider feedback needs to be promoted into `repeated_tasks/`, `repeated_issues/`, or broader team rules after a run
- current manual handling: read recent feedback, infer whether the lesson is actor-specific or reusable, then append the promoted pattern into the correct canonical bucket
- promotion target: standard promotion checklist or helper packet for post-run documentation
- promotion trigger: another run cycle where the same feedback-to-pattern promotion flow is performed again

### Vendored Python MCP Bootstrap

- recurrence signal: repeated whenever a Python-based MCP is brought in through `vendor/mcp/` and should stay isolated from the main workspace runtime
- current manual handling: clone the upstream source, create a dedicated venv inside the vendored directory, install the package there, add a wrapper under `scripts/mcp/`, register it in `.codex/config.toml` and `.vscode/mcp.json`, then update inventory and smoke evidence
- promotion target: reusable bootstrap checklist or helper script for vendored Python MCPs
- promotion trigger: another Python MCP follows the same vendor -> dedicated venv -> wrapper -> config -> inventory -> smoke sequence

### Model-Backed MCP Activation And Smoke

- recurrence signal: repeated whenever a vendored MCP needs post-install model downloads, writable cache redirection, and separate light/heavy smoke verification before it is truly usable
- current manual handling: prepare launcher env vars, run upstream post-install, check tool listing or stdio boot first, then run at least one inference tool before marking the server active
- promotion target: reusable activation checklist or model-backed launcher template
- promotion trigger: another local MCP requires the same post-install -> cache override -> client-based smoke sequence

### Review Surface Canonicalization

- recurrence signal: repeated whenever a human-review markdown surface is created from run artifacts and later needs to be reconciled against `project_domain/runs/reports/` versus `user_decisions/`
- current manual handling: inspect the actual review purpose, move the canonical review artifact under `project_domain/runs/reports/`, keep decision promotion separate, and patch references or runtime examples that still point to the wrong bucket
- promotion target: reusable review-surface filing guide or a stricter review-builder skill contract
- promotion trigger: another review workflow creates duplicate surfaces across `project_domain` and `user_decisions`

### Batch-Specific Utility Generalization

- recurrence signal: repeated whenever a one-off script or review surface built for a named batch such as `phase1_caption_10w` needs to become a reusable skill or canonical helper
- current manual handling: remove batch-specific defaults, make the batch input explicit, replace hardcoded titles or paths with parameters, then realign examples and runtime notes
- promotion target: a standard hardening checklist for converting one-off utilities into reusable scripts or skills
- promotion trigger: another batch-specific helper is promoted into `skills/` or broader team-facing documentation

### Phase0 Smoke Split Verification

- recurrence signal: repeated whenever object isolation, OCR, and context-package quality must be checked before committing to a larger experiment fanout
- current manual handling: run a bounded isolation smoke first, then run standalone OCR separately to see whether isolation actually improves the usable text surface
- promotion target: reusable phase0 smoke script bundle plus report template
- promotion trigger: another pre-caption preprocessing experiment needs the same isolate -> OCR -> compare workflow

### Context Package Builder To Caption Runner Injection

- recurrence signal: repeated whenever a reviewed OCR or context-package artifact should feed a later caption rerun without replacing the original no-context baseline
- current manual handling: add explicit context-package CLI flags, map packages by `source_image_path`, sanitize review-only fields, then verify the runner with a fake client before live API use
- promotion target: reusable integration checklist or prompt-safe context adapter helper
- promotion trigger: another caption or rerun surface needs the same reviewed-context -> additive injection flow

### UV-Managed Vendor MCP Pinning

- recurrence signal: repeated whenever a third-party MCP should be kept reproducible inside `vendor/mcp/` rather than installed ad hoc into a floating venv
- current manual handling: create a minimal `pyproject.toml`, sync a dedicated `.venv` with `uv sync`, keep `uv.lock`, then wire a launcher that points to the vendored executable
- promotion target: reusable `uv-managed MCP vendor skeleton` template plus onboarding checklist
- promotion trigger: another externally sourced MCP is adopted and must be pinned through `pyproject.toml` and `uv.lock`

### Install-State Versus Boot-State Separation

- recurrence signal: repeated whenever a heavy MCP can be fully installed and launcher-wired, but should not be marked boot-verified until a separate bounded runtime smoke is recorded
- current manual handling: verify `pyproject.toml`, `uv.lock`, binary presence, and launcher wiring first, then keep `boot_verified=false` until an actual stdio smoke artifact exists
- promotion target: reusable install-smoke report template and inventory status rule
- promotion trigger: another model-heavy MCP has a long first-run initialization path and the install step finishes earlier than trustworthy runtime verification

### Experiment Baseline Reframing And Cross-Document Sync

- recurrence signal: repeated whenever a smoke or review result changes the next recommended experiment path and the new baseline must be propagated across the master plan, phase plans, KB, checklist, and tool notes
- current manual handling: update the active experiment narrative first, then patch every dependent canonical document so that baseline, fallback path, and next-step wording stay aligned
- promotion target: reusable baseline-shift checklist or post-smoke synchronization packet
- promotion trigger: another experiment result changes the primary path from the one previously documented in multiple canonical files

### Traceback-To-Launcher Environment Hardening

- recurrence signal: repeated whenever a third-party runtime fails during import or startup, but the real fix is an environment override or path redirection in the launcher rather than a source edit
- current manual handling: inspect the traceback, identify the env vars or cache roots involved, patch the launcher, then rerun the smallest possible command to confirm the launcher-level fix
- promotion target: reusable launcher-hardening checklist plus env-override snippet library
- promotion trigger: another local MCP or model-backed CLI reveals a startup failure that is resolved by launcher-controlled environment variables

### Component Split Table And OCR Surface Generation

- recurrence signal: repeated whenever a transparent or semi-transparent extracted image must be split into disconnected components, reviewed in a table, and checked for per-component text before downstream caption work
- current manual handling: run alpha connected-components, export one PNG per component, OCR each component image, then write markdown and JSON review surfaces
- promotion target: reusable component-review skill or pre-caption packet builder
- promotion trigger: another phase0 or reviewed-isolation branch needs the same component split plus OCR review flow
- current promoted surface: `skills/component-split-ocr-review` with a thin wrapper over `scripts/build_component_split_ocr_report.py`

### Shared Deterministic Image Processing Core Extraction

- recurrence signal: repeated whenever the same local image-processing step is needed by more than one workflow surface and naive copy-paste would create behavior drift
- current manual handling: extract the shared deterministic core into a workspace library, keep thin entrypoints, and add a config or service wrapper when multiple workflows reuse the same core
- promotion target: reusable refactor checklist or helper guidance for deterministic local image-processing modules
- promotion trigger: another local image-processing step is reused across worker, builder, and review surfaces

### Alpha-Split-Only Candidate Batch Classification

- recurrence signal: repeated whenever conservative preprocessing needs a deterministic prefilter that separates alpha-split candidates from full-image-baseline files
- current manual handling: run the alpha-only batch classifier, emit report and summary artifacts, and review the `alpha_split_sufficient` subset before any downstream promotion
- promotion target: reusable transparent-image triage skill or review-gated subset packet
- promotion trigger: another preprocessing branch needs the same conservative candidate discovery step
- current promoted surface: `skills/transparent-component-triage` with a thin wrapper over `skills/object-isolation-correction/scripts/classify_alpha_split_batch.py`

### Vendored MCP Onboarding

- recurrence signal: repeated whenever a third-party MCP must be vendored, isolated, launcher-wired, config-registered, inventory-synced, and smoke-verified before being treated as active
- current manual handling: vendor under `vendor/mcp/`, isolate runtime, create launcher under `scripts/mcp/`, register in config, update inventory and session registry, then collect bounded smoke evidence
- promotion target: reusable onboarding skill or packet template
- promotion trigger: another workspace-local MCP follows the same vendor -> launcher -> config -> inventory -> smoke path
- current promoted surface: `skills/vendored-mcp-onboarding`

### Parser Sidecar To Canonical Schema Promotion

- recurrence signal: repeated whenever a parser MCP returns markdown plus nested detailed JSON sidecars, and the project must promote that result into a stable canonical schema rather than keep consuming raw tool output
- current manual handling: capture a bounded raw parse artifact, extract the first stable table payload, recover provenance from the source manifest, then normalize into the canonical `Table -> Row -> Cell` JSON
- promotion target: reusable normalization helper or parser-bridge skill
- promotion trigger: another parser backend or document-analysis MCP needs the same raw-result -> canonical-schema promotion path
- current promoted surface: `skills/parser-sidecar-to-canonical-schema-promotion` backed by `scripts/promote_parser_sidecar_to_canonical_schema.py`

### Bounded Table-Branch Activation Slice Closure

- recurrence signal: repeated whenever a planned activation sequence must be closed with real evidence before the next stage is allowed to begin
- current manual handling: execute the minimum ordered slice `triage -> boot smoke -> real parse smoke -> canonical normalization -> wrapper spec`, then patch the master plan and phase plan so the next active item becomes explicit
- promotion target: reusable activation-slice checklist or packet bundle for new parser or branch rollouts
- promotion trigger: another dormant branch needs the same evidence-first activation path before it is treated as runnable
- current promoted surface: `skills/table-branch-activation-slice`

### Semantic Artifact Regeneration After Runner Contract Change

- recurrence signal: repeated whenever a bounded runner already produced valid artifacts, but a later contract or metadata fix means those artifacts should be regenerated rather than merely patched in place
- current manual handling: patch the runner, rerun the same bounded input set, then keep the regenerated manifest as the truth source for downstream docs and indexes
- promotion target: reusable rerun-after-contract-change checklist
- promotion trigger: another smoke or bounded experiment needs regeneration because a field name, experiment label, or provenance rule changed after the first successful run

### Packetized Subagent Skill Creation Sidecars

- recurrence signal: repeated whenever a new or promoted skill produces the same disjoint sidecar artifact families and parallel drafting would help, but shared files such as `SKILL.md`, registries, and master plans must stay single-owner
- current manual handling: keep the main agent as architect and integrator, issue file-backed task packets, delegate `runtime`, `troubleshooting`, `knowledge_bases`, or `evals` pages to subagents, then integrate centrally
- promotion target: reusable subagent strategy guide and sidecar packet template for repeated skill creation
- promotion trigger: another skill-creation cycle uses the same write-set ownership split across sidecar pages
- current proven example: `skills/table-branch-activation-slice`

### Existing Skill Page-Split Sidecar Expansion

- recurrence signal: repeated whenever an initially thin skill accumulates enough workflow detail that it should be page-split rather than rewritten
- current manual handling: keep the root `SKILL.md` lean, add `runtime` and `troubleshooting`, then add topic-specific references, checklist, KB, and evals while preserving the working runtime surface
- promotion target: reusable page-split expansion checklist or sidecar skeleton template
- promotion trigger: another existing skill needs shard rules, packet rules, or review boundaries that no longer fit cleanly in a single page
- current proven example: `skills/image-job-dispatcher`
- eval note: `evals/evals.json` should stay skill-local, but its axes should align with `agent-tool-benchmark` when the skill governs orchestration, packetized workers, or tool-use quality
- later proven examples: `skills/image-worker`, `skills/image-result-auditor`

### Benchmark-Aware Eval Layering For Orchestration Skills

- recurrence signal: repeated whenever a skill participates in packetized workers, subagent orchestration, MCP truth-source handling, or tool-use scoring and local evals need to stay compatible with `agent-tool-benchmark`
- current manual handling: keep `evals/evals.json` as the local acceptance layer, add a benchmark alignment section, map benchmark metrics into skill-local interpretations, then validate the JSON
- promotion target: reusable eval-layering checklist or benchmark-aware eval template for orchestration skills
- promotion trigger: another orchestration or tool-use skill needs benchmark-aligned local evals
- current proven examples: `skills/image-job-dispatcher/evals/evals.json`, `skills/image-worker/evals/evals.json`, `skills/image-result-auditor/evals/evals.json`, `skills/table-branch-activation-slice/evals/evals.json`

### Skill Factory Dispatcher

- recurrence signal: repeated whenever a repeated pattern should be promoted into a new skill or an existing skill should be expanded through packetized sidecar generation
- current manual handling: triage the pattern, choose new-versus-expansion, issue disjoint sidecar packets, keep shared files main-agent-owned, then integrate and smoke centrally
- promotion target: reusable `skill-factory-dispatcher` skill and sidecar packet bundle
- promotion trigger: another multi-skill promotion cycle uses the same packetized sidecar workflow
- current canonical inputs: `task_packets/standard/skill_creation_sidecar_standard_packet.json`, `task_packets/canonical/skill_creation_sidecar_canonical_packet.json`

### Ready-Arm Comparison Anchor Construction

- recurrence signal: repeated whenever a planned multi-arm experiment has only a subset of arms ready, but the currently runnable arms still need to be locked into a comparison-ready baseline before later arms arrive
- current manual handling: normalize the ready arms into a shared comparison record, write a bounded anchor manifest and report, and keep promotion state explicit instead of waiting for every planned arm to finish
- promotion target: reusable comparison-anchor builder or a standard packet for staggered multi-arm experiments
- promotion trigger: another experiment reaches a `subset ready / remainder pending` state and still needs a stable comparison baseline for later merge

### Context Package Adapter Reuse For New Caption Arms

- recurrence signal: repeated whenever a new caption arm needs richer evidence, but the existing caption runner surface should stay stable

### True Small-Batch Four-Mode Bundle Assembly From Shared Closure Set

- recurrence signal: repeated whenever a downstream comparison or auto-eval lane is ready, but only some images have every required arm closed
- current manual handling: inspect the shared image intersection, keep the consumer running on a `1-image template` if needed, and emit a waiver instead of overstating batch readiness
- promotion target: reusable shared-closure-set bundle assembler for multi-arm evaluation lanes
- promotion trigger: another experiment needs nonregenerative batch assembly from partially closed deterministic arms
- current proven example: `phase1` four-mode auto-eval consumed the `phase0` single-image frozen bundle because only `image11.png` had all four arms closed
- current manual handling: build a bounded adapter that reuses `context_package`, keep provenance and review state explicit, and inject only normalized enrichment artifacts rather than raw backend payloads
- promotion target: reusable adapter template or checklist for new caption-arm integration
- promotion trigger: another arm needs parser, OCR, review, or auxiliary evidence without widening the runner contract
- current proven example: parser/table-structure-enriched rerun via `scripts/parser_enriched_context_package_lib.py` and `scripts/build_parser_enriched_context_package.py`

### Read-Heavy Subagent Merge Audit With Single-Owner Finalization

- recurrence signal: repeated whenever arm-specific evidence is produced across sessions or workers and the main agent must merge the results without shared-file collisions
- current manual handling: give subagents read-heavy audit, parity-check, and normalization sidecars with disjoint write roots, while the main agent alone writes registries, final manifests, and canonical reports
- promotion target: reusable merge-audit packet set or orchestration skill for comparison-ready arm integration
- promotion trigger: another multi-arm comparison needs parallel audit and normalization, but final canonical outputs must remain single-owner

### Frozen Eval Bundle Generation For Deferred Judge Lane

- recurrence signal: repeated whenever a deterministic multi-arm comparison is ready before a semantic judge harness exists locally
- current manual handling: reuse the comparison runner, emit a read-only judge-input manifest plus a frozen eval bundle, then close the current lane with waiver and qualitative summary instead of pretending a local judge exists
- promotion target: reusable deferred-judge bundle checklist or evaluation-overlay packet
- promotion trigger: another bounded comparison becomes ready while the semantic judge consumer is still absent
- current proven example: phase-0 `4-mode` caption comparison on `image11.png`

### Reviewed Component Branch Reopen With Evidence-Backed Crop

- recurrence signal: repeated whenever a waived or blocked reviewed branch may be reopened because a semantically selected crop appears better than the full-image surface for one bounded task
- current manual handling: compare full-image and reviewed-crop OCR on the same expected token set, require explicit evidence that the reviewed crop removes noise without losing task-critical tokens, then run one bounded rerun on the reviewed crop surface
- promotion target: reusable reopen checklist or bounded packet for reviewed component branches
- promotion trigger: another reviewed component branch needs evidence-backed reopening rather than raw alpha-split promotion
- current proven example: reviewed isolated-component rerun closure on `image11.png`

### GPT Direct Image Verification For Reviewed Component Edge Cases

- recurrence signal: repeated whenever OCR-proxy evidence is too weak or too strict to close a reviewed component branch, but human pixel review is still disallowed
- current manual handling: run deterministic OCR/proxy first, escalate only the unresolved image pair to direct GPT image verification, then apply the verdict as a bounded promotion adapter instead of regenerating the arm
- promotion target: reusable direct-verification runner or escalation checklist for reviewed component edge cases
- promotion trigger: another reviewed crop remains visually strong while OCR proxy alone keeps it stuck in `pending_review`
- current proven example: `image10.png` moved from OCR-proxy false negative to `comparison_ready_reviewed_branch` through direct GPT image verification

### Dual-Input Consumer Normalization For Small-Batch Eval

- recurrence signal: repeated whenever a downstream consumer should keep running even if canonical aggregate freshness lags behind per-image frozen truth
- current manual handling: normalize input paths so the consumer can accept either aggregate bundle input or direct per-image bundle paths, then emit the actual resolved input mode into the regenerated artifact
- promotion target: reusable small-batch consumer input-normalization helper and contract
- promotion trigger: another auto-eval or judge lane must close while producer aggregate truth may still be drifting
- current proven example: `phase1` four-mode small-batch auto-eval regenerated from `image11/image7/image9` per-image bundles while also gaining aggregate-bundle input support

### Temporary Four-Arm Artifact Stabilization Into Workspace Canonical Truth

- recurrence signal: repeated whenever a useful `4-mode` image already has derived-arm artifacts, but they live under `/tmp`, imported scratch space, or otherwise noncanonical provenance that cannot be trusted as stable downstream truth
- current manual handling: copy or import the artifacts into a workspace-owned path, preserve provenance, regenerate the single-image comparison/eval bundle under canonical paths, then treat the imported image as part of the stable cohort
- promotion target: reusable stabilization/import helper for late-arriving four-arm images
- promotion trigger: another image reaches practical `4-mode` readiness from temporary or external artifacts before the workspace has canonicalized them
- current proven examples: `image10.png` stabilization from imported temp artifacts and later inclusion in the stable `phase1` cohort

### Late Cohort Expansion With Existing Builder Reuse

- recurrence signal: repeated whenever one more image reaches stable `4-mode` closure after a small-batch producer/consumer lane already exists, and the cohort should expand without rewriting the whole evaluation stack
- current manual handling: close the new image with existing per-image builders, append it into the current small-batch builder inputs, then regenerate aggregate bundle, consumer auto-eval, and corpus-ready artifacts from the same existing scripts
- promotion target: reusable `late cohort expansion` checklist or patch-first builder workflow
- promotion trigger: another image moves from excluded to stable-ready after the first batch was already declared canonical
- current proven examples: `image8.png` late inclusion into the stable `phase1` `4-mode` cohort using existing context, comparison, bundle, and auto-eval builders

### Canonical Truth Sync After Cohort Expansion

- recurrence signal: repeated whenever aggregate bundle or consumer truth changes after a late image inclusion, but closure report, master plan, artifact index, and session registry still describe the older cohort
- current manual handling: verify the new cohort size and winner counts from canonical manifests first, then patch closure/master-plan language and append missing image-specific paths into the domain artifact index and session registry
- promotion target: reusable post-expansion sync checklist for experiment truth surfaces
- promotion trigger: another bounded experiment widens its stable cohort after producer and consumer artifacts were already published
- current proven example: the `phase1` cohort moved from `4-image` to `5-image` truth after `image8.png` was frozen and required synchronized updates across closure docs and registries

### Multi-Component Reviewed Crop Recrop Candidate Selection

- recurrence signal: a reviewed branch has a valid parser-derived seed bbox, but nearby disconnected alpha components still contain title or context that should stay in the caption input surface
- current manual handling: keep the seed bbox as anchor, enumerate alpha components without promoting them directly, build a bounded `alpha_nearby_union` candidate, then score `seed_bbox` versus union candidates with the same OCR-proxy evidence surface
- promotion target: reusable reviewed-component recrop-candidate selector for multi-component images
- promotion trigger: another reviewed crop looks truncated even though a bounded nearby-component union is available
- current proven example: `scripts/reviewed_component_context_package_lib.py` now generates and evaluates `seed_bbox` and `alpha_nearby_union` candidates before selecting the final reviewed crop

### VS Code Markdown Surface Mode Switching

- recurrence signal: repeated whenever the same markdown workspace must alternate between a visual review surface and a text-authoring surface without leaving VS Code
- current manual handling: switch `workbench.editorAssociations` for `*.md`, reopen existing tabs when needed, then launch the workspace or file with `code`
- promotion target: reusable workspace-mode switch skill and launcher helper
- promotion trigger: another workspace or review workflow adopts the same `fabriqa + Foam + Text Editor` split surface
- current promoted surface: `skills/vscode-fabriqa-foam-workflow`

### Fast-Start Packet For Parallel Experiment Session Split

- recurrence signal: a bounded producer/consumer experiment split is ready, but each new session would waste time re-reading the full master plan before touching its narrow slice
- current manual handling: freeze the current slice truth, define fixed interpretation, split owned paths, and start each session from a narrow fast-start packet instead of from broad planning documents
- promotion target: reusable fast-start packet template for parallel experiment sessions
- promotion trigger: another producer/consumer split needs quick startup without repeated plan reconstruction
- current proven example: `image4` re-entry producer slice is packetized so another session can start from the current exclusion truth and recrop logic without re-reading the full experiment history

### Top-Level Consumer Provenance Projection For Eval Outputs

- recurrence signal: a downstream eval manifest already contains the right truth-source and summary, but only inside nested helper structures that make later consumers reopen the whole object model
- current manual handling: keep nested `input_resolution` and `batch_summary`, but also project the most important consumer-facing fields such as `actual_input_mode`, resolved bundle paths, winner frequency, and baseline retention to the top level
- promotion target: reusable top-level provenance projection rule for consumer-facing eval outputs
- promotion trigger: another consumer lane closes correctly but remains awkward to consume because its canonical JSON hides key provenance inside nested objects
- current proven example: `phase1` four-mode small-batch auto-eval was regenerated from canonical aggregate input and normalized with top-level input/provenance summary fields

### External Paper Cache For Edge-Case Solver Design

- recurrence signal: the codebase already has a partial local fix, but the remaining failure mode is architectural enough that implementation should pause until a small external paper set is cached and mapped to the open subproblem
- current manual handling: save a bounded paper set locally, record one manifest, then write one reference note that maps each paper to the still-open design question
- promotion target: reusable external-paper-cache workflow for bounded solver design
- promotion trigger: another edge case needs stable external references before opening a new implementation slice
- current proven example: `image4` composite-dashboard decomposition research cache saved papers for Docling, LayoutParser, PubTables-1M, DocLayout-YOLO, and compound-figure segmentation

### Control Action-Unit Migration With Inventory-Led Execution

- recurrence signal: repeated whenever a control-plane filesystem model changes, but the workspace cannot rely on ad hoc moves because many canonical reports, manifests, and references still point at the old layout
- current manual handling: write the decision first as ADR and rules, generate a machine-readable migration inventory, execute moves through a bounded migration script, then patch surviving references and publish an execution report
- promotion target: reusable control-tree migration packet plus inventory/apply script pair
- promotion trigger: another control-tree reshape changes the primary bucket model or depth sequence and requires coordinated path migration instead of one-off edits
- current proven example: 2026-03-30 migration from `control/*/runs` into `resources / registry / archive`

### Residual Registry Namespace Decomposition

- recurrence signal: repeated whenever a legacy registry namespace continues to exist after a primary migration, but the subtree actually mixes more than one registry role and should be split rather than retained as a generic bucket
- current manual handling: inspect the residual subtree, separate runtime-path metadata from job-ledger metadata into explicit registry homes, remove the leftover namespace, then update rules and path references to the new canonical homes
- promotion target: reusable residual-registry cleanup checklist and apply helper
- promotion trigger: another `registry/*` subtree survives a migration only because multiple meanings were temporarily parked under one ambiguous directory
- current proven example: `control/project_agent_ops/registry/runs/` decomposed into `registry/runtime/` and `registry/jobs/`

### Post-Migration Active Path Repair And Revalidation

- recurrence signal: repeated whenever a structural migration succeeds mechanically, but active tests, task packets, specs, or experiment plans still hardcode the old canonical paths and therefore fail or misreport readiness
- current manual handling: search only active surfaces, patch the remaining old paths, rerun the smallest bounded tests that prove the runtime now follows the new layout, then keep historical migration reports untouched as evidence
- promotion target: reusable post-migration readback-and-revalidation checklist
- promotion trigger: another control or runtime path migration leaves a small but active residue across tests, task packets, or specs after the bulk move already succeeded
- current proven example: 2026-03-30 path repairs across issued task packets, caption specs, experiment plans, and the `test_caption_arm_comparison_lib.py` / `test_four_mode_small_batch_auto_eval_lib.py` pair

### Master-Plan Overlay Split With Redirect Stub Preservation

- recurrence signal: repeated whenever a stable plan surface and a user-facing progress surface are initially drafted together, then need to be separated without breaking old references
- current manual handling: keep the stable plan or draft in `control/project_domain/resources/master_plans/`, move the user-facing overlay into `control/user_decisions/resources/notes/`, and leave a short `## Moved` redirect stub in the old location only when path continuity still matters
- promotion target: reusable master-plan overlay split checklist plus redirect-stub template
- promotion trigger: another dashboard, scoreboard, task graph, or current-state snapshot is found inside `master_plans`
- current proven example: the progress dashboard and task-graph overlays for the presentation image pipeline were split out of `master_plans` on 2026-03-30

### Multi-Agent Document Placement Audit Before Canonical Moves

- recurrence signal: repeated whenever a document bucket is semantically ambiguous enough that one agent's local intuition could misfile canonical bodies
- current manual handling: fan out multiple bounded readers, collect keep/move verdicts for the candidate files, then only move the small set of files whose role is consistently classified
- promotion target: reusable subagent-backed placement-audit packet for control-plane migrations
- promotion trigger: another workspace cleanup needs high-confidence canonical placement rather than ad hoc relocation
- current proven example: the 2026-03-30 audit used 10 subagents to verify that actual plan documents stay in `master_plans` while decision-support overlays move to `user_decisions/resources/notes`
### Projection-Profile Component Decomposition Probe For Compound Dashboards

- recurrence signal: a chart-table composite remains blocked because reviewed recrop still needs a parser seed, and the next useful question is whether deterministic decomposition can surface title/chart/lower-summary regions at all
- current workaround: run a bounded projection-profile decomposition probe and emit a manifest with regroupable candidates before escalating to heavier semantic selection
- structural fix candidate: first-class decomposition manifest generator for compound dashboards
- current proven example: `image4` decomposition probe surfaced `title_block`, `chart_region`, and `table_like_region`

### Objective-Profile Scoring For Regrouped Component Candidates

- recurrence signal: decomposition and regrouping already produced plausible candidates, but the system still needs an explicit way to separate dashboard-overview intent from table-focus intent
- current workaround: score regrouped candidates under one current objective profile and one contrast profile before any re-entry or promotion decision
- structural fix candidate: objective-profile scoring stage between regrouping and selection
- current proven example: `image4` scoring distinguished a dashboard-overview winner from a table-focus winner

### Aggregate Bundle To Human Review Surface Flattening

- recurrence signal: repeated whenever a corpus-level aggregate bundle is machine-readable and evaluation-ready, but a human reviewer still needs one portable markdown surface with embedded images, default-vs-winner separation, and per-image promotion cues
- current manual handling: read the aggregate bundle, join per-image auto-eval winner data, copy source images into a bounded review asset directory, then emit one review markdown plus one review-surface manifest
- promotion target: reusable corpus-review-surface builder for aggregate bundle inputs
- promotion trigger: another batch or corpus closure needs a human-facing review artifact without regenerating any caption arms
- current proven example: the 2026-03-30 phase-2 four-mode corpus review surface built from the 9-image corpus ready bundle and corpus auto-eval manifest

### Review Surface Manifest To Retrieval Preflight Bridge

- recurrence signal: a human-facing review surface already exists, but downstream retrieval and mapping work still needs machine-readable seeds and a preflight contract without reopening markdown or re-deriving review state
- current manual handling: treat the review manifest as the only machine truth, then project it into one decision seed, one retrieval input seed, one mapping review seed, and one preflight summary manifest/report
- promotion target: reusable review-manifest-to-preflight bridge for downstream consumer preparation
- promotion trigger: another corpus or bounded batch closes on a review surface and the next lane needs human decision capture plus retrieval-ready placeholders without touching upstream bundle truth
- current proven example: the 2026-03-30 `phase2` corpus review surface was bridged into decision, retrieval, mapping, and preflight artifacts for `Session B`

### Review Decision Ingestion To Ready Subsets

- recurrence signal: a structured human review decision seed already exists, but downstream retrieval or mapping work still needs a deterministic ingestion pass that materializes only the completed and eligible rows
- current manual handling: read the decision JSONL, filter retrieval-ready and mapping-ready rows, then emit one ingestion manifest, two ready-subset JSONLs, and one report
- promotion target: reusable review-decision ingestion stage between human decision capture and downstream execution
- promotion trigger: another review-driven workflow needs to hold downstream execution until completed rows exist while still preserving a machine-readable empty-ready state when everything is pending
- current proven example: the 2026-03-30 `phase2` corpus decision ingestion emitted zero ready rows from the all-pending seed and recorded the explicit rerun trigger

### Zero-Ready Downstream Dry-Run Contract

- recurrence signal: human review is still pending, but the workspace must already freeze the next retrieval or mapping runtime contract without starting execution
- current manual handling: read the decision-ingestion manifest plus the ready-subset JSONLs, then emit retrieval and mapping dry-run manifests with explicit `ready_to_execute` and `blocked_reason`
- promotion target: reusable downstream dry-run contract stage between decision ingestion and actual execution
- promotion trigger: another review-gated pipeline needs to keep moving while human completion is pending and must expose exact next runtime inputs without pretending execution already started
- current proven example: the 2026-03-30 `phase2` dry-run manifests recorded zero-ready retrieval and mapping states with stable blocked reasons

### Machine-Prefilled Review-Seed Drift Validation Before Ingestion

- recurrence signal: a human-edited decision seed inherits machine-prefilled fields from an upstream review surface, but ordinary JSONL editing leaves those copied fields vulnerable to silent drift until much later consumers fail
- current manual handling: treat the review surface as canonical machine truth, compare seed row order and immutable prefills against that surface at ingestion time, and fail immediately on any mismatch
- promotion target: reusable pre-ingestion drift validator for machine-prefilled decision seeds
- promotion trigger: another operator workflow copies machine truth into editable rows and needs an immediate guardrail before ready-subset materialization
- current proven example: the 2026-03-30 `phase2` review-decision ingestion now rejects edited seed rows when `comparison_winner`, `bundle_path`, priority order, or related prefills diverge from the review-surface manifest

### Single-Writer Canonical JSONL Review Entry With Owned-Row Split

- recurrence signal: a canonical JSONL is intentionally kept as the one writable decision surface, but multiple reviewers may need to work in parallel and can otherwise collide by editing the same file concurrently
- current manual handling: define the canonical seed as one-active-writer-only, require owned image ids or reviewer-local working copies when more than one reviewer participates, then merge before ingestion
- promotion target: reusable single-writer-plus-owned-row entry rule for human decision seeds
- promotion trigger: another review workflow keeps one canonical JSONL for simplicity but introduces more than one human reviewer or delegated editor
- current proven example: the 2026-03-30 `phase2` caption review decision entry guide and checklist now declare one active writer on the canonical seed and require owned-image coordination for any multi-review case

### Human-Edited Caption Arm Exception Normalization

- recurrence signal: a review contract mostly tracks existing caption arms and their promotion states, but one operator path introduces a synthetic `human_edited_caption` arm that no longer maps to the ordinary promotion-state enum
- current manual handling: document and validate the exception explicitly so `selected_caption_arm = human_edited_caption` forces `selected_caption_promotion_state = null` and `caption_edit_required = true`
- promotion target: reusable synthetic-arm exception rule for decision-capture contracts
- promotion trigger: another review or approval surface allows edited text as a first-class selection option even though the edited result is not a promoted upstream arm
- current proven example: the 2026-03-30 `phase2` corpus review decision capture contract and operator guide now treat `human_edited_caption` as a null-promotion-state exception instead of overloading existing arm-state semantics

### Warning-Only Structure Lint Before Hard Gating

- recurrence signal: the control-tree philosophy is agreed on, but enforcement still depends on human memory and ad-hoc code review instead of visible automated feedback
- current manual handling: add warning-level lint first, wire it into the normal maintenance flow, then trim false positives before considering strict failure
- promotion target: reusable staged-structure-lint rollout pattern for canonical control-plane repos
- promotion trigger: another workspace adopts a refined structure contract and needs mechanical feedback without blocking active migration or cleanup work
- current proven evidence: `vscode-markdown-review-surface/scripts/lint_repo_layout.py` started as warning-only, then got a false-positive trimming pass before stronger enforcement

### Old-Root Drift Scan With Context Allowlist

- recurrence signal: a new workspace or copied skill tree is migrated to a new repo root, but some docs intentionally mention the previous root during migration or audit while others accidentally keep stale absolute paths
- current manual handling: scan for old-root strings repo-wide, but allow migration/checklist/report contexts and warn only when the old root survives in active canonical docs or copied runtime references
- promotion target: reusable old-root drift audit pattern with explicit allowlist categories
- promotion trigger: another workspace fork or repo extraction needs stale path cleanup without drowning operators in intentional migration references
- current proven evidence: `vscode-markdown-review-surface/scripts/lint_repo_layout.py` now skips migration-like paths but is ready to flag unexpected `my-image-parser` root references elsewhere

### Lint Baseline Split Before Cleanup Execution

- recurrence signal: lint output is too large to act on directly, so operators need a stable split between inherited legacy debt and currently actionable structural violations
- current manual handling: capture one baseline report that buckets findings into legacy debt, evidence-placement debt, active structural violations, and other active contract drift before starting cleanup
- promotion target: reusable lint-baseline triage template for noisy control-plane repos
- promotion trigger: another repo accumulates enough lint noise that cleanup work risks mixing archive inheritance with true active regressions
- current proven evidence: `REPORT_control_tree_lint_baseline_split-at2026-03-30.md` now separates `my-image-parser` lint findings into actionable lanes

### Evidence To Normalized Review Surface Layering

- recurrence signal: repeated whenever image-first evidence must be turned into a human-reviewable surface without losing the machine-readable comparison contract
- current manual handling: keep the image as raw evidence, add a short normalized observation layer, then render separate comparison and decision fields such as `current default`, `winner`, `promotion state`, and `why default stays default`
- repeated invariant: do not let the same sentence carry all of `what is visible`, `what changed`, and `what should be adopted`; split those into separate fields even when the final markdown card looks compact
- repeated invariant: preserve a stable identity chain from image payload -> item id -> row/card id -> manifest record so the same judgment can be re-read later without guessing which image slice the prose referred to
- repeated invariant: observation text should stay short and fact-like; evaluative language belongs in comparison/decision fields, not in the evidence description itself
- promotion target: reusable multimodal review-surface contract or builder helper for image-plus-text decision workflows
- promotion trigger: another image-heavy or diagram-heavy review flow again needs `evidence -> normalized text -> comparison -> decision` layering instead of ad-hoc prose
- current proven evidence: the phase-2 caption corpus review surface and the VS Code review surface both converged on image evidence plus explicit normalized decision fields

### Human-Facing Markdown Versus Machine-Truth Manifest Split

- recurrence signal: repeated whenever the same review flow must satisfy both human judgment and downstream machine consumers without letting prose re-interpret structured truth
- current manual handling: emit a human-facing markdown/card surface for review, then emit a separate manifest that becomes the machine truth source and carries priority, default/winner split, and status fields explicitly
- repeated invariant: markdown may be richer, more visual, and reordered for readability, but it must not invent fields that the manifest cannot carry or silently merge fields that the manifest keeps separate
- repeated invariant: machine consumers should be able to ignore prose safely; if a downstream consumer must scrape explanation paragraphs to recover winner/default/status, the split is not clean enough
- repeated invariant: the manifest should own canonical order, ids, and state labels; markdown should be treated as a projection over those canonical fields
- promotion target: reusable dual-output review artifact pattern for multimodal decision pipelines
- promotion trigger: another surface or review stage needs both portable prose and deterministic downstream consumption from the same bounded run
- current proven evidence: `phase2` caption review uses markdown for human review and a manifest for downstream decision ingestion and dry-run consumers

### Baseline-Winner-Default Decision Card Repetition

- recurrence signal: repeated whenever comparison results are reviewed by humans and a single card or row must make baseline retention, winner selection, and promotion status legible at a glance
- current manual handling: always repeat the same per-item card schema with baseline/default, winner, promotion state, and reason fields instead of free-form mixed prose
- repeated invariant: keep baseline/default visible even when the winner looks obviously better, because the policy state often lags the comparison outcome
- repeated invariant: make the `reason` field explain baseline retention or deferment, not merely restate that a winner exists
- repeated invariant: if the item is unresolved, the card should degrade into a pending/ambiguous contract rather than pretending to be a final decision card
- promotion target: reusable decision-card schema for multimodal review surfaces
- promotion trigger: another comparison or evaluation surface risks hiding baseline retention logic inside narrative text rather than a stable row/card contract
- current proven evidence: phase-2 corpus review and related decision-support notes required explicit `default vs winner` separation to remain readable and machine-consistent

### YAML Verb-Noun Routing Hardening For Owner Families

- recurrence signal: repeated whenever a skill family tries to separate owner entrypoints from consumer specialists using YAML descriptions, but broad verbs such as `route`, `reconcile`, or `maintain` still risk over-triggering without an equally explicit noun boundary
- current manual handling: tighten the owner YAML description to the primary charter noun scope, add a family-map self-check that requires both owner-output contact and the correct owned noun, and mark non-primary surfaces as `temporarily routed` instead of letting them read as canonical owner scope
- repeated invariant: pre-routing must be possible from description verbs plus noun boundary before the body is read; if the body is required to discover that a tool is only adjacent or convention-routed, the YAML contract is still too loose
- repeated invariant: consumer specialists should keep narrow execution verbs such as `run`, `extract`, `export`, or `build`, while owner entrypoints should keep lifecycle verbs such as `reconcile`, `maintain`, `verify`, or `align`
- promotion target: reusable owner-family routing hardening pattern for skill ecosystems that mix owner entrypoints, temporarily routed adjacent surfaces, and direct-call specialists
- promotion trigger: another skill family starts to route incorrectly because YAML descriptions are broad enough to blur `canonical owner` and `consumer specialist` behavior
- current proven evidence: the 2026-04-01 `vendored-mcp-onboarding` family docs had to narrow the charter to `vendored third-party MCP` scope, add a verb/noun self-check, and label adjacent non-vendored surfaces separately

### Consumer Specialist Backlink Maintenance

- recurrence signal: repeated whenever an owner-family skill's charter is clarified and the adjacent consumer specialists' SKILL.md files must be updated to reflect the new routing contract without duplicating the same routing sentence in multiple sections
- current manual handling: add a short one-line routing backlink to `Do Not Use This Skill When` for discoverability, and replace any long routing prose in `Not Owned Here` with a noun phrase only; apply consistently across all consumer specialists in the same family in one pass
- repeated invariant: one location carries the routing verb (the `Do Not Use This Skill When` line), the other carries only the noun (the `Not Owned Here` entry); duplicating the full routing sentence in both sections creates wording drift between them on subsequent passes
- repeated invariant: the backlink must name the owner skill explicitly so a reader who starts at the consumer specialist can navigate to the owner without reading the family map
- promotion target: reusable consumer backlink normalization pass, callable whenever an owner skill's charter changes
- promotion trigger: more than two consumer specialists need their routing sections updated in the same pass, or a reviewer reports that they could not find the owner skill from a consumer entry point
- current proven evidence: `macos-ocr-evidence`, `component-split-ocr-review`, and `openai-image-caption-validation` all received normalized backlinks pointing to `vendored-mcp-onboarding` during the 2026-04-01 owner-family hardening pass

### Owner-Family Routing Status Enum Hardening

- recurrence signal: repeated whenever an owner-family skill set needs a shared vocabulary for classifying surfaces as canonical, adjacent-but-routed, or consumer-only, and that vocabulary must remain consistent across the family map, routing decision tree, quick pre-routing check, and YAML descriptions
- current manual handling: define exactly three enum values, write a legend that explains each value in terms of the *surface* (not the skill), and ensure every location that uses these values refers to the same short string; use longer explanatory phrases only in the legend, never in the cells or tree branches
- repeated invariant: the enum must be strictly 3 values; adding a 4th value such as `canonical + note` immediately breaks consistency because some docs adopt it and others do not
- repeated invariant: enum values are surface descriptors, not skill role labels; a consumer skill row can have `canonical` because its primary surface is a vendored MCP, without that meaning the skill itself is a canonical owner
- promotion target: reusable 3-value routing-status enum pattern for any skill family that mixes owner, adjacent, and consumer layers
- promotion trigger: another skill family needs a shared routing classification and risks inventing ad-hoc labels that diverge across its documents
- current proven evidence: the `vendored-mcp-onboarding` family map stabilized on `canonical` / `temporarily routed adjacent` / `consumer-only` during the 2026-04-01 hardening pass after two rounds of 4-value drift

### Lifecycle-Surface-First Routing Tree Rewrite

- recurrence signal: repeated whenever a routing decision tree starts with a domain-specific or tool-type-specific question such as `Task involves an MCP?` but the owner skill's actual scope has been broadened to include non-vendored adjacent surfaces and consumer-only paths that do not involve that tool type
- current manual handling: rewrite the tree root as `Task involves a tool lifecycle surface?` and split the first-level branches by ownership class (`canonical` / `temporarily routed adjacent` / `consumer-only`) rather than by tool type; add a lifecycle-touch gate to each non-consumer branch so that tool *usage* does not route to the owner
- repeated invariant: a routing tree that starts with a domain-type gate (MCP? filesystem? imagegen?) does not survive scope expansion because each new adjacent surface requires modifying the gate itself rather than adding a branch
- repeated invariant: both the canonical branch and the adjacent branch must carry a lifecycle-touch gate condition; a branch without a gate becomes a catch-all for consumer usage of that surface type
- promotion target: reusable lifecycle-surface-first routing tree template for owner-family skills with mixed surface types
- promotion trigger: a routing tree's first question no longer accurately filters because the owner skill has grown to include surfaces that the original gate type does not cover
- current proven evidence: the `vendored-mcp-onboarding` routing tree was rewritten from `Task involves an MCP?` to `Task involves a tool lifecycle surface?` with three branches and lifecycle-touch gates on both vendored and adjacent branches during the 2026-04-01 pass

### Cross-Workspace Semantic Owner Family Enrollment

- recurrence signal: repeated whenever my-image-parser execution skills must declare handoff to semantic owner skills that live in claude-gemini-communicator, requiring coordinated YAML description narrowing + Not Owned Here handoff + reverse ecosystem routing
- current manual handling: conservative line-by-line patch across 4+ rounds: first body handoff, then YAML verb narrowing, then handoff placement unification, then bidirectional ecosystem closure
- repeated invariant: specialist descriptions use only execution verbs (`run / extract / export / build / render / operate / audit`); owner verbs (`reinject / refine / compare / close / normalize / derive`) stay in the owner skill only
- repeated invariant: forward handoff goes in `Not Owned Here` (not `Do Not Use`); reverse routing goes in owner `Ecosystem`
- promotion target: reusable cross-workspace owner enrollment checklist with verb taxonomy validation
- promotion trigger: another set of execution skills needs to join an owner family across workspaces
- current proven evidence: `openai-image-caption-validation`, `obsidian-caption-review-builder`, `component-split-ocr-review`, `macos-ocr-evidence`, `vscode-fabriqa-foam-workflow` all enrolled into `multimodal-evidence-refinement-loop` / `image-text-cot-review` family during 2026-04-02 session

### Iterative YAML Description Verb Narrowing For Owner Family Membership

- recurrence signal: repeated whenever a specialist skill's YAML description is narrowed to fit an owner family taxonomy but residual broad verbs survive across review rounds
- current manual handling: 2~4 rounds of description-only patches, each catching verbs or nouns missed in the previous round; body edits deferred until YAML is stable
- repeated invariant: each round touches only the frontmatter `description:` line; body, script, output, workflow remain unchanged
- repeated invariant: `semantic selection`, `inspection artifact`, `review surface` (as ownership claim), `final understanding`, `machine truth` are removed from specialist descriptions and reserved for owner skills
- promotion target: verb taxonomy checklist applied before any new owner family enrollment
- promotion trigger: if a review round still finds owner-level verbs after 2+ narrowing passes on the same file
- current proven evidence: `component-split-ocr-review` needed 3 description rewrites to remove `review surface`, `inspection artifact`, `semantic selection`; `macos-ocr-evidence` and `vscode-fabriqa-foam-workflow` each needed 2 passes

### Full-Taxonomy Band Audit With Standalone Triage

- canonical source: `claude-gemini-communicator/skills/Skills-Create-Project/skill-creation-process/references/repeated-task-and-issue-patterns-at2026-03-19-13-34.md` Task 19 protocol + Task 21
- imported from: claude-gemini-communicator skill-creation-process references
- last synced: 2026-04-03
- recurrence signal: repeated whenever all owner bands are closed and remaining unassigned skills must be triaged as truly standalone or hidden family candidates
- current manual handling: glob all SKILL.md, subtract known band members, read each remaining YAML, apply Task > Action > Verb > Noun, document adjacency risks, update canonical band reference with Standalone Skills section
- repeated invariant: adjacency risk (same noun/tool, different task/audience) is documented but does not trigger reclassification unless task overlap is confirmed
- promotion target: reusable standalone triage checklist appended to the family closure audit protocol
- promotion trigger: another all-band audit cycle produces unassigned skills that need the same triage
- current proven evidence: `tmux-controller` ↔ `codex-tmux-orchestrator` (same tmux, different audience), `langfuse-codex-prompt` ↔ `agent-tool-benchmark` (eval score adjacency, different scope) — both confirmed standalone during 2026-04-02 session

### Owner Body Guardrail Backfill After YAML-First Editing

- canonical source: `claude-gemini-communicator/skills/Skills-Create-Project/skill-creation-process/references/repeated-task-and-issue-patterns-at2026-03-19-13-34.md` Task 19 substep 19a
- imported from: claude-gemini-communicator skill-creation-process references
- last synced: 2026-04-03
- recurrence signal: repeated whenever YAML description and routing are complete but the owner body still lacks Family Roles, Do not use, and Workflow sections needed for family closure
- current manual handling: insert 3 sections in one pass after YAML is stable — Family Roles → Do not use → Workflow order
- repeated invariant: Do not use routes to specialist direct-calls when specialists exist, or to cross-band skills when standalone; Workflow is action sequence, distinct from Read order (knowledge loading order)
- promotion target: post-YAML body guardrail checklist integrated into closure protocol
- promotion trigger: another owner skill passes YAML audit but fails closure item 3 and 6 due to missing body sections
- current proven evidence: Band 4 (codebase-analysis), Band 6 (artifact-lifecycle-manager), Band 8 (multimodal-evidence-refinement-loop) all had the same 3-section gap during 2026-04-02 closure

### Minute-Level Timestamp Backfill For User-Facing Note Sets

- recurrence signal: repeated whenever a workspace adopts a stricter `-atYYYY-MM-DD-HH-MM` naming rule after a body of user-facing notes was already created with day-only timestamps or mixed timestamp spellings
- current manual handling: audit the target note set as one migration unit, derive missing `HH-MM` from the least-wrong local evidence source (currently file `mtime` in local timezone), rename the full set in one pass, then update markdown references, JSON manifests, and any exported aliases together
- repeated invariant: rule adoption without backfill is incomplete; warning-only lint is useful first, but the workspace remains drifted until filenames, references, and export manifests are normalized to the same timestamp contract
- repeated invariant: mixed spellings such as `-at2026-04-05-09-17` and `-at-2026-04-05-09-17` must be normalized in the same pass; leaving both forms alive creates a second wave of drift after the initial migration
- promotion target: reusable filename-backfill migration recipe for user-facing notes that couples rename, reference replacement, and export regeneration
- promotion trigger: another directory of user-facing notes adopts minute-level timestamps after files already exist under a day-only or malformed timestamp contract
- current proven evidence: on 2026-04-05, `control/user_decisions/resources/notes/` in `my-image-parser` was normalized from mixed day-only and malformed `-at-YYYY...` names to a consistent `-atYYYY-MM-DD-HH-MM` pattern, with references and symbolic links updated in the same pass

### Directory-First User-Facing Symbolic Link Export

- recurrence signal: repeated whenever user-facing artifacts must be exposed into an external reading location and naive file-by-file symlink creation begins to sprawl or lose readability across multiple workspaces
- current manual handling: declare a manifest with workspace-prefixed alias names, sync directory symlinks as the default export surface, and create file-level symlinks only for explicitly requested spotlight documents; clean up legacy plain aliases in the same sync step
- repeated invariant: directory links are the canonical export unit for browsing; file links are exceptions for explicit spotlighting, not the baseline export strategy
- repeated invariant: alias names should include the workspace name so a reader looking across multiple workspaces can identify provenance without opening the target first
- promotion target: reusable manifest-driven export pattern for user-facing artifacts that distinguishes default directory export from explicit file spotlighting
- promotion trigger: another workspace wants to expose decision-support notes/reports through a shared `Symbolic_links` directory without relying on hidden hook side effects
- current proven evidence: on 2026-04-05, `my-image-parser` adopted `my-image-parser__user_decisions__notes` and `my-image-parser__user_decisions__reports` as default exported directories, while keeping only one explicit file spotlight symlink for the surface model reference

### Cross-Workspace Implementation Reference Deduplication

- recurrence signal: repeated whenever a decision-support workspace keeps a copied reference whose canonical implementation-oriented version lives in a sibling implementation workspace, and the duplicate copy begins to drift or no longer carries unique local value
- current manual handling: compare the decision-space copy and the implementation-space copy directly, verify whether the decision-space workspace still has live inbound references to the local copy, then delete the duplicate if the implementation copy already carries the canonical implementation framing
- repeated invariant: decision-space notes should not retain implementation references merely as convenience copies once a clear canonical implementation home exists elsewhere; duplicated copies silently fork over time
- repeated invariant: deletion is safe only after checking residual local references and confirming that the surviving copy still serves the intended reread purpose from its canonical workspace
- promotion target: reusable cross-workspace duplicate-reference pruning rule for paired decision-support and implementation workspaces
- promotion trigger: a user-facing workspace accumulates copied references whose canonical home clearly belongs to a sibling implementation repo
- current proven evidence: on 2026-04-05, `my-image-parser/control/user_decisions/resources/notes/REFERENCE_obsidian_vscode_surface_orchestration-*` was removed after verifying that the canonical implementation reference already lived under `vscode-markdown-review-surface/control/project_domain/resources/references/`

### Cross-Workspace Surface Document Re-Anchor Before Freeze

- recurrence signal: repeated whenever a bounded surface-delivery document is conceptually about the implementation workspace, but the first written draft or plan patch lands in the consumer or truth-owner workspace because both are active in the same session
- current manual handling: restate implementation owner versus truth owner, remove the misplaced draft from the wrong workspace, then recreate the same bounded interpretation under the implementation workspace only
- repeated invariant: cross-workspace surface planning must freeze under the implementation workspace; the consumer workspace may reference the surface but should not own its implementation planning document
- repeated invariant: if a misplaced document was already written, deletion or rollback in the wrong workspace happens before the correct copy is recreated
- promotion target: reusable workspace-owner re-anchor checklist for cross-workspace surface planning
- promotion trigger: another surface-delivery or adapter-plan document is drafted under the consumer workspace before the implementation-owner boundary is rechecked

### Evidence-First Documentation Freeze

- recurrence signal: repeated whenever teams want to save design or staffing documents early, but the stable interpretation really depends on runtime evidence, smoke, or validator output that has not closed yet
- current manual handling: keep provisional reasoning in session context, gather runtime and validator evidence first, then freeze result, reference/KB, master plan, and checklist in that order
- repeated invariant: bottom-up validation precedes top-down documentation freeze
- repeated invariant: operator or architect notes may guide ongoing work, but canonical freeze waits until the slice is evidence-backed
- promotion target: reusable documentation-freeze protocol for multi-agent implementation slices
- promotion trigger: another bounded slice reaches planning saturation before evidence closure and risks freezing volatile conclusions into canonical docs

### Architect-First Integration Ownership With Builder Read Gates

- recurrence signal: repeated whenever the hardest slice touches a dense integration seam and broad builder fanout would create collisions unless one architect-origin builder owns the seam first
- current manual handling: assign the architect-origin builder to the hardest integration slice, require other builders to read the relevant plan, KB/reference, contract/spec, and current target code before coding, then dispatch only disjoint implementation slices
- repeated invariant: builder start is gated by bounded architecture reading, not just packet receipt
- repeated invariant: broad builder fanout waits until module boundaries and owned paths are explicitly cut
- promotion target: reusable builder start-gate and integration-owner dispatch packet
- promotion trigger: another host-heavy surface needs many builders but still has a centralized integration seam that cannot safely be edited by everyone at once

### Code-State-First Recovery After Agent Disconnect

- recurrence signal: repeated whenever network instability or agent/session loss makes worker status unreliable, but the codebase may already contain partial or completed work from one or more lanes
- current manual handling: ignore session-level assumptions, inspect the actual target files, rerun the key validation commands directly, and classify each lane as `missing`, `partially materialized`, or `verified` before any relaunch
- repeated invariant: recovery starts from repository state, not from agent summaries or orchestration status
- repeated invariant: relaunch only the lanes with missing or unverified artifacts; do not restart already-verified lanes just because their sessions disappeared
- promotion target: reusable recovery protocol for interrupted multi-agent waves in unstable network conditions
- promotion trigger: another multi-agent slice loses worker sessions or orchestration visibility before all lanes have reported clean completion
- current proven evidence: during the 2026-04-05/06 `vscode-markdown-review-surface` caption-surface buildout, subagent disconnects were handled by checking actual seam files (`mode-router`, `webview-protocol`, `webview-html`, `webview-client`, later `webview-render-sync` split files), rerunning `npm run check` and `npm test`, then only relaunching the host/render lanes that had not yet materialized

### Sequential Architect Seam Waves Before Reduced Fanout

- recurrence signal: repeated whenever a centralized host and client monolith is too coarse for safe parallelization, but can be made parallel-safe through several behavior-preserving extraction waves
- current manual handling: run repeated architect-only seam waves, validate after each wave, and promote only the verified seams into the next staffing decision; stop the sequence as soon as reduced fanout becomes safe
- repeated invariant: each architect wave must shrink a real hotspot and produce repo-owned extraction points, not just rename existing code
- repeated invariant: staffing conclusions are recomputed after every validated wave; they are not predetermined from the original architecture sketch
- promotion target: reusable pre-fanout architect-wave protocol for host-heavy extensions or custom-editor surfaces
- promotion trigger: another codebase has one or two monolithic files that block safe path ownership, but the hotspot can be reduced through staged extraction
- current proven evidence: the `vscode-markdown-review-surface` caption-surface effort required three verified architect waves: first message/mode seams, then webview HTML/client extraction, then client concern splitting (`webview-render-sync`, `webview-wikilinks`, `webview-sidecar`) before reduced fanout was judged safe

### Reduced-Fanout Packet Launch After Verified Seams

- recurrence signal: repeated whenever full staffing is still unsafe, but a smaller number of disjoint work packets becomes viable after a few validated extraction waves
- current manual handling: define only the currently safe lanes, validate packet schema and owned-path disjointness, issue the packets, and launch a reduced subset of builders rather than waiting for the full target staffing model
- repeated invariant: reduced fanout is an intermediate operating mode, not a failure to reach the final staffing target
- repeated invariant: packet issuance happens only after seam validation has been written down and the owned paths are narrow enough to explain concretely
- promotion target: reusable reduced-fanout dispatch pattern for slices that are no longer single-owner but are not yet full-parallel-safe
- promotion trigger: another slice reaches a state where 3-6 lanes are safe but full 10+ lane dispatch is still too collision-prone
- current proven evidence: after three architect waves on 2026-04-06, `vscode-markdown-review-surface` moved from architect-only work to a four-lane reduced fanout (`host`, `render`, `contract/session-config`, `feedback-ledger`) rather than jumping directly to a 12-agent restart

### Partial-Lane Validation Before Selective Relaunch

- recurrence signal: repeated whenever some builder lanes appear to have completed materially while sibling lanes failed or disconnected, creating a mixed success surface that is easy to over-restart
- current manual handling: validate successful-looking lanes first by reading their files and rerunning the shared checks, then close those lanes conceptually and relaunch only the empty or unverified lanes
- repeated invariant: a lane that already produced valid code and passed shared checks should be treated as completed work even if the originating agent did not deliver a clean final summary
- repeated invariant: selective relaunch lowers repeated merge churn and avoids redoing working code under unstable network conditions
- promotion target: reusable mixed-lane recovery rule for multi-agent implementation bursts
- promotion trigger: another reduced-fanout or broad fanout wave finishes with some concrete artifacts present and other lanes entirely missing
- current proven evidence: in the 2026-04-06 reduced-fanout wave for `vscode-markdown-review-surface`, the `contract/session-config` and `feedback-ledger` files materialized while `host` and `render` files did not; the safe recovery path was to verify the materialized lanes first and only then relaunch the missing ones

### Conservative Multi-Stage Recovery Closure Before Feature Resume

- recurrence signal: repeated whenever a feature slice is interrupted by repo-state incidents such as restored documentation trees or session loss, and the team needs to resume work without accidentally layering new feature changes on top of stale structural drift
- current manual handling: recover in ordered stages: inspect current code state, audit restored control artifacts, patch narrow structural drift, rerun layout lint, rerun type/check commands, rerun smoke/tests, and only then reopen the next feature wave
- repeated invariant: recovery closure is not a single patch; it is a staged gate with multiple validation passes
- repeated invariant: feature continuation is deferred until structural drift and command-path instability are both re-validated
- promotion target: reusable recovery-first continuation protocol for interrupted bounded feature slices
- promotion trigger: another implementation slice is paused by accidental directory restoration, session interruption, or mixed repo/document drift before the next feature wave starts
- current proven evidence: on 2026-04-06, `vscode-markdown-review-surface` resumed the user-evaluation-surface effort only after auditing restored `control/` state, patching layout drift, rerunning `lint_repo_layout.py`, `npm run check`, and `npm test`, and then freezing the result in a validation reference

### Behavior-Preserving Seam Completion Under Recovery Gate

- recurrence signal: repeated whenever pending architect-owned seam work still needs to land during a recovery window, but the team must avoid widening semantics while the repo is being normalized
- current manual handling: finish only behavior-preserving extractions that reduce known hotspots, keep product semantics unchanged, and validate the extracted seams before any new user-facing surface behavior is attempted
- repeated invariant: seam completion during recovery is allowed only if it narrows hotspots without changing the active product contract
- repeated invariant: recovery-time refactors must end in smaller, repo-owned modules with passing checks, not just moved code
- promotion target: reusable rule for letting architecture cleanup continue safely inside a recovery-first phase
- promotion trigger: another recovery window still contains unfinished seam packets that are required for later feature work but can be closed without expanding feature scope
- current proven evidence: during the 2026-04-06 recovery closure in `vscode-markdown-review-surface`, `host-document-state`, `host-sidecar-store`, `webview-markdown-render`, and `webview-selection-sync` were added to close `HOST` and `RENDER` seams without yet starting the actual caption-evaluation slide feature

### Smoke-First Harness Stabilization Before Declaring Recovery Closed

- recurrence signal: repeated whenever structural recovery looks complete in source code, but command-path smoke remains flaky enough that the team cannot tell whether the next blocker is real product work or leftover harness instability
- current manual handling: treat smoke repair as part of recovery, fix teardown and command-path assumptions first, and do not declare recovery closed until smoke reflects the current stable host behavior
- repeated invariant: source refactors alone do not close recovery if the main smoke path still times out or asserts on stale assumptions
- repeated invariant: bounded no-op or narrower smoke coverage is acceptable during recovery when it removes false negatives without hiding product-relevant regressions
- promotion target: reusable smoke-stabilization step for recovery checklists in editor/extension projects
- promotion trigger: another repo incident leaves smoke suites failing on harness behavior rather than on the intended product contract
- current proven evidence: on 2026-04-06, `vscode-markdown-review-surface` only closed recovery after updating `smoke.test.js` to use explicit text-editor opening for `reviewSurface.openDefault`, save-before-close cleanup for dirty teardown, and bounded handling for slower built-in preview paths

### Recovery Evidence Freeze After Triple Validation

- recurrence signal: repeated whenever teams want to document recovery completion quickly, but the real closure should only be frozen after structural, static, and runtime checks all agree
- current manual handling: freeze the recovery outcome only after layout lint, code checks, and test/smoke all pass in the same post-patch state, then write a narrow validation reference rather than a broad new planning document
- repeated invariant: recovery closure requires at least three aligned validations: structure, code, and runtime
- repeated invariant: the first canonical document after recovery is a validation reference, not an expanded future-state plan
- promotion target: reusable evidence-freeze rule for incident recovery milestones
- promotion trigger: another slice reaches a tempting “probably recovered” state before all verification bands have converged
- current proven evidence: the 2026-04-06 `vscode-markdown-review-surface` recovery was frozen only after `python3 scripts/lint_repo_layout.py` returned `warnings=0`, `npm run check` passed, and `npm test` reported `54 passing`, after which `REFERENCE_caption_surface_recovery_and_wave4_validation-at2026-04-06-10-08.md` was written

### Feature-Wave Packet Ladder With Verified Freeze Between Waves

- recurrence signal: repeated whenever a bounded feature should advance through architect-first skeleton work, then session/model extraction, then later UI lanes without reopening broad fanout too early
- current manual handling: issue one concrete feature packet at a time, close it with checks and tests, freeze a narrow validation reference, and only then open the next packet in the ladder
- repeated invariant: packet progression is not `plan -> many builders`; it is `packet -> implementation -> validation -> freeze -> next packet`
- repeated invariant: reduced-fanout expansion should follow proven seams and fresh validation, not optimistic staffing intent
- promotion target: reusable feature-wave ladder protocol for bounded UI surface delivery
- promotion trigger: another editor or surface feature is developed through architect-first scaffolding and later bounded fanout
- current proven evidence: on 2026-04-06, `vscode-markdown-review-surface` advanced from `TASK-FEATURE-0001` command-opened evaluation skeleton to `TASK-FEATURE-0002` slide-session extraction only after green checks and a wave-specific validation reference, then opened `TASK-FEATURE-0003` as the next bounded seam

### Validation Reference Resync After Post-Packet Green-State Drift

- recurrence signal: repeated whenever code and tests continue to evolve after a packet is nominally complete, leaving the most recent green state ahead of the last frozen validation reference
- current manual handling: patch the existing reference to match the newest verified command path, test count, or packet closure semantics before opening the next packet
- repeated invariant: the latest green code state must not drift ahead of the latest wave validation reference for long
- repeated invariant: reference resync is part of packet closure, not optional documentation cleanup
- promotion target: reusable post-packet reference-resync checklist
- promotion trigger: another bounded packet lands a final command-path or test delta after the first validation note was already written
- current proven evidence: on 2026-04-06, `REFERENCE_caption_surface_feature_wave1_validation-at2026-04-06-10-53.md` had to be updated after `reviewSurface.openEvaluationSession` became a real registered host command and the verified suite moved to `56 passing`

### Sequential Seam Packet Progression With Intentional Path Reuse

- recurrence signal: repeated whenever a bounded feature is advanced through multiple narrow seam packets that intentionally reuse one shared orchestrator file while keeping the rest of the lane disjoint
- current manual handling: issue the next packet anyway, validate it, treat `check-paths` overlap warnings as expected for the shared seam file, and execute the packets strictly in sequence instead of in parallel
- repeated invariant: a shared seam file can be reused across adjacent packets if and only if those packets are explicitly serial, not concurrent
- repeated invariant: `check-paths` output is a triage signal, not an automatic blocker; intentional overlap must still be classified and bounded
- promotion target: reusable guidance for serial seam ladders that narrow one file over several packets
- promotion trigger: another architect-led feature ladder advances through repeated extraction packets that all touch one shared orchestration file
- current proven evidence: on 2026-04-06, `TASK-FEATURE-0003` through `TASK-FEATURE-0006` repeatedly overlapped on `decision-slides.js`, `slide-shell.js`, or adjacent seam files, but the work remained safe because each packet was executed and validated in strict sequence

### Freeze Deferral Until Flaky Validation Is Reproduced Or Explained

- recurrence signal: repeated whenever a bounded packet appears complete in code, but a runtime or extension-host test fails once in a way that may be environmental or flaky
- current manual handling: stop before writing the next validation reference, rerun the same checks, and only freeze the result after the green state is reproduced or the failure is concretely explained
- repeated invariant: packet closure in code is not enough; freeze is deferred until the validation surface itself is trustworthy again
- repeated invariant: a single flaky red is treated as a triage event, not immediately as either a real regression or harmless noise
- promotion target: reusable flake-triage rule for extension-host or UI-heavy packet validation
- promotion trigger: another feature packet hits a transient validation failure after apparently safe local code changes
- current proven evidence: on 2026-04-06, after the `slide-feedback` scaffold landed in `vscode-markdown-review-surface`, the first `npm test` run failed generically and the next step was to rerun and inspect the extension-host output before freezing any new wave reference

### Source-Level Generator Retirement After Bundler Adoption

- recurrence signal: repeated whenever a runtime path has already moved onto a bundle, but the source tree still carries helper-generated script assembly that keeps an older architectural debt alive in reviews and future maintenance
- current manual handling: switch the bundle entry to the real runtime module, remove the leftover `get...Script()` helper chain from source files, and verify that webview orchestration now imports direct runtime factories rather than stringified functions
- repeated invariant: a runtime bundle alone does not close webview-injection debt if the source modules still express their behavior as script generators
- repeated invariant: debt retirement is only complete when both the bundle path and the source-level module structure converge on the same direct-runtime model
- promotion target: reusable cleanup wave for finishing architectural migrations after the first green bundle exists
- promotion trigger: another refactor adopts a bundler or runtime container but leaves helper-generated execution paths in place across source modules
- current proven evidence: on 2026-04-07, `vscode-markdown-review-surface` moved `webpack` directly onto `src/decision/webview-client.js`, removed the remaining `getReviewSurface...Script` exports from webview and slide modules, and kept `build:webview`, `check`, and `test` green afterward

### Residual Debt Scan Before Declaring Expert Feedback Closed

- recurrence signal: repeated whenever a focused expert-review remediation seems complete in code, but the team still needs a fast, explicit scan for the exact debt patterns that were originally called out before claiming closure
- current manual handling: run a narrow pattern scan for the named debt signatures, classify legitimate false positives, rerun the full validation stack, and only then say the feedback has been addressed
- repeated invariant: remediation closure requires evidence against the original review vocabulary, not just a fresh green test run
- repeated invariant: search hits must be triaged because legitimate runtime calls can look superficially similar to the retired debt pattern
- promotion target: reusable expert-feedback closure check for codebases that are fixing named technical-debt patterns
- promotion trigger: another expert review identifies a concrete signature family such as debug logging, generator helpers, or stale API usage that needs explicit post-fix confirmation
- current proven evidence: on 2026-04-07, after removing the `function.toString()`-style helper chain in `vscode-markdown-review-surface`, the final closure step was an explicit `rg` scan for `getReviewSurface.*Script` and `.toString(`, followed by triage of the remaining `asWebviewUri(...).toString()` as a legitimate URI serialization call and a full green validation pass

### Cross-Repo Product Review And Codex Handoff

- promotion status: promoted on 2026-04-07 to shared family skill `Skills-Create-Project/cross-repo-product-review`
- recurrence signal: repeated whenever a downstream surface repo reaches a milestone and needs quality validation before integration, followed by developer handoff for fixes and re-verification
- current manual handling: classify files by role (Host/Entry, Data Contract, Slide Seams, Webview/Render, Host State, Tests), perform line-by-line expert review, classify findings as Critical/Major/Minor, hand off to Codex for fixes, re-verify fixes with ultrathink analysis, record remaining concerns as checklist
- repeated invariant: product intent must be confirmed with the user before review begins — mischaracterizing the product purpose invalidates all downstream analysis
- repeated invariant: findings must be re-verified after Codex fix, not assumed closed; Codex fixes can introduce new concerns (innerHTML escape, sync I/O, spread merge collision)
- promotion target: `CHECKLIST_cross_repo_product_review.md` — review preparation + review perspectives + handoff format; `cross-repo-product-review` skill — file classification automation + review perspective prompt generation
- promotion trigger: same pattern repeats on `vscode-markdown-review-surface` or another surface repo for a second time
- current proven evidence: on 2026-04-07, `vscode-markdown-review-surface` product review followed this exact flow: 6-category file classification → line-by-line review → 3 Critical + 5 Major + 7 Minor findings → Codex handoff → 12 fixes verified → 3 remaining concerns documented → repeated issues/tasks extracted
- multi-round convergence (2026-04-07): 1차 15건 → 2차 3건 잔여 → 3차 2건 잔여(1건 실질 버그 + 1건 코드 스멜) → Expert 직접 수정으로 수렴. 잔여 1-2건 수준에서는 Codex 핸드오프보다 Expert 직접 수정이 효율적
- repeated invariant (추가): Codex 패치는 지적된 항목만 수정하는 경향 — 같은 구조적 클래스의 형제 필드를 놓칠 수 있음 (`ISSUE_partial_structural_fix_same_class_different_fields.md`)
- detail file: `TASK_cross_repo_product_review_and_codex_handoff.md`

### Decision Contract Cross-Field Test Expansion

- promotion status: absorbed on 2026-04-07 into `Skills-Create-Project/async-migration-verify/checklist-forimplementation/async-migration-implementation-checklist.md`
- recurrence signal: repeated whenever `decision-contract.js` gains new validation rules or cross-field constraints and the test suite needs proportional expansion
- current manual handling: identify new/changed rules, write at least 3 tests per rule (valid path, invalid path, boundary value), test cross-field constraints bidirectionally, verify `buildDecisionRowTemplate()` self-consistency, confirm patch validation covers same rules
- repeated invariant: 150+ validation rules with only 4-7 tests is a structural imbalance; any rule change must be accompanied by proportional test coverage
- repeated invariant: cross-field constraints must be tested bidirectionally (A requires B, B requires A)
- promotion target: checklist for decision-contract rule changes; script for generating test skeletons from rule definitions
- promotion trigger: next cross-field rule addition to decision-contract triggers the same test expansion pattern
- current proven evidence: on 2026-04-07, Codex expanded decision-contract tests from 4 to 7, adding `keeps neutral pending template valid`, `rejects machine-prefilled and contradictory decision patches`, `applies a human-only patch and preserves row validity` — but the ratio of 7 tests to 150+ rules remains low
- detail file: `TASK_decision_contract_cross_field_test_expansion.md`

### Async Migration Verification

- promotion status: promoted on 2026-04-07 to shared family skill `Skills-Create-Project/async-migration-verify`
- recurrence signal: repeated whenever Codex or a developer converts sync I/O to async and the patch needs expert verification beyond "tests pass"
- current manual handling: 6-checkpoint verification — (1) dead import scan, (2) duplicated parse/validate logic identification, (3) concurrent access protection + UX feedback, (4) error path test addition, (5) TOCTOU improvement confirmation, (6) error message quality (file path inclusion)
- repeated invariant: "tests pass" after async migration proves functional equivalence, not migration completeness; structural residue (dead imports, duplicated logic, missing guards) survives green tests
- repeated invariant: sync→async creates new failure modes (concurrent calls, event-loop yield between writes) that sync code never had — these need explicit verification
- promotion target: `CHECKLIST_async_migration_verification.md` — 6개 체크포인트; grep 기반 dead import / duplication 자동 탐지 script
- promotion trigger: another sync→async migration across this or another repo triggers the same 6-point verification
- current proven evidence: on 2026-04-07, `decision-session-artifacts.js` async migration triggered all 6 checkpoints — dead `fs` import removed, `parsePersistedFeedbackLedger` extracted, `feedbackSaveInFlight` + UX feedback added, malformed JSON/JSONL rejection tests added (81→83 passing), TOCTOU resolved, error messages enriched with file paths
- detail file: `TASK_async_migration_verification.md`

### Post-Promotion Family Validator Hardening Before Declaring Skill Ready

- recurrence signal: repeated whenever a new skill looks complete at the content level (`SKILL.md`, KB, checklist, evals exist), but family-level validators still reject it on structural conventions, naming discipline, or portability assumptions
- current manual handling: treat the first "skill exists" state as provisional, run the full family validator stack (`quick_validate --strict`, artifact-order verification, portability audit), and harden the skill until every validator closes before declaring it reusable
- repeated invariant: skill promotion is not complete when the content is written; it is complete only after family validators agree that the skill is structurally portable and convention-safe
- repeated invariant: validator closure often reveals second-order fixes such as overly long `SKILL.md`, missing timestamped canonical artifacts, weak eval structure, or script/TDD gaps that are invisible in a casual smoke pass
- promotion target: reusable post-promotion hardening step for any shared-family skill creation or migration workflow
- promotion trigger: another promoted skill passes semantic review first but still fails strict family validators on structure or artifact policy
- current proven evidence: on 2026-04-08, both `cross-repo-product-review` and `async-migration-verify` initially looked promotion-ready, but only became family-ready after `quick_validate.py --strict`, `verify_artifact_order.py`, and `skill_portability_audit.py` drove additional fixes to SKILL compression, canonical timestamped artifacts, scoreable eval structure, and helper/test coverage

### Timestamped Canonical Chain Additive Repair Without Deleting Legacy Skill Artifacts

- recurrence signal: repeated whenever older untimestamped KB/checklist artifacts are still semantically useful, but stricter family validators now require minute-level timestamped canonical files and ordered artifact chains
- current manual handling: preserve the older files in place, add a new timestamped canonical chain that satisfies validator expectations, and let the validator point at the new chain rather than deleting or mutating historical artifacts
- repeated invariant: when implementation is cheap but recovery is expensive, canonical repair should prefer additive layering over destructive cleanup
- repeated invariant: artifact-order compliance can be restored by adding a newer canonical chain without erasing prior evidence, as long as the new chain is unambiguous and validator-visible
- promotion target: reusable artifact-lifecycle rule for skill migrations that must satisfy stricter timestamp/order requirements without losing older context
- promotion trigger: another skill family introduces timestamp or artifact-order rules after legacy files already exist and remain useful for recovery or provenance
- current proven evidence: on 2026-04-08, `cross-repo-product-review` and `async-migration-verify` kept earlier untimestamped KB/checklist files, then added minute-stamped canonical KB and checklist files so `verify_artifact_order.py --skill-dir ...` passed without deleting the old artifacts

### Static Validation Capture Before Smoke Capture Before First Measured Run

- recurrence signal: repeated whenever a new skill or workflow artifact should become benchmarkable, but the team needs a reproducible progression from structural validity to runnable smoke to scoreable measurement instead of jumping straight to a score sheet
- current manual handling: first capture strict validator output as a frozen eval artifact, then capture one real smoke command, then fill the first measured benchmark score sheet using those artifacts as evidence
- repeated invariant: the first measured run is only credible when structural validation evidence and runnable smoke evidence already exist as separate artifacts
- repeated invariant: `evals.json` being valid is not enough for benchmark-grounded review; scoreability requires concrete prompt/assertion structure plus captured validation and smoke traces
- promotion target: reusable eval bootstrap ladder for new shared skills and benchmark-aligned workflow artifacts
- promotion trigger: another skill or reusable workflow wants `agent-tool-benchmark`-style scoring before it has frozen validation/smoke evidence
- current proven evidence: on 2026-04-08, both promoted skills added `quick-validate-capture-*.json/.md`, `smoke-command-capture-*.json/.md`, and only then filled `benchmark-score-sheet-*.md` with first measured values (`pass_rate`, `resolve_rate`, `action_score`)

### Typed Decision Form Lift Before Declaring Multi-Image Surface Usable

- recurrence signal: repeated whenever slide-based evaluation storage and writeback already exist, but the user-facing surface is still driven by raw JSON patch input that only developers can comfortably use
- current manual handling: replace the raw patch textarea with a typed decision form that maps directly onto the editable decision-contract fields, then translate changed form values back into a bounded `decision_patch`
- repeated invariant: persistence being live is not the same as the surface being usable; a human evaluation surface is still incomplete if the primary edit path is raw JSON
- repeated invariant: the cheapest safe migration path is to keep the existing host/writeback contract and only change the UI layer that gathers human-supplied fields
- promotion target: reusable UI-hardening pattern for moving from debug-oriented patch entry to typed evaluation controls without rewriting persistence
- promotion trigger: another bounded review surface has working writeback but still exposes its main decision path as raw JSON or developer-only inputs
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` added `slide-decision-form.js`, replaced the default `Decision Patch (JSON)` textarea in `slide-feedback.js`, and routed the form through `buildDecisionSlidesDecisionPatch(...)` in `decision-slides.js`, after which the suite moved to `87 passing`

### Session-Level Completion Summary Before Multi-Image Surface Closure

- recurrence signal: repeated whenever a slide-by-slide review surface can navigate and save per-item edits, but still lacks any single place that tells the operator whether the whole image set is actually complete
- current manual handling: add a dedicated session-summary module that computes completion, pending, deferred, retrieval-blocked, and row-update counts from the current slide set, then render that summary in the shell before calling the surface "closed"
- repeated invariant: a multi-image review surface is not operationally complete if it can show only the current item and cannot summarize whole-session readiness
- repeated invariant: whole-session completion is a distinct layer above slide context, slide feedback, and persistence, and needs its own module instead of being spread ad hoc across shell markup
- promotion target: reusable summary-layer step for any bounded multi-item evaluation surface
- promotion trigger: another review cockpit reaches "single-item edit works" status but still cannot answer "how many items are done?" or "is the session ready?"
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` added `slide-session-summary.js`, lifted `sessionSummary` into `slide-view-model.js`, rendered a `Session Summary` panel in `slide-shell.js`, and grew the validated suite from `87 passing` to `91 passing`

### Cross-Skill Dependency YAML Registration After Skill Creation

- recurrence signal: repeated whenever a new skill is created or promoted that references or is referenced by other skills, but `cross_skill_dependencies.yaml` is not created
- current manual handling: identify provider/consumer relationships, create bidirectional YAML entries in both skills' `references/` directories, verify consistency
- repeated invariant: cross-skill dependencies that exist only in prose (KB, checklist, guardrails) are invisible to automated validators and drift silently
- repeated invariant: bidirectional consistency is required — every `provider` entry in skill A must have a matching awareness in skill B
- promotion target: checklist for post-creation dependency audit + YAML validator script for bidirectional consistency
- promotion trigger: another skill is created without `cross_skill_dependencies.yaml` and the missing link is discovered during review
- current proven evidence: on 2026-04-08, both `cross-repo-product-review` and `async-migration-verify` were created without `cross_skill_dependencies.yaml` despite having an explicit cross-skill trigger (API-surface change escalation) and both being Band 1 specialists under `verification-decision-gate`; fixed by creating bidirectional YAML in both
- detail file: `TASK_cross_skill_dependency_yaml_registration.md`

### Band Owner Family Registration After Specialist Skill Promotion

- recurrence signal: repeated whenever a new specialist is promoted to a Band but the Band owner's SKILL.md YAML description, Family Roles, and the canonical owner-task-bands document are not all updated simultaneously
- current manual handling: update 3 locations — (1) owner SKILL.md `description` frontmatter routing clause, (2) owner SKILL.md `Family Roles` specialists list, (3) `owner-task-bands-at*.md` Band specialists list with adjacency notes
- repeated invariant: the YAML `description` is the primary routing surface for agent skill selection; a specialist missing from the description will not be routed to even if it exists in the Family Roles body
- repeated invariant: Band adjacency (e.g., "primary Band 1, secondary adjacency Band 3/Band 2") must be documented in specialist notes, not left implicit
- promotion target: checklist for 6-step Band registration + linter scanning owner YAML descriptions for missing specialist names
- promotion trigger: another specialist is promoted to a Band but routing fails because the owner description was not updated
- current proven evidence: on 2026-04-08, `cross-repo-product-review` and `async-migration-verify` were promoted as Band 1 specialists but initially missing from `verification-decision-gate/SKILL.md` description/Family Roles and `owner-task-bands-at2026-04-02.md`; fixed by updating all 3 locations with routing clauses and specialist notes
- detail file: `TASK_band_owner_family_registration_after_specialist_promotion.md`

### Partial DOM Save-State Update Before Declaring Form UX Stable

- recurrence signal: repeated whenever a review surface already has typed inputs and save actions, but transient UI states such as `dirty`, `saving`, `saved`, or `error` are still being considered through whole-shell re-rendering
- current manual handling: keep full shell rendering for init/navigation only, and move save-state changes onto narrowly targeted DOM updates for the button label, disabled state, dirty chip, and status/error notes
- repeated invariant: transient save-state updates must not destroy in-progress form input, textarea contents, or cursor position
- repeated invariant: once a shell owns typed form inputs, save-state UX should be applied as an upsert/update layer rather than a rerender layer
- promotion target: reusable save-UX hardening step for any bounded review surface with live form input
- promotion trigger: another review surface introduces typed inputs and then discovers that status updates reset those inputs through blanket rerendering
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` kept `renderDecisionSlidesShell()` for init/navigation but moved save-state UI updates in `decision-slides.js` to targeted DOM mutation, preserving typed decision form input while adding `dirty/saving/saved` UX and growing the suite to `92 passing`

### Validation Preview Layer Before Save UX Closure

- recurrence signal: repeated whenever a typed decision form exists and save UX exists, but the operator still learns about contract violations only after pressing Save
- current manual handling: compute a changed-only draft patch from current form values, merge it with the current persisted row, run contract validation on the merged draft row, and surface `idle | ready | blocked` preview state before save
- repeated invariant: `dirty` is not enough; an evaluation surface is still incomplete if it cannot distinguish "changed and ready" from "changed but blocked"
- repeated invariant: preview validation should reuse the same contract layer as persistence, rather than inventing a second UI-only rule system
- promotion target: reusable draft-validation step for typed review/evaluation surfaces that already have bounded editable-field contracts
- promotion trigger: another review cockpit adds typed form controls but still relies on save-time failure as the first point where contract errors become visible
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` added `evaluateDecisionSlidesDecisionDraft(...)` in `slide-decision-form.js`, lifted preview state through `slide-view-model.js`, rendered preview feedback in `slide-feedback.js`, blocked save on `blocked` drafts in `decision-slides.js`, and increased the validated suite from `92 passing` to `96 passing`

### Post-Implementation Save-UX Consistency Review

- recurrence signal: repeated whenever a Codex or subagent delivers a save-UX implementation that passes all tests but contains subtle consistency issues discoverable only through manual code review
- current manual handling: 5-point post-delivery review — (1) indentation consistency, (2) guard-without-feedback, (3) cascaded DOM double-update, (4) transient state affordances, (5) dead code after consolidation
- repeated invariant: save-UX implementations consistently pass automated tests but fail on these 5 patterns because tests verify state transitions and output, not code quality or UX edge cases
- repeated invariant: the 5 patterns are orthogonal — fixing one does not prevent the others
- promotion target: reusable 5-point post-implementation review checklist for any save-UX delivery on bounded review surfaces
- promotion trigger: another save-UX implementation is delivered and the same 5-point review reveals 2+ of these patterns again
- current proven evidence: on 2026-04-08, Codex delivered save-UX + validation-preview for `vscode-markdown-review-surface` with 96 tests passing; post-review found all 5 patterns — indent error in `decision-slides.js:108`, silent saving guard at `:250`, double DOM update at `:291`, transient `saved` button gap in `slide-view-model.js:66`, dead `clearDecisionSlidesFeedbackNotes` function at `:170`; all fixed, tests still 96 passing
- detail file: `TASK_post_implementation_save_ux_consistency_review.md`

### Donor Stack Boundary Fix Before Cross-Repo Integration Planning

- recurrence signal: repeated whenever two external repos look composable at first glance, but the real value lies in harvesting a narrow parser/donor layer rather than adopting either runtime whole
- current manual handling: inspect both codebases, classify each candidate module into `host`, `truth`, `donor`, or `downstream export`, then write the integration plan only after those ownership boundaries are locked
- repeated invariant: cross-repo integration planning drifts immediately if "which repo owns runtime" and "which repo owns truth" are not decided before module selection
- repeated invariant: the right integration shape is usually `host keeps ownership, external repos donate narrow modules`; full-runtime adoption is the exceptional case, not the default
- promotion target: reusable pre-implementation integration-design step for donor-based architecture work
- promotion trigger: another plan tries to combine a proven host repo with one or more external repos and the first question is "which modules should we use?"
- current proven evidence: on 2026-04-08, `slidev` + `slides-grab` integration planning for `vscode-markdown-review-surface` only stabilized after the modules were split into `slidev parser only`, `slides-grab selection/annotation/validation donor only`, and `current extension remains host/truth owner`, after which a canonical integration master plan could be written without widening into a generic PPT product

### Canonical Workspace Relocation After Cross-Workspace Drafting

- recurrence signal: repeated whenever a design artifact is drafted from the analyst's current workspace, but the artifact actually belongs to a different product workspace that owns the implementation
- current manual handling: save the draft if needed to avoid loss, copy it into the owning workspace's canonical control tree, then remove the misplaced duplicate so future readers have one obvious source
- repeated invariant: temporary drafting in the wrong workspace is recoverable, but leaving two authoritative-looking copies creates silent drift
- repeated invariant: canonical ownership belongs with the repo that owns the implementation and control plane, not the repo that happened to host the planning session
- promotion target: reusable artifact-placement correction step for cross-workspace planning sessions
- promotion trigger: another master plan, KB, or checklist is produced while the agent is operating from repo A but the document is actually for repo B
- current proven evidence: on 2026-04-08, the `slidev + slides-grab integration` master plan was first written under `my-image-parser/control/.../master_plans`, then relocated to `vscode-markdown-review-surface/control/project_domain/resources/master_plans/` as the canonical copy and deleted from the original workspace to avoid split authority

### Intent And Non-Intent Front-Loading Before Integration Execution

- recurrence signal: repeated whenever an integration plan risks being misread as a broader product rewrite because the tool names imply a larger scope than the actual intended slice
- current manual handling: add `Intent` and `Non-Intent` near the top of the canonical plan before implementation packets are derived
- repeated invariant: when external tools have strong product identities of their own, integration plans must front-load what the combined product is and explicitly what it is not
- repeated invariant: boundary text near the top prevents downstream implementers from mistaking a bounded donor integration for a full product transplant
- promotion target: reusable front-matter hardening step for plans that combine strong external donors or alternate hosts
- promotion trigger: another integration plan is likely to be misread as "tool X inside tool Y" rather than a bounded adaptation
- current proven evidence: on 2026-04-08, the canonical `slidev + slides-grab` integration master plan only became unambiguous after adding top-level `Intent` and `Non-Intent` sections clarifying that the target is a VS Code slide-edit-intent surface, not native PowerPoint inside VS Code

### Critique-As-Execution-Redesign Gate After Intent Lock

- recurrence signal: repeated whenever a critique document appears to attack a newly written plan, but the real question is whether it rejects the product direction or only invalidates the current execution strategy
- current manual handling: compare the critique against canonical intent/boundary KBs first, classify each finding as either `intent contradiction` or `execution redesign`, and only then decide whether the plan should be abandoned, narrowed, or reworked
- repeated invariant: critiques that say "intent correct, execution requires redesign" are not direction reversals; they are implementation-gate documents
- repeated invariant: product intent should be checked against canonical intent/boundary docs before treating execution-level criticism as a strategic rejection
- promotion target: reusable verification step for reading expert critiques without over-correcting product scope
- promotion trigger: another design or integration critique includes strong critical findings but still agrees with intent and high-level boundary
- current proven evidence: on 2026-04-08, `REFERENCE_slidev_slides_grab_master_plan_critique-at2026-04-08.md` was evaluated against the canonical `slides-grab` adaptation KB, region-grounding KB, and integration master plan, and was found to align with product intent while demanding redesign of donor extraction granularity, host/webview split, and source-mapping contracts rather than rejecting the direction itself

### Function-Level Donor Harvest Narrowing After Coupling Audit

- recurrence signal: repeated whenever an early integration plan names donor modules at file level, but a later coupling audit shows that only a few pure functions or algorithms are actually reusable
- current manual handling: downgrade the harvest unit from `module` to `function/algorithm`, separate reusable pure helpers from DOM/runtime-bound code, and rewrite the extraction plan around wrappers or reimplementation
- repeated invariant: donor files often mix pure helpers with runtime-coupled code; module-level reuse claims are usually too coarse for bounded host integrations
- repeated invariant: the right narrowing move is not "abandon donor strategy" but "shrink donor scope to pure logic and stable contract ideas"
- promotion target: reusable donor-audit step for cross-repo adaptation work after first-pass module selection
- promotion trigger: another donor integration starts with file-level reuse claims and later discovers DOM, native-binary, or runtime-environment coupling inside the same file
- current proven evidence: on 2026-04-08, `slidev + slides-grab` planning initially named `editor-bbox.js`, `editor-select.js`, `codex-edit.js`, `image-contract.js`, and `validation/core.js` as donor inputs; critique review then narrowed practical reuse to items like `normalizeSelection()`, `buildCodexEditPrompt()`, `classifyImageSource()`, and small algorithm helpers while marking whole DOM- and Playwright-bound modules as reference-only

### Post-Delivery New Module Test File Verification

- recurrence signal: repeated whenever a new source module (e.g., `slide-renderer.js`) is delivered without a corresponding test file, and the gap is only noticed during a later review rather than at delivery time
- current manual handling: reviewer discovers the missing test file during critique, flags it, and a follow-up task is created to add the test file after the fact
- repeated invariant: every new `.js` source module under `src/` should have a corresponding `.test.js` file under `src/test/suite/` at delivery time, not as a later follow-up
- repeated invariant: the cost of writing a basic test file at delivery is low; the cost of discovering missing coverage later (during an unrelated review or after a regression) is much higher
- promotion target: reusable post-delivery verification step that checks for 1:1 source-to-test file correspondence
- promotion trigger: another new module is delivered without a test file and the gap is discovered only during review
- current proven evidence: on 2026-04-08, `slide-renderer.js` (121 lines, 3 exported functions) was found to have zero test coverage — `slide-parser.test.js` existed but `slide-renderer.test.js` did not; `extractTitleAndImages` in `slide-parser.js` also had no direct test despite being a public export
- detail file: `repeated_tasks/TASK_post_delivery_new_module_test_file_verification.md`

### Pure Writeback Contract Before Host Apply Wiring

- recurrence signal: repeated whenever a UI slice reaches `selection -> intent` readiness and the next temptation is to wire source mutation directly into the host before the patch shape is frozen as a pure contract
- current manual handling: add a pure `writeback-contract` module first, then a pure `writeback-state` module, then a pure `writeback-apply` helper, and only after those tests pass allow runtime/protocol/host wiring
- repeated invariant: host apply logic is much easier to validate and refactor when `patch_id`, `operation`, `target`, and `replacement_markdown` are already fixed as a reusable contract
- repeated invariant: `edit intent -> patch` and `patch -> source replace` should be separately testable before any webview or VS Code command path is involved
- promotion target: reusable execution order for any source-backed editing surface that grows from preview-only into bounded writeback
- promotion trigger: another surface can already express selection + intent and is about to add writeback
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` added `slide-writeback-contract.js`, `slide-writeback-state.js`, and `slide-writeback-apply.js` with dedicated tests before wiring `slide-preview-runtime.js`, `webview-protocol.js`, and `extension.js` to actual apply; the suite grew from `157 passing` to `171 passing` before runtime/host apply was enabled

### Bounded Transaction Helper Extraction After Host Apply Success

- recurrence signal: repeated whenever a first implementation proves that a host-side apply path works, but the success branch still manually orchestrates `next text`, `next preview state`, and transient-state reset inline inside a large command/provider file
- current manual handling: extract a transaction helper that returns `nextText`, refreshed preview state, cleared selection state, cleared intent state, and post-apply writeback state as one reusable bundle, then wrap host-side document replacement behind a narrow host helper
- repeated invariant: once writeback succeeds, the hard part is not only document replacement but also restoring a consistent post-apply state graph; that reset logic should not remain ad hoc inside the provider
- repeated invariant: extension/provider files should consume a reusable transaction result rather than own the semantics of state reassembly
- promotion target: reusable host-transaction extraction step for bounded writeback slices in editor extensions
- promotion trigger: another editor surface lands inline success-path orchestration for document mutation plus UI reset and that logic starts growing inside the host/provider
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` first wired writeback apply directly in `extension.js`, then extracted `slide-writeback-transaction.js` and `slide-writeback-host.js` so the provider consumed a bounded transaction result instead of assembling `nextText` and transient resets inline; validated by `slide-writeback-transaction.test.js`, `slide-writeback-host.test.js`, and `178 passing`

### Expert Evaluation Packet After Vertical Slice Closure

- recurrence signal: repeated whenever a vertical slice becomes broad enough that an external reviewer or expert can no longer reconstruct the product intent, execution path, and validated boundary just from commit diffs or scattered chat notes
- current manual handling: write a single evaluation packet in the owning workspace's `references/` tree with `Intent`, `Non-Intent`, entry path, core module path, closed slice summary, review focus, and evidence links
- repeated invariant: once a slice spans parser, renderer, runtime, protocol, host state, and writeback, expert review quality drops unless the execution path is explicitly narrated
- repeated invariant: expert-facing review docs should describe both the intended product boundary and the exact code path that currently embodies it
- promotion target: reusable close-out artifact step for any multi-module vertical slice that is ready for expert review
- promotion trigger: another product slice requires external evaluation and the implementation path now spans 5+ cooperating modules
- current proven evidence: on 2026-04-08, after closing `selection -> intent -> patch -> bounded apply` in `vscode-markdown-review-surface`, a dedicated packet `REFERENCE_slide_preview_writeback_evaluation_packet-at2026-04-08.md` was written with intent, non-intent, entry path, core execution path, evidence files, and open scope so an expert could review without reconstructing the slice from chat history
- reinforcement (2026-04-08, same session): the initial packet required 2 precision calibration rounds — claims exceeded test boundaries ("stable", "closed", "sufficient" without scope qualification), hardcoded metrics staled immediately, and disclosures were structurally misplaced. This confirms that writing the packet is necessary but not sufficient; a post-creation precision calibration pass is also needed (see `TASK_post_critique_evaluation_document_precision_calibration.md`)

### Giant Runtime To Pure-Seam Extraction Before Visual Proof

- recurrence signal: repeated whenever a bounded UI slice has already closed its core contract chain, but the main runtime still concentrates DOM updates, pointer session logic, host sync, and downstream state coordination inside one orchestration closure
- current manual handling: reread the giant runtime file, identify pure or reusable seams first, then extract markup, DOM helpers, host-sync payload builders, pointer/selection runtime, and linked-state normalization before attempting broader verification or integration
- repeated invariant: actual runtime proof is much cheaper after orchestration responsibilities are pulled into small helpers with their own tests
- repeated invariant: cross-mode expansion should not proceed while the runtime entry file remains the dominant owner of both behavior and state normalization
- promotion target: reusable runtime-decomposition checklist for webview/editor slices that have outgrown a single orchestration file
- promotion trigger: another custom-editor or webview slice reaches `contract complete` status but runtime-level verification is still blocked by one large closure
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` extracted `slide-preview-markup.js`, `slide-preview-dom.js`, `slide-preview-host-sync.js`, `slide-preview-selection-runtime.js`, and later `slide-preview-linked-state.js` out of `slide-preview-runtime.js` before extending verification into actual webview hit proof and cross-mode bridge work

### Actual Webview Hit Proof After Fake-Geometry Contract Closure

- recurrence signal: repeated whenever contract tests using fake geometry pass, but the product still depends on real rendered hit accuracy inside the live webview
- current manual handling: keep the contract tests, then add a bounded webview probe path that measures actual rendered block rectangles and verifies `bbox -> source_range` mapping against the live preview instead of only fake `getBoundingClientRect` fixtures
- repeated invariant: algorithmic intersection proof is not the same thing as visual hit accuracy proof; both are required before claiming the selection surface is trustworthy
- repeated invariant: real layout verification should be added only after the parser, renderer, mapping, and selection contracts are already reusable and independently tested
- promotion target: reusable actual-webview probe harness for source-backed selection surfaces
- promotion trigger: another render-backed selection surface reaches contract-level green status but still relies on fake geometry for its last proof step
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` added `slide-preview-visual-probe.js` plus `slide-preview-visual-probe.test.js` and `slide-preview-visual-hit-accuracy.test.js`, which exposed and then corrected a live hit bug in `slide-selection-contract.js` where the oversized slide wrapper was incorrectly treated as a valid selection candidate

### Sidecar Bridge Before Cross-Mode Workflow Coupling

- recurrence signal: repeated whenever one bounded surface starts producing useful results that a second mode should see, but full workflow coupling would spread unstable assumptions too early
- current manual handling: define a small bridge artifact first, persist it in a lightweight sidecar store, and let the second mode read only the summary that it needs instead of importing the first mode's full internal state
- repeated invariant: the cheapest safe integration step is usually a bounded summary bridge, not direct state sharing or immediate truth-source unification
- repeated invariant: a bridge artifact lets reuse and review happen before mode-level coupling decisions are frozen
- promotion target: reusable cross-mode sidecar bridge template for bounded editor surfaces
- promotion trigger: another pair of modes needs to share patch or review outcomes before their truth models are ready to merge
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` added `slide-preview-bridge.js` and `host-sidecar-store.js`, then patched `decision-slides-view-model.js`, `slide-shell.js`, and `extension.js` so `decision-slides` could read a bounded summary of `slide-preview` writeback results without directly coupling to the preview runtime state

### Linked-State Normalization Extraction Across Host And Webview

- recurrence signal: repeated whenever host and webview both normalize the same dependent state chain, such as `selection -> edit intent -> writeback`, and drift risk grows as the chain expands
- current manual handling: reread both normalization paths, extract the linked-state transitions into one shared helper, then patch both host and runtime to consume the same contract before further product expansion
- repeated invariant: once the same dependent state chain is normalized in two places, reuse should be forced before additional features are layered on top
- repeated invariant: state drift is much cheaper to prevent with a shared normalizer than to debug after mode bridge or writeback logic multiplies the affected surfaces
- promotion target: reusable linked-state coordinator pattern for host/webview pairs
- promotion trigger: another feature duplicates chained state normalization across runtime and host or across two cooperating modes
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` introduced `slide-preview-linked-state.js` and refactored both `slide-preview-runtime.js` and `extension.js` to consume it, aligning selection, edit-intent, and writeback normalization before additional runtime splitting and bridge expansion

### Post-Critique Evaluation Document Precision Calibration

- recurrence signal: repeated whenever an agent critiques and patches an evaluation/reference document, but the first patch is directionally correct yet imprecise in scope qualification, structural placement, or evidence granularity
- current manual handling: user provides detailed feedback per section, agent re-patches; typically requires 1-2 calibration rounds to reach expert-ready precision
- repeated invariant: the first critique patch tends to use the document's own overclaiming language, blend proven/unproven in single sentences, place disclosures where structurally convenient rather than where readers need them, and leave hardcoded metrics that stale immediately
- repeated invariant: calibration corrections fall into 6 recurring categories — (1) hardcoded metrics → structural descriptions, (2) blended claims → proven/unproven separation, (3) scope overstatement → conservative qualification, (4) misplaced disclosure → structural position, (5) flat mixed lists → typed/prioritized buckets, (6) direct vs adjacent evidence → label separation
- promotion target: reusable post-critique precision checklist applied after the first patch round, before presenting to the user
- promotion trigger: another evaluation document is patched and requires 2+ correction rounds on the same structural issues
- current proven evidence: on 2026-04-08, `REFERENCE_slide_preview_writeback_evaluation_packet-at2026-04-08.md` required 2 calibration rounds (6 items × 2 rounds = 12 corrections) covering all 6 categories before reaching precision accepted by the user
- recent recurrence extension: on 2026-04-09, the same 6 calibration categories repeated on `REFERENCE_review_surface_progress_and_expert_evaluation_packet-at2026-04-08.md`, and a further cross-document consistency pass was required to reconcile the detailed writeback packet with later implementation and test progress
- detail file: `repeated_tasks/TASK_post_critique_evaluation_document_precision_calibration.md`

### Submission Packet To Steward Response Freeze

- recurrence signal: repeated whenever an implementation lane submits a status/requirements refresh packet and the central steward must convert it into canonical next-step decisions instead of leaving the packet as advisory context
- current manual handling: reread the submission packet, compare it against current contracts and operator policy, answer the unresolved questions explicitly, then persist the result as a user-decision note plus registry entry
- repeated invariant: cross-repo progress packets are not source-of-truth by themselves; they must be reinterpreted through current workspace policy before implementation can continue
- repeated invariant: the steward response must freeze at least `evaluation body`, `required UX`, `completion criterion`, `lane boundary`, and `source of truth`
- promotion target: reusable `submission packet -> steward decision note` response protocol for control-plane management work
- promotion trigger: another repo or sub-lane submits a requirement refresh or readiness packet that asks for completion criteria or UX direction clarification
- current proven evidence: on 2026-04-09, `SUBMISSION_review_surface_requirement_refresh_and_status_packet-for-control-plane-program-steward-at2026-04-09.md` was converted into `NOTE_review_surface_requirement_response_by_control-plane-program-steward-at2026-04-09-14-17.md`, and the response was registered in `control/user_decisions/registry/decision_index.json`

### Artifact-Contract-First Gate Before Human Evaluation Execution

- recurrence signal: repeated whenever a review surface can already bootstrap and open a session, but the actual human decision depends on candidate payloads that are not yet carried in the session artifact contract
- current manual handling: classify bootstrap/open as intermediate readiness only, freeze a contract-extension requirement first, and postpone the human evaluation run until the surface can render the needed comparison payloads in-bounds
- repeated invariant: `session opens` is not the same claim as `evaluation surface is acceptable`
- repeated invariant: if a reviewer must choose among arm outputs, those outputs must exist as explicit contract fields before evaluation execution starts
- promotion target: reusable readiness gate for evaluation surfaces that look operational before their decision body is actually encoded in artifacts
- promotion trigger: another review workflow shows working navigation/form UX but still lacks explicit candidate payloads needed for the judgment itself
- current proven evidence: on 2026-04-09, the review-surface bootstrap path was treated as valid but incomplete, and the Steward response froze `artifact contract extension` ahead of `actual 10-image evaluation run`
- recent recurrence extension: later on 2026-04-09, the same gate had to be applied a second time after candidate comparison landed — the team still had to audit session-local bundle availability against the canonical comparison truth set, suppress non-ready slide controls, and decide whether the current first-10 session was actually runnable before starting human evaluation
- later recurrence extension II: later on 2026-04-09, the gate had to expand once more beyond machine-readable truth — the team still needed an evaluator-first UX pass, advanced-metadata collapse, Korean operator copy, and an explicit save-target explanation before the live surface could be trusted for human use
- detail file: `repeated_tasks/TASK_artifact_contract_first_gate_before_human_evaluation_execution.md`

### Lane-Split Preservation While Acceptance Bar Tightens

- recurrence signal: repeated whenever one lane is product-ready enough to attract feature pressure from an adjacent lane, but the correct move is to preserve the split and tighten the acceptance requirements of the target lane instead of collapsing both modes together
- current manual handling: keep the two-lane model explicit, decide which lane owns the missing UX, and raise that lane's completion bar without reopening the other lane's bounded proof scope
- repeated invariant: lane merging is not the default response to missing UX in one lane; often the right move is to preserve the split and improve the lane that owns the user task
- repeated invariant: when one lane is a proof lane and the other is a decision lane, acceptance criteria should tighten on the decision lane first
- promotion target: reusable lane-boundary preservation rule for multi-surface products with one proof lane and one execution/evaluation lane
- promotion trigger: another product slice proposes collapsing two neighboring modes because one surface lacks user-facing clarity or comparison features
- current proven evidence: on 2026-04-09, `decision-slides` was kept as the human evaluation lane and `slide-preview` was kept as the source-grounded writeback proof lane, while the completion bar for `decision-slides` was raised to require candidate comparison UX

## 2026-04-09 Codex Workspace Retrospective Addendum

1. A missing backup and deleted directory incident changed the priority from `public-prep` to `local safety first`.
2. A minimal Git safety net was created before broader cleanup so later edits would be recoverable.
3. Ignore boundaries and one sanitized config surface were landed first, before broader snapshots.
4. A broad agent-facing workspace surface was committed next so `scripts/`, `skills/`, and `control/resources` were no longer living only in the working tree.
5. Path cleanup then proceeded by surface class rather than blanket replacement: stable docs were sanitized, active experiment evidence and user-edited files were left alone.
6. The cleanup target shifted again after the user clarified that ongoing experiments should later run on stronger remote compute; runtime portability started to outrank cosmetic public-prep cleanup.
7. Vendored OCR and ML-adjacent runtime surfaces were then hardened with env overrides and `.venv`/`venv` fallback so the same repo can move more easily toward Docker or hosted-agent execution later.

### Git-Safety Snapshot Before Boundary Cleanup

- recurrence signal: repeated whenever a workspace needs aggressive cleanup or restructuring before a reliable Git recovery point exists, especially after an accidental deletion or missing-backup incident
- current manual handling: initialize Git first, land a narrow boundary commit (`.gitignore` and one sanitized config surface), then take a broad agent-facing snapshot commit before any larger cleanup wave
- repeated invariant: cleanup should not start from an unversioned workspace once the cost of lost local state is visible
- repeated invariant: the first safe commit can be narrower than the intended public surface as long as it establishes a recoverable baseline
- promotion target: reusable `local safety bootstrap before cleanup` checklist for volatile workspaces
- promotion trigger: another repo or workspace needs path cleanup, scope reduction, or public-prep work while still lacking a recoverable Git baseline
- current proven evidence: on 2026-04-09, `my-image-parser` first landed `1825804` (`chore(init): add ignore boundaries and sanitized mcp snippet`) and then `495f295` (`chore(snapshot): add broad agent-facing workspace surface`) before broader cleanup continued
- detail file: `repeated_tasks/TASK_git_safety_snapshot_before_boundary_cleanup.md`

### Surface-Classified Path Sanitization Across Mixed Workspace Surfaces

- recurrence signal: repeated whenever the same workspace contains stable docs, runtime examples, external truth references, local-private paths, and scratch outputs, all with machine-local absolute paths that cannot be treated the same way
- current manual handling: classify each path first (`repo-local doc`, `local-private`, `external workspace`, `scratch/tmp`, `runtime/config surface`), then replace it with the correct form (`repo-relative`, local placeholder, external placeholder, `<TMP_DIR>`, or env/template placeholder), validate, and commit in small topical batches
- repeated invariant: path cleanup is a classification task before it is a search-and-replace task
- repeated invariant: forcing every path into repo-relative form creates new drift when the original reference was intentionally local-private, external, or runtime-bound
- promotion target: reusable path-class decision table, lint rule set, or cleanup checklist for GitHub-prep and portability waves
- promotion trigger: another mixed control-plane/execution-plane repo needs machine-local path cleanup without flattening all path semantics into one rule
- current proven evidence: on 2026-04-09, `my-image-parser` used this pattern across tracked docs and config surfaces, landing batch commits such as `b13bab7`, `432db92`, `cfbeb21`, `cc309e2`, and `abab530`
- detail file: `repeated_tasks/TASK_surface_classified_path_sanitization_across_mixed_workspace_surfaces.md`

### Runtime Portability Hardening Across Code And Skill Docs

- recurrence signal: repeated whenever vendored runtimes or local ML-adjacent tools assume one exact interpreter path, venv layout, or launcher root and therefore become sticky to the original workstation
- current manual handling: patch runtime code first to honor env overrides and dual `.venv`/`venv` fallback, then patch `runtime.md` and troubleshooting pages so documented launch paths match the new code behavior, and finally rerun lightweight validation such as `py_compile`
- repeated invariant: runtime portability is not closed until code and skill docs agree on the same interpreter and launcher resolution strategy
- repeated invariant: portability cleanup should preserve the bounded runtime contract instead of deleting local tool support outright
- promotion target: reusable `vendored runtime portability hardening` checklist for scripts plus skill-side runtime/troubleshooting pages
- promotion trigger: another local OCR, parser, or model-backed tool should stay in the repo while becoming less tied to one machine layout
- current proven evidence: on 2026-04-09, `my-image-parser` landed `92f444c` and `09cfec6`, hardening vendored launcher/runtime assumptions in `scripts/` and the related OCR-oriented `skills/*/references/runtime.md` and `troubleshooting.md` pages
- detail file: `repeated_tasks/TASK_runtime_portability_hardening_across_code_and_skill_docs.md`

### Scope-Freeze Reclassification Before Forcing More UX Work

- recurrence signal: repeated whenever an implementation lane looks blocked under one interpretation, but a user clarification changes the ownership boundary and reveals that the lane is only cross-validation or support work for a different main test
- current manual handling: restate the user clarification as a scope-freeze note, rewrite the closure boundary in closed-question form, then patch reports and master-plan docs so the old blocker interpretation becomes historical rather than active
- repeated invariant: blocker status is not absolute; it depends on what the lane is actually supposed to prove
- repeated invariant: once the user clarifies `main test` versus `cross-validation lane`, the steward must freeze that distinction in a decision artifact before continuing implementation pressure
- promotion target: reusable `scope freeze -> closure reclassification` protocol for control-plane stewardship
- promotion trigger: another slice is about to attract extra feature work only because a support lane was being mistaken for the main product-under-test
- current proven evidence: on 2026-04-09, `my-image-parser` converted the user clarification "image captioning is the main test; this is cross-validation" into `NOTE_review_surface_cross_validation_scope_freeze-at2026-04-09-19-03.md`, then reclassified the review-surface lane as closed in `REPORT_phase2_review_surface_cross_validation_slice_closure-at2026-04-09-19-03.md`

### Mixed-Readiness Cohort Closure By Terminal Defer-Or-Complete Policy

- recurrence signal: repeated whenever an evaluation cohort contains both comparison-ready items and structurally non-ready items, but the lane still needs a bounded terminal outcome instead of another round of widening work
- current manual handling: freeze the cohort, mark ready rows as `completed`, mark non-ready rows as explicit `deferred / manual_lane`, ensure no row remains `pending`, then validate that the session artifact now expresses a full terminal state
- repeated invariant: a mixed-readiness cohort can still close if non-ready rows are truthfully deferred rather than silently excluded or left pending
- repeated invariant: terminal-state completeness is often more important than uniform readiness when the lane is only producing bounded evaluation evidence
- promotion target: reusable `terminal defer-or-complete` closure pattern for bootstrap review sessions and mixed evidence cohorts
- promotion trigger: another review or audit cohort mixes ready, excluded, and missing-source rows but still needs one canonical session outcome
- current proven evidence: on 2026-04-09, the first-10 bootstrap session in `my-image-parser` was closed by writing `image1`-`image6` as `deferred / manual_lane` and `image7`-`image10` as `completed`, yielding `pending = 0` in the session-local `decision-seed.jsonl`

### Historical Blocker Report Supersession After Boundary Change

- recurrence signal: repeated whenever an earlier report is still factually correct about past conditions, but its conclusion is no longer the active gate because scope, ownership, or success criteria changed
- current manual handling: keep the old report, add an explicit supersession section, create a new closure report under the new boundary, and patch the active runbook/master plan to point at the new canonical interpretation
- repeated invariant: historical evidence should be preserved, but its conclusion must be demoted once a newer boundary decision supersedes it
- repeated invariant: rewriting history is worse than superseding it; the steward should preserve the old diagnosis and only retire its gating force
- promotion target: reusable `historical blocker -> superseded historical report` documentation pattern
- promotion trigger: another workspace slice changes closure boundary after a blocker report has already been published and cited
- current proven evidence: on 2026-04-09, `REPORT_phase2_review_surface_current_evaluation_gate_verdict-at2026-04-09-18-37.md` gained a `Supersession` section and the active closure moved to `REPORT_phase2_review_surface_cross_validation_slice_closure-at2026-04-09-19-03.md`

## 2026-04-13 Codex Lean Portfolio Retrospective Addendum

1. The slice was first narrowed from platform-scale ambition to one lean `02_1` portfolio draft with a frozen 6-slide system-first story.
2. Before deck authoring, the execution contract had to be frozen explicitly: exact slide mapping, output paths, review artifacts, and skill ownership all needed concrete paths instead of plan-level intent.
3. The implementation then split into two parallel artifacts: one real 6-slide deck for review and six single-slide render-source decks for slide-by-slide QA.
4. Visual QA did not close in one pass. The first render exposed wrap and density problems, so the deck had to be rebuilt with compressed copy rather than redesigned from scratch.
5. Review publication had to stay two-layered: repo-local canonical artifacts first, then external symbolic-link exposure for easier human inspection.
6. The last step was not deck content but packaging accuracy: render directories had to be normalized, preview caveats documented, and later Git handoff prompts narrowed so partially committed work would not be over-staged.

### Lean Execution-Contract Freeze Before Portfolio Authoring

- recurrence signal: repeated whenever a plan is directionally accepted but still contains `or`, `optional`, or unfrozen output paths, so implementation would otherwise drift at the first authoring step
- current manual handling: freeze the exact slide mapping, deck path, render path, role-matrix path, review index path, and authoring owner before repo-tracked deck work starts
- repeated invariant: portfolio authoring becomes expensive the moment visual and path choices are left as live decisions during implementation
- repeated invariant: a lean slice only stays lean if output artifacts and slide ownership are frozen before design work begins
- promotion target: reusable `execution contract freeze` checklist for bounded portfolio or presentation slices
- promotion trigger: another image-led deck or review surface moves from planning to implementation while still carrying unresolved `or/optional` branches
- current proven evidence: on 2026-04-13, `my-image-parser` had to freeze the 6-slide mapping and concrete output surfaces in `PLAN_lean_ppt_image_character_portfolio_slice-at2026-04-11.md` before the lean `02_1` portfolio deck could be built consistently

### Provider-Backed Skill Declaration In Review Index

- recurrence signal: repeated whenever a user explicitly cares which skill owns authoring and which auxiliary skill shapes copy or labeling, and that decision must survive beyond chat
- current manual handling: persist the skill ownership declaration into the review-facing index instead of leaving it implicit in the conversation
- repeated invariant: if a slice depends on both an authoring owner and a wording-support skill, the review packet should name both explicitly
- repeated invariant: skill provenance belongs in the review index once the user has made it part of the acceptance criteria
- promotion target: reusable `skill usage declaration` section for public/review-facing artifact indexes
- promotion trigger: another slice uses one owner skill plus one or more auxiliary skills and the user expects that dependency to be visible in the final packet
- current proven evidence: on 2026-04-13, `REFERENCE_lean_02_1_system_first_portfolio_review_index-at2026-04-13.md` explicitly recorded `<CODEX_HOME>/skills/pptx/SKILL.md` as the PPT authoring owner and `<CLAUDE_SKILLS_ROOT>/semantic-clarity-enhanced/SKILL.md` as requested copy support

### Scratch Deck Plus Single-Slide Render-Source Generation

- recurrence signal: repeated whenever a new portfolio deck needs whole-deck delivery and per-slide visual QA, but the render tool is more reliable on single-slide sources than on full multi-slide navigation output
- current manual handling: build the review deck from scratch and emit one single-slide render-source deck per slide in the same build step
- repeated invariant: per-slide QA becomes simpler when render sources are generated as first-class outputs rather than improvised later
- repeated invariant: a render-source directory is often the cheapest bridge between a canonical deck artifact and visual QA tooling
- promotion target: reusable `deck + render_sources` generation pattern for image-led PPT slices
- promotion trigger: another bounded deck needs deterministic slide-by-slide preview generation and review evidence
- current proven evidence: on 2026-04-13, `scripts/build_lean_02_1_system_first_portfolio.py` generated both `lean_02_1_system_first_v1.pptx` and six `render_sources/slide-*-source.pptx` artifacts for the lean `02_1` portfolio slice

### Preview-First QA Followed By Copy Compression Rebuild

- recurrence signal: repeated whenever the first visual pass reveals wrap pressure, footer collisions, or copy density problems, but the correct fix is copy compression and hierarchy tightening rather than layout redesign
- current manual handling: run a first render pass, record slide-specific findings, patch the source build script to reduce or tighten copy, then rebuild and reverify
- repeated invariant: image-led slides usually fail first on text density, not on missing structure
- repeated invariant: one fix-and-reverify cycle should be treated as the minimum close condition for bounded deck slices
- promotion target: reusable `preview -> compress copy -> rebuild -> reverify` QA loop for lean presentation work
- promotion trigger: another deck slice passes structural build checks but fails visual readability on its first rendered pass
- current proven evidence: on 2026-04-13, `REPORT_lean_02_1_system_first_portfolio_visual_qa-at2026-04-13-13-30.md` recorded first-pass wrap/overflow findings on slides 2-5, then closed only after a copy-compression rebuild and one reverify cycle

### External Review Surface Symlink Publication After Internal Artifact Freeze

- recurrence signal: repeated whenever canonical review artifacts live inside the repo, but the user wants a second, cleaner review surface in an external `Symbolic_links` directory
- current manual handling: freeze repo-local artifacts first, then expose only the review index, QA report, and deliverable deck through external symlinks
- repeated invariant: external review surfaces should mirror already-frozen artifacts, not become a second authoring surface
- repeated invariant: symbolic links are a publication step, not part of the canonical artifact set
- promotion target: reusable `internal freeze -> external symbolic review surface` publication pattern
- promotion trigger: another slice must be inspected from a cleaner shared folder without moving canonical artifacts out of the repo
- current proven evidence: on 2026-04-13, `my-image-parser` published the lean portfolio deck, review index, and QA report into `Date_Project/sesac_seocho_dataanalysis/Symbolic_links` only after the repo-local artifacts and QA report were frozen

## 2026-04-13 Codex Public Surface Packaging Addendum

1. The packaging wave did not start from zero; several lean portfolio artifacts had already landed in earlier commits, so the first step was reconstructing what was already committed versus what still remained.
2. Safe packaging then proceeded in bounded batches: text-only notes and reports first, binary review artifacts next, and JSON-heavy evidence bundles only after path sanitization.
3. The review-surface session bundle looked small enough to keep, but its whole JSON tree was still machine-local, so it had to be normalized before it could become a public review artifact.
4. Binary review evidence was packaged only after size and scope checks showed the set was bounded and review-facing rather than tool/runtime residue.
5. The final lean follow-up was not a new artifact but a stale pointer correction: one plan still referenced an older timestamped QA report filename that no longer existed.
6. The wave closed with a stricter handoff rule: inspect remaining candidate files, but if the lean slice is already committed, stop and report clean status instead of manufacturing another commit.

### Bounded Public Surface Packaging After Partial Prior Commits

- recurrence signal: repeated whenever a bounded slice already landed across multiple earlier commits, but a later packaging pass still needs to determine what remains safely committable
- current manual handling: reconstruct the slice's landed commits first, treat the file list as `candidate files to inspect`, then commit only the still-uncommitted safe remainder in small batches
- repeated invariant: a follow-up packager should not infer a mandatory stage set from a bounded candidate list
- repeated invariant: once the bounded slice is effectively committed, the correct next action is a clean-status report, not an empty follow-up commit
- promotion target: reusable packaging checklist for `already committed / still pending / risky / out-of-scope`
- promotion trigger: another artifact slice is resumed after partial prior commits and the next agent must avoid over-staging old or unrelated changes
- current proven evidence: on 2026-04-13, `my-image-parser` had to package lean `02_1` artifacts after earlier commits such as `7874c72`, `2a7beb6`, and `999e72b`, and later closed the remaining safe pointer fix in `2b09aae`
- detail file: `repeated_tasks/TASK_bounded_public_surface_packaging_after_partial_prior_commits.md`

### Evidence Bundle Path Placeholder Sanitization Before Commit

- recurrence signal: repeated whenever an evidence bundle is structurally valid and worth preserving, but embeds machine-local absolute paths across JSON and JSONL payloads
- current manual handling: enumerate the bundle, replace the machine-local prefix with `<REPO_ROOT>/`, revalidate every JSON/JSONL payload, then commit the sanitized bundle as evidence
- repeated invariant: evidence bundles can often be preserved without regeneration if path normalization stays purely structural
- repeated invariant: JSON/JSONL evidence trees need format-aware sanitization, not markdown-style relative-link rewriting
- promotion target: reusable session-bundle sanitizer and validation checklist
- promotion trigger: another small review or audit bundle contains host-local path residue but should remain in repo history
- current proven evidence: on 2026-04-13, `my-image-parser` normalized the review-surface session bundle and committed it in `3d1e4a1`
- detail file: `repeated_tasks/TASK_evidence_bundle_path_placeholder_sanitization_before_commit.md`

### Binary Evidence Batch Packaging With Scope Guard

- recurrence signal: repeated whenever a review-facing slice includes PPTX, JPG renders, or screenshots that are small enough to keep in Git but only if their scope is explicitly bounded
- current manual handling: measure size first, enumerate the exact binary set, confirm it is review evidence rather than runtime residue, then commit it separately from text docs and vendor decisions
- repeated invariant: binary evidence should be staged as one bounded proof batch, not by recursively trusting adjacent directories
- repeated invariant: size and scope both matter before a binary commit becomes acceptable
- promotion target: reusable bounded-binary packaging preflight
- promotion trigger: another presentation or review slice needs to keep visual proof artifacts without accidentally absorbing caches or bulky tool payloads
- current proven evidence: on 2026-04-13, `my-image-parser` committed the lean `02_1` PPTX, six render-source decks, six JPG previews, three screenshots, and one `.surface.json` as a bounded evidence batch in `999e72b`
- detail file: `repeated_tasks/TASK_binary_evidence_batch_packaging_with_scope_guard.md`

## 2026-04-13 Codex Public Entry, Dispatch, And Raw Vendor Addendum

1. The next wave did not start with deck work. It started by freezing the role boundary so public-entry packaging would not reopen toolization.
2. Only after that boundary reset did the readable `Start Here` surface get built from already-existing local truth: `v1` and `v2` review indexes first, then the page-link guide and regeneration handoff guide.
3. Git packaging was then kept as a second packet, not part of the entry packet. The chain only continued because the new `Start Here` doc left one relevant repo-local change.
4. The chain then committed exactly that one entry artifact after re-running bounded JSON and file-existence checks.
5. A separate meta wave later packaged the dispatch prompt, the two packets, and the boundary note as reusable dispatch infrastructure.
6. In parallel, the raw vendor request needed a completely different path: nested vendor repos had to be ingested through tracked-file-only staging rather than normal recursive `git add`.

### Role Boundary Freeze Before Public Entry Packaging

- recurrence signal: repeated whenever a readable public-entry request sits on top of already-existing routing contracts and execution artifacts, so a navigation pass can easily drift into toolization
- current manual handling: freeze the role split first, record it in one boundary note, then use that note as the source of truth for entry packets and public-entry docs
- repeated invariant: public-entry packaging is safer once toolization ownership is frozen before any doc writing starts
- repeated invariant: if the boundary is implicit, the packaging lane starts mutating contracts or semantics by accident
- promotion target: reusable `toolization owner vs public-surface packager` boundary-freeze preflight
- promotion trigger: another stack needs a readable public entry surface while already carrying nontrivial machine-readable routing and handoff artifacts
- current proven evidence: on 2026-04-13, `my-image-parser` first wrote `NOTE_role_boundary_reset_between_control_plane_program_steward_and_public_surface_architect-at2026-04-13-16-07.md`, then used it to constrain the lean `02_1` public-entry wave
- detail file: `repeated_tasks/TASK_role_boundary_freeze_before_public_entry_packaging.md`

### Start Here Public Entry Packaging From Existing Truth Surfaces

- recurrence signal: repeated whenever the real local truth for a slice already exists across review indexes, role matrices, handoff guides, and QA reports, but another agent still cannot find the right entry path in one pass
- current manual handling: gather the current review truth first, then package one `Start Here` doc that orders local review truth, bridge artifacts, regeneration handoff, and routing design without rewriting the underlying contracts
- repeated invariant: the fastest public entry surface is usually a readable ordering of existing truths, not a new concept document
- repeated invariant: if the entry surface starts replacing manifests or review indexes, it has crossed back into control-plane work
- promotion target: reusable multimodal-PPT `Start Here` template
- promotion trigger: another review stack becomes hard to enter because its truth surfaces are all present but scattered
- current proven evidence: on 2026-04-13, `my-image-parser` created `REFERENCE_lean_02_1_multimodal_ppt_start_here-at2026-04-13.md` and committed it in `c496b83`
- detail file: `repeated_tasks/TASK_start_here_public_entry_packaging_from_existing_truth_surfaces.md`

### Chained Public Entry Then Conditional Git Handoff

- recurrence signal: repeated whenever a readable-entry packet must sometimes be followed by a commit packet, but only if the first packet leaves a bounded repo-local change
- current manual handling: execute the entry packet first, inspect the worktree again, run the git-handoff validations, and commit only the remaining bounded delta
- repeated invariant: `make it readable` and `package it in git` should stay as separate scopes even when they happen back to back
- repeated invariant: a chained follow-up should create one bounded commit or no commit, never an automatic second wave by assumption
- promotion target: reusable chained-dispatch rule for `ENTRY -> conditional GIT HANDOFF`
- promotion trigger: another doc/public-surface pass may or may not leave a repo-local delta and needs bounded follow-up packaging
- current proven evidence: on 2026-04-13, `my-image-parser` formalized the chain in `REFERENCE_public_surface_architect_chained_dispatch_prompt-at2026-04-13.md` and then committed only the generated `Start Here` doc in `c496b83`
- detail file: `repeated_tasks/TASK_chained_public_entry_then_conditional_git_handoff.md`

### Tracked-File-Only Raw Vendor Source Import From Nested Repos

- recurrence signal: repeated whenever the user explicitly wants raw vendor inclusion, but vendored tool trees still contain nested `.git`, local installs, model payloads, or generated residue
- current manual handling: measure and classify the vendor trees first, preserve nested git metadata outside the tree, and stage only the vendor repo's originally tracked files into the host repo
- repeated invariant: raw vendor inclusion does not justify absorbing local runtime residue
- repeated invariant: `recursive add of vendor tree` and `tracked-file-only vendor source import` are different tasks and should not be treated as the same thing
- promotion target: reusable raw-vendor-ingestion workflow
- promotion trigger: another host repo must absorb vendor source directly while still excluding local installs, model caches, and nested repo metadata
- current proven evidence: on 2026-04-13, `my-image-parser` imported four vendor trees in `2562031` after confirming host-side vendor ignore boundaries and using tracked-file-only staging
- detail file: `repeated_tasks/TASK_tracked_file_only_raw_vendor_source_import_from_nested_repos.md`
