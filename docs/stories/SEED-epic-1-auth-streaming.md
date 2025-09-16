# Story Seed — Epic 1: OAuth‑Secured Sample MCP (S1–S7)

Purpose: Give the Scrum Master a precise map from PRD/Architecture shards to story drafts. Each story block lists Inputs, Deliverables, and Gate evidence.

Note: File paths are workspace‑relative.

## S1 — Bootstrap env and healthcheck
- Inputs:
  - docs/prd/epic-list.md
  - docs/architecture/observability-health.md
  - docs/architecture/configuration-environment-variables.md
  - .env.example
- Deliverables:
  - `.env.example` confirmed; `GET /healthz` returns `{ "ok": true }`.
- Gate (A pre‑req):
  - docs/validation.md (Health step) and curl output in commit/PR.

## S2 — Traefik routing + TLS labels
- Inputs:
  - docs/prd/epic-list.md
  - docs/architecture/reference-deployment-docker-traefik-proposed.md
  - compose.yaml
- Deliverables:
  - Traefik labels for MCP router; TLS enabled; health reachable over HTTPS.
- Gate (A pre‑req):
  - docs/validation.md (Health via Traefik) evidence.

## S3 — PRM + 401 hint
- Inputs:
  - docs/prd/requirements.md (FR1–FR2)
  - docs/architecture/prm-shape-minimal-example-mvp.md
  - sample-deep-research-mcp/sample_mcp.py
  - docs/validation.md (PRM + 401 sections)
- Deliverables:
  - `/.well-known/oauth-protected-resource` JSON served; unauth `GET /mcp` → 401 with PRM in `WWW-Authenticate`.
- Gate A evidence:
  - Curl outputs stored in PR/issue.

## S4 — OAuth 2.1 validation (JWKS, iss/aud)
- Inputs:
  - docs/prd/requirements.md (FR3)
  - docs/architecture/security-controls.md
  - docs/architecture/configuration-environment-variables.md
  - docs/validation.md (OIDC discovery + JWKS)
  - sample-deep-research-mcp/sample_mcp.py
- Deliverables:
  - JWTVerifier configured with `KC_ISSUER`, `KC_JWKS_URI?`, `MCP_AUDIENCE` (+ optional fallback) and header‑only Bearer enforced.
- Gate B evidence:
  - OIDC/JWKS curls; successful authenticated call (any minimal tool call OK).

## S5 — Streamable‑HTTP transport (preferred) + SSE fallback
- Inputs:
  - docs/prd/requirements.md (FR4, FR8)
  - docs/architecture/performance-slos-mvp-targets.md
  - scripts/stream_smoke.py
  - sample-deep-research-mcp/sample_mcp.py
- Deliverables:
  - Default transport http (`/mcp`) with streaming chunks; SSE fallback preserved.
- Gate C evidence:
  - Stream smoke output in PR; note p95 TTFB < 2s or chunk cadence ≥ 10.

## S6 — RFC 8414 path‑insert shim
- Inputs:
  - docs/prd/requirements.md (FR6)
  - docs/architecture/reference-deployment-docker-traefik-proposed.md
  - docs/validation.md (2b shim checks)
  - compose.yaml
- Deliverables:
  - Traefik ReplacePathRegex rewrite mapping `/.well-known/*` → realm‑first paths; verified.
- Gate C evidence:
  - Curl outputs for both shimmed endpoints.

## S7 — ChatGPT Developer‑mode onboarding + validation scripts
- Inputs:
  - docs/onboarding-chatgpt.md
  - scripts/validate_mvp.sh
  - docs/architecture/frnfr-gates-evidence-map.md
- Deliverables:
  - Connector added; end‑to‑end search+fetch works; evidence captured.
- Gate D evidence:
  - Screenshot(s) and logs attached to PR/issue.

## Cross‑Cutting References
- Out‑of‑Scope (guardrails): docs/prd/out-of-scope-mvp.md
- SLOs & Perf: docs/architecture/performance-slos-mvp-targets.md
- Security: docs/architecture/security-controls.md
- ADRs (accepted): docs/adr/README.md

## Suggested Story Structure (per Sx)
- Story: “Sx: <title>”
- Acceptance Criteria: Gate reference + concrete curl/script outputs.
- Tasks: update code/labels/envs; run validation; attach evidence.
- Rollback: re‑deploy previous image; revert labels if needed.
