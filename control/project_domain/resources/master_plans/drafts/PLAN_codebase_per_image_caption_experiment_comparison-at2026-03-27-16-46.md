# Codebase Per-Image Caption Experiment Comparison Plan

## Status

Draft

## Purpose

This plan defines the main experiment we actually need in this codebase:

one image at a time
→ generate caption records
→ store per-image outputs
→ compare execution paths
→ decide which path becomes the default caption workflow

The comparison target is not "captioning in general."
It is specifically the codebase-local per-image caption experiment under the current repository structure.

## Primary Question

Which execution path is the best default for this repository when the goal is:

- factual per-image captioning
- resumable per-image records
- compatibility with later rename and metadata phases
- practical operation in this workspace

## Source Draft Coverage

This draft is a consolidation plan.
It must not silently replace the seven existing draft plans without recording what was inherited.

### Draft Inventory

1. `PLAN_canva_presentation_image_mapping_data_flow-at2026-03-27-15-29.md`
2. `PLAN_codebase_per_image_caption_experiment_comparison-at2026-03-27-16-46.md`
3. `PLAN_cv_mcp_caption_eval_metadata_flow-at2026-03-27-15-29.md`
4. `PLAN_image_caption_pipeline_data_flow-at2026-03-27-15-29.md`
5. `PLAN_image_obsidian_style_parsing-at2026-03-27-15-27.md`
6. `PLAN_image_table_row_rag_worksheet_mcp-at2026-03-27-15-29.md`
7. `PLAN_presentation_image_mapping_extension-at2026-03-27-15-29.md`

### Coverage Matrix

#### Draft 1. Canva presentation image mapping data flow

Inherited into this plan:

- presentation-derived image datasets are valid experiment sources
- caption review and downstream rerun rules matter
- source presentation and local artifact boundaries must stay explicit

Not directly merged:

- retrieval, reranking, outlier writing, and final presentation generation

Reason:

- those are downstream consumers of caption output, not part of the caption-arm comparison itself

#### Draft 2. This comparison draft

Owned directly here:

- four-arm experiment framing
- dataset parity rules
- evaluation dimensions
- final default-path decision criteria

#### Draft 3. CV MCP caption evaluation metadata flow

Inherited into this plan:

- per-image sequential batch thinking
- caption generation plus evaluation plus metadata plus rename as a full lifecycle
- artifact layout discipline
- failure policy thinking

Merged specifically into:

- Arm B MCP and Subagent orchestration
- shared evaluation dimensions
- output location planning

Not directly merged:

- moondream-based independent evaluator as a mandatory component

Reason:

- the current comparison target is execution-path comparison first, not evaluator architecture lock-in

#### Draft 4. Image caption pipeline data flow

Inherited into this plan:

- one image is the execution unit
- registry-first persistence
- execution-state and image-state separation
- commit gate after caption persistence

Merged specifically into:

- Arm B structure
- decision rules
- baseline artifact expectations

#### Draft 5. Image obsidian style parsing

Inherited into this plan:

- canonical record thinking
- explicit job, artifact, and execution object separation
- rerun policy discipline

Not directly merged:

- Obsidian, JS, Python, worksheet, and generic IR export branches

Reason:

- they are broader transformation architecture, not the immediate caption experiment

#### Draft 6. Image table row rag worksheet mcp

Inherited into this plan:

- canonical schema first mindset
- fallback policy mindset
- success criteria framing

Not directly merged:

- table extraction, RAG indexing, worksheet export, MCP read surface

Reason:

- this draft is adjacent but not part of the per-image caption experiment scope

#### Draft 7. Presentation image mapping extension

Inherited into this plan:

- draft caption vs approved caption distinction
- downstream consumers must use approved values only
- presentation-derived image path as a valid experiment source

Not directly merged:

- embedding generation, candidate retrieval, reranker top-5, mapping review

Reason:

- those phases start after caption generation and review

### Consolidation Rule

If a future patch changes this comparison plan, it must explicitly state whether the change:

- absorbs content from one of the seven drafts
- supersedes a section of one of the seven drafts
- or intentionally leaves a draft outside the experiment scope

This prevents silent drift between the comparison plan and the source drafts.

## Master Plan Alignment

This comparison draft is not a replacement for the canonical master plan.
It is an experiment-preparation slice under the presentation-image master plan.

Canonical references:

- `control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md`
- `control/project_domain/resources/specs/contracts/presentation_image_pipeline_spec.json`
- `control/project_domain/resources/specs/prose/SPEC_openai_image_caption_runner.md`
- `control/project_domain/resources/specs/prose/SPEC_full_image_standalone_ocr_context_package_baseline.md`

Operational registries and inventories:

- `control/project_agent_ops/registry/runtime/session_paths.json`
- `control/project_agent_ops/registry/tools/tool_inventory.json`
- `control/project_agent_ops/resources/tools_inventory/REFERENCE_mcp_setup.md`
- `control/project_domain/resources/cross_validation/index.json`

Master-plan rules that constrain this experiment:

- the pipeline remains presentation-image-centric even when a narrow caption experiment is isolated
- MCP-first orchestration is still the preferred architecture
- one image per worker is the preferred subagent pattern
- JSON records are preferred over CSV for LLM-facing data
- only approved captions are downstream-authoritative

This experiment may compare narrower paths, but every result should report how that path diverges from the preferred master-plan architecture.

## Current Baseline Interpretation

Two baseline meanings must stay separated:

1. comparison baseline for the four-arm caption experiment
   - Arm A remains the baseline comparison arm for direct extracted-image captioning
2. active next-step baseline for context-enriched reruns
   - `full-image + standalone OCR + reviewed context package + context-injected caption rerun`

Interpretation rule:

- do not rewrite the four-arm comparison just because the active next-step baseline changed
- do report whether any arm is being compared against the extracted-image baseline, the context-enriched baseline, or both

## Required Control Buckets

The following four buckets must exist before experiment artifacts are added or normalized:

- `control/project_domain/resources/knowledge_bases/`
- `control/project_domain/resources/checklists/`
- `control/project_agent_ops/resources/task_packets/standard/`
- `control/project_agent_ops/resources/task_packets/canonical/`

Current status in this workspace:

- all four buckets already exist

Interpretation rule:

- `knowledge_bases` stores reusable experiment knowledge and distilled findings
- `checklists` stores consistency and implementation checklists
- `task_packets/standard` stores reusable task packet templates
- `task_packets/canonical` stores accepted task packets used as authoritative execution handoff artifacts

This experiment plan should create or update artifacts in those buckets instead of inventing parallel ad hoc directories.

## Comparison Arms

We will compare four paths.

### Arm A. Direct OpenAI API on extracted images

Definition:

- use the local runner at `scripts/caption_images_openai.py`
- call OpenAI Responses API with `gpt-4.1`
- process one image at a time
- persist JSON ledger rows after each image

Current codebase surface:

- script: `scripts/caption_images_openai.py`
- spec: `control/project_domain/resources/specs/prose/SPEC_openai_image_caption_runner.md`
- reviewed context baseline spec:
  `control/project_domain/resources/specs/prose/SPEC_full_image_standalone_ocr_context_package_baseline.md`
- skill: `skills/openai-image-caption-validation/SKILL.md`
- existing smoke result:
  `analysis/cross_validation/02_1/openai_api/smoke_gpt41_media_extract_job.json`

This remains the current comparison baseline arm for extracted-image captioning.
It is not identical to the newer context-enriched rerun baseline.

### Arm B. MCP and Subagent orchestration

Definition:

- use MCP-backed job and image state
- dispatch one image per worker
- use subagent isolation per image
- completion is recognized from registry or task state, not from free-form worker text

Current codebase surface:

- `skills/image-job-dispatcher`
- `skills/image-worker`
- `skills/image-result-auditor`
- `skills/image-commit-manager`
- `skills/vendored-mcp-onboarding`
- MCP setup scripts under `scripts/mcp/`

This arm is an orchestration comparison, not just a model comparison.
It tests whether MCP-backed control is better for traceability, retry, and later mutation gates.

### Arm C. Main Agent led local extraction path

Definition:

- the main agent stays in one process
- image discovery, ordering, caption call, and ledger write all happen in one local control loop
- no subagent fan-out
- no MCP task state required for the first slice

Expected implementation direction:

- reuse `scripts/caption_images_openai.py` logic or split its reusable core
- keep all progress in one local job ledger
- compare simplicity and operator effort against Arm B

This arm exists because the simplest operational path may still win for small and medium batches.

### Arm D. PPT slide screenshot capture -> image to OpenAI API (`gpt-4.1`)

Definition:

- capture slide screenshots from a viewer surface
- treat screenshots themselves as image inputs
- run them through the OpenAI caption path

Current codebase surface:

- screenshot skill: `skills/pptx-slide-screenshot-capture`
- smoke report:
  `control/project_agent_ops/resources/smoke/SMOKETEST_pptx_slide_screenshot_capture-at2026-03-26.md`
- cross-validation directories under:
  `analysis/cross_validation/`

This arm tests whether screenshot-based inputs produce better or worse captions than direct extracted media assets.

## What Must Stay Constant Across Arms

To make the comparison meaningful, the following must stay fixed whenever possible:

- model family for OpenAI path: `gpt-4.1`
- prompt version for OpenAI direct runner unless a comparison explicitly tests prompt variance
- output contract:
  - `caption`
  - `alt_text`
  - `structured_metadata`
  - `new_filename_candidate`
- per-image unit of processing
- stable image ordering within each dataset

When a context-enriched rerun is enabled, the context package contract should also stay fixed:

- image surface remains explicit
- OCR surface remains explicit
- context package provenance remains explicit
- reviewed-only branch promotions stay visible in the record

## Shared Canonical Record Expectations

Even if different arms use different orchestration styles, they should converge on one normalized comparison record per image.

Minimum normalized fields:

- `job_id`
- `image_id`
- `source_path`
- `input_surface`
- `execution_arm`
- `status`
- `caption`
- `alt_text`
- `structured_metadata`
- `new_filename_candidate`
- `raw_response_ref`
- `error`
- `started_at`
- `finished_at`

Recommended optional fields:

- `approved_caption`
- `caption_review_status`
- `metadata_status`
- `rename_status`
- `trace_ref`
- `usage`
- `latency_ms`

This normalization rule is inherited from the job/artifact/execution separation ideas that appear across multiple earlier drafts.

## Experiment Readiness Snapshot

### Arm A. Direct OpenAI API

Status:

- ready now

Evidence:

- local runner exists
- one-image smoke already passed
- dataset-jsonl path already works

### Arm B. MCP and Subagent orchestration

Status:

- infrastructure ready
- comparison report normalization still pending

Evidence:

- workspace MCP stack is registered and boot-verified
- custom image skills are installed

### Arm C. Main Agent local path

Status:

- concept ready
- not yet split into a distinct implementation surface

Required next step:

- define whether Arm C is a thin wrapper over the OpenAI runner or a separate local control loop

### Arm D. PPT slide screenshot to OpenAI API

Status:

- partially ready

Evidence:

- screenshot capture skill exists
- screenshot smoke exists
- `xcrun` is available in cross-validation tool checks

Current constraint:

- `soffice` and `pdftoppm` are unavailable in the recorded cross-validation tool snapshot

Implication:

- viewer-surface screenshot flow is currently more ready than office-export fallback rasterization

## Shared Evaluation Dimensions

Each arm must be compared on the same dimensions.

### Quality

- factual correctness
- visible text accuracy
- object and scene coverage
- hallucination rate
- filename candidate usefulness

### Operational Behavior

- resumability after interruption
- ease of retrying failed rows
- trace clarity
- artifact completeness
- human review readiness

### Performance

- total runtime
- mean latency per image
- failure rate
- API usage visibility

### Integration Fitness

- how naturally the output feeds rename and metadata phases
- how naturally the output fits the existing registry structure
- how easy it is to audit later

## Candidate Datasets

We should use at least two dataset types.

### Dataset Set 1. Small local screenshot set

Directory:

- `analysis/added_screenshots/`

Use:

- smoke tests
- prompt sanity checks
- fast reruns

### Dataset Set 2. Extracted PPTX media

Candidate directories:

- `analysis/pptx_jobs/02_1/media/`
- `analysis/pptx_extract/`
- `analysis/cross_validation/02_1/openai_api/media_extract_dataset.jsonl`

Use:

- baseline extracted-image comparison
- direct media vs screenshot comparison

### Dataset Set 3. Slide screenshots

Candidate directories:

- `analysis/cross_validation/02_1/slide_screenshots/`
- `analysis/cross_validation/02_1/slide_screenshots_simctl/`
- `analysis/cross_validation/02_1/slide_screenshots_simctl_dataset.jsonl`

Use:

- Arm D screenshot path
- screenshot vs extracted-media comparison

## Planned Output Locations

### Arm A

- default ledger target:
  `registry/image_caption_jobs/`
- cross-validation runs may also write under:
  `analysis/cross_validation/<job>/openai_api/`

### Arm B

- MCP state remains authoritative
- we should still export a normalized experiment report under:
  `analysis/cross_validation/<job>/mcp_subagent/`

### Arm C

- local-led runner outputs should go under:
  `analysis/cross_validation/<job>/main_agent_local/`

### Arm D

- screenshot artifacts stay under screenshot job directories
- caption outputs should go under:
  `analysis/cross_validation/<job>/openai_api_screenshot/`

## Reference And Tool Appendix

The following references and tool surfaces were not explicit in the first draft and are now appended for experiment preparation.

### Additional Reference Files

- `control/project_agent_ops/registry/runtime/session_paths.json`
- `control/project_agent_ops/registry/tools/tool_inventory.json`
- `control/project_agent_ops/registry/external_reference_index.json`
- `control/project_domain/resources/reports/url_health_check-at2026-03-26.json`
- `control/project_domain/resources/cross_validation/index.json`
- `control/project_domain/resources/references/REFERENCE_desktop_screenshot_agent_graph_ir.md`

### Additional Tool Surfaces

#### Upstream Or Source Tools

- `canva`
  - relevant when the experiment source is a Canva presentation instead of an already-exported local PPTX

#### Caption And Metadata Tools

- `cv-mcp`
- `filesystem`
- `exiftool`

These already appear in other drafts and the MCP setup reference, and they are now explicitly recognized as experiment-related tool surfaces here as well.

#### Control-Plane Tools

- `agent-task-manager-mcp`
- `conport`

These are mandatory comparison references for Arm B even if execution begins from a smaller local baseline.

#### Runtime And Capture Tools

- `xcrun`
  - available
- `soffice`
  - unavailable in the recorded cross-validation index
- `pdftoppm`
  - unavailable in the recorded cross-validation index

This matters because Arm D should prefer simctl or viewer-surface capture routes over office-export fallback in the current environment.

#### Reference-Only External URLs

The URL health-check report confirms the currently reachable external reference classes:

- OpenAI Codex customization and skills docs
- MCP server repositories
- `openai/skills`
- `cv-mcp`
- `agent-task-manager-mcp`
- `ConPort`
- `ExifTool_MCP`

These URLs are not source of truth, but they are active reference inputs and should not be omitted from experiment-prep reasoning.

## Phase Plan

### Phase 0. Codebase Inventory and Contract Freeze

Goals:

- confirm current script and skill entrypoints
- freeze output contract for all four arms
- choose one naming convention for comparison artifacts

Required files already present:

- `scripts/caption_images_openai.py`
- `skills/openai-image-caption-validation/SKILL.md`
- `skills/pptx-slide-screenshot-capture/SKILL.md`
- `control/project_domain/resources/specs/prose/SPEC_openai_image_caption_runner.md`

### Phase 1. Baseline Arm A Smoke and Batch

Steps:

1. run one-image smoke on `analysis/added_screenshots/`
2. verify ledger shape and raw response archive
3. run a small multi-image batch
4. store summary metrics

This phase establishes the direct OpenAI baseline.

### Phase 2. Arm C Main Agent Local Path

Steps:

1. define the local-only control loop
2. reuse the same output contract as Arm A
3. run on the same image subset
4. compare complexity and output parity

Decision focus:

- is a single-process local runner simpler without losing too much control?

### Phase 3. Arm B MCP and Subagent Path

Steps:

1. register the image set into MCP-backed state
2. dispatch one image per worker
3. collect results only from MCP-backed records
4. export comparison-ready summaries

Decision focus:

- does the orchestration overhead buy us enough retry and audit value?

### Phase 4. Arm D Screenshot -> OpenAI API

Steps:

1. capture slide screenshots from the same source presentation
2. generate a dataset JSONL or directory input
3. run the OpenAI caption path on screenshots
4. compare screenshot captions against extracted-media captions

Decision focus:

- do viewer-surface screenshots preserve more useful context than direct extracted media?

### Phase 5. Comparison and Selection

Required outputs:

- one comparison table across all four arms
- one quality summary
- one operational summary
- one recommendation for default workflow

## Minimum Comparison Table

Each experiment report should include at least:

- arm name
- input dataset
- image count
- success count
- failure count
- average latency per image
- output ledger path
- raw response archive path
- factuality notes
- visible text notes
- resumability notes
- operator burden notes

## Patch Checklist For Future Consolidation

Whenever this plan is patched, verify all of the following:

- Draft 1 Canva flow was checked for source-boundary and rerun implications
- Draft 3 CV MCP flow was checked for lifecycle and failure-policy implications
- Draft 4 image caption pipeline flow was checked for registry and commit-gate implications
- Draft 5 obsidian-style parsing draft was checked for job or artifact model implications
- Draft 6 table-row-rag draft was checked only for reusable schema or fallback ideas
- Draft 7 presentation mapping extension was checked for approved-caption downstream rules
- new experiment arms, if added, are mapped back to this coverage section

## Decision Rules

The default path should not be chosen only by caption quality.
It must satisfy all of the following:

1. acceptable factual quality
2. resumable per-image artifacts
3. clear failure recovery
4. compatibility with downstream rename and metadata stages

Recommended priority order:

1. factual correctness
2. stable and inspectable artifacts
3. rerun and retry safety
4. operational simplicity
5. speed

## Expected Risks

### Risk 1. Cross-arm unfairness

- one arm may use different input surfaces or prompts
- mitigation: freeze dataset and output contract per comparison round

### Risk 2. Hidden orchestration cost

- MCP and subagent overhead may dominate small batches
- mitigation: compare both one-image smoke and small batch behavior

### Risk 3. Screenshot vs extracted-media mismatch

- screenshots may include UI chrome or surrounding context not present in extracted media
- mitigation: treat this as part of the experiment, not as noise

### Risk 4. Registry drift

- direct runs and MCP-backed runs may write outputs in different shapes
- mitigation: define a normalized comparison schema before broad runs

## Immediate Next Actions

1. treat Arm A as the baseline and rerun a one-image smoke into `registry/image_caption_jobs/`
2. use `session_paths.json`, `tool_inventory.json`, and `cross_validation/index.json` as the fixed experiment-prep registry inputs
3. define the normalized experiment report schema used by all four arms
4. implement or document the Arm C local-main-agent path explicitly
5. define the exact MCP-backed execution artifact for Arm B
6. choose one presentation job, then run extracted-media vs screenshot comparison for Arm D

## Working Conclusion

The codebase already has enough surface to start the experiment.
What is still missing is not basic captioning capability.
What is missing is a single comparison frame that evaluates:

- direct OpenAI API
- MCP plus subagent orchestration
- main-agent local control
- screenshot-to-OpenAI path

This plan establishes that comparison frame.

## Appended Patch: Phase0 Core 4-Mode Readiness At 2026-03-28

Bounded status on the shared target image `image11.png`:

- Arm A `Direct OpenAI API on extracted images`: ready
- OCR-enriched rerun on top of Arm A: ready for comparison
- parser/table-structure-enriched rerun: ready for comparison
- reviewed isolated-component rerun: not ready, explicitly waived

Current decision:

- do not start the intended `4-mode` comparison yet
- do allow a bounded `3-mode` comparison among:
  - extracted-image baseline
  - OCR-evidence-enriched rerun
  - parser-enriched rerun

Required re-entry gate for the isolated arm:

- one reviewed isolated component must prove better than the original full image on a shared source image before the arm is promoted into the live comparison set

## Appended Patch: Reviewed Isolated Component Reopen At 2026-03-28

- shared image used for closure:
  - `01_full_presentation_2026-03-17:image11.png`
- reviewed isolated component surface:
  - table-only crop derived from merged candidate structure evidence
- evidence comparison against the full-image OCR:
  - expected table-token coverage remained `16 / 16`
  - extraneous token count improved from `7` to `0`
- bounded rerun status:
  - `completed`
- comparison interpretation:
  - the isolated arm is now comparison-ready for the bounded core 4-mode test
  - this does not promote isolated components to unattended default preprocessing
- updated readiness verdict:
  - `Yes` for the bounded 4-mode comparison on the shared image
