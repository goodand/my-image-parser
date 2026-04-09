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
