# Integration Points and External Dependencies (Planned per PRD)

## External Services
| Service  | Purpose                | Integration Type | Notes                                 |
|--------- |------------------------|------------------|---------------------------------------|
| Keycloak | OAuth 2.1 IdP          | OIDC/JWKS        | Enforce `iss` and `aud` claims        |
| Traefik  | TLS + routing + rewrites| Reverse proxy    | Labels for host routing, RFC 8414 shim |
| ChatGPT  | MCP Developer‑mode     | Client           | Performs OAuth; streams tool calls     |

## Internal Integration Points
- PRM route under `/.well-known/oauth-protected-resource` must be public.
- Protected MCP endpoints must 401 with PRM hint when unauthenticated.
- JWT validation occurs in‑app for MVP (no ForwardAuth); Traefik provides TLS and routing.
