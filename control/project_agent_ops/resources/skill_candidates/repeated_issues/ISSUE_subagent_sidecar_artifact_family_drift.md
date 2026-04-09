# Issue: Subagent Sidecar Artifact Family Drift

## Recurrence Signal

Subagent-authored skill sidecars, especially `runtime.md` and `troubleshooting.md`, can describe an ideal or future artifact family as if it were the current bounded evidence surface.

Typical signs:

- generic JSONL family names are written even though the current bounded run produced timestamped JSON artifacts
- a review gate is described with stronger language than the current evidence actually proves
- a sidecar mixes "current workspace" claims with "future integration" claims without labeling the difference

## Current Example

`table-branch-activation-slice` initially described parser-smoke and normalized outputs with generic `phase0_table_parser_*` JSONL artifact names, while the current bounded run actually produced:

- `phase0_paddleocr_table_parse_smoke_at2026_03_28.json`
- `phase0_paddleocr_table_parse_raw_at2026_03_28.json`
- `phase0_paddleocr_table_parse_normalized_at2026_03_28.json`

It also described the triage gate as `xhigh` even though the currently verified artifact only proved a reviewed triage manifest.

## Why It Matters

- direct verification becomes noisy because sidecars appear to point at missing files
- later agents may treat an aspirational artifact contract as already implemented
- confidence in packetized subagent sidecar generation drops if the main agent has to reinterpret every path claim

## Current Workaround

- verify subagent-created sidecars directly against real files, smoke reports, and tests
- patch current-state claims down to the proven bounded evidence surface
- reserve future or ideal artifact families for plans or explicitly labeled future-work notes

## Structural Fix Candidate

- add a direct review pass after packetized sidecar generation
- require `current bounded example` wording whenever a sidecar references artifact names not enforced by code
- require claim-level file existence checks before accepting subagent-authored runtime surfaces
