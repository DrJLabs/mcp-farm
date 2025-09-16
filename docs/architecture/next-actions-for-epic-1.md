# Next Actions (for Epic 1)

1. S1: Add `.env.example` and `/healthz`; wire BIND_HOST logic (127.0.0.1 vs 0.0.0.0). [DONE]
2. S2: Introduce Dockerfile and compose; verify Traefik routing to health. [DONE]
3. S3: Implement PRM route and 401 PRM hint. [DONE]
4. S4: Add JWT validation (JWKS, iss/aud enforcement) with structured audit logs. [DONE]
5. S5: Enable Streamable‑HTTP (prefer) with SSE fallback; record streaming evidence. [DONE]
6. S6: RFC 8414 path‑insert shim via Traefik ReplacePathRegex on `auth.localhost` mapping `/.well-known/*` → `/realms/mcp/.well-known/*`; add validation steps. [DONE]
7. S7: ChatGPT Developer‑mode onboarding + validation scripts; confirm custom connector works end‑to‑end. [DONE]
