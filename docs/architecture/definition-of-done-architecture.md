# Definition of Done (Architecture)

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
