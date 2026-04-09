# Parser Sidecar To Canonical Schema Promotion

## Pattern

Convert a bounded parser raw sidecar artifact into the canonical `Table -> Row -> Cell` JSON before any downstream wrapper or consumer reads the result.

## Why It Repeats

- parser backends often return raw markdown plus nested JSON sidecars
- downstream consumers should not repeatedly parse parser-native payloads
- provenance recovery and canonical normalization are easy to do inconsistently by hand

## Current Promoted Surface

- `skills/parser-sidecar-to-canonical-schema-promotion`

## Boundary

This pattern owns:

- raw sidecar inspection
- provenance recovery
- canonical normalization

It does not own:

- parser MCP execution
- downstream read-only wrapper consumption
- worksheet export
