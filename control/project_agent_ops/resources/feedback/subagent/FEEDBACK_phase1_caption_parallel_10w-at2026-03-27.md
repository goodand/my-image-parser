# Subagent Feedback: Phase 1 Caption Parallel 10w

## Scope

- experiment: `phase1_caption_10w`
- path: extracted media + OpenAI `gpt-4.1`
- worker shape: one shard per worker, one ledger per worker

## What worked

- issued task-packets with `locked_paths` prevented output overlap
- per-worker ledger plus sidecars made verification easy
- the shard manifest gave one canonical place to inspect ownership
- completed batch total was readable from worker-owned outputs

## What failed or degraded

- the live Codex session still enforced the earlier `max_threads = 6` cap even after the repo-local `.codex/config.toml` was added
- because of that, the 10-worker run had to execute in two waves instead of a single 10-way fan-out

## Operational takeaway

- repo-local `.codex/config.toml` is the right canonical place to pin `max_threads = 10`
- but the new cap should be expected only from a fresh Codex session
- for the current live session, completed workers may need to be explicitly closed before new workers can be spawned

## Reusable guidance

1. create shard manifest first
2. create issued task-packets with `locked_paths`
3. run one-image smoke gate
4. start parallel workers
5. close completed workers if the live session still holds old thread caps
6. aggregate only from worker ledgers, not from chat text
