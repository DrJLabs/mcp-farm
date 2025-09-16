# Sequence Flows (Text)
- Unauthenticated request → PRM hint:
  1) Client → `GET /mcp` → Server returns `401` with `WWW-Authenticate: Bearer resource_metadata="<PRM>"`.
- OAuth login via PRM:
  1) Client reads PRM; 2) Client discovers AS metadata; 3) Auth Code + PKCE; 4) Token; 5) Calls MCP with Bearer.
- Authenticated Streamable‑HTTP tool call:
  1) Client POSTs to `/mcp` with Bearer; 2) Server verifies JWT (iss/aud/exp/nbf);
  3) Session established; 4) Tool executes; 5) Streamed chunks returned; 6) Audit log written.
- SSE fallback:
  1) Client connects `/sse`; 2) Messages via `/messages/`; 3) Same auth checks enforced.

## ASCII Sequence Diagram (MVP)
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

## Traefik Rate Limit Middleware (Example)
Add this to compose labels to protect the MCP router:
```yaml
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
