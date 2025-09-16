# Stories

## Epic 1 — OAuth-Secured Sample MCP

Use these seeds to draft S1–S7 stories. Reference the listed shards for context and acceptance.

- Seed Map: docs/stories/SEED-epic-1-auth-streaming.md
- PRD Shards: docs/prd/index.md
- Architecture Shards: docs/architecture/index.md
- ADRs: docs/adr/README.md

Story guidance

- Keep each story scoped to one Sx
- Link acceptance to Gate A–D as applicable
- Attach curl/script outputs as evidence in PRs

## Epic 2 — Testing & Tooling Baseline

Use these seeds and drafted stories to roll out repo-wide tooling, coverage, and CI.

- Seed Map: docs/stories/SEED-epic-2-testing-foundations.md
- Issue Tracker: https://github.com/DrJLabs/mcp-farm/issues/5
- Baseline Plan: docs/issues/testing-tooling-baseline.md (if relocated, update links)

Story guidance

- Ensure dependencies between S1–S5 (Ruff baseline → CI → documentation) remain explicit in each story.
- Capture command outputs (Ruff, ty, pytest, CI runs) as evidence in PRs or Issue #5 comments.
