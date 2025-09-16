# ChatGPT Developer‑Mode Onboarding (MCP Connector)

This guide connects ChatGPT to the OAuth‑secured Sample MCP in this repo.

Date: 2025-09-15

## Prerequisites
- Stack running via `docker compose up -d` with valid `.env`.
- Hostnames resolve: `mcp.localhost`, `auth.localhost` → 127.0.0.1.
- PRM and OIDC discovery validated (see docs/validation.md).
- You have a plan that supports custom MCP connectors in ChatGPT (see Help Center for availability and roles).

References
- Connectors in ChatGPT (custom MCP support, how to connect; notes on required tools). [OpenAI Help]  
  Settings → Connectors → add app; custom connectors require tools `search` and `fetch`.  
- MCP Authorization and PRM (spec).  

## 1) Confirm server readiness
```bash
curl -sS https://mcp.localhost/.well-known/oauth-protected-resource | jq
curl -sS https://auth.localhost/realms/mcp/.well-known/openid-configuration | jq '.issuer,.jwks_uri'
curl -isk https://mcp.localhost/mcp | sed -n '1,15p'  # expect 401 + WWW-Authenticate with PRM URL
```

## 2) Add the connector in ChatGPT
1. Open ChatGPT (web or desktop) and sign in.
2. Go to Settings → Connectors.
3. Choose “Custom Connectors (MCP)” and click Connect.
4. Enter the MCP Server URL: `https://mcp.localhost` (ChatGPT will discover PRM and initiate OAuth).
5. Complete the Keycloak login and consent. PKCE is handled by ChatGPT.

Notes
- In Business/Enterprise/Edu workspaces, only owners/admins (or users granted permission) can add custom connectors. After enabling, members still authenticate individually on first use.
- If you see “This MCP server doesn’t implement our specification,” confirm the server exposes tools named `search` and `fetch` (this sample does).

## 3) Use the connector in chat
1. Open a new chat.
2. Click Tools → Use connectors → select your new connector (name may include host).
3. Try:
   - “Use the cupcake MCP to search for chocolate orders.”
   - Then call fetch by ID returned by search.

Expected behavior
- Chat shows connector enabled. Tool calls stream via Streamable‑HTTP (preferred). SSE is available as fallback.
- Authorization: first call redirects you to login if the token isn’t present; subsequent calls send Bearer tokens header‑only.

## 4) Troubleshooting
- 401 without OAuth prompt: confirm PRM endpoint and that `KC_ISSUER` matches your realm public URL.
- Audience mismatch: set `MCP_AUDIENCE` = `MCP_SERVER_URL`, and optionally `MCP_ALT_AUDIENCE` if required by the client; restart container.
- TLS/host mismatch: ensure Traefik certificate covers `mcp.localhost` and `.env` URLs match.
- “Spec not implemented”: confirm tools `search` and `fetch` exist and are visible.

## 5) Capture evidence for Gate D
- Screenshot the connector configuration and the first successful search + fetch in ChatGPT.
- Save server logs that show a validated JWT (`iss`, `aud`) and Streamable‑HTTP request path `/mcp`.

