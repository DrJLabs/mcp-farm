# Requirements

## Functional (FR)
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

## Non-Functional (NFR)
- NFR1: Linux + Docker deployment; configuration is label/env‑driven only.
- NFR2: OAuth 2.1 Authorization Code with PKCE (S256); Authorization Server exposes RFC 8414 metadata.
- NFR3: No realm structural changes; updating client redirect URIs is permitted.
- NFR4: Secrets never committed; provide `.env.example`; logs must redact tokens in both app and proxy. Prohibit tokens in URLs; sanitize request/response logs.
- NFR5: Traefik‑only routing changes; no static file mounts; include tested label blocks.
- NFR6: Bootstrap a new OAuth‑enabled MCP from the sample in ≤ 30 minutes.
