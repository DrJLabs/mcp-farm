# Story Seed — Epic 2: Testing & Tooling Baseline

Purpose: Define the implementation roadmap that elevates linting, formatting, type checks, and automated tests to production-ready coverage. This epic flows from GitHub issue #5 and the testing/tooling plan.

Note: File paths are workspace-relative unless noted.

## Epic Objectives

- Enforce Ruff lint + format across the entire monorepo using a shared configuration.
- Extend automation to documentation assets (Markdown/JSON/YAML) via Prettier.
- Raise automated test coverage for the sample MCP and supporting scripts with measurable coverage thresholds.
- Introduce CI enforcement (uv, Ruff, ty, pytest --cov) so regressions are blocked before merge.
- Document the new developer workflow, ensuring contributors can run the baseline locally.

## Success Metrics

- `uvx ruff check` and `uvx ruff format --check` pass cleanly on every push; Ruff config lives at repo root.
- Pytest suite produces ≥80% line coverage and exercises sample MCP tool functions plus streaming smoke.
- CI pipeline (GitHub Actions) fails on lint, format, type checking, or coverage regressions and uploads coverage artifacts.
- Developer onboarding docs describe the lint/format/test commands and are referenced by at least one story handoff.

## Backlog Seeds (Sx)

### S1 — Repo-level Ruff & Prettier baseline

- Inputs:
  - docs/issues/testing-tooling-baseline.md
  - fastmcp/.pre-commit-config.yaml
  - fastmcp/pyproject.toml (tool.ruff, tool.ty)
- Deliverables:
  - Root `pyproject.toml` (or `.ruff.toml`) that scopes Ruff to `fastmcp/`, `tests/`, `sample-deep-research-mcp/`, `scripts/`.
  - Repo-level `.pre-commit-config.yaml` running Ruff lint/format and Prettier (Markdown/JSON/YAML).
- Gate T1 evidence:
  - `uvx ruff check` and `uvx ruff format --check` succeed locally; Prettier dry-run shows no changes.

### S2 — Harmonize package configs & type checks

- Inputs:
  - fastmcp/pyproject.toml (`tool.ty` and Ruff overrides)
  - docs/issues/testing-tooling-baseline.md (Plan §2)
- Deliverables:
  - Duplicate Ruff settings removed or updated to inherit root config.
  - `tool.ty.src.include` covers sample MCP and shared tests; ignored rules triaged or ticketed.
- Gate T2 evidence:
  - `uv run ty check` passes; documented list of remaining ignores with rationale in issue #5.

### S3 — Unit and integration coverage expansion

- Inputs:
  - sample-deep-research-mcp/sample_mcp.py
  - tests/
  - scripts/stream_smoke.py
  - docs/validation.md (smoke requirements)
- Deliverables:
  - Pytest unit tests for `search`/`fetch` tool paths and auth edge cases.
  - Stream smoke script wrapped in pytest (mark `integration`).
  - `pytest-cov` configured with ≥80% threshold; HTML/XML outputs stored under `tests/coverage/`.
- Gate T3 evidence:
  - `uv run pytest --cov` report meeting threshold; integration marks listed in `pytest --markers`.

### S4 — CI workflow enforcement

- Inputs:
  - .github/workflows (new)
  - docs/issues/testing-tooling-baseline.md (Plan §4)
  - scripts/validate_mvp.sh
- Deliverables:
  - `.github/workflows/ci.yml` covering uv sync, Ruff lint, Ruff format check, ty check, pytest with coverage, artifact upload.
  - Cache strategy for `~/.cache/uv` documented in workflow.
- Gate T4 evidence:
  - Successful CI run on feature branch; failure example when formatting intentionally broken (screenshots/log in PR).

### S5 — Developer experience documentation

- Inputs:
  - docs/validation.md
  - onboarding-chatgpt.md (structure reference)
  - README.md (setup instructions)
- Deliverables:
  - Updated `docs/validation.md` (or new `docs/testing.md`) describing local commands for Ruff, Prettier, ty, pytest.
  - Quickstart snippet added to README.md.
- Gate T5 evidence:
  - Documentation reviewed and linked from issue #5; onboarding checklist references new commands.

## Dependencies & Risks

- Requires GitHub Actions access in repo (confirm permissions).
- Potential ty rule churn—schedule follow-up if ignored Diagnostics still exceed tolerances after S2.
- Streaming smoke tests may need mock Keycloak tokens; coordinate with Dev to provide fixtures.

## Related Work

- GitHub Issue #5 “Harden testing and tooling baseline for MCP Farm”.
- PRD Gates: supports FR8 and validation readiness checkpoints.
- ADR 001 (Streamable HTTP) informs streaming smoke acceptance.

## Acceptance Gates Summary

- **Gate T1**: Ruff + Prettier automation proven locally.
- **Gate T2**: Type checker spans shared modules and passes.
- **Gate T3**: Coverage target met with new tests.
- **Gate T4**: CI workflow blocks regressions; artifact uploaded.
- **Gate T5**: Documentation updated for developers.

## Handoff Notes

- Once Gate T3 passes, QA can begin authoring risk-based test designs against the expanded suite.
- Coordinate with Scrum Master to slice S1–S5 into sprint stories; ensure each story references this seed and issue #5.
