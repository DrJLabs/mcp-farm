# Validation Guide (PRM, 401 Hint, OIDC, Streamable‑HTTP)

This guide validates the OAuth‑secured Sample MCP behind Traefik.

Prereqs

- DNS or `/etc/hosts` entries for `mcp.localhost` and `auth.localhost` → 127.0.0.1
- `docker compose up -d` with `compose.yaml` from repo root
- `.env` created from `.env.example`, issuer and URLs set

## 1) Protected Resource Metadata (PRM)

```bash
curl -sS https://mcp.localhost/.well-known/oauth-protected-resource | jq
```

Expect JSON with:

- `resource: "https://mcp.localhost"`
- `authorization_servers: ["https://auth.localhost/realms/mcp"]`

## 2) OIDC Discovery and JWKS (realm-first)

````bash
curl -sS https://auth.localhost/realms/mcp/.well-known/openid-configuration | \
  jq '.issuer,.jwks_uri,.authorization_endpoint,.token_endpoint'

## 2b) RFC 8414 Path-Insert Shims (via Traefik)

The proxy maps `/.well-known/*` to Keycloak’s realm-first metadata using ReplacePathRegex.

Test both endpoints at the host root; both should succeed and reflect the same realm:

```bash
# OIDC Discovery (shimmed)
curl -sS https://auth.localhost/.well-known/openid-configuration | jq '.issuer,.jwks_uri'

# OAuth Authorization Server Metadata (RFC 8414) (shimmed)
curl -sS https://auth.localhost/.well-known/oauth-authorization-server | jq '.issuer,.jwks_uri'
````

````

## 3) 401 with PRM hint (unauthenticated)

```bash
curl -isk https://mcp.localhost/mcp | sed -n '1,20p'
````

Expect:

- `HTTP/2 401`
- `WWW-Authenticate: Bearer resource_metadata="https://mcp.localhost/.well-known/oauth-protected-resource"`

## 4) Health Check

```bash
curl -sS https://mcp.localhost/healthz | jq
```

Expect: `{ "ok": true }`

## 5) Streamable‑HTTP Smoke (authenticated)

Acquire a bearer token from Keycloak for your client and export it:

```bash
export BEARER_TOKEN="<access_token>"
export MCP_SERVER_URL="https://mcp.localhost"
python scripts/stream_smoke.py
```

Expect a tools list, e.g. `{"tools":["search","fetch"]}`. This confirms an authenticated
Streamable‑HTTP round‑trip via Traefik.

Notes

- If Streamable‑HTTP is unavailable in the FastMCP build, set `TRANSPORT=sse` and use
  an SSE client. For MVP we accept SSE as fallback while preferring Streamable‑HTTP.

---

## Appendix: Admin Token Audience Verification (Keycloak)

Purpose: verify `iss` and `aud` on a real token without exposing secrets in logs.

Prereqs

- A confidential service client with service accounts enabled (e.g., `mcp-smoke`) and a mapper adding your MCP audience to the access token.
- Environment values in your private `.env` (not committed): `MCP_AUDIENCE`, `KC_ISSUER` (or `OIDC_ISSUER`).

Steps (generic; replace hostnames as needed)

1. Get an admin token for a service client (client credentials grant) and mint a service token for `mcp-smoke`.
2. Decode token payload locally to inspect claims (do not print the token itself):

```bash
ACCESS_TOKEN="<redacted>"
PAYLOAD=$(printf '%s' "$ACCESS_TOKEN" | cut -d. -f2 | tr '_-' '/+')
PAD=$(( (4 - ${#PAYLOAD}%4) % 4 )); PAYLOAD="$PAYLOAD"$(printf '=%.0s' $(seq 1 $PAD))
printf '%s' "$PAYLOAD" | base64 -d | jq '{iss,aud,azp,exp}'
```

Expect

- `iss` equals your realm issuer (e.g., `https://<auth-host>/auth/realms/<realm>`)
- `aud` contains your MCP audience and any secondary audiences (e.g., client IDs)

Notes

- Keep audience strict: set primary to your MCP identifier (URL or a dedicated resource client) and optionally accept a secondary audience for compatibility.
