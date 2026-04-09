# Desktop Screenshot Agent Graph IR Reference

This document is a reference asset, not a skill entrypoint.
Use it when a broader architecture note is needed for screenshot-driven agent graphs, typed JSON IR, and trace modeling.
Do not treat this file as a trigger surface for a single skill.

## Purpose

Capture the broader design direction for:

- desktop or simulator screenshot capture workflows
- typed JSON IR for agent graphs
- DOT-first human visualization
- AST-first condition and formula storage
- Langfuse-compatible runtime traces

This reference exists because the design scope is wider than one skill boundary.

## Recommended Ownership Split

- Screenshot capture workflow: narrow operational skill
- Agent graph IR and schema authoring: contract or schema layer
- Mermaid conversion strategy: existing Mermaid strategy skill
- Langfuse integration: existing Langfuse prompt or trace integration skill

## Canonical Source of Truth

The canonical form should be typed JSON IR.

Recommended shape:

- `AgentSpec` for static graph structure
- `AgentRun` for dynamic execution trace
- stable ids for nodes, edges, scopes, routes, and conditions
- explicit split between static spec and runtime events

Why:

- JSON is LLM-friendly
- typed models can emit JSON Schema
- DOT and Mermaid can both be derived from the same source
- runtime trace can map cleanly into Langfuse or a compatible JSON trace

## Representation Rules

### Static spec

Keep these as first-class fields:

- `nodes`
- `edges`
- `scopes`
- `conditions`
- `router_decisions`
- `formulae`

### Runtime trace

Keep these separate from the spec:

- `trace_id`
- `session_id`
- `selected_route`
- `scope_instance_id`
- `iteration_id`
- `stop_reason`
- `tool_call`
- `artifact_ref`

### Screenshot artifacts

Do not store only raw blobs in the trace.
Prefer:

- `artifact_ref`
- `sha256`
- `width`
- `height`
- `capture_mode`
- optional OCR or UI-tree references

## Visual Representation Policy

- Primary human-facing graph output: Graphviz DOT
- Secondary document-friendly output: Mermaid
- Conflict rule: regenerate both from JSON IR, never hand-edit them as source of truth

This keeps nested routing and loop scopes stable while still allowing lightweight README diagrams.

## Parsing and Library Strategy

Prefer mature parsers and validators first.

- typed model and schema: Pydantic + JSON Schema
- graph analysis: NetworkX
- DOT import or render: Graphviz + pydot
- Mermaid import only: official Mermaid parser
- formula handling: AST-first, with LaTeX derived later

Do not hand-roll parsers if an official parser already exists.

## Validation Guardrails

At minimum, validate:

- unique node ids
- valid scope references
- router scopes with two or more route edges
- loop scopes with iteration and stop fields recorded at exit
- AST to rendered representation consistency
- route selection recorded once per router decision

## Recommended First Vertical Slice

Keep the first slice small.

Suggested first slice:

1. typed `AgentSpec` JSON
2. validator for id and scope integrity
3. DOT renderer
4. minimal runtime `AgentRun` trace
5. one screenshot artifact record with metadata

Do not start with Mermaid, Langfuse, custom DSL parsing, and full UI automation all at once.

## Relation To Local Screenshot Capture

In this workspace, the narrow operational entrypoint is:

- `skills/pptx-slide-screenshot-capture`

That skill owns only:

- simulator-based slide screenshot capture for PPTX cross-validation

It does not own:

- broad IR design
- Mermaid strategy
- Langfuse integration
- metadata commit
- final presentation regeneration

## Current Workspace Fit

This reference supports the current three-way validation framing:

1. media extract -> OpenAI caption validation
2. current local PPTX media extract
3. simulator-visible slide screenshot -> OpenAI caption validation

The third path currently depends on a valid viewer surface before `simctl screenshot` is useful.

## When To Read This Reference

Read this file when:

- deciding how to represent screenshot-driven agent graphs
- separating canonical IR from rendered diagrams
- defining validator boundaries before implementation
- planning a future Langfuse-compatible trace model

Do not read this file just to run the current PPTX screenshot capture workflow.
