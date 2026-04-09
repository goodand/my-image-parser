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
