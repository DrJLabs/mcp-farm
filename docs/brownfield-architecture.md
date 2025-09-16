# mcp-farm Brownfield Architecture Document

## Introduction

This document captures the current state of the mcp-farm repository with emphasis on the MVP defined in the PRD: securing the included sample MCP server with OAuth 2.1 behind Traefik/Keycloak and preferring Streamable‑HTTP transport (SSE as fallback). It is written to support AI agents implementing Epic 1.

### Document Scope

Focused on areas relevant to: Epic 1 “OAuth‑Secured Sample MCP” (PRM + 401 hint, OAuth 2.1 + PKCE, JWKS validation, Traefik routing/TLS, Streamable‑HTTP preferred, SSE fallback).

### Change Log

| Date       | Version | Description                                                  | Author |
| ---------- | ------- | ------------------------------------------------------------ | ------ |
| 2025-09-15 | 1.1     | ADRs accepted; elicitation applied; Ready for Implementation | Arch   |
| 2025-09-15 | 1.0     | Initial brownfield analysis                                  | Arch   |

## Quick Reference – Key Files and Entry Points

### Critical Files

- Main entry (sample MCP): `sample-deep-research-mcp/sample_mcp.py`
- Data fixture: `sample-deep-research-mcp/records.json`
- Python deps: `sample-deep-research-mcp/requirements.txt`
- Readme: `sample-deep-research-mcp/README.md`
- PRD: `docs/prd.md`

- FastMCP reference repo: `fastmcp/` (source and docs for transports and server patterns)

### Enhancement Impact Areas (from PRD)

- Add PRM endpoint: `/.well-known/oauth-protected-resource`
- 401 responses include `WWW-Authenticate: Bearer resource_metadata="<PRM URL>"`
- JWT validation against Keycloak JWKS; enforce `iss` and `aud`
- Prefer Streamable‑HTTP transport; retain SSE fallback
- Traefik TLS + routing via labels; optional RFC 8414 path‑insert rewrites
- Env configuration: `MCP_SERVER_URL`, `KC_ISSUER`, `MCP_AUDIENCE`, CORS

## High‑Level Architecture

### Technical Summary (Current)

- Single Python FastMCP server started via `FastMCP.run(transport="sse", host="127.0.0.1", port=8000)`.
- No authentication/authorization; no PRM route; no JWT verification.
- Transport: SSE only at present; Streamable‑HTTP not yet configured.
- Execution is a single process intended for local development (binds to `127.0.0.1`).

### Actual Tech Stack

| Category  | Technology | Version/Notes                     |
| --------- | ---------- | --------------------------------- |
| Language  | Python     | 3.x (CPython)                     |
| MCP SDK   | fastmcp    | `2.5.2` (from `requirements.txt`) |
| MCP Core  | mcp        | `1.9.2` (from `requirements.txt`) |
| Transport | SSE        | Default in `sample_mcp.py`        |

### Repository Structure Reality Check

- Root contains project docs and BMAD agent config.
- Sample server resides in `sample-deep-research-mcp/` (no containerization files present here).
- Docs include PRD and OAuth/Keycloak primers under `docs/`.

## Source Tree and Module Organization

```text
./
├─ docs/
│  ├─ prd.md
│  └─ brownfield-architecture.md (this file)
└─ sample-deep-research-mcp/
   ├─ sample_mcp.py          # FastMCP server with tools (SSE transport)
   ├─ requirements.txt       # python deps (fastmcp, mcp, pydantic, etc.)
   ├─ records.json           # sample data
   └─ README.md
```

### Key Modules and Their Purpose

- `sample_mcp.py`
  - `create_server()` builds a `FastMCP` named "Cupcake MCP" with two tools:
    - `search(query: str) -> SearchResultPage` (keyword search over `records.json`)
    - `fetch(id: str) -> FetchResult` (lookup by id)
  - Main guard runs the server: `create_server().run(transport="sse", host="127.0.0.1", port=8000)`
- Pydantic models: `SearchResult`, `SearchResultPage`, `FetchResult` model tool inputs/outputs.

## Data Models and APIs

### Pydantic Models (tool schemas)

- `SearchResult { id, title, text }`
- `SearchResultPage { results: list[SearchResult] }`
- `FetchResult { id, title, text, url?, metadata? }`

### MCP Transport Endpoints (Current)

- SSE transport exposed by FastMCP runner on `http://127.0.0.1:8000` (per README).
- No Streamable‑HTTP endpoint configured yet.
- No PRM route; unauthenticated requests do not advertise PRM metadata.

## Technical Debt and Known Issues (Current)

1. No OAuth 2.1 integration: missing PRM route and JWT validation.
2. SSE‑only; Streamable‑HTTP not yet wired (required/preferred per PRD).
3. Binds to `127.0.0.1` for local development; when containerized behind Traefik, the app must bind `0.0.0.0` so Traefik can reach it over the bridge network.
4. No healthcheck endpoint; no restart policy; limited operational notes.
5. No log redaction policy; risk of leaking sensitive headers if added later.

### Workarounds and Gotchas

- Container networking: Inside containers, binding to 127.0.0.1 isolates the process from other containers. Bind `0.0.0.0` when running under Traefik; keep `127.0.0.1` only for local, non-container runs.
- Tool schemas are embedded; any auth layer must not alter tool I/O contracts.

## Integration Points and External Dependencies (Planned per PRD)

### External Services

| Service  | Purpose                  | Integration Type | Notes                                  |
| -------- | ------------------------ | ---------------- | -------------------------------------- |
| Keycloak | OAuth 2.1 IdP            | OIDC/JWKS        | Enforce `iss` and `aud` claims         |
| Traefik  | TLS + routing + rewrites | Reverse proxy    | Labels for host routing, RFC 8414 shim |
| ChatGPT  | MCP Developer‑mode       | Client           | Performs OAuth; streams tool calls     |

### Internal Integration Points

- PRM route under `/.well-known/oauth-protected-resource` must be public.
- Protected MCP endpoints must 401 with PRM hint when unauthenticated.
- JWT validation occurs in‑app for MVP (no ForwardAuth); Traefik provides TLS and routing.

## Development and Deployment (Current Reality)

### Local Development Setup

1. `cd sample-deep-research-mcp`
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python sample_mcp.py` (starts SSE on `127.0.0.1:8000`)

### Build and Deployment Process

- No Dockerfile/compose in this folder at present; Traefik labels and containerization to be added during Epic 1.

## Testing Reality

- No test suite present for the sample server.
- Validation for MVP to be provided as scripts/docs (PRM/AS/401 checks, Streamable‑HTTP round‑trip).

## If Enhancement PRD Provided – Impact Analysis

### Files That Will Need Modification

- `sample-deep-research-mcp/sample_mcp.py`: add PRM route, 401 PRM hint behavior, JWT validation (JWKS), switch/add Streamable‑HTTP transport; use `0.0.0.0` bind in container, `127.0.0.1` for local dev.

### New Files/Modules Likely Needed

- `docs/validation.md` (or similar) with curl examples for PRM/AS/401/stream tests.
- Containerization (Dockerfile/compose) and Traefik labels (host routing, optional RFC 8414 path‑insert rewrites).
- `.env.example` capturing `MCP_SERVER_URL`, `KC_ISSUER`, `MCP_AUDIENCE`.

### Integration Considerations

- Ensure PRM is reachable unauthenticated through Traefik.
- JWT validation must reject tokens with wrong `iss`/`aud`; accept one configured fallback audience if required by ChatGPT.
- Prefer Streamable‑HTTP; keep SSE fallback for compatibility/testing.

## Appendix – Useful Commands

```bash
# Local sample server
python sample_mcp.py

# Skeleton for validation (to be implemented during Epic 1)
curl -sS https://<mcp-host>/.well-known/oauth-protected-resource | jq
curl -i  https://<mcp-host>/mcp/... # expect 401 with WWW-Authenticate PRM hint
# Streamable‑HTTP smoke (expect 200 and streamed chunks)
```

## Operational Notes & Validation (Added)

### Networking Assumptions

- Local: bind `127.0.0.1:8000`.
- In container behind Traefik: bind `0.0.0.0:8000` so Traefik can connect via the bridge network.
- Validate from Traefik:
  - `docker exec -it traefik sh -lc "apk add --no-cache curl >/dev/null 2>&1 || true; curl -i http://mcp:8000/healthz"` → expect 200.

### Transport Capability Check

- Confirm Streamable‑HTTP support in FastMCP (see `fastmcp/` repo). If unavailable, satisfy Gate C with SSE for MVP and plan Streamable‑HTTP post‑MVP.

### PRM and 401 Ownership

- Ensure app emits 401 with PRM hint:
  - `curl -i https://<mcp-host>/mcp/messages/ | sed -n '1,15p'` → expect `WWW-Authenticate: Bearer resource_metadata="https://<mcp-host>/.well-known/oauth-protected-resource"`.

### Audience Policy

- Enforce `aud=MCP_SERVER_URL`. Optional fallback via `MCP_ALT_AUDIENCE`; log when fallback is used.

### Discovery Smoke Tests

```bash
curl -sS https://<oauth-host>/.well-known/oauth-authorization-server/realms/<realm> | jq '.token_endpoint,.authorization_endpoint,.jwks_uri'
curl -sS https://<oauth-host>/realms/<realm>/.well-known/openid-configuration | jq '.issuer,.jwks_uri'
```

### Streaming Acceptance

- First chunk < ~2s and ≥10 chunks total through Traefik for Streamable‑HTTP (or equivalent SSE cadence).

## Reference Deployment — Docker + Traefik (Proposed)

This section provides a minimal, copy‑pasteable baseline for Epic 1. It is intentionally simple and label‑driven so it can be adapted per host.

### Dockerfile (sample‑deep‑research‑mcp)

```dockerfile
# ./sample-deep-research-mcp/Dockerfile
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Default dev bind; override via env in compose
ENV BIND_HOST=0.0.0.0 BIND_PORT=8000
CMD ["python", "sample_mcp.py"]
```

### Compose with Traefik Labels

```yaml
# ./compose.yaml (reference)
version: "3.9"
services:
  traefik:
    image: traefik:v3.1
    command:
      - --providers.docker=true
      - --entrypoints.web.address=:80
      - --entrypoints.websecure.address=:443
      - --certificatesresolvers.dev.acme.tlschallenge=true
      - --certificatesresolvers.dev.acme.email=you@example.com
      - --certificatesresolvers.dev.acme.storage=/letsencrypt/acme.json
    ports: ["80:80", "443:443"]
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - traefik_data:/letsencrypt

  mcp:
    build:
      context: ./sample-deep-research-mcp
    environment:
      MCP_SERVER_URL: https://mcp.localhost
      KC_ISSUER: https://auth.localhost/realms/mcp
      MCP_AUDIENCE: https://mcp.localhost
      MCP_ALT_AUDIENCE: "" # optional fallback; leave empty by default
      BIND_HOST: 0.0.0.0
      BIND_PORT: 8000
      LOG_LEVEL: info
    expose: ["8000"]
    labels:
      - traefik.enable=true
      - traefik.http.routers.mcp.rule=Host(`mcp.localhost`)
      - traefik.http.routers.mcp.entrypoints=websecure
      - traefik.http.routers.mcp.tls=true
      - traefik.http.routers.mcp.tls.certresolver=dev
      - traefik.http.services.mcp.loadbalancer.server.port=8000
      # Optional: RFC 8414 path‑insert shim on the auth host
      # Map /.well-known/openid-configuration → /realms/mcp/.well-known/openid-configuration
      # Requires the Keycloak service to be attached to the same network and reachable as "keycloak".

  keycloak:
    image: quay.io/keycloak/keycloak:25.0
    command: ["start"]
    environment:
      KC_PROXY: edge
      KC_HOSTNAME: auth.localhost
      KC_HTTP_ENABLED: "true"
    expose: ["8080"]
    labels:
      - traefik.enable=true
      - traefik.http.routers.kc.rule=Host(`auth.localhost`)
      - traefik.http.routers.kc.entrypoints=websecure
      - traefik.http.routers.kc.tls=true
      - traefik.http.routers.kc.tls.certresolver=dev
      - traefik.http.services.kc.loadbalancer.server.port=8080
      # Optional RFC 8414 path‑insert shim (ReplacePathRegex)
      - traefik.http.routers.kc-discovery.rule=Host(`auth.localhost`) && PathPrefix(`/.well-known/`)
      - traefik.http.routers.kc-discovery.entrypoints=websecure
      - traefik.http.routers.kc-discovery.tls=true
      - traefik.http.routers.kc-discovery.middlewares=kc-discovery-rewrite
      - traefik.http.middlewares.kc-discovery-rewrite.replacepathregex.regex=^/\.well-known/(.*)
      - traefik.http.middlewares.kc-discovery-rewrite.replacepathregex.replacement=/realms/mcp/.well-known/$${1}

volumes:
  traefik_data: {}
```

Notes

- For production, replace `mcp.localhost` and `auth.localhost` with real FQDNs and use a DNS‑validated resolver. The above is suitable for local testing with hosts entries.
- The MCP container binds `0.0.0.0:8000` so Traefik can reach it. Local non‑container runs may keep `127.0.0.1`.

## Configuration — Environment Variables

| Variable           | Purpose                            | Example                                                           |
| ------------------ | ---------------------------------- | ----------------------------------------------------------------- |
| `MCP_SERVER_URL`   | Canonical external URL of MCP      | `https://mcp.localhost`                                           |
| `KC_ISSUER`        | Keycloak Issuer (realm public URL) | `https://auth.localhost/realms/mcp`                               |
| `KC_JWKS_URI`      | Optional explicit JWKS URI         | `https://auth.localhost/realms/mcp/protocol/openid-connect/certs` |
| `MCP_AUDIENCE`     | Expected `aud` claim               | `https://mcp.localhost`                                           |
| `MCP_ALT_AUDIENCE` | Optional fallback audience         | `` (empty)                                                        |
| `BIND_HOST`        | Bind interface inside container    | `0.0.0.0`                                                         |
| `BIND_PORT`        | Bind port                          | `8000`                                                            |
| `ALLOWED_ORIGINS`  | CORS allowlist if needed           | `https://chat.openai.com`                                         |
| `LOG_LEVEL`        | App log level                      | `info`                                                            |

Implementation Guidance

- Validate envs at startup and emit a single structured line summarizing effective values (excluding secrets).
- Do not log tokens or Authorization headers; ensure redaction in both success and error paths.

## PRM Shape — Minimal Example (MVP)

The PRD requires a PRM endpoint at `/.well-known/oauth-protected-resource`. The minimal shape we will expose for MVP is:

```json
{
  "resource": "https://mcp.localhost",
  "authorization_servers": ["https://auth.localhost/realms/mcp"]
}
```

Notes

- The exact metadata fields are validated via our acceptance script; the above is a minimal, practical payload for clients to discover the AS and correlate the resource.
- Return `application/json; charset=utf-8` and cache for a short TTL (e.g., 60s) to allow config changes during bring‑up.

## Security Controls

- Bearer in header only; reject tokens in query/path.
- Enforce `iss == KC_ISSUER` and `aud in {MCP_AUDIENCE, MCP_ALT_AUDIENCE?}` (if fallback configured, log usage once per minute max to avoid noise).
- Clock skew tolerance ≤ 60s; verify `exp` and `nbf`.
- Structured audit log for auth decisions: outcome, reason, subject (sub), truncated jti, client_id if present.
- CORS: default deny; allow only known MCP client origins if required (ChatGPT typically does not need CORS for SSE/HTTP from server‑side).

Rate Limiting & Request Limits

- Traefik rate limit (per source IP): average 50 rps, burst 25 (tune with evidence).
- Max body size: 2 MiB (Traefik middleware) for MCP endpoints.

## Observability & Health

- Add `/healthz` returning 200 and a minimal body `{ "ok": true }` (unauthenticated) — used by Traefik/docker healthchecks.
- Logs: JSON lines; include `request_id`, `user_agent`, `remote_addr`, `transport` (sse|http-stream), and `latency_ms` for each request.
- Startup banner: dump effective transport(s) enabled and PRM URL.

Monitoring (MVP)

- Logs to stdout; container logs aggregated by platform.
- Optional: enable Traefik Prometheus metrics; no app metrics for MVP.

## Risks & Mitigations

- Streamable‑HTTP availability: If not fully supported by current FastMCP version, Gate C allows SSE fallback; document measured latency so we can upgrade later.
- Audience mismatch from ChatGPT: permit `MCP_ALT_AUDIENCE` for compatibility, but gate with audit logging and a 90‑day deprecation note.
- Path‑insert discovery differences: include the Traefik ReplacePathRegex shim for clients that expect RFC 8414 at `/.well-known/...` without realm prefix.

## Definition of Done (Architecture)

- Reference Dockerfile and compose with Traefik labels reviewed and stored in this doc.
- Env configuration table complete and mirrored in `.env.example` (to be added in S1).
- PRM example payload defined; acceptance script to verify presence and 401 PRM hint.
- Security/observability notes actionable by devs; health endpoint specified.
- All above mapped to PRD Gates A–C.

Accepted ADRs

- 001 Prefer Streamable‑HTTP over SSE (keep SSE fallback) — Accepted (docs/adr/001-prefer-streamable-http-over-sse.md)
- 002 In‑app JWT verification vs Traefik ForwardAuth — Accepted (docs/adr/002-in-app-jwt-vs-traefik-forwardauth.md)
- 003 PRM at well‑known on MCP host — Accepted (docs/adr/003-prm-at-well-known-on-mcp-host.md)
- 004 RFC 8414 path‑insert shim via Traefik — Accepted (docs/adr/004-rfc-8414-path-insert-shim-via-traefik.md)
- 005 Bind policy: 127.0.0.1 local / 0.0.0.0 container — Accepted (docs/adr/005-bind-policy-127-0-0-1-local-0-0-0-0-container.md)

## Next Actions (for Epic 1)

1. S1: Add `.env.example` and `/healthz`; wire BIND_HOST logic (127.0.0.1 vs 0.0.0.0). [DONE]
2. S2: Introduce Dockerfile and compose; verify Traefik routing to health. [DONE]
3. S3: Implement PRM route and 401 PRM hint. [DONE]
4. S4: Add JWT validation (JWKS, iss/aud enforcement) with structured audit logs. [DONE]
5. S5: Enable Streamable‑HTTP (prefer) with SSE fallback; record streaming evidence. [DONE]
6. S6: RFC 8414 path‑insert shim via Traefik ReplacePathRegex on `auth.localhost` mapping `/.well-known/*` → `/realms/mcp/.well-known/*`; add validation steps. [DONE]
7. S7: ChatGPT Developer‑mode onboarding + validation scripts; confirm custom connector works end‑to‑end. [DONE]

## Scope Boundaries (Out of Scope for MVP)

- Multi‑tenant UI, user management UI, or admin console.
- Non‑Keycloak identity providers and non‑Traefik ingress.
- Traefik ForwardAuth or centralized auth proxy.
- Persistent databases and data migrations; sample remains file‑backed.
- Advanced monitoring stack (Prometheus/Grafana) beyond Traefik metrics.

## FR/NFR → Gates & Evidence Map

- FR1/FR2 (PRM + 401 hint) → Gate A → sample_deep_research_mcp (RemoteAuthProvider) + docs/validation.md steps 1 & 3.
- FR3 (JWT validation iss/aud/JWKS) → Gate B → JWTVerifier config via env; curl OIDC + signed token test.
- FR4/FR8 (Streamable‑HTTP preferred + streaming acceptance) → Gate C → scripts/stream_smoke.py, validate_mvp.sh.
- FR5/FR6 (Traefik TLS + discovery shim) → Gate C → compose.yaml labels; validation 2b.
- FR7 (Env config) → Gate A → .env.example + config table.
- FR9 (Tool functionality preserved) → Gate D → ChatGPT onboarding evidence.
- NFRs (SLOs, security) → Gate D → SLOs section and security controls.

## Deployment & CI/CD (MVP)

- Environments: local (venv), compose (staging/prod style). Single image artifact.
- Release: update image and compose; rollback via previous image tag.
- CI: Lint + minimal smoke (build image, run `python -m pyflakes` if configured). Full CI deferred.

## Status

Ready for Implementation

Sign‑Off

- Deciders: Architect, PM (Security consulted for auth/networking)
- Date: 2025-09-15

---

## Elicitation Plan (Pre‑Dev Questions)

- Identity & OAuth:
  - KC realm URL and client config? Token TTL, clock skew, and refresh policy?
  - Required scopes (if any) for tools; are fine‑grained scopes needed?
  - Audience policy: single `MCP_SERVER_URL` or dual (`MCP_ALT_AUDIENCE`) for compatibility?
- Networking & TLS:
  - Final hostnames and certificates; staging vs prod endpoints? HSTS desired?
  - Any corporate proxy or split‑DNS constraints?
- Transport & Performance:
  - Minimum streaming cadence and max payload per chunk? Client idle timeout?
  - Concurrency expectations (simultaneous chats) and CPU/RAM budget per container?
- Logs & Observability:
  - Retention days; log redaction requirements beyond Authorization header?
  - Centralized logging target (e.g., Loki/ELK) and required fields?
- Operations & SLOs:
  - Target uptime (MVP) and maintenance windows? Restart policy?
  - Backup/restore needs (config only vs data later)?
- Compliance & Security:
  - Any audit requirements (who accessed what, when)? Time source policy (NTP)?
  - Threats of concern (DoS, token replay, trace leakage) and acceptance posture?

## Architecture Decisions (ADR Summary)

- ADR‑001: Prefer Streamable‑HTTP; keep SSE as fallback.
  - Rationale: Lower latency, fewer redirects; aligns with client expectations.
- ADR‑002: In‑app JWT verification; Traefik handles TLS/routing only.
  - Rationale: Simpler deployment, fine‑grained control; ForwardAuth deferred.
- ADR‑003: Advertise PRM at `/.well-known/oauth-protected-resource` on MCP host.
  - Rationale: RFC 9728 compatibility; drives 401 hint and client bootstrapping.
- ADR‑004: RFC 8414 path‑insert shim on auth host.
  - Rationale: Client discovery parity without realm URL knowledge.
- ADR‑005: Bind `127.0.0.1` local; `0.0.0.0` in containers.
  - Rationale: Container networking; safety in local runs.

## Sequence Flows (Text)

- Unauthenticated request → PRM hint:
  1. Client → `GET /mcp` → Server returns `401` with `WWW-Authenticate: Bearer resource_metadata="<PRM>"`.
- OAuth login via PRM:
  1. Client reads PRM; 2) Client discovers AS metadata; 3) Auth Code + PKCE; 4) Token; 5) Calls MCP with Bearer.
- Authenticated Streamable‑HTTP tool call:
  1. Client POSTs to `/mcp` with Bearer.
  2. Server verifies JWT (iss/aud/exp/nbf).
  3. Session established.
  4. Tool executes.
  5. Streamed chunks returned.
  6. Audit log written.
- SSE fallback:
  1. Client connects `/sse`; 2) Messages via `/messages/`; 3) Same auth checks enforced.

### ASCII Sequence Diagram (MVP)

```text
Client (ChatGPT)          Traefik                   MCP Server                     Keycloak (Auth)
      |                     |                            |                                  |
      | 1) GET /mcp        |                            |                                  |
      |------------------->|  route to MCP              |                                  |
      |                     |-------------------------->|  401 + WWW-Authenticate (PRM)    |
      |<-------------------|                            |                                  |
      | 2) GET /.well-known/oauth-protected-resource    |                                  |
      |------------------->|--------------------------->|  PRM JSON                        |
      |<-------------------|<---------------------------|                                  |
      | 3) GET /.well-known/openid-configuration        |                                  |
      |------------------->|----------------------------|--------------------------------->|  OIDC JSON
      |<-------------------|<---------------------------|<---------------------------------|  (issuer,jwks_uri)
      | 4) Auth Code + PKCE (browser flow)              |                                  |
      |----------------------------------------------- SSO -------------------------------->|
      |<---------------------------------------------- Tokens ------------------------------|
      | 5) POST /mcp (Bearer)  |                        |                                  |
      |------------------------>|----------------------->|  Verify JWT (iss/aud/jwks)       |
      |                        |                        |---> Execute tool, stream chunks  |
      |<------------------------|<-----------------------|  Streamable-HTTP response        |
```

### Traefik Rate Limit Middleware (Example)

Add this to your service definition to protect the MCP router:

```yaml
services:
  mcp:
    # ... other service config
    labels:
      - traefik.enable=true
      - traefik.http.routers.mcp.rule=Host(`mcp.localhost`)
      - traefik.http.routers.mcp.entrypoints=websecure
      - traefik.http.routers.mcp.tls=true
      - traefik.http.routers.mcp.tls.certresolver=dev
      - traefik.http.services.mcp.loadbalancer.server.port=8000
      # Rate limit: average 50 rps with burst 25 over 1s per source IP
      - traefik.http.middlewares.mcp-rl.ratelimit.average=50
      - traefik.http.middlewares.mcp-rl.ratelimit.burst=25
      - traefik.http.middlewares.mcp-rl.ratelimit.period=1s
      - traefik.http.routers.mcp.middlewares=mcp-rl
```

## Threat Model (STRIDE) & Controls

- Spoofing: JWT verification (JWKS, iss/aud), TLS, header‑only Bearer.
- Tampering: TLS 1.2+; reject tokens with invalid signature or claims.
- Repudiation: JSON audit logs (request_id, sub, client_id, outcome, reason).
- Information Disclosure: Redact Authorization; avoid logging bodies by default; CORS deny by default.
- DoS: Configure server timeouts, max body size, and connection limits at Traefik; document rate‑limit plan.
- Elevation of Privilege: Optional scopes; least‑privilege tool set; no token in URL.

## Performance & SLOs (MVP Targets)

- Availability: 99.5% monthly.
- TTFB (stream start): < 2s p95 via Traefik.
- Stream cadence: ≥ 10 chunks for representative long tools; keep‑alive every ≤ 30s.
- Error budget: 0.5% server 5xx.
- Capacity: Single container handles ≥ 50 concurrent sessions on 1 vCPU / 512 MB RAM.
- Timeouts: Client idle 90s; request timeout 120s; JWKS cache TTL 60m.

## Ops Runbook (MVP)

- Health: `GET /healthz` (200 `{ok:true}`).
- Logs: JSON lines with `request_id`, `transport`, `latency_ms`, `client_id?`.
- JWKS: Cache and refresh on key rotation; restart not required.
- TLS: Managed by Traefik; ensure SANs cover hosts; renewals via ACME.
- Deploy: `docker compose up -d`; rollbacks by image pin.
- Incident: Capture request_id and timeframe; verify JWKS and Traefik health; tail logs by service.

## Definition of Ready (for Dev)

- Hostnames, TLS, and `.env` values confirmed and versioned.
- KC realm and client exist; redirect URIs registered; token TTLs chosen.
- Audience policy decided; fallback audience (if any) documented.
- SLO targets and timeouts accepted.
- Logging fields agreed; retention and redaction requirements documented.

## Outstanding Risks & Open Questions

- Streamable‑HTTP availability across client variants; fallback performance.
- Audience mismatch in some clients; whether to keep fallback beyond MVP.
- Rate limiting policy (Traefik vs app) and thresholds.
- Long‑running tools and chunk sizing; backpressure behavior.

## Architecture Sign‑Off Checklist

- Requirements mapped to gates (A–D) with evidence plan.
- ADRs recorded and accepted by stakeholders.
- Threat model reviewed; mitigations accepted.
- SLOs approved; ops runbook acknowledged.
- Definition of Ready met; dev can proceed.
