# Feedback Buckets

Canonical root for agent and model feedback created after project start:

- `control/project_agent_ops/resources/feedback/claude/`
- `control/project_agent_ops/resources/feedback/gemini/`
- `control/project_agent_ops/resources/feedback/codex/`
- `control/project_agent_ops/resources/feedback/subagent/`

Rules:

- provider- or agent-specific feedback belongs under the matching bucket
- subagent execution feedback belongs under `feedback/subagent/`
- reusable operational summaries stay in `resources/`, not `runs/`
- if the same lesson repeats, promote it into `skill_candidates/repeated_tasks/` or `skill_candidates/repeated_issues/`
