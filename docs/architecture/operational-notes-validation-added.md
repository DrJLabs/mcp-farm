# Operational Notes & Validation (Added)

## Networking Assumptions
- Local: bind `127.0.0.1:8000`.
- In container behind Traefik: bind `0.0.0.0:8000` so Traefik can connect via the bridge network.
- Validate from Traefik:
  - `docker exec -it traefik sh -lc "apk add --no-cache curl >/dev/null 2>&1 || true; curl -i http://mcp:8000/healthz"` → expect 200.

## Transport Capability Check
- Confirm Streamable‑HTTP support in FastMCP (see `fastmcp/` repo). If unavailable, satisfy Gate C with SSE for MVP and plan Streamable‑HTTP post‑MVP.

## PRM and 401 Ownership
- Ensure app emits 401 with PRM hint:
  - `curl -i https://<mcp-host>/mcp/messages/ | sed -n '1,15p'` → expect `WWW-Authenticate: Bearer resource_metadata="https://<mcp-host>/.well-known/oauth-protected-resource"`.

## Audience Policy
- Enforce `aud=MCP_SERVER_URL`. Optional fallback via `MCP_ALT_AUDIENCE`; log when fallback is used.

## Discovery Smoke Tests
```bash
curl -sS https://<oauth-host>/.well-known/oauth-authorization-server/realms/<realm> | jq '.token_endpoint,.authorization_endpoint,.jwks_uri'
curl -sS https://<oauth-host>/realms/<realm>/.well-known/openid-configuration | jq '.issuer,.jwks_uri'
```

## Streaming Acceptance
- First chunk < ~2s and ≥10 chunks total through Traefik for Streamable‑HTTP (or equivalent SSE cadence).
