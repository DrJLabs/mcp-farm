# mcp-farm Product Requirements Document (PRD)

> Status: Draft v0.8 — Added Out-of-Scope, Status & KPIs, and architecture references on 2025-09-15

## Goals and Background Context

### Goals
- Establish a repeatable framework for creating MCP servers secured with Keycloak‑provided OAuth 2.1, compatible with ChatGPT’s MCP Developer Mode connectors.
- Deliver a working OAuth-secured sample MCP server at `sample-deep-research-mcp` that remains fully functional when connected to ChatGPT.
- Keep scope minimal: prioritize OAuth compatibility and stability over additional features.

### Status & KPIs (MVP)
- Target readiness: Architecture “Ready for Implementation” by 2025-09-20.
- Bootstrap time: ≤ 30 minutes to bring up a new OAuth‑enabled MCP from the sample.
- Streaming TTFB: < 2s p95 through Traefik (see architecture SLOs).
- Error budget: ≤ 0.5% server 5xx during validation.

### Background Context

Problem Statement: Create a repeatable OAuth 2.1 framework for MCP servers behind Traefik/Keycloak so ChatGPT Developer‑mode can authenticate and reliably stream tool calls; MVP is the included sample server working end‑to‑end with OAuth.

This project aims to standardize how multiple MCP servers authenticate via OAuth (Keycloak) while remaining fully compatible with ChatGPT’s MCP Developer Mode connectors, including deep-research style connectors that require no tool-type limits and write capabilities. The immediate objective is to secure the included sample server and establish a pattern that can be reused for additional MCP servers with minimal effort. Primary user is the project maintainer (single-user scenario) running on Linux and ultimately deploying via Docker.

### Change Log
| Date       | Version | Description                     | Author |
|------------|---------|---------------------------------|--------|
| 2025-09-14 | 0.1     | Initial scaffold created        | PM     |
| 2025-09-15 | 0.2     | Populated goals/background; added constraints and metrics | PM |
| 2025-09-15 | 0.3     | Preferred Streamable‑HTTP; added Traefik ingress section; replaced FR/NFR; expanded risks | PM |
| 2025-09-15 | 0.4     | Added Epic List, sequenced stories, and acceptance gates | PM |
| 2025-09-15 | 0.5     | MVP clarifies in‑app JWT (no ForwardAuth); stronger Streamable‑HTTP acceptance; Traefik noted as router/TLS only | PM |
| 2025-09-15 | 0.6     | Added Problem Statement, Out‑of‑Scope, and Performance & Reliability notes | PM |
| 2025-09-15 | 0.7     | Noted local `fastmcp/` reference repo; clarified container bind (0.0.0.0) vs local (127.0.0.1) | PM |
| 2025-09-15 | 0.8     | Added explicit Out‑of‑Scope, Status & KPIs, and references to architecture SLOs/evidence map | PM |

## Requirements

### Functional (FR)
- FR1: Serve PRM at `/.well-known/oauth-protected-resource` advertising at least one Authorization Server (Keycloak) and the canonical MCP base URL. Include PRM per RFC 9728; `resource` equals `MCP_SERVER_URL`.
- FR2: Return 401 with `WWW-Authenticate: Bearer resource_metadata="<PRM URL>"` for unauthenticated protected endpoints.
- FR3: Validate bearer JWTs using Keycloak JWKS; enforce `iss` (realm public URL) and audience bound to the MCP base (accept configured fallback audience if needed for ChatGPT compatibility, with audit logging). Bearer tokens MUST be in the `Authorization` header only; never in query or path.
- FR4: Expose MCP over HTTPS via Traefik using Streamable‑HTTP as the preferred transport; keep SSE available as a fallback.
- FR5: Add Traefik labels to route the MCP host to the service/port (no static Traefik files). Enable TLS via Traefik.
- FR6: If clients request RFC 8414 path‑insert discovery, provide Traefik replace‑path labels to map path‑insert → Keycloak realm‑first metadata. No realm structural changes expected; client redirect URI registration may be required.
- FR7: Configure via env: `MCP_SERVER_URL`, `KC_ISSUER`, `MCP_AUDIENCE`, and any CORS/allowed origins required by the client.
- FR8: Provide a validation script/docs to verify PRM, RFC 8414 metadata, OIDC discovery, 401 PRM hint, and a Streamable‑HTTP round‑trip through Traefik (expect 200 and streaming chunks).
  - Acceptance signal: Observe either ≥10 streamed chunks or early‑flush streaming headers end‑to‑end through Traefik; record evidence (timestamped curl or logs).
- FR9: Preserve all existing sample server tool functionality when authenticated via ChatGPT Developer‑mode.

### Non-Functional (NFR)
- NFR1: Linux + Docker deployment; configuration is label/env‑driven only.
- NFR2: OAuth 2.1 Authorization Code with PKCE (S256); Authorization Server exposes RFC 8414 metadata.
- NFR3: No realm structural changes; updating client redirect URIs is permitted.
- NFR4: Secrets never committed; provide `.env.example`; logs must redact tokens in both app and proxy. Prohibit tokens in URLs; sanitize request/response logs.
- NFR5: Traefik‑only routing changes; no static file mounts; include tested label blocks.
- NFR6: Bootstrap a new OAuth‑enabled MCP from the sample in ≤ 30 minutes.

## Out of Scope (MVP)
- Multi‑tenant UI, user management UI, or admin console.
- Non‑Keycloak identity providers or non‑Traefik ingress.
- Traefik ForwardAuth/centralized auth proxy in MVP (in‑app JWT used).
- Persistent databases and data migrations; sample remains file‑backed.
- Advanced monitoring stack beyond Traefik metrics; app‑level metrics deferred.

## User Interface Design Goals
- TBD — captured after requirements pass 1.

## Technical Assumptions
- Tech stack: FastMCP framework.
- AuthN/AuthZ: OAuth 2.1 Authorization Code with PKCE (S256) via Keycloak; Authorization Server exposes RFC 8414 metadata.
- Host OS: Linux for development; containerized deployment via Docker.
- Target client: ChatGPT MCP Developer Mode connectors (must interoperate cleanly).
- Transport: Streamable‑HTTP preferred; SSE supported as fallback for compatibility.
- JWT validation occurs in‑app for MVP (no Traefik ForwardAuth); Traefik provides TLS termination and routing only.
- Scope restraint: No additional feature work beyond securing and validating the sample server.
 - Local reference: `fastmcp/` repository is included for implementation details (transports, examples) to inform Epic 1.

## Data Model Overview
- TBD.

## Integrations
- Keycloak (OAuth 2.1 provider).
- ChatGPT MCP Developer Mode (client/connectors).

## Ingress & Routing (Traefik)
- TLS via Traefik with valid certificates matching public hostnames.
- Route MCP host to container service/port using labels; no static Traefik files.
- Provide optional RFC 8414 path‑insert shims via `replacePathRegex` to map to Keycloak realm‑first endpoints.
- Verify Streamable‑HTTP long‑lived streaming works through Traefik; adjust timeouts/headers if needed. Keep SSE fallback.
- MVP: do not enable ForwardAuth; consider edge auth post‑MVP if multiple services need centralized policy. Ensure unauthenticated 401 originates from the MCP app with proper PRM hint.

## Performance & Reliability Notes (MVP)
- Streaming: Streamable‑HTTP initial headers within ~2s; support long‑lived sessions (≥10 minutes) via Traefik timeouts/keep‑alive.
- SSE Fallback: If used, send keep‑alive events (e.g., every 15s) to prevent idle closure.
- Healthcheck: Expose `GET /healthz` (200) and container `HEALTHCHECK` probing that endpoint.
- Restart Policy: Container restart `unless-stopped` (or equivalent) with backoff.
- Observability: Include request ID correlation in logs; redact Authorization headers.

## Release Strategy
- MVP: Secure `sample-deep-research-mcp` with OAuth and validate end‑to‑end functionality in ChatGPT.
- Post‑MVP: Template/boilerplate for rapidly adding new OAuth‑enabled MCP servers.

## Out of Scope (MVP)
- End‑user UI/portal and multi‑tenant user management.
- Non‑Keycloak identity providers or SAML/OAuth hybrids.
- Non‑Traefik ingress controllers or Kubernetes manifests.
- Automated Dynamic Client Registration flows (manual redirect‑URI registration only).
- Multi‑region HA, autoscaling, or disaster recovery planning.
- Advanced rate limiting, billing, or audit/compliance reporting beyond basic logs.

## Risks & Mitigations
- TLS/Certificates: Invalid SANs or mismatched hosts → Use Traefik TLS with correct hosts; ensure `MCP_SERVER_URL` matches.
- RFC 8414 Discovery Shape: Path‑insert vs realm‑first → Add Traefik replace‑path shims; confirm both discovery URLs resolve.
- Redirect URIs: Missing/incorrect in existing Keycloak client → Register exact HTTPS callbacks (may be the only Keycloak change).
- Audience Binding: Strict `aud` mismatch from ChatGPT → Allow configured fallback audience with audit logging; prefer MCP URL.
- Streaming Stability: Streamable‑HTTP/SSE timeouts through Traefik → Tune proxy timeouts/keep‑alive; verify headers.
- Transport Evolution: Future preference shifts → Document migration; keep SSE fallback initially.
- Token Leakage: Authorization header in logs → Enforce redaction in app and Traefik; never echo tokens.
- CORS Scope: Over‑permissive defaults → Restrict to necessary origins or disable if not required.
- Label Fragility: Regex/quoting errors break discovery → Ship tested label blocks and a smoke test.
- Env Drift: `MCP_SERVER_URL` / `KC_ISSUER` / `MCP_AUDIENCE` inconsistencies → Single `.env.example`; reference consistently.

## Success Metrics
- “Done” for MVP: Included sample MCP server works properly with OAuth in ChatGPT, preserving all existing functionality.
- Repeatability: New OAuth‑enabled MCP server can be bootstrapped in ≤30 minutes following the template.

## Epic List
- Epic 1: OAuth‑Secured Sample MCP
  - Deliver Streamable‑HTTP MCP behind Traefik with TLS.
  - Publish PRM and 401 `WWW-Authenticate` hint per RFC 9728.
  - Wire OAuth 2.1 + PKCE S256 to Keycloak (reuse existing realm/client; register redirect URIs if needed).
  - Validate JWT via JWKS; enforce `iss`/`aud`; header‑only bearer.
  - Add Traefik labels (incl. optional RFC 8414 path‑insert shims).
  - Provide validation docs/script and ensure ChatGPT Developer‑mode end‑to‑end works.

- Epic 2 (Post‑MVP, optional): Reusable Template & Bootstrap
  - Extract sample into a minimal template package.
  - Provide `.env.example`, compose, and tested Traefik label blocks.
  - “New server in ≤30 minutes” walkthrough + smoke test.

### Epic 1 Stories (Sequential)
- S1: Bootstrap env and healthcheck
  - Output: `.env.example`; health endpoint routed via Traefik HTTPS.
- S2: Traefik routing + TLS labels
  - Output: Host → container:port; smoke `200` on health.
- S3: PRM + 401 hint
  - Output: `/.well-known/oauth-protected-resource` valid; 401 includes `WWW-Authenticate` with PRM URL.
- S4: OAuth 2.1 validation
  - Output: JWKS verify; enforce `iss` and `aud`; header‑only bearer.
- S5: Streamable‑HTTP transport (preferred)
  - Output: Streamable‑HTTP round‑trip through Traefik (200 + streaming chunks); SSE fallback still works.
- S6: RFC 8414 path‑insert shims (conditional)
  - Output: Traefik replace‑path rules pass discovery smoke.
- S7: ChatGPT Developer‑mode onboarding + validation scripts
  - Output: Connector added; end‑to‑end tool calls succeed; scripts confirm PRM/AS/401/stream.

### Acceptance Gates (Map to FR/NFR)
- Gate A (after S3): FR1–FR2 satisfied.
- Gate B (after S4): FR3, NFR2 satisfied.
- Gate C (after S5): FR4, FR8 satisfied.
- Gate D (after S7): FR9 + Success Metrics “Done for MVP”.

References
- See docs/brownfield-architecture.md sections “FR/NFR → Gates & Evidence Map” and “Performance & SLOs (MVP Targets)” for detailed evidence and targets.

## Deployment Parameters (To Be Confirmed)
- MCP Hostname (prod): <mcp.example.com>
- Auth Hostname (prod): <auth.example.com>
- ACME Contact Email: <ops@example.com>
- TLS: Traefik with certificate resolver (DNS/TLS challenge); SANs must match hostnames above
- DNS: A/AAAA records to Traefik ingress; internal networking unchanged

## Responsibility Matrix (MVP)
| Task | Owner | When |
|------|-------|------|
| Register/confirm DNS for MCP/Auth | Human (Ops) | Before S2 |
| Configure ACME email/cert resolver | Human (Ops) | Before S2 |
| Create Keycloak realm + client; register redirect URIs | Human (Ops/Sec) | Before S3–S4 |
| Implement PRM/401/JWT/transport per FRs | Dev Agent | S3–S5 |
| Configure Traefik labels, TLS, and discovery shim | Dev Agent | S2, S6 |
| Run validation scripts and capture evidence | Dev Agent | Gates A–C |
| Add ChatGPT connector and authenticate | Human (User) | S7 |

## CI/CD Note (MVP)
- CI: Lint + build image + minimal smoke (health endpoint curl via ephemeral container).
- Artifacts: Docker image tagged per commit; compose-driven release.
- Rollback: Re-deploy previous image tag; revert compose labels if needed.

## Checklist Results Report
 - PM Checklist: Comprehensive mode run on 2025-09-15

Summary
- Problem Definition & Context: PASS (minor clarifications suggested)
- MVP Scope Definition: PASS (explicit out-of-scope recommended)
- UX Requirements: WAIVED (backend service; no end-user UI)
- Functional Requirements: PASS (testable FRs, dependencies, gates)
- Non-Functional Requirements: PASS with notes (security solid; perf/reliability minimal for MVP)

Details
- 1.1 Problem Statement: PASS — Goal and audience (single maintainer) clear; add a one-line explicit problem statement for clarity.
- 1.2 Goals & Success Metrics: PASS — “MVP done in ChatGPT” and “≤30 min bootstrap” measurable; consider adding a target date/baseline.
- 1.3 Research & Insights: WAIVED — internal tool for solo maintainer; no market research required.
- 2.1 Core Functionality: PASS — FR/NFR and stories map to goal; acceptance gates defined.
- 2.2 Scope Boundaries: CONCERN — Add explicit Out-of-Scope list (e.g., multi-tenant UI, non-Keycloak IdPs, non‑Traefik ingress).
- 2.3 MVP Validation: PASS — PRM/AS/401 checks + Streamable‑HTTP acceptance signal and ChatGPT onboarding.
- 3.x UX: WAIVED — no product UI; retain section as N/A.
- 4.1–4.3 Functional Quality: PASS — FRs are specific and MCP‑spec aligned; stories sequenced; add per‑story ACs if needed later.
- 5.1 Performance: TODO — note acceptable streaming latency/timeouts (e.g., initial headers <2s; keep‑alive configured).
- 5.2 Security & Compliance: PASS — OAuth 2.1 + PKCE, JWKS, header‑only bearer, log redaction.
- 5.3 Reliability & Resilience: TODO — document minimal expectations (e.g., restart policy, health endpoint routed via Traefik).
- 5.4 Technical Constraints: PASS — FastMCP, Keycloak, Traefik, Docker captured.

Action Items
- A1: Add Out-of-Scope list under Release Strategy or a new section. [Owner: PM]
- A2: Add one‑line explicit problem statement at top of Background. [Owner: PM]
- A3: Record minimal perf/reliability notes (timeouts, healthcheck, restart). [Owner: PM]

## Next Steps
- Draft UX Expert prompt after PRD first pass.
