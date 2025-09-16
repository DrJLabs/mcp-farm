# Tooling & Testing Quickstart

Use these commands before opening a PR to ensure code style and tests match the repo baseline.

## 1. Install Pre-commit Hooks

```bash
uvx pre-commit install
```

This installs the repo-level hooks so Ruff and Prettier run automatically on staged files.

## 2. Ruff Lint

```bash
uvx ruff check .
```

Runs the linter across `fastmcp/`, `tests/`, `sample-deep-research-mcp/`, and `scripts/` using the shared root configuration.

## 3. Ruff Format

```bash
uvx ruff format --check .
```

Verifies formatting and import order without writing changes. To autofix, drop `--check`.

## 4. Prettier Docs & Config Files

```bash
npx prettier --check '**/*.{md,mdx,json,yaml,yml}'
```

Ensures Markdown, JSON, and YAML assets stay consistent.

## 5. Pytest Smoke

```bash
uv run pytest -q
```

Execute the current pytest suite. Stories may require deeper coverage—see QA assessments for scenario-level guidance.

## Troubleshooting

- If `npx` complains about Node, install Node 18+ or enable Corepack (`corepack enable`).
- Clear caches with `rm -rf ~/.cache/uv` if dependency resolution stalls.
- Re-run `uvx pre-commit install` after updating `.pre-commit-config.yaml`.
