# Quick Reference – Key Files and Entry Points

## Critical Files
- Main entry (sample MCP): `sample-deep-research-mcp/sample_mcp.py`
- Data fixture: `sample-deep-research-mcp/records.json`
- Python deps: `sample-deep-research-mcp/requirements.txt`
- Readme: `sample-deep-research-mcp/README.md`
- PRD: `docs/prd.md`

- FastMCP reference repo: `fastmcp/` (source and docs for transports and server patterns)

## Enhancement Impact Areas (from PRD)
- Add PRM endpoint: `/.well-known/oauth-protected-resource`
- 401 responses include `WWW-Authenticate: Bearer resource_metadata="<PRM URL>"`
- JWT validation against Keycloak JWKS; enforce `iss` and `aud`
- Prefer Streamable‑HTTP transport; retain SSE fallback
- Traefik TLS + routing via labels; optional RFC 8414 path‑insert rewrites
- Env configuration: `MCP_SERVER_URL`, `KC_ISSUER`, `MCP_AUDIENCE`, CORS
