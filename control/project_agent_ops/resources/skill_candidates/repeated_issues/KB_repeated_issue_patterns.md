# Repeated Issue Patterns

## Purpose

Track repeated project-agent operational issues that should be standardized, linted, or promoted into troubleshooting or skill-candidate material.

## Source Of Truth

- This file is the canonical repeated-issue pattern log under `project_agent_ops/resources/skill_candidates/repeated_issues/`.
- Keep entries tied to observable recurrence, not one-off noise.

## Candidate Pattern Format

For each candidate, record:

- issue name
- recurrence signal
- current workaround
- structural fix candidate
- escalation trigger

## Current Repeated Issue Patterns

### Machine-Readable Filename Drift

- recurrence signal: older packet JSON artifacts still violate lowercase snake_case policy and reappear in linter runs
- current workaround: leave artifacts in place and treat them as a cleanup target
- structural fix candidate: rename or reclassify legacy packet JSON files under a controlled migration rule
- escalation trigger: if the same lint class appears again in new generated machine-readable artifacts

### Non-Canonical Path Drift

- recurrence signal: migrated documents and scripts occasionally retain earlier `analysis/` or pre-control paths
- current workaround: patch references when discovered during review or lint follow-up
- structural fix candidate: stronger path registry checks plus document-path linting
- escalation trigger: if a new active document or script reintroduces a pre-control canonical path

### Caption Completeness Drift

- recurrence signal: a completed caption in the phase-1 sample review ended mid-string while still passing the current structured-output contract
- current workaround: catch the issue during human sampling review before downstream reuse
- structural fix candidate: add a post-generation completeness validator or retry gate for truncated caption text
- escalation trigger: if another completed caption artifact shows incomplete sentence termination or obviously cut-off content

### Sandboxed macOS OCR Drift

- recurrence signal: macOS-native OCR paths can fail inside the sandbox while the same OCR call succeeds unsandboxed on the same local image
- current workaround: rerun OCR unsandboxed before concluding that an image contains no usable text
- structural fix candidate: explicitly mark native OCR as an unsandboxed execution surface in skills, task packets, and tool inventory
- escalation trigger: if another Vision-backed OCR or image-analysis tool shows the same sandbox-only failure pattern
- recent confirmation: the new full-image OCR context-package builder reproduced the same pattern on `image11.png`, returning a Foundation fallback error in sandbox and `ocr_status=usable` when rerun unsandboxed

### Vendored OCR Fallback Activation Drift

- recurrence signal: a complementary OCR fallback can be vendored and documented, but still fail to become an active runtime path because local build or activation steps are incomplete
- current workaround: keep the fallback as reference-only and continue using the validated MCP surface first
- structural fix candidate: add a standard vendor-activation checklist that requires a clean build or executable smoke before a vendored tool is promoted into the active tool surface
- escalation trigger: if another vendored CLI or Xcode-based helper remains half-integrated after clone, setup, and local smoke attempts

### System Skill Registry Drift

- recurrence signal: built-in system skills such as `imagegen` are available in the Codex runtime but omitted from workspace inventory because local documentation focuses on MCP launchers and custom skills
- current workaround: manually append a system-skill note to inventory and workspace references when the gap is discovered
- structural fix candidate: keep an explicit `system_skill_notes` section in tool inventory and cross-link it from workspace setup references
- escalation trigger: if another system skill is used in planning or execution without appearing in the workspace inventory or setup references
- adjacent recurrence: project-local MCP configs and promoted workspace skills can drift from `tool_inventory.json`; compare `.codex/config.toml`, `.vscode/mcp.json`, `tool_inventory.json`, and `skills/*/SKILL.md` together during audit
- current extension: keep global/system skill buckets separate from workspace custom skill buckets; do not let `global_codex_skills_confirmed` absorb repo-local skills such as `image-job-dispatcher` or `image-worker`

### Vendored Runtime Bootstrap Permission Drift

- recurrence signal: creating a venv or installing heavy dependencies inside `vendor/mcp/` can require escalated permissions or look incomplete until the long-running install process is explicitly rechecked
- current workaround: rerun the blocked step with escalation, then verify success by checking the installed executable or `pip show` rather than trusting the intermediate session state alone
- structural fix candidate: add a standard verification checklist for vendored runtime bootstrap that includes executable presence, import success, and help or boot checks
- escalation trigger: if another vendored MCP repeats the same permission or ambiguous-install-state pattern

### Stdio Stdout Pollution In Machine-Readable MCP

- recurrence signal: a stdio MCP emits human-readable output on stdout during startup, import, or first inference and risks colliding with transport traffic
- current workaround: move launcher diagnostics and vendored logging to stderr, redirect noisy library stdout during import/model load, and verify with a real MCP client transport
- structural fix candidate: add stdio hygiene review and client-based smoke to the default vendored MCP onboarding flow
- escalation trigger: if another stdio MCP needs patching because `print(...)`, default stdout logging, or library banners appear before or during tool calls

### Model Cache Path Permission Drift

- recurrence signal: model-backed libraries try to write cache or settings files into vendored source paths and fail under the current runtime until a writable override is exported
- current workaround: override cache-related env vars in the launcher and rerun the same inference tool to confirm the problem is environmental
- structural fix candidate: standard launcher cache-path override block plus an inventory note for required env vars
- escalation trigger: if another local ML MCP only becomes stable after redirecting settings or cache writes into workspace-owned directories

### Review Surface Bucket Drift

- recurrence signal: the same review artifact can end up under both `project_domain/runs/reports/` and `user_decisions/runs/` when a vault-like human review surface is treated as if it were already a decision record
- current workaround: keep the full review under `project_domain/runs/reports/` and only promote explicit decision outcomes into `user_decisions`
- structural fix candidate: tighten skill runtime examples and linter rules so review builders do not suggest `user_decisions` as the canonical first destination
- escalation trigger: if another run produces duplicate review markdowns across both buckets

### Batch-Specific Review Hardcoding Drift

- recurrence signal: a helper script or skill wrapper advertises itself as generic, but still embeds a named batch in defaults such as `phase1_caption_10w`, review headings, or output examples
- current workaround: patch the utility after review by making input globs and review titles explicit arguments
- structural fix candidate: add a review checklist for promoted scripts that rejects batch-specific defaults unless the utility is intentionally single-purpose
- escalation trigger: if another script promoted into `skills/` still carries a batch-specific default that changes its meaning outside the original run

### Mixed Review Asset Strategy Drift

- recurrence signal: review surfaces alternate between direct links, copied assets, and symlink-backed vault prefixes, making the canonical embed strategy unclear
- current workaround: prefer copied assets for the canonical review surface and treat symlink-prefixed vault paths as compatibility mode only
- structural fix candidate: document one canonical embed mode in the skill and push other modes into clearly labeled compatibility examples
- escalation trigger: if a future review surface fails to render or creates another ambiguous asset tree because multiple embed strategies remain equally implied

### Automatic Component Selection Semantic Drift

- recurrence signal: object-isolation smoke can succeed mechanically while `find()` returns no semantic match and `detect()` falls back to unrelated classes such as `darkness` or `cancer`
- current workaround: review the original image plus the selected crop before trusting the isolated component, and keep full-image OCR as the safer context surface
- structural fix candidate: add a semantic-selection gate that compares intended prompt, detected crop, and OCR usefulness before promoting isolated outputs
- escalation trigger: if another phase0 or object-isolation batch produces mechanically valid but semantically wrong crops
- recent confirmation: the alpha-only batch classified `9` files as `alpha_split_sufficient`, but several of those had very high disconnected-fragment counts such as `82`, `85`, `139`, and `140`, which shows that component count alone still over-promotes fragment-heavy slides

### Combined ImageSorcery And OCR Runner Drift

- recurrence signal: ImageSorcery and standalone OCR both work independently, but a combined Python runner can still produce OCR fallback failures after the isolation stage
- current workaround: split the verification into two steps and treat standalone OCR as the current truth source when combined-runner OCR disagrees
- structural fix candidate: isolate the OCR subprocess contract, add a dedicated smoke for combined orchestration, and avoid assuming that a successful standalone OCR call implies in-runner stability
- escalation trigger: if another integrated phase0 runner mixes local MCP/image tooling and OCR in one process and reproduces the same disagreement

### Context Package Prior Caption Leakage

- recurrence signal: a reviewed context package includes prior baseline caption text inside a summary field and the later rerun path is tempted to inject that whole field into the next prompt
- current workaround: sanitize prompt-bound context so OCR excerpt and PPT-local provenance survive, but prior caption or alt-text phrasing does not
- structural fix candidate: split review-facing context fields from prompt-safe context fields or enforce a sanitizer in the runner
- escalation trigger: if another reviewed context artifact contains prior model output and the next rerun path tries to consume it directly

### Open-Vocabulary Geometry Support Drift

- recurrence signal: text-prompted object finding appears available, but geometry return is unstable or unsupported in the same workspace/runtime
- current workaround: treat `find` as bbox-first, use `detect` when masks or polygons are required, and fall back to bounded imagegen repair when bbox-only isolation is not enough
- structural fix candidate: keep workspace-specific capability notes for model-backed MCP tools and verify bbox support separately from geometry support
- escalation trigger: if another open-vocabulary MCP or model path advertises geometry but fails the same way in workspace smoke

### Home-Scoped ML Cache Permission Drift

- recurrence signal: third-party ML runtimes default to cache or temp directories under the user home, then fail in the current workspace or sandbox because that path is not writable
- current workaround: inspect the runtime source or traceback, find the cache env var, and redirect it into a workspace-owned log or cache directory through the launcher
- structural fix candidate: add a standard `home cache override` block for model-backed launchers and record the exact env vars in tool inventory
- escalation trigger: if another MCP or CLI runtime fails because it tries to write under `~/.something` before the first real tool call

### Heavy First-Boot Verification Drift

- recurrence signal: an MCP appears installed because the executable and lockfile exist, but `--help` or first stdio boot still hangs, downloads models, or blocks on heavyweight initialization
- current workaround: separate installation verification from runtime verification, record an install smoke first, and defer `boot_verified=true` until a bounded boot smoke is captured
- structural fix candidate: formalize dual status fields such as `installed` and `boot_verified`, plus a standard smoke sequence for heavy runtimes
- escalation trigger: if another newly installed MCP is prematurely treated as active before first-run initialization behavior is audited

### Model Hoster Connectivity Precheck Drift

- recurrence signal: a model-backed runtime performs external hoster checks during import or startup even when the actual experiment only needs local mode, causing avoidable startup friction
- current workaround: disable the precheck through the launcher when the runtime supports it, then keep the actual local inference smoke as the source of truth
- structural fix candidate: add `hoster precheck bypass` review to the launcher hardening checklist for local-first ML MCPs
- escalation trigger: if another local-first inference runtime blocks or slows startup because of nonessential network reachability checks

### Mechanically Verified But Pipeline-Invalid Drift

- recurrence signal: a tool or MCP passes registration, boot, or basic smoke checks, but the output still does not improve the actual experiment path enough to justify batch promotion
- current workaround: keep the tool marked as available, but demote it from the active baseline until a pipeline-level comparison shows real utility
- structural fix candidate: formalize a second verification layer that separates `tool works` from `tool improves the target pipeline`
- escalation trigger: if another newly integrated capability passes technical smoke yet still degrades or fails the downstream experiment outcome

### Installed Parser Without Canonical Wrapper Drift

- recurrence signal: a parser runtime is successfully installed and registered, but the project still lacks the local normalization layer that maps raw parser output into the canonical schema and MCP surface
- current workaround: treat the parser as a candidate backend only, keep the canonical `Table -> Row -> Cell` layer conceptual, and defer `get_tables/get_table_rows/get_cells` exposure until normalization is implemented
- structural fix candidate: require a schema-normalization step and wrapper contract before any parser is treated as the project’s canonical table surface
- escalation trigger: if another parser or document-analysis backend gets marked active before its raw output is mapped into the project’s canonical schema

### Venv Interpreter Symlink Resolution Drift

- recurrence signal: a vendored Python runtime under `.venv/bin/python` is normalized with `Path.resolve()` and silently turns into the system interpreter path, dropping the venv package set
- current workaround: preserve the entrypoint path as entered or use `expanduser()` only, then verify the same workload with the intended vendored runtime
- structural fix candidate: standard runtime-path helper and code-review rule that forbids resolving `.venv/bin/python` style subprocess entrypoints
- escalation trigger: if another vendored Python worker or batch runner loses site-packages only after path normalization or reports a system interpreter in generated artifacts

### Import-Time Heavy Dependency Surface Drift

- recurrence signal: a local script or helper has a correct runtime implementation, but `--help` or other lightweight surface paths still fail because heavy libraries are imported at module import time
- current workaround: move `numpy`, `PIL`, or similar heavy imports into the runtime function that actually needs them, then verify both `--help` and the real execution path
- structural fix candidate: review rule that CLI surfaces should stay import-light unless the tool is intentionally single-runtime only
- escalation trigger: if another builder or helper requires the vendored runtime just to expose its CLI surface or breaks before argument parsing

### Manifest Key Drift In Provenance Recovery

- recurrence signal: a generated manifest exposes the right provenance data, but the lookup fails because the code assumes an older or alternative top-level key such as `images` instead of the current `exported_images`

### Subagent Sidecar Artifact Family Drift

- recurrence signal: a packetized subagent writes `runtime.md` or `troubleshooting.md` using ideal or future artifact-family names as if they were the current bounded evidence surface
- current workaround: re-verify the sidecar directly against real smoke artifacts, reports, tests, and file existence, then patch current-state language down to the proven bounded run
- structural fix candidate: require a post-subagent claim-verification pass before accepting sidecar pages into the active skill surface
- escalation trigger: if another packetized sidecar points to missing files or overstates current integration status instead of clearly labeling future-work contracts

### Subagent Read-Only Audit Timeout Nonblocking

- recurrence signal: a read-only explorer or auditor subagent is launched as an independent checker, but times out while the main agent is already able to verify the same files directly
- current workaround: keep the subagent audit nonblocking, finish the canonical verdict locally, and close the timed-out subagent
- structural fix candidate: encode in strategy docs that main-agent direct verification stays canonical whenever local evidence is already available
- escalation trigger: if a later workflow becomes blocked on a subagent audit result that the main agent could have verified directly
- current workaround: inspect the concrete manifest shape, patch the lookup, and rerun the smallest bounded artifact generation step
- structural fix candidate: central manifest-shape helper plus schema validation for provenance lookups before downstream normalization runs
- escalation trigger: if another bounded runner or normalizer writes empty provenance fields even though the source manifest already contains the needed data

### Smoke Runner Semantic Identity Drift

- recurrence signal: one bounded runner begins as a boot smoke helper, then grows into a richer parse or normalization surface while still emitting an older experiment name or status semantics
- current workaround: fix the emitted experiment identity, rerun the same bounded workload, and treat regenerated artifacts as the canonical truth
- structural fix candidate: separate runner modes explicitly or enforce output-contract checks that fail when artifact identity no longer matches the invoked mode
- escalation trigger: if another smoke or runner artifact is technically valid but mislabeled enough to confuse indexing, plan state, or downstream interpretation

### Warm-Cache But Still Long-Latency Parser Drift

- recurrence signal: a model-backed parser has all required weights cached locally, yet bounded real-image calls still take minutes and can be mistaken for a hung or broken process
- current workaround: distinguish cache-hit progress from true deadlock, keep generous bounded timeouts for the first real parse slice, and rely on produced artifacts instead of silence on stdout alone

### True Small-Batch Bundle Absent For Nonregenerative Eval

- recurrence signal: an evaluation consumer is mechanically ready, but the repo does not yet contain a true multi-image frozen bundle covering the requested arm set without regenerating upstream deterministic artifacts
- current workaround: let the consumer close on the existing template bundle, emit an explicit waiver, and keep the result labeled as `1-image template consumption` rather than `small-batch readiness`
- structural fix candidate: shared-closure-set bundle assembly that only promotes to small-batch once multiple images have every required arm closed
- escalation trigger: if another evaluation lane is described as small-batch even though only one image exists in the shared closure set
- structural fix candidate: add latency expectations and phase markers for `boot`, `tool list`, and `real parse` in the smoke runner contract
- escalation trigger: if another parser-backed MCP repeatedly looks stalled after cache warm-up and causes false failure diagnosis

### Anchor-Ready But Full-Comparison-Incomplete Drift

- recurrence signal: a subset of experiment arms is already comparison-ready and gets mistaken for a fully runnable multi-arm comparison
- current workaround: publish a bounded anchor comparison artifact first and mark the remaining arms as pending, waived, or blocked instead of implying full readiness
- structural fix candidate: explicit readiness states such as `anchor_ready`, `merge_ready`, `waived`, and `blocked` in comparison manifests and reports
- escalation trigger: if another plan starts scheduling a full comparison from only partial arm readiness

### Pending-Review Rerun Promotion Drift

- recurrence signal: a rerun appears richer than the current baseline, but the enabling context package or evidence bundle is still `pending_review`
- current workaround: keep the rerun in `comparison_only` state and preserve the existing baseline as the current default until the review gate closes
- structural fix candidate: promotion-state enforcement in comparison builders so reviewed gates are checked before default promotion
- escalation trigger: if another enriched rerun is treated as the new default before its context review state is closed

### Cross-Arm Comparison Contract Parity Drift

- recurrence signal: two or more arms refer to the same source image, but differ in visible comparison fields such as `input_surface`, `prompt_version`, `review_status`, or provenance shape, which makes side-by-side interpretation misleading
- current workaround: normalize every arm into a shared comparison record that carries source-image equality, ledger reference, execution arm, input surface, prompt version, and review gate fields
- structural fix candidate: require a common comparison schema before any new arm can be merged into a multi-arm report
- escalation trigger: if another arm is added to a comparison surface without the parity fields needed to explain what actually changed

### Partial Arm Readiness Overstated As Full Comparison Ready

- recurrence signal: several arms are already runnable, but a blocked or waived arm is quietly ignored and the workspace starts speaking as if the full planned comparison is ready
- current workaround: publish ready count, blocked arms, waiver status, and a final yes or no readiness verdict in the summary report
- structural fix candidate: comparison readiness template that separates `ready_for_comparison`, `waived`, and `blocked` states from the final full-experiment readiness decision
- escalation trigger: if another staged experiment starts calling itself fully ready when only a subset of arms has actually closed

### Sandboxed macOS OCR Fails On Derived Component Images

- recurrence signal: a newly derived crop or reviewed component image fails macOS OCR in sandbox even though the same image succeeds unsandboxed and remains semantically useful
- current workaround: rerun OCR unsandboxed on the derived image before waiving the reviewed branch, then preserve both the sandbox failure and the unsandboxed success as evidence
- structural fix candidate: explicit OCR-runtime policy for derived images that distinguishes source-image OCR from crop-image OCR behavior on macOS
- escalation trigger: if another reviewed component or derived crop is treated as low quality when the real problem is sandboxed OCR runtime failure

### Repo-Local Semantic Judge Harness Absent

- recurrence signal: a bounded comparison surface is already implemented and comparison-ready, but the repo still lacks a first-party semantic judge runner for the same evaluation scope
- current workaround: emit a frozen eval bundle, write a judge waiver, and preserve a manual qualitative summary without mutating promotion state
- structural fix candidate: later evaluation-overlay runner that consumes the frozen bundle directly instead of re-reading raw ledgers
- escalation trigger: if another comparison lane becomes ready and the workspace starts implying semantic judge execution without an actual local harness

### OCR Proxy False Negative On Clean Reviewed Crop

- recurrence signal: a reviewed crop looks semantically cleaner than the full image, but the OCR proxy comparator still returns `false` because the baseline already has zero extras or the crop introduces a couple of harmless OCR artifacts
- current workaround: preserve the OCR proxy evidence, then escalate the specific image pair to direct GPT image verification instead of forcing a waiver
- structural fix candidate: hybrid reviewed-branch gate that combines OCR proxy with a bounded direct-image semantic tie-break for edge cases
- escalation trigger: if another reviewed branch stays blocked even though the crop visually preserves the full table and clearly suppresses non-table noise

### Single-Backend Failure Masks Alternate Four-Mode Closure

- recurrence signal: one derived-arm backend fails on an image and the workspace starts treating that image as excluded, even though another backend or single-source fallback could still close the same arm set
- current workaround: do not stop at the first failed parser/helper backend; verify whether the remaining evidence stack can still produce parser-enriched and reviewed-component artifacts before excluding the image
- structural fix candidate: explicit `alternate closure route` check in eligibility scans so backend-specific failures do not collapse the whole image prematurely
- escalation trigger: if another image is marked nonready because Apple, parser, or OCR helper failed once while a second backend could still close the bounded branch

### Runner Output Fresh But Canonical Manifest Stale

- recurrence signal: a runner prints correct updated batch state in stdout or returns the expected object in-memory, but the canonical file on disk remains stale at an older image set or summary
- current workaround: verify the on-disk manifest directly after every regeneration and, if needed, call the underlying library or write path explicitly to force canonical output refresh
- structural fix candidate: add post-write readback validation inside the runner so it fails loudly when stdout truth and disk truth diverge
- escalation trigger: if another bounded regeneration claims success but the canonical manifest still reflects the previous cohort or winner counts

### Late Cohort Expansion Outruns Closure And Registry Sync

- recurrence signal: a new image is correctly promoted into the stable cohort, but closure reports, master plan text, artifact index, or session registry still describe the earlier cohort size and winner distribution
- current workaround: treat producer and consumer regeneration as incomplete until closure docs and registries are patched to the same cohort size, image list, and promotion interpretation
- structural fix candidate: require a final `truth sync` phase after every cohort expansion that checks docs and registry surfaces against the canonical manifests
- escalation trigger: if another small-batch or corpus-ready cohort grows while user-facing closure docs still cite the old image set

### Aggregate Bundle Truth-Source Drift For Downstream Consumer

- recurrence signal: decision-level readiness is already correct, but the downstream consumer still points at an older or stale aggregate bundle shape
- current workaround: verify the aggregate image set first, then let the consumer close on per-image frozen bundles if aggregate freshness is not yet trustworthy
- structural fix candidate: dual-input consumer normalization plus explicit `actual_input_mode` and resolved bundle-path recording in the downstream artifact
- escalation trigger: if another evaluation lane reuses a stale aggregate file even though fresher per-image frozen bundles already exist

### Seed-BBox-Only Reviewed Crop Truncation On Multi-Component Images

- recurrence signal: a reviewed crop is built only from a parser-derived seed bbox, while nearby disconnected alpha components still hold title or context that belongs to the same useful caption surface
- current workaround: preserve the seed bbox as anchor, enumerate nearby alpha components, build a bounded recrop candidate such as `alpha_nearby_union`, then select the final reviewed crop through the same OCR-proxy comparison surface
- structural fix candidate: generalized reviewed-component candidate selection with explicit skip/selection metadata for nearby-component union recrops
- escalation trigger: if another reviewed branch is treated as weak or excluded only because the seed-only crop truncated meaningful nearby context

### Custom Editor Active-Text-Editor Drift

- recurrence signal: a custom markdown editor renders the visual review surface correctly, but extension features that depend on `window.activeTextEditor.document` lose command support or autocomplete
- current workaround: reopen the note with `Text Editor` before `[[wikilink]]` authoring or commands such as `Foam: Update Wikilink Definitions`, and keep the custom editor only for same-page visual editing
- structural fix candidate: explicit split-surface runtime contract plus a mode-switch helper that updates `workbench.editorAssociations` and relaunches the workspace or target file
- escalation trigger: if another custom editor or workspace review surface reproduces the same `activeTextEditor`-bound extension failure
- current proven example: `fabriqa` same-page image editing combined with `Foam` backlinks and link-definition commands

### Master-Plan Reread Overhead On Parallel Bounded Sessions

- recurrence signal: parallel producer/consumer sessions keep re-entering through broad plan documents even though the actual slice only depends on a small frozen truth subset
- current workaround: issue a fast-start packet with explicit truth sources, fixed interpretation, owned paths, and non-goals so the session can begin immediately
- structural fix candidate: packet-first session split workflow for bounded experiment slices
- escalation trigger: if another parallel bounded session spends more effort reconstructing plan context than executing its own slice

### Nested-Only Consumer Provenance Drift

- recurrence signal: a consumer artifact is logically correct, but downstream readers still have to inspect nested helper sections just to discover input mode, resolved truth-source paths, or winner frequency
- current workaround: preserve the nested detail, but also surface the key provenance and summary fields at the top level of the canonical consumer manifest
- structural fix candidate: explicit top-level consumer projection rule for downstream eval outputs
- escalation trigger: if another eval manifest remains programmatically awkward even though the underlying truth is already correct

### Regrouping-Only Fix Stalls Without Component Decomposition

- recurrence signal: a composite image still feels semantically unresolved after better crop union or regrouping logic, because the underlying components were never decomposed cleanly in the first place
- current workaround: stop treating regrouping as the whole solution, gather bounded external references for layout or compound-figure decomposition, and reopen implementation as a staged `decomposition -> regrouping -> scoring` problem
- structural fix candidate: explicit decomposition stage before regrouping for composite analytical images
- escalation trigger: if another edge case keeps oscillating between exclusion and recrop tweaks without ever getting a real component decomposition strategy
- current strategy reference: `REFERENCE_component_decomposition_strategy-at2026-03-30.md`

### Table-Seed Dependency Blocks Compound Dashboard Reentry

- recurrence signal: full-image OCR is usable and the image looks decomposable, but parser/reviewed reentry stays blocked because no stable table seed exists
- current workaround: stop retrying table-seeded reviewed recrop first and run a decomposition probe that can surface title/chart/lower-summary regions without a table seed
- structural fix candidate: decomposition stage that can begin before parser-normalized table cells exist
- escalation trigger: if another dashboard-style image is visually structured but still cannot enter reviewed recrop because the pipeline requires table-cell seed data too early

### Objective-Profile Mismatch Hides True Candidate Winner

- recurrence signal: a narrow regrouped candidate looks strong, but only because the scoring objective silently drifted from dashboard-overview intent to table-focus intent
- current workaround: record one current objective profile and one contrast profile, then keep the mainline recommendation bound to the current objective only
- structural fix candidate: explicit objective-profile scoring gate before re-entry or promotion
- escalation trigger: if another composite figure keeps oscillating between full-image and narrow-crop recommendations because the scoring objective was never made explicit

### Ambiguous Registry Namespace Role Mixing

- recurrence signal: a single `registry/*` bucket keeps surviving because it sounds convenient, but the contents actually represent different synchronization roles such as runtime path maps and job ledgers
- current workaround: inspect the concrete files, split them into narrower registry homes with one dominant meaning each, and update rules so the old mixed namespace is explicitly noncanonical
- structural fix candidate: registry-namespace lint rule that rejects generic buckets once their contents map cleanly onto more specific registry roles
- escalation trigger: if another residual registry subtree bundles unrelated synchronization bodies under one vague name after a migration
- current proven example: `control/project_agent_ops/registry/runs/` mixed session-path synchronization with image-caption job ledgers until it was decomposed into `registry/runtime/` and `registry/jobs/`

### Empty Namespace Residue After Role Absorption

- recurrence signal: a directory remains in the control tree after its semantic role has already been absorbed by existing registry files elsewhere, leaving an empty namespace that looks official but carries no body
- current workaround: verify the directory is empty and unreferenced, confirm that the actual synchronization role already lives in existing registry bodies, then remove the empty namespace and document why it is no longer canonical
- structural fix candidate: periodic empty-namespace audit for `control/*/registry/` and `control/*/resources/` plus explicit rules for when a reserved bucket is allowed to exist
- escalation trigger: if another empty control namespace survives migration and starts creating ambiguity about where the real canonical body lives
- current proven example: `control/project_agent_ops/registry/skills/` remained as an empty bucket after skill inventory settled under `registry/tools/tool_inventory.json` and runtime path sync settled under `registry/runtime/session_paths.json`

### Migration-Complete But Active Surface Still Uses Legacy Paths

- recurrence signal: a migration report says the filesystem move is complete, but active tests, packets, specs, or plans still fail because they hardcode pre-migration canonical paths
- current workaround: treat the migration as incomplete until active surfaces are rescanned, patch only the live references, rerun bounded tests, and leave historical documents unchanged as migration evidence
- structural fix candidate: post-migration active-surface verification step that checks tests, executable scripts, task packets, and specs before the migration can be called finished
- escalation trigger: if another control or registry migration is declared done before active runtime-facing documents and tests stop referencing the legacy paths
- current proven example: after the 2026-03-30 control-tree cleanup, active references in issued task packets, caption specs, experiment plans, and two caption-eval tests still pointed at `control/project_agent_ops/registry/runs/` or `control/project_domain/runs/`

### Unicode Path Normalization Drift In Control-Tree Lint

- recurrence signal: the control-tree lint works on one absolute path spelling of the repo, but crashes when scanned paths and repo-root paths use different Unicode normalization forms such as NFC vs NFD
- current workaround: normalize both absolute path strings before computing repo-relative paths, then keep lint output string-based instead of relying on raw `Path.relative_to(...)`
- structural fix candidate: centralized normalized-path helper for all control-plane scripts that compare absolute paths across macOS filesystems
- escalation trigger: if another lint, migration, or registry script crashes only on one path spelling of the same workspace
- current proven example: `lint_control_tree.py` crashed on 2026-03-30 when `my-image-parser` was referenced through mixed normalized Korean path spellings

### Decision-Support Overlay Drift Into Master Plans

- recurrence signal: user-facing dashboards, task graphs, scoreboards, or current-state overlays get written under `control/project_domain/resources/master_plans/` because they discuss the master plan, even though their real role is decision support
- current workaround: move the canonical overlay into `control/user_decisions/resources/notes/`, leave a redirect stub only if path continuity matters, and add a warning-only lint rule for future drift
- structural fix candidate: explicit placement contract plus filename/lint classifier for decision-support overlays
- escalation trigger: if another status-reading surface is filed under `master_plans` instead of `user_decisions`
- current proven example: `REFERENCE_master_plan_progress_dashboard-at2026-04-05-09-17.md` and `REFERENCE_master_plan_task_graphs-at2026-04-05-09-17.md` were moved out of `master_plans` on 2026-03-30

### Comparison Winner And Active Default Conflation In Review Surfaces

- recurrence signal: a comparison artifact clearly identifies a per-image winner, but downstream readers start treating that winner as if it were already the active default because the review surface does not separate winner state from default-retention policy
- current workaround: always render `current default`, `comparison winner`, `winner promotion state`, and `why default stays default` as separate fields in the human-facing review surface
- structural fix candidate: mandatory review-surface contract that splits comparison outcome from default-promotion status for every image row
- escalation trigger: if another review or dashboard artifact reports a winner without also showing baseline retention and promotion-state guardrails
- current proven example: the 2026-03-30 phase-2 four-mode corpus review surface needed explicit default-vs-winner separation for all 9 images

### Review Markdown Reopened Instead Of Manifest Truth

- recurrence signal: a review flow already emits a machine-readable manifest, but a later consumer reparses the markdown review and duplicates logic that was already canonically captured in structured fields
- current workaround: if the review surface declares `machine_truth_source = manifest` and `markdown_human_facing_only = true`, downstream machine consumers must read the manifest only
- structural fix candidate: manifest-first review-consumer contract plus lint/checklist rule against markdown reparsing when machine truth was already emitted
- escalation trigger: if another review-to-consumer bridge starts parsing prose markdown again or manually reconstructing priority/default/winner fields that are already present in the manifest
- current proven example: the 2026-03-30 `phase2` corpus review surface let `Session B` build retrieval and mapping preflight seeds entirely from the manifest

### Decision Seed Contract And Seed Row Shape Drift

- recurrence signal: a prose spec and machine-readable contract describe one review decision row shape, but the generated seed JSONL still follows an older nested-template layout
- current workaround: regenerate the seed immediately after contract changes and verify that required flat fields exist on every row before downstream consumers use it
- structural fix candidate: contract-first regeneration check plus one bounded ingestion smoke after every decision-capture schema change
- escalation trigger: if another decision-capture workflow updates the contract or report vocabulary without regenerating the canonical seed rows
- current proven example: the 2026-03-30 `phase2` corpus decision capture briefly diverged until the Session B bridge regenerated the seed into the flat row contract

### Zero-Ready State Hidden Without Dry-Run Manifest

- recurrence signal: all decision rows are still pending, but no explicit downstream artifact states that retrieval or mapping are blocked only because no completed rows exist
- current workaround: emit dry-run manifests with `ready_to_execute = false`, a stable `blocked_reason`, and the planned downstream outputs whenever ready subsets are empty
- structural fix candidate: mandatory dry-run reporting stage after decision ingestion when ready counts are zero
- escalation trigger: if another phase reaches decision ingestion and downstream readers still have to infer blocked state from empty JSONL files alone
- current proven example: the 2026-03-30 `phase2` dry-run manifests made the zero-ready retrieval and mapping state explicit

### Canonical JSONL Concurrent Edit Collision Risk

- recurrence signal: a review workflow keeps one canonical JSONL as the editing surface, but more than one reviewer may touch it and no row ownership or locking rule exists
- current workaround: freeze the canonical file to one active writer, require owned image ids or reviewer-local working copies for parallel review, and merge before ingestion
- structural fix candidate: row-level ownership or lock-aware helper for canonical JSONL review entry
- escalation trigger: if another reviewer or agent is expected to edit the same canonical seed concurrently
- current proven example: the 2026-03-30 `phase2` review-decision entry surface initially had no ownership rule and had to be hardened with a single-writer policy

### Machine-Prefilled Review Seed Drift Hidden Until Late Consumer Failure

- recurrence signal: upstream review truth is copied into editable seed rows, but the workflow relies only on prose warnings such as “do not edit these fields,” so accidental changes stay invisible until later ingestion or downstream consumers misbehave
- current workaround: compare immutable seed fields and row order directly against the review-surface manifest before materializing any ready subsets, and fail fast on the first mismatch
- structural fix candidate: generic immutable-prefill validator for human-edited machine-seeded artifacts
- escalation trigger: if another editable seed carries copied machine truth without an automated drift check at the earliest bounded consumer boundary
- current proven example: the 2026-03-30 `phase2` decision ingestion now raises `Machine-prefilled field drift detected` instead of silently accepting edited machine fields

### Synthetic Human-Edited Arm Breaks Promotion-State Assumptions

- recurrence signal: a decision contract introduces `human_edited_caption` as a selectable arm even though promotion-state enums were defined only for upstream generated arms
- current workaround: treat the synthetic arm as a null-promotion-state exception and couple it to explicit edit-required semantics instead of trying to map it onto an existing promotion-state label
- structural fix candidate: contract rule template for synthetic reviewed outputs that are selectable but not promotable upstream arms
- escalation trigger: if another approval surface allows reviewer-authored text but still asks operators to choose from upstream arm-state enums
- current proven example: the 2026-03-30 `phase2` corpus review decision contract had to add an explicit `human_edited_caption -> selected_caption_promotion_state = null` rule

### Structure Philosophy Exists In Docs But Not In Lint

- recurrence signal: a workspace has a clear control-plane philosophy such as `root > control > project meaning > action unit`, but the linter only checks filenames and a few placement cases so structural drift keeps leaking in
- current workaround: keep the philosophy in canonical rules, then add targeted lint warnings for the few boundaries that matter most, such as non-canonical action-unit buckets and exceptional `control/*/resources/scripts` usage
- structural fix candidate: philosophy-to-lint mapping process that turns accepted structure rules into small, staged warning codes instead of leaving them prose-only
- escalation trigger: if another control-plane cleanup has to be explained repeatedly because the canonical structure is documented but not mechanically surfaced
- current proven example: `my-image-parser/control/team/resources/scripts/lint_control_tree.py` now warns on non-canonical action-unit directories and non-team `control/*/resources/scripts` usage

### Old-Root Drift Detection Without Allowlist Creates Migration Noise

- recurrence signal: a repo adds stale-path detection after a workspace migration, but the first scan flags intentional migration checklists, reports, and handoff docs that legitimately mention the previous root
- current workaround: treat migration/checklist/report/handoff paths as an explicit allowlist and reserve warnings for active canonical docs and copied runtime references
- structural fix candidate: stale-path lint contract with required allowlist categories for migration-era documents
- escalation trigger: if a stale-path scan becomes noisy enough that operators start ignoring it entirely
- current proven example: the `vscode-markdown-review-surface` old-root scan was designed to skip migration-like contexts so that only real `my-image-parser` drift remains actionable

### Large Lint Output Hides The Real Structural Blocker

- recurrence signal: the raw lint result mixes archive inheritance, preserved payload naming, evidence-placement drift, and active structure violations into one long list, making it hard to decide what actually blocks the next canonical move
- current workaround: create a baseline split that isolates active structural violations from legacy debt before choosing cleanup work
- structural fix candidate: standard lint-baseline reporting step whenever findings exceed direct human readability
- escalation trigger: if another large lint run again drives discussion into raw counts instead of the small set of true active blockers
- current proven example: the `my-image-parser` control-tree lint currently reports `317` findings, but the first active-structure split shows only `2` immediate structural violations

### Image Evidence And Text Judgment Drift Apart

- recurrence signal: a multimodal review surface shows the correct image evidence, but the accompanying text either overcommits, underdescribes, or quietly points at a different fact than the image actually supports
- current workaround: separate raw observation text from final decision text, keep the image visible next to both, and force short fact-like observation fields before any promotion or default-retention language
- failure signature: once one paragraph starts mixing `what is visible`, `what changed`, and `what should be done`, later readers can no longer tell which parts are evidence and which parts are policy interpretation
- structural fix candidate: multimodal review contract that distinguishes `evidence`, `observation`, `comparison`, and `decision` layers instead of allowing one blended paragraph
- escalation trigger: if another image-heavy review or debugging surface starts producing prose that reads persuasive but no longer traces cleanly back to the displayed image
- current proven example: repeated caption-review and surface-debugging work showed that image evidence stays stable while mixed narrative text drifts fastest

### Comparison Outcome And Policy Decision Collapse Into One Field

- recurrence signal: a surface correctly computes a winner or before/after delta, but operators start reading that outcome as if the policy decision to promote or replace the current default has already been made
- current workaround: split comparison outcome from policy decision using stable fields such as `winner`, `baseline/default`, `promotion state`, and `reason`
- failure signature: visually strong candidates get interpreted as already-approved replacements because the unresolved policy state is not given equal weight with the comparison result
- structural fix candidate: mandatory separation between comparison fields and policy-state fields in multimodal decision surfaces
- escalation trigger: if another review artifact or dashboard reports a better-looking candidate and readers immediately assume the baseline changed
- current proven example: phase-2 caption review needed explicit `current default` and `comparison winner` separation to stop downstream readers from conflating the two

### Human Reading Order And Machine Schema Order Diverge

- recurrence signal: a human-facing review surface is arranged for visual judgment, but the machine-readable schema stores the same facts in a different order or grouping, causing later drift when consumers reconstruct meaning differently
- current workaround: define one canonical field order for machine truth, then make the human surface follow that same semantic grouping even if the visual card layout is richer
- failure signature: humans read top-to-bottom as `image -> observation -> winner -> decision`, while the manifest is encoded as `status -> winner -> default -> reason`; later bridges silently reinterpret intent from the wrong field order
- structural fix candidate: paired human/machine schema mapping for review surfaces with explicit field-group parity
- escalation trigger: if another markdown review, dashboard, or decision bridge needs to re-derive field meaning because the human order and manifest order no longer line up
- current proven example: priority, default/winner split, and promotion fields had to be re-fixed in the phase-2 review manifest so downstream consumers could ignore prose safely

### Ambiguous Multimodal State Hidden Without Explicit Pending Marker

- recurrence signal: an image/text comparison produces a plausible candidate improvement, but the real state is still `pending_context_review`, `ambiguous`, or otherwise not ready for promotion, and the surface does not visually emphasize that deferment
- current workaround: surface pending or ambiguous states as first-class markers and elevate them in priority ordering instead of burying them inside explanation text
- failure signature: the image looks compelling and the prose sounds optimistic, so reviewers mentally collapse `candidate` into `approved` unless the unresolved state is more visually salient than the candidate itself
- structural fix candidate: review-surface rule that every unresolved multimodal item must carry an explicit pending/ambiguous state field plus a visual emphasis contract
- escalation trigger: if another reviewer or downstream agent mistakes a visually strong candidate for an approved default simply because the unresolved state was not made salient enough
- current proven example: `comparison_only_pending_context_review` arms in the caption corpus had to be highlighted separately from ordinary winner/default comparisons

### Owner-Family Charter Drift Between YAML, Family Map, And Adjacent Skill Docs

- recurrence signal: an owner-family skill is correctly narrowed at the YAML level, but the body, family-map labels, routing tree, or adjacent consumer skill docs still use broader nouns such as `workspace MCP lifecycle` and quietly widen the effective routing surface again
- current workaround: treat the YAML description as the routing contract, then audit the family map, routing tree, checklist, and adjacent consumer skills together so the same noun boundary and routing-status vocabulary survive across every surface
- failure signature: reviewers think the owner skill canonically owns all tool lifecycle questions, while the repeated-task evidence actually only justifies a narrower primary charter such as `vendor -> launcher -> config -> inventory -> smoke` for vendored MCPs
- structural fix candidate: one canonical verb/noun self-check plus one shared routing-status enum reused across YAML, family maps, and adjacent consumer backlinks
- escalation trigger: if another owner-family documentation pass fixes one surface but leaves enum drift, broadened noun scope, or MCP-only routing language in nearby docs
- current proven example: the 2026-04-01 `vendored-mcp-onboarding` family docs needed repeated tightening to separate canonical vendored-MCP ownership from temporarily routed non-vendored surfaces and to keep consumer backlinks aligned

### MCP-Only Vocabulary Residual In Adjacent-Surface Documents

- recurrence signal: after an owner skill's charter is broadened to include non-vendored adjacent surfaces, MCP-specific vocabulary persists in table headers (`Primary MCP Surface`), Consumer Layer intro sentences (`These skills use MCPs`), pre-routing check phrasing, and individual `What It Does Not Own` cells even when those rows have no MCP dependency
- current workaround: audit every location that uses domain-type vocabulary (MCP, tool, surface) and update each to the broadened noun that matches the actual scope; rename table headers from `Primary MCP Surface` to `Primary Lifecycle Surface`, update intro sentences, and change individual cells that contain `MCP lifecycle` to `tool lifecycle` when the row's primary surface is not an MCP
- failure signature: a reviewer reads the Consumer Layer table and concludes that all rows must depend on an MCP because the header and intro say so, even though some rows explicitly show `—` for their primary surface
- structural fix candidate: include a vocabulary audit step in the family-map drift prevention checklist; specifically check that table headers, intro sentences, and individual cells use the broadest noun that correctly describes their actual scope
- escalation trigger: if a subsequent review pass finds MCP-only language surviving in a table, cell, or routing check that was supposed to cover adjacent or consumer-only surfaces
- current proven example: the `vendored-mcp-onboarding` family map required three rounds of vocabulary correction to eliminate all residual `MCP` references from rows and sections that covered adjacent tools and consumer-only skills

### Execution Skill YAML Description Too Broad For Owner Family Membership

- recurrence signal: after enrolling a specialist skill into an owner family, the YAML description still uses owner-level verbs or nouns that overlap with the semantic owner's trigger surface
- current workaround: iterative description-only narrowing across 2~4 review rounds, each catching residual broad verbs missed in the previous pass
- failure signature: pre-routing picks the specialist when the owner should have been selected, because the specialist description still says `review surface`, `semantic selection`, or `inspection artifact`
- structural fix candidate: verb taxonomy checklist (`owner: reinject/refine/compare/close/normalize/derive` vs `specialist: run/extract/export/build/render/operate/audit`) applied before enrollment
- escalation trigger: if a review round still finds owner-level verbs after 2+ narrowing passes on the same file
- current proven example: `component-split-ocr-review` needed 3 description rewrites; `macos-ocr-evidence` and `vscode-fabriqa-foam-workflow` each needed 2 passes during the 2026-04-02 owner family enrollment session

### Handoff Placement Inconsistency Across Specialist Skills In Same Family

- recurrence signal: when multiple specialist skills in the same owner family receive handoff links in different sections (`Do Not Use` vs `Not Owned Here`), subsequent patches drift because editors copy the nearest example rather than a consistent rule
- current workaround: unify all handoff to `Not Owned Here` end, keep `Do Not Use` for trigger routing only; apply consistently across all specialists in one pass
- failure signature: a reviewer edits one specialist by copying the handoff style from a sibling specialist and introduces a mixed pattern (`Do Not Use` + `Not Owned Here` both carrying owner links)
- structural fix candidate: family enrollment checklist that requires handoff in exactly one canonical section (`Not Owned Here`) with a fixed 2-line format per owner
- escalation trigger: if a post-enrollment review finds mixed handoff placement within the same family
- current proven example: `obsidian-caption-review-builder` initially had handoff in `Do Not Use` while `image-result-auditor`, `component-split-ocr-review`, `openai-image-caption-validation` had it in `Not Owned Here`; unified to `Not Owned Here` during the 2026-04-02 session

### Over-Routing Via Missing Lifecycle-Touch Gate In Non-Primary Branch

- recurrence signal: a routing decision procedure has a lifecycle-touch gate in the primary (canonical) branch — routing proceeds only if the task touches launcher, config, inventory, setup, or smoke — but an equivalent gate is absent from the adjacent or temporarily-routed branch, causing consumer-only use of adjacent tools or system skills to incorrectly route to the owner skill
- current workaround: add the same lifecycle-touch gate condition to every non-consumer branch in the routing procedure, not only the primary branch; if the task only uses the surface's output, it should fall through to the consumer-only path regardless of which surface type it uses
- failure signature: a task that simply calls `imagegen` or reads from `filesystem` routes to the owner skill because it matched the adjacent-surface branch before the lifecycle-touch condition was checked
- structural fix candidate: routing procedure review rule that requires every non-consumer branch to carry an explicit `only if the task touches lifecycle surfaces` gate clause; treat missing gates as a structural defect, not a style choice
- escalation trigger: if another routing procedure fix or expansion adds a new surface branch without adding a lifecycle-touch gate, reopening the over-routing path
- current proven example: the `vendored-mcp-onboarding` quick pre-routing check had a gate in step 1 (vendored MCP) but not in step 2 (adjacent tools), causing any adjacent-tool task to route to the owner before the lifecycle condition was enforced

### Unconditional Checklist Item N/A Fatigue

- recurrence signal: a checklist item that applies only to a minority of runs — typically one with an `if this surface has...` or `if dependencies include...` condition — is added to a generic checklist without a skip condition, causing most runs to encounter a gate that is always N/A for that context and eventually treat the item as boilerplate noise
- current workaround: add an explicit skip condition as a parenthetical prefix on the checklist item, e.g., `*(skip if Supporting Tool Surface contains no system skills)*`; the skip condition must be checkable before the item body is read, not embedded at the end
- failure signature: operators run the checklist repeatedly and mechanically mark the conditional item as N/A without reading its body, which means the condition it was meant to catch is no longer being evaluated
- structural fix candidate: checklist authoring rule that requires any conditional item to carry its skip/apply guard as the first token, not embedded in the item body; use `*(N/A unless X)*` or `*(skip if not X)*` phrasing
- escalation trigger: if a post-run checklist review shows a conditional gate being marked N/A without a documented reason, suggesting the skip condition was not evaluated consciously
- current proven example: the `mcp_inventory_sync_checklist.md` system-skill coverage check was initially added as an unconditional final-gate item; it was converted to a conditional `*(skip if Supporting Tool Surface contains no system skills)*` item after the fatigue risk was identified

### Owner Body Guardrail Gap After YAML-Only Edit Rounds

- canonical source: `claude-gemini-communicator/skills/Skills-Create-Project/skill-creation-process/references/repeated-task-and-issue-patterns-at2026-03-19-13-34.md` Issue 21
- imported from: claude-gemini-communicator skill-creation-process references
- last synced: 2026-04-03
- recurrence signal: owner YAML description is well-formed with specialist routing, but the body lacks Do not use, Family Roles, and Workflow sections, causing closure checklist items 3 and 6 to fail
- current workaround: insert the missing 3 sections in a separate pass after YAML stabilization
- failure signature: closure checklist reports partial failure even though YAML audit passes cleanly
- structural fix candidate: extend the YAML-first editing protocol to include a mandatory body guardrail backfill step before declaring YAML editing complete
- escalation trigger: if another owner skill passes YAML audit but fails body guardrail closure in a subsequent audit round
- current proven evidence: Band 4 (codebase-analysis), Band 6 (artifact-lifecycle-manager), Band 8 (multimodal-evidence-refinement-loop) in the claude-gemini-communicator workspace all had the same 3-section gap during 2026-04-02/03 full-taxonomy closure

### Read Order Presence Mistaken For Workflow Presence

- canonical source: `claude-gemini-communicator/skills/Skills-Create-Project/skill-creation-process/references/repeated-task-and-issue-patterns-at2026-03-19-13-34.md` Issue 22
- imported from: claude-gemini-communicator skill-creation-process references
- last synced: 2026-04-03
- recurrence signal: an owner skill has a Read Order section (knowledge loading order) that is mistaken for a Workflow section (action sequence), causing the closure guardrail check to appear passed when it has not
- current workaround: treat Read Order and Workflow as distinct sections with different purposes; add Workflow separately even when Read Order exists
- failure signature: a skill auditor marks Workflow as present because Read Order exists, then downstream consumers expect action steps but find only a file reading sequence
- structural fix candidate: closure checklist item 6 should explicitly note that Read Order does not satisfy the Workflow requirement
- escalation trigger: if another audit marks Workflow as present based on a non-Workflow section such as Read Order, Quick Start, or Setup
- current proven evidence: `codebase-analysis` and `artifact-lifecycle-manager` both had Read Order but no Workflow during the 2026-04-02/03 closure audit

### Closure Patch Introduces Adjacent Band Vocabulary

- canonical source: `claude-gemini-communicator/skills/Skills-Create-Project/skill-creation-process/references/repeated-task-and-issue-patterns-at2026-03-19-13-34.md` Issue 24
- imported from: claude-gemini-communicator skill-creation-process references
- last synced: 2026-04-03
- recurrence signal: when filling a closure gap by writing new body content, the writer defaults to familiar vocabulary from an adjacent band rather than staying within the target band's verb taxonomy
- current workaround: cross-check newly written action phrases against the target band's owner verb taxonomy, replace adjacent-band verbs with handoff expressions
- failure signature: Gemini or reviewer flags the new content as overlapping another band's ownership surface
- structural fix candidate: pre-write checklist that maps the target band's allowed verbs before drafting new Workflow or Do not use content
- escalation trigger: if another closure patch introduces vocabulary from a different band and requires a post-hoc micro-patch
- current proven evidence: Band 4 (codebase-analysis) Workflow step 4 used "KB/checklist/export 정리" (Band 2 artifact production vocabulary), narrowed to "handoff-ready evidence package" after Gemini review

### Day-Only User-Facing Timestamp Drift Persists After Rule Adoption

- recurrence signal: a workspace adds a lint rule requiring minute-level timestamp suffixes for user-facing notes, but the existing notes remain on older day-only filenames, so the policy is technically adopted while the active corpus is still structurally non-compliant
- current workaround: treat rule introduction as phase 1 only, then schedule a corpus-wide filename backfill; do not declare the naming policy complete until the backfill and reference regeneration pass is finished
- failure signature: the workspace starts producing `DOC004` warnings on nearly every existing user-facing note, and operators mentally downgrade the new rule to background noise because nothing actionable was migrated yet
- structural fix candidate: pair every new filename lint rule with an explicit migration packet or baseline report that lists the backfill scope and the evidence source for missing timestamp components
- escalation trigger: a new filename policy begins to warn on a whole directory and no follow-up rename migration is planned in the same milestone
- current proven evidence: `my-image-parser` adopted `DOC004` for `control/user_decisions/resources/notes/` on 2026-04-05, then needed a second migration pass to actually convert all day-only notes to minute-level filenames

### Timestamp Syntax Variant Creates False Persistence Of Drift

- recurrence signal: a team agrees on a canonical timestamp token like `-atYYYY-MM-DD-HH-MM`, but manual renames or generated filenames accidentally introduce a near-match variant such as `-at-YYYY-MM-DD-HH-MM`
- current workaround: normalize the syntax variant immediately and rerun the lint pass before assuming the rule itself is broken; include exact canonical examples in the rule and helper manifest to reduce human memory drift
- failure signature: recently renamed documents still trigger the same timestamp warning, leading reviewers to suspect the lint logic is wrong when the real issue is the extra delimiter in the filename
- structural fix candidate: add a dedicated lint note or targeted test example that explicitly rejects the malformed `-at-YYYY...` variant so the failure mode is recognizable
- escalation trigger: a post-migration lint run shows the same timestamp warning on newly renamed files that were expected to be clean
- current proven evidence: the first 2026-04-05 rename pass for five `REFERENCE_*` notes used `-at-2026-...` instead of `-at2026-...`, which kept `DOC004` alive until the pattern was normalized in a second pass

### Duplicate Reference Copies Lose Canonical Workspace Ownership

- recurrence signal: the same implementation reference is kept in both a decision-support workspace and an implementation workspace, even though only one of them should own the canonical implementation framing
- current workaround: compare the copies directly, decide which workspace has the correct ownership framing, and remove the duplicate from the non-owning workspace once local references are confirmed absent
- failure signature: users cannot tell whether the implementation truth lives in the implementation repo or the decision-support repo, and later edits change only one copy while the other quietly stales
- structural fix candidate: duplicate-reference audit rule for cross-workspace artifacts that asks `does this workspace own the implementation framing, or is it only rereading it?`
- escalation trigger: a copied reference begins to diverge in structure, section names, or purpose statement from the sibling workspace that clearly implements the surface
- current proven evidence: on 2026-04-05, `my-image-parser` retained a longer decision-space copy of `REFERENCE_obsidian_vscode_surface_orchestration-*` while `vscode-markdown-review-surface` already had the canonical implementation reference, and the duplicate was pruned after direct comparison

### Cross-Workspace Planning Ownership Drift

- recurrence signal: repeated whenever implementation-owner and truth-owner workspaces are both active in one session and a bounded surface-delivery plan or reference is briefly written into the wrong workspace
- current workaround: remove the misplaced patch from the non-owning workspace, restate the owner boundary explicitly, and recreate the document only under the implementation workspace
- failure signature: a stewardship agent or later reader infers that the consumer or truth-owner workspace now owns the implementation plan because its master plan or drafts were patched first
- structural fix candidate: mandatory owner-boundary check before freezing any cross-workspace plan, KB, or reference
- escalation trigger: another implementation concern causes consumer-workspace planning contamination or steward confusion

### Feedback Artifact Expansion Toward Second Truth Plane

- recurrence signal: repeated whenever helpful review-support artifacts such as feedback JSON, region notes, or review ledgers begin to accumulate enough fields that they resemble a full decision record
- current workaround: keep artifact naming strict, limit the feedback artifact to history and review support, and preserve one explicit downstream decision truth
- failure signature: reviewers can no longer tell whether a final decision should be read from the feedback artifact or from the canonical decision seed
- structural fix candidate: truth-plane naming guard plus schema checks that prevent feedback artifacts from silently duplicating full decision rows
- escalation trigger: another review-support artifact begins carrying enough decision state to behave like a second canonical source

### Unverified Operational Allocation Freeze Drift

- recurrence signal: repeated whenever a tool list, MCP assignment, or multi-agent staffing map becomes detailed enough to look final before owned paths, runtime stability, or role boundaries have been validated
- current workaround: separate confirmed allocation from provisional allocation, record only the verified core, and defer the rest until path overlap and runtime feasibility are checked
- failure signature: operators or builders treat a provisional staffing matrix as final, then discover that timeout-prone MCPs, overlapping owned paths, or role ambiguity invalidate the recorded allocation
- structural fix candidate: staffing-and-tooling verification gate before operational allocation docs are frozen
- escalation trigger: another agent allocation or tool matrix is documented as final before owned-path and runtime feasibility checks are complete

### Host-Heavy Parallel Builder Collision Risk

- recurrence signal: repeated whenever a centralized host file or protocol handler attracts many planned builders before its seams are modularized
- current workaround: keep one architect-origin builder on the integration seam, cut module boundaries first, and dispatch other builders only onto disjoint files or newly isolated modules
- failure signature: multiple builders need the same host file or message-router surface, causing merge collisions and accidental truth-boundary regressions
- structural fix candidate: pre-dispatch hotspot scan and locked-path expansion rule for host-heavy surfaces
- escalation trigger: another multi-builder slice attempts wide parallelization against a still-centralized host file

### Session-Level Status Becomes Less Reliable Than Code-State Reality

- recurrence signal: a worker agent times out, disconnects, or returns only an orchestration summary while the repository may already contain valid changes from that lane or from sibling lanes
- current workaround: downgrade agent/session status to advisory only, inspect the target files directly, and classify recovery from repository reality before reassigning work
- failure signature: teams overreact to an errored or missing agent summary by restarting whole waves, even though some lanes have already landed correct code that only lacked a clean final report
- structural fix candidate: recovery checklist that always asks `what files exist now?` and `what checks pass now?` before any relaunch decision
- escalation trigger: another interrupted multi-agent run leaves uncertainty about whether progress exists in code but not in orchestration metadata
- current proven evidence: the 2026-04-06 reduced-fanout work on `vscode-markdown-review-surface` showed disconnected worker sessions while `session-config`, `decision-contract`, and `feedback-ledger` files were already present in the tree

### Reduced-Fanout Lanes Fail Asymmetrically Under Network Instability

- recurrence signal: a smaller builder wave is launched with disjoint owned paths, but unstable network conditions still cause only a subset of lanes to report or persist changes
- current workaround: evaluate each lane independently instead of treating the reduced-fanout wave as all-or-nothing; verify the materialized lanes, preserve them, and relaunch only the missing lanes
- failure signature: one or two lanes produce working artifacts while sibling lanes remain empty, yet the team treats the entire wave as failed and risks overwriting good work on a blanket rerun
- structural fix candidate: lane-by-lane completion ledger for reduced fanout that records `materialized + verified`, `materialized + unverified`, and `missing`
- escalation trigger: another reduced-fanout wave suffers partial network loss or mixed worker exits
- current proven evidence: during the 2026-04-06 `vscode-markdown-review-surface` reduced fanout, the `host` and `render` lanes remained missing while the `contract/session-config` and `feedback-ledger` lanes left real source and test files behind

### Shared Validation Command Can Flake During Toolchain Refresh

- recurrence signal: the same validation command that previously passed begins to behave inconsistently because the local toolchain cache, downloaded test binary, or extension-host bootstrap state changes mid-session
- current workaround: rerun the shared validation command from the code-state recovery step, distinguish a genuine code failure from toolchain refresh/download behavior, and avoid freezing conclusions until the command completes cleanly again
- failure signature: `npm test` alternates between clean passes, interactive refresh prompts, download attempts, or silent non-zero exits, making it unclear whether the new code failed or the validation environment shifted underneath it
- structural fix candidate: explicit test-runtime stabilization note for extension-host projects that rely on cached VS Code binaries and can fall back into refresh/download mode after interruption
- escalation trigger: a repeated command that was already green in the same slice starts failing or prompting due to environment refresh rather than source changes
- current proven evidence: in the 2026-04-06 validation loop for `vscode-markdown-review-surface`, repeated `npm test` runs encountered cached-binary discovery, download attempts, an overwrite prompt, and a silent exit before later runs returned to normal passing output

### Recovered Control Trees Reopen Previously Closed Layout Violations

- recurrence signal: repeated whenever a deleted or damaged `control/` subtree is restored from backup or snapshot material and old non-canonical directories reappear even though the workspace had already normalized them
- current workaround: treat restored control content as provisional, rerun layout lint immediately, and patch restored drift before trusting any recovered planning or packet artifacts
- failure signature: repo-layout lint starts reporting action-unit violations that were already closed in earlier migration waves, usually under `runs/`, hidden editor state, or legacy runtime folders
- structural fix candidate: post-recovery normalization checklist for restored `control/` trees before any feature continuation begins
- escalation trigger: another workspace restoration repopulates directories that violate the current canonical layout model
- current proven evidence: on 2026-04-06, `vscode-markdown-review-surface` recovery surfaced restored `control/project_domain/runs` and an empty `control/user_decisions/.obsidian`, both of which had to be removed or archived again before recovery could be declared closed

### Narrow Cross-Workspace Truth References Are Misread As Old-Root Drift

- recurrence signal: repeated whenever task packets or operational artifacts intentionally reference a sibling truth-owner workspace, but layout lint treats those references as stale old-root strings because the repo-local pattern is too broad
- current workaround: narrow the lint exception to the specific artifact family and specific external truth-owner references that are intentionally allowed, rather than suppressing the rule globally
- failure signature: recovery audits flag legitimate packet references to an external truth owner as if they were accidental stale paths, creating noise during structural normalization
- structural fix candidate: scoped allowlist semantics for packet/reference files that are allowed to point at external truth-owner workspaces
- escalation trigger: another recovery or lint pass reports cross-workspace truth-owner paths even though the architecture intentionally keeps truth outside the current implementation repo
- current proven evidence: during the 2026-04-06 recovery closure in `vscode-markdown-review-surface`, `RL006` had to be narrowed so issued task packets could keep their intentional `my-image-parser/control/...` truth-owner references without reintroducing broad stale-path exceptions

### Dirty Teardown In Smoke Suites Masks Real Recovery State

- recurrence signal: repeated whenever editor or extension smoke tests leave documents dirty or unsaved and the teardown path hangs, causing recovery to appear incomplete even though the source code may already be correct
- current workaround: stabilize teardown first by saving or closing bounded editor state explicitly, then rerun the suite to separate harness cleanup failure from genuine feature or recovery regressions
- failure signature: `after all` hooks time out, open editors remain dirty, or cleanup failures dominate the smoke output more than the product assertions themselves
- structural fix candidate: shared smoke helper that normalizes save-before-close behavior for tests that modify working documents
- escalation trigger: another smoke suite fails in teardown more often than in the actual product assertions after a recovery patch
- current proven evidence: on 2026-04-06, `vscode-markdown-review-surface` recovery remained blocked until `smoke.test.js` adopted save-before-close cleanup, resolving the `after all` timeout on `reviewSurface.open`

### Preview-Oriented Smoke Paths Can Exceed Recovery Value

- recurrence signal: repeated whenever a slower preview or auxiliary command path stays flaky during recovery, even though the main host behavior is already stable enough to move forward
- current workaround: keep the preview path bounded, degrade it to a narrow no-op or lighter assertion temporarily, and preserve strict checks on the main command paths that represent the actual continuation blocker
- failure signature: recovery remains “open” only because a slower preview path is unstable, while the primary editor/open-default paths are already healthy
- structural fix candidate: recovery-time smoke priority model that distinguishes core user-path stability from slower auxiliary preview paths
- escalation trigger: a future recovery is blocked by a preview-oriented or optional command path whose instability no longer reflects the main product risk
- current proven evidence: during the 2026-04-06 recovery closure, `vscode-markdown-review-surface` treated the built-in preview smoke path as bounded while keeping the editor and `openDefault` command paths strict, allowing recovery to close on the real user-path contract

### Recovery Completion Shifts The Next Blocker To Feature-Boundary Discipline

- recurrence signal: repeated whenever a team spends several iterations on recovery and then continues to reason as if repo-state failure is still the main blocker even after checks have gone green
- current workaround: after recovery validation passes, explicitly restate the next blocker as feature-boundary discipline or scoped implementation work, not as generalized recovery uncertainty
- failure signature: planning and staffing continue to orbit recovery language even though the remaining risk has moved to scope control, truth-plane discipline, or next-wave feature ownership
- structural fix candidate: post-recovery blocker handoff note that names the new primary constraint once recovery is closed
- escalation trigger: another slice keeps deferring feature continuation because the team mentally remains in incident-response mode after validation already passed
- current proven evidence: once `vscode-markdown-review-surface` recovery closed on 2026-04-06 with clean lint, check, and test results, the next real blocker became keeping the user-evaluation-surface wave bounded rather than continuing generic recovery work

### Command Contribution And Host Registration Drift

- recurrence signal: repeated whenever a command is documented or contributed in `package.json`, but the actual host registration or execution path in `extension.js` lags behind and the feature appears more complete on paper than in runtime
- current workaround: verify both layers together, then patch the host registration and smoke the official command path before counting the packet as closed
- failure signature: the command name appears in contributions and planning docs, yet `executeCommand(...)` still fails or the surface only works through an older internal entrypoint
- structural fix candidate: packet done-definition and smoke rules that require both contribution and live host registration for any new public command
- escalation trigger: another bounded feature claims a command-open path while only one of `package.json` or `extension.js` has actually been updated
- current proven evidence: on 2026-04-06, `reviewSurface.openEvaluationSession` existed in the contributed command surface before `src/extension.js` registered the host command, and the gap had to be closed before wave1 could be frozen honestly

### Validation Reference Lags The Latest Verified Green State

- recurrence signal: repeated whenever a validation note is written at the first green point, but a later bounded patch changes the official command path, packet closure wording, or passing test count without immediately resyncing the frozen reference
- current workaround: patch the existing validation reference as soon as the newer green state is verified, rather than treating the mismatch as harmless documentation lag
- failure signature: code and tests are green on the latest path, but the nearby wave reference still describes the previous command path or lower passing-count baseline
- structural fix candidate: explicit `reference resync required` step in packet closure once any post-freeze green-state delta lands
- escalation trigger: another packet finishes with a changed command path, acceptance claim, or test count while the most recent validation reference still advertises the older state
- current proven evidence: on 2026-04-06, the feature-wave-1 reference had to be updated after the official evaluation command path was fully wired and the verified suite moved from the earlier count to `56 passing`

### Serial Seam Packets Trigger Benign Path-Overlap Warnings

- recurrence signal: repeated whenever adjacent seam packets intentionally share one orchestration or shell file and `packet_builder.py check-paths` reports overlap even though the packets are not meant to run in parallel
- current workaround: classify the overlap as intentional serial reuse, keep execution strictly sequential, and avoid treating the warning as if it were a real parallel-lane conflict
- failure signature: `check-paths` emits overlap warnings on the shared seam file and can look like a packet-boundary mistake even when the plan intentionally narrows that file across consecutive waves
- structural fix candidate: packet metadata or triage guidance that distinguishes serial seam reuse from true parallel path conflict
- escalation trigger: another reduced-fanout wave repeatedly warns on one shared file and the team starts hesitating because the warning is read as a hard blocker
- current proven evidence: on 2026-04-06, `TASK-FEATURE-0003` through `TASK-FEATURE-0006` all produced overlap warnings on shared seam files such as `decision-slides.js` and `slide-shell.js`, but the warnings were benign because the packets were executed in sequence

### Extension-Host Validation Can Fail With Runtime Noise Before A Stable Verdict

- recurrence signal: repeated whenever `npm test` for an extension-host or webview-heavy surface fails with a generic runner error, crashed network service, or webview/runtime noise before a clear assertion failure is visible
- current workaround: rerun the same validation command, inspect the second run for runtime signatures, and defer any documentation freeze until the green state is reproduced or the real failing assertion is isolated
- failure signature: the first run ends with a broad `TestRunFailedError` or runtime crash line such as `Network service crashed`, while the visible assertion stream remains incomplete
- structural fix candidate: dedicated extension-host flake triage guidance plus log capture for noisy runtime failures that are not yet mapped to a single product regression
- escalation trigger: another bounded feature packet lands clean local code, but validation still fails once through runtime noise before a trustworthy pass or concrete regression appears
- current proven evidence: on 2026-04-06, the first `npm test` after the `slide-feedback` scaffold failed with a generic extension-host test runner error, and the rerun later surfaced runtime noise including a network-service crash line before the team could decide whether the wave was truly green

### Runtime Bundle Migration Can Leave Source-Level Generator Debt Behind

- recurrence signal: repeated whenever a project adopts a bundled runtime path and looks architecturally migrated from the outside, but the source modules still contain helper-generated execution patterns from the pre-bundle design
- current workaround: inspect the source tree directly for generator exports and script-construction helpers, then remove them so the source architecture matches the runtime architecture
- failure signature: reviews still find `get...Script()` helpers or equivalent generator chains even though the bundle entry and runtime behavior are already using a compiled asset
- structural fix candidate: post-bundler cleanup checklist that requires source-level generator removal, not just successful bundling
- escalation trigger: another bundler adoption or runtime-container refactor is declared complete while the source modules still advertise the previous helper-based execution model
- current proven evidence: on 2026-04-07, `vscode-markdown-review-surface` already had a working webpack-driven webview build, but the expert-debt closure was not complete until the remaining source-level script-generator exports were removed from the webview and slide modules

### Broad Debt Scans Produce Benign False Positives That Need Semantic Triage

- recurrence signal: repeated whenever the team uses grep-style pattern scans to confirm that a named technical debt is gone, but the same token also appears in legitimate code paths that should not be removed
- current workaround: classify remaining matches semantically before patching, and document why the residual occurrence is valid rather than chasing the scan to zero blindly
- failure signature: a closure scan still reports a token such as `.toString(` even though the remaining usage is a legitimate serialization or framework call unrelated to the original debt family
- structural fix candidate: debt-scan triage guidance that distinguishes exact helper debt from allowed runtime/library usage
- escalation trigger: another expert-feedback remediation depends on pattern-search evidence and risks over-patching because the scan vocabulary is broader than the actual code smell
- current proven evidence: on 2026-04-07, the final scan in `vscode-markdown-review-surface` still matched `asWebviewUri(...).toString()` in `host-document-state.js`, but that occurrence was correctly triaged as valid URI serialization rather than leftover webview script-injection debt

### Contract Template Vs Validator Self-Consistency Drift

- recurrence signal: a module exports both a factory/template function and a validator, but the factory's default output fails the validator; tests pass only because test helpers silently patch the incompatible fields
- current workaround: add a self-consistency test that calls `validate(template())` with zero overrides; audit test helpers that override template fields for masking bugs
- failure signature: downstream consumers that call the template directly hit immediate validation errors, while the test suite stays green because `buildBaseRow()` or equivalent silently injects valid values
- structural fix candidate: mandatory self-consistency test for any module that co-exports a factory and a validator; lint rule that flags test helpers overriding factory output fields without an explicit justification comment
- escalation trigger: another schema module introduces a factory or template whose output fails its own validator, or test helpers inject silent fixes that hide the mismatch
- current proven evidence: on 2026-04-07, `decision-contract.js` `buildDecisionRowTemplate()` returned `use_for_retrieval: false` + `retrieval_block_reason: null`, which always failed `validateDecisionRow()`; fixed by adding `review_status !== 'pending'` guard
- detail file: `ISSUE_contract_template_vs_validator_self_consistency_drift.md`

### Cross-Module Data Shape Validation Gap

- recurrence signal: two modules share a data shape (one produces, one consumes), but the consumer validates only the outer container and accepts the inner payload as any object
- current workaround: import the shape owner's validator into the consumer module and apply it at entry time before persistence
- failure signature: invalid inner payloads are persisted to disk and only fail during downstream processing, far from the point of entry
- structural fix candidate: cross-module validation rule requiring that any embedded payload shape is validated by importing the owning module's validator at entry time
- escalation trigger: another module accepts a nested payload from an external shape owner without importing the owner's validator
- current proven evidence: on 2026-04-07, `feedback-ledger.js` accepted `decision_patch` with `isObject()` only, bypassing `decision-contract.js` field rules; fixed by adding `validateDecisionPatch()` and calling it inside `validateFeedbackEntry()`
- detail file: `ISSUE_cross_module_data_shape_validation_gap.md`

### Debug Logging Residue In Production Surface

- recurrence signal: `console.log` debug statements remain in committed production code paths after development, producing noise in extension host output and leaking internal state
- current workaround: grep for `console.log` in `src/` before merge; add an eslint rule that flags `console.log` (allow `console.error` and `console.warn`)
- failure signature: in stdio-based protocols (MCP), stdout pollution can corrupt transport; in extension hosts, debug logs slow output and confuse users
- structural fix candidate: eslint `no-console` rule scoped to `src/` with `console.error` and `console.warn` exceptions, plus CI gate
- escalation trigger: another `console.log` debug statement is found in committed production code in `src/`
- current proven evidence: on 2026-04-07, `extension.js:125,127` had `console.log('[wikilink-debug]...')` and `webview-wikilinks.js` had multiple debug logs; removed by Codex in same session
- detail file: `ISSUE_debug_logging_residue_in_production_surface.md`
- linked pattern: `ISSUE_stdio_stdout_pollution_in_machine_readable_mcp.md`

### Webview Script Injection Via Function ToString

- recurrence signal: webview-side code is delivered by calling `function.toString()` on host-side functions and injecting the result as inline `<script>` content, breaking under minification and creating invisible coupling
- current workaround: use a bundler (webpack, esbuild) to create a separate webview entry point; test webview modules as regular Node.js modules via `require()`
- failure signature: any refactor or minification silently breaks the webview; no type checking between host and webview function signatures; source maps impossible
- structural fix candidate: mandatory bundler-based webview delivery for all VS Code extension webview surfaces; ban `function.toString()` for code delivery
- escalation trigger: another webview or iframe receives code via `function.toString()` or template literal injection instead of a bundled entry point
- current proven evidence: on 2026-04-07, `slide-view-model.js`, `slide-shell.js`, `slide-context.js`, `slide-feedback.js` all had `getReviewSurface*Script()` functions; fixed by switching to webpack bundle with entry `src/decision/webview-client.js` and factory function pattern
- detail file: `ISSUE_webview_script_injection_via_function_tostring.md`

### Guard Filter Set Missing Alias Forms

- promotion status: absorbed on 2026-04-07 into `Skills-Create-Project/async-migration-verify/checklist-forconsistency-evaluation/async-migration-6-checkpoint.md` checkpoint 1 variant
- recurrence signal: a programmatic guard constructs a blocklist/allowlist from a canonical source, but the runtime accepts multiple naming conventions for the same entity; the guard covers only one form, leaving alias forms unblocked
- current workaround: generate entries for every accepted naming convention when building the filter set; add at least one test that uses the alias form
- failure signature: `require('fs')` is blocked but `require('node:fs')` passes the same guard undetected; the guard looked correct because `.replace()` suggested normalization was happening
- structural fix candidate: mandatory alias-form enumeration step when building any programmatic filter set; verify normalization direction (stripping vs generating variants)
- escalation trigger: another guard or blocklist is built from a single naming convention while the runtime accepts multiple forms of the same identifier
- current proven evidence: on 2026-04-07, `webpack.config.js` `RejectNodeBuiltinImportsPlugin` used `builtinModules.flatMap(name => [name, name.replace(/^node:/, '')])` which was a no-op; fixed by generating `[bare, \`node:${bare}\`]` to cover both forms
- detail file: `ISSUE_guard_filter_set_missing_alias_forms.md`
- linked pattern: timestamp syntax variant issues (same class — near-match variants bypassing a gate)

### Partial Structural Fix — Same Class, Different Fields

- promotion status: absorbed on 2026-04-07 into `Skills-Create-Project/cross-repo-product-review/checklist-forconsistency-evaluation/review-convergence-consistency-checklist.md`
- recurrence signal: a structural fix (spread reordering, validation addition, precedence adjustment) is applied only to the fields explicitly named in a review; structurally identical sibling fields remain unprotected
- current workaround: identify all members of the structural class before applying the fix; enumerate addressed vs remaining members in the fix description
- failure signature: the fix appears complete because named fields are addressed, but a follow-up review discovers the identical vulnerability on sibling fields; each partial round costs a full review-handoff-verify cycle
- structural fix candidate: "fix the class, not the instance" rule — any structural fix must be applied to all members of the same structural class in one pass
- escalation trigger: another structural fix addresses only the named fields while leaving structurally identical siblings unprotected, requiring a follow-up round
- current proven evidence: on 2026-04-07, Codex 2nd patch moved `ordinal`/`title` after spread in `slide-session.js` but left `slide_id`/`image_id` before spread with the same collision vulnerability; Codex 3rd patch had to fix again; each round cost a full review cycle
- detail file: `ISSUE_partial_structural_fix_same_class_different_fields.md`

### Dead Import After API Migration

- promotion status: absorbed on 2026-04-07 into `Skills-Create-Project/async-migration-verify/checklist-forconsistency-evaluation/async-migration-6-checkpoint.md` checkpoint 1
- recurrence signal: after migrating all call sites from one API surface to another (sync→async, old library→new library), the original import survives with no direct call sites; it only serves as a derivation step (e.g., `fs` used only to access `fs.promises`)
- current workaround: grep for the old module import across all migrated files; verify at least one direct call site remains; if derivation-only, destructure directly
- failure signature: readers seeing `const fs = require('fs')` assume sync methods are still active; audits for "fully async?" are skipped because the old import is present
- structural fix candidate: post-migration import audit step; linter rule that flags imports with no direct member access
- escalation trigger: another API migration leaves the old import in place with no direct call sites
- current proven evidence: on 2026-04-07, `decision-session-artifacts.js` had `const fs = require('fs')` after all sync calls were converted to `fsp.*`; changed to `const fsp = require('fs').promises`
- detail file: `ISSUE_dead_import_after_api_migration.md`
- linked pattern: Runtime Bundle Migration Can Leave Source-Level Generator Debt Behind (same class — migration leaves structural residue)

### Sync/Async Logic Duplication Drift Point

- promotion status: absorbed on 2026-04-07 into `Skills-Create-Project/async-migration-verify/checklist-forconsistency-evaluation/async-migration-6-checkpoint.md` checkpoint 2
- recurrence signal: when adding an async variant of an existing sync function, the core logic (parsing, normalization, validation) is copy-pasted instead of extracted into a shared helper
- current workaround: extract shared processing logic into a pure synchronous helper; sync and async variants differ only in the I/O call
- failure signature: a validation rule change is applied to one variant and missed in the other; tests exercise only one variant, so drift is invisible until production hits the untested path
- structural fix candidate: mandatory shared-helper extraction when adding async variants of sync functions; test both variants against the same assertion set
- escalation trigger: another async variant is added by copying the sync body instead of extracting a shared helper
- current proven evidence: on 2026-04-07, `feedback-ledger.js` had `readFeedbackLedger` (sync) and `readFeedbackLedgerAsync` with identical 5-line parse/normalize/validate blocks; extracted to `parsePersistedFeedbackLedger(raw, filePath)` with file-path-enriched error messages
- detail file: `ISSUE_sync_async_logic_duplication_drift_point.md`

### Concurrency Guard Without UX Feedback

- promotion status: absorbed on 2026-04-07 into `Skills-Create-Project/async-migration-verify/checklist-forconsistency-evaluation/async-migration-6-checkpoint.md` checkpoint 3
- recurrence signal: a technical concurrency guard (in-flight flag, mutex, debounce) silently drops blocked actions without informing the user
- current workaround: provide visible feedback when an action is blocked (status message, spinner, disabled button); prefer latest-wins queue over drop-on-busy
- failure signature: user clicks Save twice quickly; second save is silently dropped; user believes both succeeded but only the first was persisted — silent data loss masquerading as success
- structural fix candidate: mandatory UX feedback rule for any concurrency guard; guard implementations must include a user-visible status update before returning
- escalation trigger: another concurrency guard (debounce, in-flight flag, lock) is added that silently drops user actions without feedback
- current proven evidence: on 2026-04-07, `extension.js` `onSaveDecisionFeedback` had `feedbackSaveInFlight` that silently returned; fixed by adding `statusMessage: "Save already in progress"` + `pushDocumentState()`
- recurrence on 2026-04-08: `decision-slides.js` client-side `saveState === 'saving'` guard silently returned; host-side guard was unreachable because client guard fires first; same anti-pattern at a different architectural layer; fixed by adding `statusMessage: 'Save already in progress.'`
- detail file: `ISSUE_concurrency_guard_without_ux_feedback.md`

### Loose Skill Promotion Appears Finished Before Family Validator Closure

- recurrence signal: repeated whenever a new skill has the obvious artifact set (`SKILL.md`, KB, checklist, evals), so the team treats it as done before strict family validators are actually run
- current workaround: declare the first content-complete state provisional, then require strict validator closure before promotion is considered finished
- failure signature: the skill reads well to humans but still fails on family conventions such as `SKILL.md` length/pattern, canonical artifact order, portability rules, or eval shape
- structural fix candidate: explicit `family validator closure` gate after promotion and before registry/eval-ready claims
- escalation trigger: another new shared skill looks done in review but changes again after `quick_validate --strict` or artifact-order validation is finally run
- current proven evidence: on 2026-04-08, both `cross-repo-product-review` and `async-migration-verify` needed a second hardening round after initial promotion to satisfy strict validator requirements

### Untimestamped Legacy Skill Artifacts Block Artifact-Order Validation

- recurrence signal: repeated whenever older KB/checklist files are still useful and semantically correct, but newer validators require minute-level timestamp syntax and canonical ordering across skill artifacts
- current workaround: keep the old files for provenance, add a new timestamped canonical chain, and point validation at the new chain instead of deleting the old files
- failure signature: `verify_artifact_order.py` fails even though the actual content is present and correct, because the canonical file names do not match the required `-atYYYY-MM-DD-HH-MM` style
- structural fix candidate: additive canonical-chain repair policy for validator upgrades that would otherwise force destructive renames or deletions
- escalation trigger: another family validator starts enforcing timestamp/order rules after useful untimestamped artifacts already exist
- current proven evidence: on 2026-04-08, both promoted skills needed fresh minute-stamped KB/checklist files before artifact-order validation would pass, while the older untimestamped files were intentionally preserved

### Eval JSON Can Be Valid Yet Not Scoreable Enough For Benchmark-Grounded Review

- recurrence signal: repeated whenever `evals.json` is syntactically valid and maybe even human-readable, but it is too loose to support repeatable scoring against a benchmark framework
- current workaround: tighten eval artifacts to include explicit prompt, expected output, assertions, and referenced files, then connect them to a benchmark metric mapping before claiming the evals are ready
- failure signature: JSON validation passes, but reviewers still cannot derive `Pass Rate`, `Resolve Rate`, or `Action Score` because the eval contract is underspecified
- structural fix candidate: benchmark-ready eval schema profile layered on top of plain JSON validity for shared skills
- escalation trigger: another skill claims to be eval-ready with a valid `evals.json` that lacks enough structure for measurable review
- current proven evidence: on 2026-04-08, both promoted skills had to move from generic eval descriptions to `prompt / expected_output / assertions / files` structure plus `agent-tool-benchmark` metric mapping before the first measured score sheets could be filled

### Placeholder Scripts Directory Triggers TDD Warnings Until A Real Helper And Test Exist

- recurrence signal: repeated whenever a skill keeps a placeholder `scripts/` directory for structural completeness, but family validation or human review interprets the empty implementation area as missing executable value or missing TDD coverage
- current workaround: either remove the placeholder if it is truly unnecessary, or replace it with one low-cost reusable helper and a direct test so the directory carries real implementation evidence
- failure signature: the skill structure looks correct, but validator/reviewer confidence stays low because `scripts/` contains only `.gitkeep` while the skill claims automation or reusable operational support
- structural fix candidate: rule that placeholder implementation directories must be backed by either explicit "no scripts required" rationale or one real helper/test pair
- escalation trigger: another skill keeps an empty `scripts/` directory and trips TDD/implementation expectations during strict validation
- current proven evidence: on 2026-04-08, `cross-repo-product-review` moved beyond a placeholder `scripts/` directory by adding `review_file_classifier.py` and `test_review_file_classifier.py`, which then served as real smokeable automation evidence for the skill

### Raw JSON Patch Input Keeps A Human Evaluation Surface In Developer Mode

- recurrence signal: repeated whenever the underlying writeback contract is already valid, but the default user path still asks the operator to hand-author JSON objects instead of using domain-shaped controls
- current workaround: move the JSON patch behind the scenes, render typed fields for the editable contract surface, and serialize only changed values back into the patch
- failure signature: the surface technically works, yet a human reviewer must type objects like `{\"review_status\":\"completed\"}` to perform normal evaluation actions
- structural fix candidate: typed-form-first rule for any human-facing decision surface that already has a bounded editable-field contract
- escalation trigger: another evaluation UI claims to be usable while still exposing raw JSON as the primary editing affordance
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` still depended on a `Decision Patch (JSON)` textarea in `slide-feedback.js` even though guarded writeback already existed; fixed by introducing `slide-decision-form.js` and changed-only patch generation in `decision-slides.js`

### Slide-Level Visibility Can Mask Whole-Session Completion Gaps

- recurrence signal: repeated whenever a review surface shows the current slide clearly and can even save slide-level feedback, but gives the operator no compact signal for total completion state across the full image order
- current workaround: compute a session summary from the slide set and render it in the shell as a first-class panel, rather than expecting the operator to infer completeness by navigating manually
- failure signature: the operator can answer "what is on this slide?" but not "how many images are still pending?", "which ones are deferred?", or "is the session ready for validation?"
- structural fix candidate: mandatory whole-session summary panel for any multi-item evaluation cockpit once per-item save is live
- escalation trigger: another multi-item review surface reaches feature parity at the item level but still cannot expose whole-session readiness
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` had context, feedback, navigation, and writeback, but `slide-shell.js` still explicitly said validator summary remained follow-on; fixed by adding `slide-session-summary.js`, wiring it through `slide-view-model.js`, and rendering session-level completion state in the shell

### Repo-Specific Rules Hardcoded In Generic Skill Script

- recurrence signal: a shared skill in `Skills-Create-Project/` contains scripts with path-matching or naming rules tied to a single repo's directory structure (e.g., `src/decision/`, `session-config`, `webview-`)
- current workaround: add a docstring marking the script as a reference implementation for the specific repo; note that reuse requires replacing rules or extracting to config
- failure signature: the script classifies files correctly for the original target repo but returns `unclassified` for every file in a different repo, giving a false impression of completeness
- structural fix candidate: extract classification rules into an external JSON/YAML config file; script reads rules from config, making it repo-agnostic; each target repo provides its own rule file
- escalation trigger: another shared skill bundles a script with repo-specific assumptions that break on a second repo
- current proven evidence: on 2026-04-08, `cross-repo-product-review/scripts/review_file_classifier.py` had `src/decision/`, `session-config`, `decision-contract`, `feedback-ledger`, `slide-`, `webview-`, `host-`, `mode-router` hardcoded for `vscode-markdown-review-surface`; fixed by adding a reference-impl docstring
- detail file: `ISSUE_repo_specific_rules_hardcoded_in_generic_skill_script.md`

### Checklist Template/Instance Duplication Without Convention

- recurrence signal: a newly created skill has paired files in checklist directories — one with a timestamp suffix and one without — with identical content and no convention explaining which is template vs instance
- current workaround: delete the non-timestamp duplicate when confirmed identical; retain only the timestamp file (matches workspace convention where all other skills use timestamp-only)
- failure signature: edits applied to one copy are not applied to the other, causing silent drift; `SKILL.md` Read Order references only the timestamp file, making the non-timestamp copy orphaned
- structural fix candidate: skill creation workflow explicitly produces only timestamp files; if a stable-name alias is needed, use a redirect note, not a full copy
- escalation trigger: another skill is created with the same paired-file pattern causing drift or validator confusion
- current proven evidence: on 2026-04-08, both `cross-repo-product-review` and `async-migration-verify` had 3 pairs of identical timestamp/non-timestamp checklist files; 3 non-timestamp duplicates were deleted after diff confirmed identity
- detail file: `ISSUE_checklist_template_instance_duplication_without_convention.md`

### Absorbed Task Lane Missing Escalation Trigger

- recurrence signal: a repeated task pattern is absorbed into a parent skill as a sidecar checklist item, and the KB `Absorbed Inputs` lists it, but no standalone re-separation criteria is documented
- current workaround: explicitly add an escalation trigger line in both the implementation checklist and the KB entry; format: "if executed independently (no parent-skill context) N+ times, promote to standalone skill"
- failure signature: the absorbed task is executed independently 3+ times but nobody notices because no trigger threshold is documented; the parent skill's checklist grows silently overloaded
- structural fix candidate: skill creation workflow requires every absorbed task lane to have an explicit escalation trigger at absorption time; skill template includes an `escalation_trigger` field
- escalation trigger: another task is absorbed into a parent skill without a documented standalone-promotion threshold
- current proven evidence: on 2026-04-08, `TASK_decision_contract_cross_field_test_expansion.md` was absorbed into `async-migration-verify` as implementation step 7 but initially had no escalation trigger; fixed by adding step 8 and KB escalation annotation
- detail file: `ISSUE_absorbed_task_lane_missing_escalation_trigger.md`

### Full Shell Re-Render On Transient Save State Destroys In-Progress Form Input

- recurrence signal: a bounded review surface introduces typed controls, then continues to refresh transient UI states (`saving`, `saved`, status notes) by replacing the entire shell markup
- current workaround: reserve full shell render for init/navigation and handle transient save-state changes through targeted DOM updates to existing nodes
- failure signature: textarea contents vanish, select controls reset, and cursor position jumps whenever save state flips, even though the current slide has not actually changed
- structural fix candidate: "no full rerender for transient state" rule for any surface with live form input; require a narrow update path for labels, disabled state, chips, and notes
- escalation trigger: another surface uses a full rerender to reflect status-only changes after typed form input has been introduced
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` needed to keep `renderDecisionSlidesShell()` off the save-status path because full rerender would wipe the typed decision form; fixed by extending `updateDecisionSlidesSaveUi()` in `decision-slides.js` to mutate only button/dirty/status/error nodes

### Dirty State Without Draft Validation Still Permits Save-Then-Fail UX

- recurrence signal: a surface correctly detects that the operator changed something, but treats every dirty draft as equally saveable even when the changed draft violates the underlying contract
- current workaround: add a draft-validation preview layer that evaluates the changed patch against the current persisted row before save and exposes `ready` vs `blocked`
- failure signature: the operator sees `Save Changes`, clicks it, and only then discovers a preventable contract error such as missing `retrieval_block_reason` after setting `use_for_retrieval=false`
- structural fix candidate: save UX should be driven by both `isDirty` and `draftValidationState`, with blocked drafts disabling save and surfacing the error list in place
- escalation trigger: another typed form relies only on dirty detection while deferring all rule enforcement to the persistence/writeback boundary
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` initially had `dirty/saving/saved` UX but no save-time preview, then added `evaluateDecisionSlidesDecisionDraft(...)`, preview state in `slide-view-model.js`, preview markup in `slide-feedback.js`, and blocked-save semantics in `decision-slides.js`, closing the gap at `96 passing`

### Cascaded State Mutation Double DOM Update

- recurrence signal: a state-mutation helper function is called immediately before a broader state mutation that overwrites the exact same fields the helper just set, causing two DOM updates where only the second matters
- current workaround: remove the helper call when the subsequent state mutation already covers all its fields; extract non-overlapping side effects if any
- failure signature: two sequential DOM paints for the same nodes in the same synchronous frame; the first paint is never visible to the user but adds execution time
- structural fix candidate: review all state-mutation helper call sites to verify that callers do not immediately overwrite the helper's output; helpers that only reset fields should not be called before a broader set-all-fields mutation
- escalation trigger: another state-change helper is called immediately before a broader state mutation that overwrites all fields the helper just set
- current proven evidence: on 2026-04-08, `decision-slides.js` `submitDecisionSlidesFeedback()` called `clearDecisionSlidesFeedbackNotes()` → `setDecisionSlidesUiState()` → DOM update, then immediately called `setDecisionSlidesUiState({ saveState: 'saving', statusMessage: '...', errorMessage: '' })` → DOM update, overwriting the same nodes; fixed by removing `clearDecisionSlidesFeedbackNotes()` call and deleting the now-unused function
- detail file: `ISSUE_cascaded_state_mutation_double_dom_update.md`

### Transient State Machine Gap Allowing Unintended Interaction

- recurrence signal: a state machine has a transient auto-reset state (e.g., `saved` → `idle` after 2 seconds) where UI affordances such as button enabled/disabled state are left at their default instead of being explicitly designed for the transient window
- current workaround: explicitly design UI affordances for each transient state; default to disabling interactive elements during transient states unless there is a specific reason to keep them active
- failure signature: user interacts with a UI element during the transient window and hits an error path that should not be reachable (e.g., clicking "Saved" triggers "enter a comment before saving" error)
- structural fix candidate: state machine UX review must include transient states; each state in the machine needs an explicit UI affordance specification, not just the primary states
- escalation trigger: another transient auto-reset state is added to a state machine without explicitly deciding whether interactive elements should be enabled or disabled during the transient window
- current proven evidence: on 2026-04-08, `slide-view-model.js` had `saveDisabled` condition with `saveState !== 'saved'` exception that kept the button clickable during the 2-second `saved` window; clicking "Saved" triggered the empty-payload error path; fixed by simplifying to `!isDirty`
- detail file: `ISSUE_transient_state_machine_gap_unintended_interaction.md`

### Dead Code Residue After Guard Consolidation

- recurrence signal: a helper function's only call site is removed during refactor, but the function definition remains; compiles without error and passes all tests, invisible without static analysis
- current workaround: when removing a call site, immediately search for other call sites; if zero remaining, delete the function definition in the same patch
- failure signature: dead function in codebase increases cognitive load; name implies active use and may mislead future developers into re-adding calls
- structural fix candidate: post-refactor dead-code scan or lint rule for unreferenced inner functions
- escalation trigger: another refactor removes a call site but leaves the function definition, and the dead code is only discovered later during unrelated review
- current proven evidence: on 2026-04-08, `decision-slides.js` `clearDecisionSlidesFeedbackNotes()` became unreferenced after its only call site was removed during the double-DOM-update fix; TypeScript diagnostic flagged it; deleted in the same patch
- detail file: `ISSUE_dead_code_residue_after_guard_consolidation.md`

### Full Donor Runtime Adoption Temptation In Bounded Integration Planning

- recurrence signal: repeated whenever a host repo considers integrating a well-known external repo and the first instinct is to embed the donor's full runtime rather than harvest only the narrow useful layer
- current workaround: force an ownership split across `host runtime`, `truth owner`, `donor modules`, and `downstream export`; reject modules that would move runtime ownership away from the proven host without explicit product approval
- failure signature: integration language drifts toward "tool X inside tool Y", runtime boundaries blur, and the plan silently widens from bounded adaptation into product replacement
- structural fix candidate: a mandatory donor-boundary matrix before any implementation plan that combines multiple external repos
- escalation trigger: another external integration proposal starts by comparing entire products instead of the exact modules needed for the target slice
- current proven evidence: on 2026-04-08, `slidev` and `slides-grab` initially looked like candidates for broad reuse in `vscode-markdown-review-surface`, but code inspection showed the correct shape was `@slidev/parser` plus `slides-grab` selection/annotation/validation donors only, with the existing VS Code extension retaining host and truth ownership

### Canonical Artifact Saved In The Wrong Workspace

- recurrence signal: repeated whenever an agent drafts a plan or KB while operating in one repo, but the artifact's true owner is another repo's control tree
- current workaround: relocate the artifact into the owning workspace immediately, keep only one canonical copy, and delete the misplaced duplicate after successful placement
- failure signature: two identical or near-identical "master plans" exist under different workspaces, both look authoritative, and later edits risk landing in the wrong one
- structural fix candidate: workspace-ownership check before artifact creation, especially for cross-repo design tasks
- escalation trigger: another cross-workspace planning session creates an artifact under the analyst repo rather than the implementation-owning repo
- current proven evidence: on 2026-04-08, the `slidev + slides-grab integration` plan was first written under `my-image-parser` because that was the active workspace, then moved to `vscode-markdown-review-surface/control/.../master_plans` and removed from `my-image-parser` once the ownership mismatch was noticed

### Integration Plan Misread As Broader Product Rewrite

- recurrence signal: repeated whenever external tool names carry strong product identities and a bounded integration plan can be mistaken for a full product transplant
- current workaround: front-load explicit `Intent` and `Non-Intent` sections near the top of the canonical plan before module decisions or phases
- failure signature: reviewers infer "native PPT in VS Code" or another oversized goal even though the actual plan is only a bounded donor integration with retained host ownership
- structural fix candidate: require top-of-document product-intent clarification for cross-repo integration plans that mention end-user tools with broad existing scope
- escalation trigger: another integration document starts with module lists and phases before stating what the combined product is not
- current proven evidence: on 2026-04-08, the canonical `slidev + slides-grab` plan remained easy to overread until `Intent` and `Non-Intent` were appended at the front, clarifying that the target is a VS Code slide-edit-intent surface rather than native PowerPoint inside VS Code

### Execution Critique Misread As Intent Rejection

- recurrence signal: repeated whenever a harsh critique contains multiple critical findings and reviewers collapse that into "the direction is wrong" even though the document explicitly preserves the product intent
- current workaround: check the critique verdict against canonical intent documents first; if the critique agrees with intent and boundary, classify it as an execution redesign gate instead of a strategic reversal
- failure signature: the team abandons or needlessly pivots a valid product direction because execution-level feasibility criticism is interpreted as disagreement with the higher-level goal
- structural fix candidate: critique-reading template with separate fields for `intent agreement`, `boundary agreement`, and `execution disagreement`
- escalation trigger: another review document says some form of "intent correct, execution plan requires redesign" but downstream discussion still treats it as a no-go on the product itself
- current proven evidence: on 2026-04-08, `REFERENCE_slidev_slides_grab_master_plan_critique-at2026-04-08.md` was verified against canonical KBs and found to support the bounded VS Code slide-edit-intent direction while rejecting only the original execution details

### Module-Level Donor Reuse Claim Hides Function-Level Coupling

- recurrence signal: repeated whenever an integration plan lists external source files as reusable donors, but later review shows those files contain a mix of reusable pure functions and unreusable runtime-specific code
- current workaround: replace file-level reuse claims with function-level or algorithm-level harvest notes; explicitly mark DOM-coupled, native-binary, or environment-specific parts as reference-only
- failure signature: a plan appears implementable because file names look promising, but the actual code is hard-coupled to another app's DOM, server, browser, or binary toolchain
- structural fix candidate: donor audit table that splits each candidate file into `pure reusable`, `wrapper needed`, and `reference only`
- escalation trigger: another donor-based design claims reuse of whole files before reading their internal dependency shape
- current proven evidence: on 2026-04-08, the first `slidev + slides-grab` plan treated `editor-bbox.js`, `editor-select.js`, and `validation/core.js` as reusable donor modules; critique review then showed that only small pure helpers/algorithms were reusable while the bulk of each file was coupled to slides-grab DOM or Playwright runtime

### Post-Delivery Test Assertion Weakness

- recurrence signal: repeated whenever a new test file is delivered or existing tests are patched, and the assertions use patterns that silently pass on wrong data (e.g., `find()` instead of positional index, single-field checks instead of full-object coverage, missing negative path tests)
- current workaround: manual review catches weak assertions post-delivery and strengthens them in a follow-up patch — replacing `find()` with positional `[i]`, adding complete-set coverage, inserting negative-path tests
- failure signature: tests pass green but fail to catch regressions because assertions match loosely, check only one field, or never exercise error/null/boundary inputs
- structural fix candidate: test assertion strength checklist integrated into post-delivery review, requiring positional checks for ordered data, full-field coverage for config objects, and at least one negative path per public function
- escalation trigger: another test file is delivered where `find()` is used on ordered arrays, or a public function has zero negative-path tests, and the gap is only discovered during a later unrelated review
- current proven evidence: on 2026-04-08, 7 instances across 3 test files in `vscode-markdown-review-surface` — `decision-slides-acceptance.test.js` used `find()` on ordered rows and missed `needs_row_update`; `evaluation-session-open.test.js` checked only `image_order` instead of full config and had 0 negative-path tests (4 added in patch)
- detail file: `repeated_issues/ISSUE_post_delivery_test_assertion_weakness.md`

### Error Double-Surface: Show And Throw In Command Handlers

- recurrence signal: repeated whenever a VS Code `registerCommand` callback catches an error, calls `vscode.window.showErrorMessage()`, and then re-throws — causing the user to see the error twice (once in the notification, once in VS Code's unhandled-rejection dialog)
- current workaround: manual review catches the pattern and replaces `throw error` with `return` after the `showErrorMessage` call
- failure signature: users see duplicate error notifications for a single failure — one from the explicit `showErrorMessage`, one from VS Code's default error handler catching the re-thrown exception
- structural fix candidate: command-handler error pattern rule: after `showErrorMessage`, always `return` (never `throw`); if telemetry needs the stack, log it separately before returning
- escalation trigger: another command handler is delivered with `showErrorMessage` followed by `throw` in the same catch block
- current proven evidence: on 2026-04-08, `extension.js` line 332 in `vscode-markdown-review-surface` had `throw error` after `showErrorMessage(error.message)` — patched to `return`
- detail file: `repeated_issues/ISSUE_error_double_surface_show_and_throw.md`

### Host Apply Success Branch Hides A Reusable Transaction Contract

- recurrence signal: repeated whenever a first writeback implementation lands in an extension/provider file and the success path manually performs document replacement, preview refresh, selection reset, intent reset, and post-apply status handling in one local branch
- current workaround: extract a transaction helper and a narrow host helper so the provider consumes a reusable `transaction` object instead of owning all post-apply semantics
- failure signature: host logic works once but becomes hard to review and extend because the meaning of "successful apply" is encoded as a hand-written cluster of assignments in a single command handler
- structural fix candidate: after the first successful bounded apply path, immediately scan for inline `nextText + reset state + status message` orchestration and lift it into a reusable transaction contract
- escalation trigger: another editor/provider success path grows beyond document replacement into 3+ UI state resets without a dedicated transaction helper
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` initially applied slide-preview writeback directly inside `extension.js`; the path was then refactored into `slide-writeback-transaction.js` and `slide-writeback-host.js`, leaving `extension.js` to consume the returned transaction rather than encode post-apply semantics inline

### Patch Preview Without Explicit Post-Apply Reset Leaves Stale Editing Context

- recurrence signal: repeated whenever a surface can preview and apply a bounded patch, but the design does not yet specify what happens to selection, intent, and patch state immediately after success
- current workaround: define post-apply behavior as part of the transaction contract — reparse preview state from new source text, clear selection manifest, clear edit intent, clear writeback draft, and surface a bounded success note
- failure signature: after apply, the UI still shows a stale `region_id`, stale intent, or stale patch preview that no longer matches the new source text, making the operator think the previous selection is still live
- structural fix candidate: writeback transactions must own both source mutation and transient-state reset; post-apply reset is not optional polish
- escalation trigger: another writeback flow adds apply before deciding whether stale selection/intent state should persist or reset
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` avoided stale preview context by making `slide-writeback-transaction.js` return refreshed preview state plus cleared selection/edit-intent/writeback states after `replace_source_range` apply, and validated that reset behavior in `slide-writeback-transaction.test.js`

### Expert Review Quality Collapses Without A Path-Oriented Evaluation Packet

- recurrence signal: repeated whenever a vertical slice spans many cooperating modules and an expert is asked to review it without a single document that states intent, non-intent, entry path, and evidence path
- current workaround: write an evaluation packet in `references/` that explains what was built, where the product starts, which modules define the execution path, what is proven, and what remains open
- failure signature: reviewers spend most of their time reconstructing scope from chat and file diffs, and may misjudge the slice because intent and current boundary are implicit
- structural fix candidate: once a slice spans parser, renderer, protocol, runtime, host, and tests, expert review must be preceded by a path-oriented packet instead of relying on conversational memory
- escalation trigger: another multi-module slice is ready for external review but there is no single document that ties product intent to code path and evidence
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` needed `REFERENCE_slide_preview_writeback_evaluation_packet-at2026-04-08.md` so an expert could evaluate the `slide-preview` writeback slice without reconstructing the path from chat history

### Contract-Level Geometry Pass Can Hide A Live Selection-Candidate Bug

- recurrence signal: repeated whenever fake-geometry or contract-level hit tests pass, but the real rendered surface still maps selection to the wrong block because a wrapper element or layout artifact participates in hit-testing
- current workaround: add an actual webview probe, compare live rendered rectangles against expected source-backed blocks, then tighten the candidate filter so structural wrappers cannot win the hit test
- failure signature: unit tests stay green while live selection resolves to an oversized container or another non-semantic block instead of the intended source-backed content block
- structural fix candidate: pair contract-level geometry tests with at least one live-render hit test and maintain an explicit structural filter for valid selection candidates
- escalation trigger: another source-mapped selection surface passes fake-rect tests but produces wrong block mapping in a real rendered preview
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` added live visual-hit proof for `slide-preview` and discovered that `slide-selection-contract.js` still admitted the full-slide wrapper as a selection candidate until the filter was tightened

### Mode Integration Pressure Before Reuse-Seam Closure

- recurrence signal: repeated whenever a new surface becomes useful enough that there is pressure to connect it to an adjacent mode immediately, even though its main runtime is still a large orchestration file with mixed responsibilities
- current workaround: postpone broad coupling, reread the runtime, extract reusable seams first, and only then allow cross-mode bridge or workflow integration work to proceed
- failure signature: cross-mode wiring lands while the unstable runtime still owns message generation, pointer logic, DOM mutation, and state normalization, making later refactors expensive and risky
- structural fix candidate: an integration gate that requires runtime seam extraction before mode-to-mode coupling expands beyond a bounded bridge
- escalation trigger: another mode bridge is proposed while the producing surface still depends on one dominant orchestration file for most of its behavior
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` delayed broader `slide-preview -> decision-slides` coupling until pieces like `slide-preview-host-sync.js`, `slide-preview-selection-runtime.js`, and `slide-preview-linked-state.js` had been extracted out of `slide-preview-runtime.js`

### Cross-Mode Result Sharing Without A Lightweight Bridge Drifts Into Direct Coupling

- recurrence signal: repeated whenever one mode starts producing artifacts another mode should reference, and the first instinct is to pass internal state directly between them
- current workaround: define a small bridge summary artifact, persist it through a sidecar store, and let the receiving mode read only that summary instead of the producer's live state graph
- failure signature: two modes begin to depend on each other's runtime-specific internals, so a change in preview/writeback state shape immediately breaks the review lane or forces simultaneous edits across both modes
- structural fix candidate: canonical bounded bridge artifact for cross-mode summary sharing before any deeper workflow merger
- escalation trigger: another pair of surfaces starts exchanging internal runtime state rather than a reduced persisted summary
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` avoided direct `slide-preview` to `decision-slides` coupling by introducing `slide-preview-bridge.js` plus `host-sidecar-store.js`, then had `decision-slides` consume only the bounded bridge summary

### Duplicated Host/Webview State Normalization Drifts Over Time

- recurrence signal: repeated whenever host and webview both reconstruct the same dependent state chain with slightly different local logic
- current workaround: reread both normalization paths, extract the chain into a shared helper, and patch both call sites to depend on the same normalizer before layering additional behavior on top
- failure signature: selection, edit-intent, or writeback states appear to match initially, then diverge subtly after one side adds a new reset or validation rule and the other side does not
- structural fix candidate: shared linked-state coordinator for any cross-surface dependent state chain that is normalized in more than one place
- escalation trigger: another host/webview pair duplicates chained normalization logic instead of consuming one shared helper
- current proven evidence: on 2026-04-08, `vscode-markdown-review-surface` extracted `slide-preview-linked-state.js` after both `slide-preview-runtime.js` and `extension.js` were normalizing the `selection -> edit intent -> writeback` chain, reducing drift risk before further bridge and runtime work

### Document Capability Claim Exceeds Proven Test Boundary

- recurrence signal: repeated whenever a reference or evaluation document uses "closed", "sufficient", or "stable" to describe a capability, but the test suite only proves a narrower subset of that claim
- current workaround: post-critique review splits every claim into proven (with specific test file citations) and not yet proven (with specific gap description), and qualifies scope words like "stable" with their actual boundary (e.g., "current slide context, not durable across source mutations")
- failure signature: reviewers trust document language and approve a slice without noticing that the test boundary is narrower than the claim implies; unproven gaps persist silently
- structural fix candidate: proven/unproven split requirement for every capability claim in evaluation and reference documents, plus mandatory scope qualification for "stable", "sufficient", and "closed"
- escalation trigger: another evaluation document claims a capability is closed while the test suite only proves a contract-level or mock-based subset, and the gap is discovered during expert review rather than at creation time
- current proven evidence: on 2026-04-08, `REFERENCE_slide_preview_writeback_evaluation_packet-at2026-04-08.md` made 4 overclaims — "source mapping sufficient" (only contract-level), "stable region_id" (only current slide context), "writeback closed" (only mock replaceDocument), "178 passing" (no runtime orchestration test) — all corrected across 2 calibration rounds
- recent recurrence extension: on 2026-04-09, the same class reappeared in `REFERENCE_review_surface_progress_and_expert_evaluation_packet-at2026-04-08.md` and in the stale mismatch between the progress packet and the detailed writeback packet, where bootstrap readiness was initially overstated and later-closed proof gaps were still described as unproven
- detail file: `repeated_issues/ISSUE_document_capability_claim_exceeds_proven_test_boundary.md`

### Flat Concern-Type Mixing In Reference Document Sections

- recurrence signal: repeated whenever a reference document section (especially Open Scope or Next Steps) lists items of different concern types (product expansion, integration debt, architecture debt, verification debt) in a single flat list without grouping or priority
- current workaround: reviewer re-sorts the list into typed/prioritized buckets during critique, then patches the document structure
- failure signature: readers cannot distinguish urgency or ownership from a flat list; review discussions spend time classifying items before evaluating them
- structural fix candidate: require typed/prioritized bucket structure for Open Scope and equivalent sections when the list exceeds 4 items of mixed concern types
- escalation trigger: another reference document's Open Scope or equivalent section contains 5+ items of mixed concern types in a flat list, and a reviewer has to re-sort before prioritizing
- current proven evidence: on 2026-04-08, the same evaluation packet had (1) Open Scope mixing product/integration/architecture/verification in 9 flat bullets, fixed by splitting into Integration/Verification → Product Expansion → Architecture/Maintainability with priority order; (2) Why This Matters mixing value statement with isolation disclosure, fixed by extracting `## Current Isolation Boundary` as an independent section
- recent recurrence extension: on 2026-04-09, the upper progress packet repeated the same issue by mixing cross-repo coordination status with product readiness and by mixing direct slice proof with adjacent/shared evidence before both sections were split structurally
- detail file: `repeated_issues/ISSUE_flat_concern_type_mixing_in_reference_sections.md`

### Bootstrap-Ready Surface Misread As Final Evaluation Surface

- recurrence signal: repeated whenever a UI lane can already generate/open a session and display an image, and that operational success is misread as proof that the surface is ready for the intended human judgment
- current workaround: separate `bootstrap/open readiness` from `evaluation-body completeness`, then freeze which additional UX or artifact fields are still mandatory before the lane can count as complete
- failure signature: teams start or even declare completion of human evaluation work on a surface that still lacks the actual comparison payload required for bounded judgment
- structural fix candidate: explicit readiness split between `open-path proof` and `decision-body proof`
- escalation trigger: another review surface reaches open/preview success but the user still cannot inspect the decisive candidate payloads inside the surface
- current proven evidence: on 2026-04-09, the `decision-slides` bootstrap path was working for the first 10 images, but the Steward response still classified the lane as incomplete because arm-by-arm candidate caption/alt text comparison was missing
- recent recurrence extension: later on 2026-04-09, even after candidate comparison landed, the same first-10 bootstrap session still proved only partial readiness because `image1`-`image5` were `excluded`, `image6` was `missing_source_record`, and only `image7`-`image10` were comparison-ready while the canonical phase2 truth set pointed to a different 9-image closure set
- later recurrence extension II: later on 2026-04-09, live operator testing reproduced the same confusion when `image1` showed a valid preview but no candidate captions; the missing body looked like a rendering failure until bundle availability and truth-set mismatch were rechecked
- detail file: `repeated_issues/ISSUE_bootstrap_ready_surface_misread_as_final_evaluation_surface.md`

### Metadata-Only Decision Form Masks Missing Candidate Comparison

- recurrence signal: repeated whenever a review surface contains a rich decision form with fields like `active default`, `comparison winner`, or `promotion state`, and that makes the surface look semantically complete even though the underlying candidate texts are not actually visible
- current workaround: treat metadata as secondary context only and require an explicit candidate-text comparison section when the human task is to choose among candidate outputs
- failure signature: reviewers are asked to approve or reject candidate arms based on labels and derived metadata rather than on the candidate texts themselves
- structural fix candidate: mandate a `candidate comparison present` check before accepting any review surface whose output selects among model/arm candidates
- escalation trigger: another surface shows image preview plus decision metadata but still does not render the candidate caption/alt-text payload that the form refers to
- current proven evidence: on 2026-04-09, the submission packet and screenshots showed a metadata-centric right panel, and the Steward response explicitly rejected `decision metadata form only` as sufficient UX for this phase
- recent recurrence extension: later on 2026-04-09, the same issue reappeared on non-ready slides because `decision-seed.jsonl` still carried `active_default_arm` and `comparison_winner` values for `image1`-`image6` even though the session-local bundles for those slides were `excluded` or `missing_source_record`; the UI had to be patched to gate on `candidate_bundle.availability`
- later recurrence extension II: later on 2026-04-09, even after candidate comparison and gating existed, the operator still experienced the surface as system-oriented because metadata and advanced fields dominated the default reading path; the UI had to be re-cut so image + candidate caption cards + one primary question came first and persistence targets were explained explicitly
- detail file: `repeated_issues/ISSUE_metadata_only_decision_form_masks_missing_candidate_comparison.md`

### Human-Facing Markdown Reparsing Substitutes For Candidate Contract

- recurrence signal: repeated whenever human-readable markdown already contains captions or summaries, and the team is tempted to reuse that markdown as the effective source-of-truth for in-surface comparison instead of extending the explicit artifact contract
- current workaround: demote markdown to supporting context, then extend the session/bootstrap artifact to carry the comparison payloads as structured fields
- failure signature: candidate comparison depends on implicit parsing rules against prose reports, causing drift between the displayed evaluation body and the actual canonical decision inputs
- structural fix candidate: require structured candidate payloads in the artifact contract whenever the evaluation lane depends on arm-by-arm comparison
- escalation trigger: another workflow proposes reparsing review markdown to reconstruct candidate texts that should instead be present in a machine-readable session artifact
- current proven evidence: on 2026-04-09, the Steward response rejected ad hoc reparsing of `REVIEW_phase1_caption_10w_obsidian_caption_review-at2026-03-27-19-08.md` as the canonical comparison source and required explicit session artifact contract extension instead

## 2026-04-09 Codex Workspace Issue Retrospective Addendum

1. The triggering incident was not a logic bug but missing recoverability: a directory disappeared before a safety commit existed.
2. Once Git recovery was added, the next blocker was not code generation but mixed path semantics inside docs, config snippets, and runtime examples.
3. The same absolute-path string class kept appearing across stable docs, live experiment evidence, external references, and local runtime/config surfaces, but each class needed a different treatment.
4. A second boundary then surfaced: ongoing experiment evidence could not be cleaned the same way as reusable agent-facing docs without risking truth drift.
5. After the user clarified the future need for Docker or Codex Web execution, vendored runtime assumptions became a more important blocker than further cosmetic document cleanup.

### Stable-Doc Cleanup Collides With Live Experiment Evidence

- recurrence signal: repeated whenever GitHub-prep or portability cleanup starts while reports, manifests, and some specs are still part of an active experiment loop or are being edited live by the user
- current workaround: sanitize stable docs, skills, scripts, and reusable references first; leave live experiment evidence and actively edited truth-source files untouched until they are frozen
- failure signature: a cleanup wave starts to rewrite current experiment semantics, source-of-truth interpretation, or user-edited evidence instead of merely removing machine-local drift
- structural fix candidate: explicit workspace rule or labeling scheme that distinguishes `stable reusable surface` from `live evidence surface` before bulk cleanup starts
- escalation trigger: another cleanup pass encounters active reports/manifests/specs interleaved with reusable docs and cannot safely decide what may be normalized
- current proven evidence: on 2026-04-09, `my-image-parser` deliberately left ongoing experiment surfaces such as `SPEC_corpus_review_decision_capture.md` and current review/evidence files untouched while surrounding tracked reusable docs were sanitized
- detail file: `repeated_issues/ISSUE_stable_doc_cleanup_collides_with_live_experiment_evidence.md`

### Path-Class Misclassification During Workspace Cleanup

- recurrence signal: repeated whenever machine-local absolute paths appear in many artifact families, but the correct replacement differs depending on whether the path is repo-local, local-private, external, scratch, or runtime-bound
- current workaround: classify the path surface first, then patch with the right transformation: docs to repo-relative, local-private references to local placeholders, sibling/external truth references to external placeholders, scratch paths to `<TMP_DIR>`, and config/runtime snippets to env or template placeholders
- failure signature: blanket relative-path rewrites make runtime examples unusable, erase intentional external-reference semantics, or accidentally imply that ignored local-private assets belong inside the repo
- structural fix candidate: shared path-class decision table and lint support for mixed control-plane/execution-plane repositories
- escalation trigger: another cleanup wave reaches the question `should all absolute paths just become relative paths?` and the answer depends on artifact class rather than string shape alone
- current proven evidence: on 2026-04-09, `my-image-parser` explicitly adopted the rule `docs -> relative`, `runtime -> dynamic/env-based`, `TOML/config snippets -> placeholder`, and used that distinction across multiple sanitization commits
- detail file: `repeated_issues/ISSUE_path_class_misclassification_during_workspace_cleanup.md`

### .venv-Only Vendored Runtime Assumption Drift

- recurrence signal: repeated whenever vendored OCR or ML-adjacent helpers assume one exact `.venv/bin/python` style layout, but the actual runtime later needs to work with `venv`, env-provided interpreters, or a different launcher root
- current workaround: add env overrides first, add `.venv`/`venv` fallback second, then patch the related skill runtime and troubleshooting docs so the documented surface matches the hardened code
- failure signature: the runtime or helper works only on the original workstation layout, or fails silently on another machine because interpreter discovery is over-constrained
- structural fix candidate: shared vendored-runtime interpreter resolver and review rule that forbids `.venv`-only assumptions in portable launcher surfaces
- escalation trigger: another vendored local tool hardcodes one interpreter layout even though the repo is being prepared for stronger remote compute later
- current proven evidence: on 2026-04-09, `my-image-parser` patched `scripts/full_image_ocr_context_package_lib.py`, `scripts/run_phase0_imagesorcery_ocr_smoke.py`, and the related OCR skill docs so they now support env overrides and `.venv`/`venv` fallback instead of one fixed local layout
- detail file: `repeated_issues/ISSUE_venv_only_vendored_runtime_assumption_drift.md`

### Cross-Validation Lane Mistaken For The Main Product Gate

- recurrence signal: repeated whenever a support lane, audit lane, or cross-validation lane accumulates enough open UX work that the team starts treating it as the main completion blocker for the broader product
- current workaround: explicitly restate which lane is the main test and which lane is auxiliary, then freeze the support lane's own closure boundary in a separate decision note
- failure signature: the team keeps adding polish or feature requirements to the auxiliary lane because its incompleteness is being misread as evidence that the main product test cannot close
- structural fix candidate: required `main test vs support lane` classification before accepting any blocker claim from an auxiliary surface
- escalation trigger: another evaluation tool or governance surface starts attracting completion pressure that properly belongs to a different core test lane
- current proven evidence: on 2026-04-09, `my-image-parser` initially treated review-surface UX incompleteness as a master-plan blocker until the user clarified that image captioning is the main test and the review surface is cross-validation only

### Uniform-Readiness Assumption Overconstrains Bounded Evidence Cohorts

- recurrence signal: repeated whenever a cohort is assumed to be valid only if every row is equally comparison-ready, even though the actual goal is bounded evidence and the lane can tolerate explicit deferrals
- current workaround: separate `uniform readiness` from `terminal truthfulness`, then allow mixed cohorts to close when ready rows are completed and non-ready rows are explicitly deferred
- failure signature: the team keeps chasing a perfectly homogeneous cohort even though the current evidence lane only needs terminal row states and truthful non-ready handling
- structural fix candidate: explicit rule that mixed-readiness cohorts may still close if their closure semantics are `complete or defer`, not `complete or hide`
- escalation trigger: another bootstrap or pilot cohort remains open only because excluded or unsupported rows are being treated as invalid rather than terminal deferrals
- current proven evidence: on 2026-04-09, the first-10 bootstrap review session in `my-image-parser` was initially considered non-closable because it mixed `excluded`, `missing_source_record`, and `ready` rows, but later closed once `image1`-`image6` were treated as explicit `manual_lane` deferrals

### Historical Blocker Conclusion Keeps Blocking After Scope Changes

- recurrence signal: repeated whenever an earlier blocker report stays in circulation after the scope or ownership boundary changed, so people continue operating from an outdated conclusion
- current workaround: add a supersession note to the older report, publish a new closure or boundary report, and retarget active references in runbooks or master plans
- failure signature: teams keep citing an older blocker artifact even though a newer scope decision already changed what counts as closure
- structural fix candidate: mandatory supersession section whenever a report's facts remain valid but its gating conclusion no longer does
- escalation trigger: another report is still referenced as current blocker evidence after a scope-freeze note or boundary decision changed the active interpretation
- current proven evidence: on 2026-04-09, `REPORT_phase2_review_surface_current_evaluation_gate_verdict-at2026-04-09-18-37.md` remained historically valid but had to be explicitly superseded once `NOTE_review_surface_cross_validation_scope_freeze-at2026-04-09-19-03.md` changed the active closure boundary

## 2026-04-13 Codex Lean Portfolio Issue Retrospective Addendum

1. The first blocker was not slide design but tool realism: render success in one environment did not mean render files actually existed.
2. The second blocker was path behavior: Quick Look rendering was brittle when launched against machine-local absolute paths with mixed Korean and space-heavy segments.
3. After real renders landed, the next blocker was observational rather than structural: repeated same-filename preview passes could stay stale even when the deck had changed.
4. Packaging then surfaced a canonical-artifact issue: transitional source-named JPGs sat beside final render JPGs and diluted the review directory.
5. The last blocker was coordination language: a Git handoff prompt overclaimed what should be staged even though several lean artifacts had already been committed in earlier commits.

### Sandbox-Success Quick Look Render That Produces No Files

- recurrence signal: repeated whenever Quick Look thumbnail generation reports a successful run inside the sandboxed execution path, but no rendered files actually appear in the expected output directory
- current workaround: treat `qlmanage -t` success logs as provisional only, then rerun the render path outside the sandbox or with escalated execution before trusting the artifact count
- failure signature: shell output suggests render completion, yet the render directory remains empty and downstream QA cannot find preview images
- structural fix candidate: explicit post-render existence check and documented rule that sandbox success logs do not count as artifact proof
- escalation trigger: another PPT preview workflow depends on Quick Look thumbnails and the first run reports success without writing files
- current proven evidence: on 2026-04-13, the lean `02_1` portfolio render flow in `my-image-parser` only produced real thumbnails after rerunning `qlmanage -t` outside the sandbox path

### Absolute-Path Quick Look Render Drift On Mixed-Locale Paths

- recurrence signal: repeated whenever Quick Look is invoked against long absolute paths containing mixed Korean and space-heavy directory segments, and render behavior becomes less reliable than the equivalent repo-relative invocation
- current workaround: run from repo root, pass repo-relative source paths, and write output into a fresh `/tmp` directory instead of trusting absolute-path invocation
- failure signature: the same source deck renders inconsistently depending on whether the command receives an absolute machine-local path or a repo-relative path under the same cwd
- structural fix candidate: standard render helper that normalizes source paths to repo-relative form before invoking Quick Look
- escalation trigger: another local render helper starts failing or drifting only on machine-local absolute paths while the relative-path form still works
- current proven evidence: on 2026-04-13, `scripts/render_lean_02_1_system_first_portfolio.py` stabilized the lean portfolio render path by deriving `source_path.relative_to(ROOT)` and rendering into a temp directory under `/tmp`

### Same-Filename Preview Cache Masks Final Deck Changes

- recurrence signal: repeated whenever a repeated visual QA cycle reuses the same preview filenames, and Quick Look cache serves stale thumbnails even though the saved deck content has changed
- current workaround: reset Quick Look cache, then verify the deck text with `markitdown` and treat the `.pptx` deck as the source of truth whenever preview and deck disagree
- failure signature: slide text or title changes are visible in the saved deck but the preview still shows the earlier wording, causing false drift reports
- structural fix candidate: mandatory `deck truth beats preview cache` rule plus a second-source verification step such as `markitdown`
- escalation trigger: another deck slice needs multiple same-filename re-render passes and reviewers start trusting stale preview images over the saved presentation
- current proven evidence: on 2026-04-13, the lean portfolio QA report had to record a `pass_with_preview_cache_caveat` verdict because repeated Quick Look previews could stay stale even after copy fixes were saved into the final deck

### Canonical Render Directory Polluted By Transitional Source-Named JPGs

- recurrence signal: repeated whenever render conversion or manual QA steps leave both transitional `*-source.jpg` files and canonical `slide-*.jpg` files in the same review directory
- current workaround: move or discard transitional outputs and keep the canonical render directory limited to the review-facing final filenames
- failure signature: the render directory contains duplicate-looking files for the same slide, making artifact counts ambiguous and creating noisy review surfaces
- structural fix candidate: explicit cleanup step that separates transitional render intermediates from canonical review renders
- escalation trigger: another deck slice reports the right slide count logically but the render directory contains extra source-named JPGs that confuse validation
- current proven evidence: on 2026-04-13, the lean `02_1` portfolio render directory initially contained both `slide-*-source.jpg` and `slide-*.jpg`, and only became canonical after the `*-source.jpg` set was moved out of the review directory

### Commit Handoff Overclaims Mandatory Stage Set After Partial Prior Commits

- recurrence signal: repeated whenever a follow-up Git handoff is written after some artifacts were already committed in earlier commits, but the prompt still presents a file list as if all listed items must now be staged together
- current workaround: downgrade the list to `candidate files to inspect`, make sensitive registry files conditional, and instruct the next agent to report clean status instead of creating an empty follow-up commit
- failure signature: the receiving agent interprets a guidance list as a mandatory stage set, over-stages files, or creates an unnecessary commit even though the relevant artifacts are already landed
- structural fix candidate: handoff template that distinguishes `inspect`, `stage if modified`, and `do not create empty commit`
- escalation trigger: another commit-preparation prompt is written after partial prior commits and the next agent cannot tell whether new work actually remains
- current proven evidence: on 2026-04-13, the lean `02_1` portfolio commit handoff had to be corrected after the user surfaced existing commits `7874c72`, `2a7beb6`, and `999e72b`, plus a review that changed `Expected tracked files` into `Expected candidate files to inspect`

## 2026-04-13 Codex Public Surface Packaging Issue Addendum

1. The packaging lane first hit a provenance problem: several intended public artifacts were already committed, so a naive follow-up stage list would have overclaimed what still remained.
2. The next blocker was evidence portability: the small review-surface session bundle carried machine-local absolute paths throughout JSON and JSONL payloads.
3. After that, the largest remaining blocker was boundary shape rather than file count: vendored tool directories were still nested repos with their own history and heavy payloads.
4. The last lean-specific blocker was a stale pointer rather than missing output: one plan still referenced an older timestamped QA report path after the newer report was already committed.

### Nested Vendored Repo Surface Blocks Raw Inclusion

- recurrence signal: repeated whenever a vendored tool directory looks like a candidate for packaging, but still carries nested `.git` plus local install residue or heavy payloads
- current workaround: classify the vendor as a separate ingestion decision, keep host-side wrappers in scope, and exclude the raw vendor tree from the normal public-surface commit wave
- failure signature: raw `git add vendor/...` would absorb nested repo history, misleading residue, or oversized tool payloads into the host repo
- structural fix candidate: explicit vendor-ingestion workflow separate from normal review-surface packaging
- escalation trigger: another packaging pass reaches untracked vendor repos that are large, nested, or only indirectly referenced by host-side launchers
- current proven evidence: on 2026-04-13, `my-image-parser` measured `vendor/mcp/imagesorcery-mcp` at `1.9G` and found nested `.git` across four vendored tool trees, so the packaging wave excluded them
- detail file: `repeated_issues/ISSUE_nested_vendored_repo_surface_blocks_raw_inclusion.md`

### Review Surface Session Bundle Absolute Path Residue

- recurrence signal: repeated whenever a session bundle is small enough to preserve but still embeds machine-local absolute paths in nearly every config, manifest, bundle, or row payload
- current workaround: normalize repo-bound path prefixes to `<REPO_ROOT>/`, revalidate the entire JSON and JSONL tree, then commit the sanitized bundle as evidence
- failure signature: the evidence bundle is logically complete but cannot be published or committed safely because it leaks workstation-local paths everywhere
- structural fix candidate: reusable session-bundle path normalizer for JSON and JSONL evidence trees
- escalation trigger: another bounded evidence bundle is valuable enough to keep, but still leaks host-local path prefixes throughout its payloads
- current proven evidence: on 2026-04-13, `my-image-parser` had to sanitize the 14-file review-surface session bundle before it could land in `3d1e4a1`
- detail file: `repeated_issues/ISSUE_review_surface_session_bundle_absolute_path_residue.md`

### Timestamped Artifact Pointer Drift After Later QA Regeneration

- recurrence signal: repeated whenever a plan or index points at a timestamped artifact filename and a later regeneration produces the same artifact role under a newer timestamp
- current workaround: verify the old path is stale, confirm the newer artifact already exists, and patch only the pointer without reopening semantic design decisions
- failure signature: the bounded slice is materially complete, but one or more plans still point at missing timestamped artifacts from an earlier QA pass
- structural fix candidate: stable alias or latest-pointer convention for timestamped QA outputs
- escalation trigger: another bounded artifact slice looks complete except for broken pointers to older timestamped report files
- current proven evidence: on 2026-04-13, `my-image-parser` had to patch `PLAN_lean_ppt_image_character_portfolio_slice-at2026-04-11.md` from a missing `...10-18.md` QA report to the committed `...13-30.md` report before landing `2b09aae`
- detail file: `repeated_issues/ISSUE_timestamped_artifact_pointer_drift_after_later_qa_regeneration.md`
