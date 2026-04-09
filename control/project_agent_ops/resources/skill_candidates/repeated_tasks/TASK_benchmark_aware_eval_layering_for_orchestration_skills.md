# Repeated Task: Benchmark-Aware Eval Layering For Orchestration Skills

## Pattern

When a skill governs packetized workers, tool-use quality, MCP truth sources, or subagent orchestration, its local `evals/evals.json` should stay skill-local but align its metric vocabulary with `agent-tool-benchmark`.

## Stable Recipe

1. keep `evals/evals.json` as the local acceptance layer
2. add an explicit `benchmark_alignment_layer` reference to `agent-tool-benchmark`
3. declare primary benchmark metrics that fit the skill surface
4. interpret each metric in skill-specific terms instead of inventing a new scoring vocabulary
5. keep local assertions and fail signals grounded in the skill's actual boundary
6. validate the JSON and check that the benchmark vocabulary still matches the orchestration surface

## Why It Repeats

- orchestration skills need both local boundary tests and higher-level quality metrics
- packetized workflows reuse the same benchmark axes across dispatcher, worker, auditor, and activation skills
- without explicit layering, local eval files drift into ad hoc metric names

## Promotion Target

- reusable eval-layering checklist
- sidecar template for benchmark-aware orchestration skills

## Current Proven Example

- `skills/image-job-dispatcher/evals/evals.json`
- `skills/image-worker/evals/evals.json`
- `skills/image-result-auditor/evals/evals.json`
- `skills/table-branch-activation-slice/evals/evals.json`
