# Repeated Issue Candidate: Venv Interpreter Symlink Resolution Drift

## Why This Repeats

Vendored runtimes under `.venv/bin/python` can be symlinked to the system interpreter.
If a script normalizes that path with `Path.resolve()`, it can accidentally drop the venv context and lose installed packages.

## Observed Workspace Case

- `skills/object-isolation-correction/scripts/classify_alpha_split_batch.py`
- first batch run produced `ModuleNotFoundError: No module named 'numpy'`
- root cause: the report surface and worker invocation dereferenced the vendored interpreter path

## Current Workaround

- keep runtime interpreter paths as entered or `expanduser()` only
- do not `resolve()` venv interpreter paths before subprocess execution
- verify by rerunning the same workload and checking the expected package import path

## Structural Fix Candidate

- standard launcher/runtime-path helper that preserves venv entrypoints
- code review rule: `Path.resolve()` is allowed for regular files but not for `.venv/bin/python` style runtime entrypoints

## Escalation Trigger

Escalate if another vendored Python runtime:

- drops site-packages unexpectedly
- reports system Python in a generated run artifact
- only fails after a path normalization or report-generation refactor
