# Ingress & Routing (Traefik)
- TLS via Traefik with valid certificates matching public hostnames.
- Route MCP host to container service/port using labels; no static Traefik files.
- Provide optional RFC 8414 path‑insert shims via `replacePathRegex` to map to Keycloak realm‑first endpoints.
- Verify Streamable‑HTTP long‑lived streaming works through Traefik; adjust timeouts/headers if needed. Keep SSE fallback.
- MVP: do not enable ForwardAuth; consider edge auth post‑MVP if multiple services need centralized policy. Ensure unauthenticated 401 originates from the MCP app with proper PRM hint.
