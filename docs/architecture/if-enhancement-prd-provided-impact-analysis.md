# If Enhancement PRD Provided – Impact Analysis

## Files That Will Need Modification
- `sample-deep-research-mcp/sample_mcp.py`: add PRM route, 401 PRM hint behavior, JWT validation (JWKS), switch/add Streamable‑HTTP transport; use `0.0.0.0` bind in container, `127.0.0.1` for local dev.

## New Files/Modules Likely Needed
- `docs/validation.md` (or similar) with curl examples for PRM/AS/401/stream tests.
- Containerization (Dockerfile/compose) and Traefik labels (host routing, optional RFC 8414 path‑insert rewrites).
- `.env.example` capturing `MCP_SERVER_URL`, `KC_ISSUER`, `MCP_AUDIENCE`.

## Integration Considerations
- Ensure PRM is reachable unauthenticated through Traefik.
- JWT validation must reject tokens with wrong `iss`/`aud`; accept one configured fallback audience if required by ChatGPT.
- Prefer Streamable‑HTTP; keep SSE fallback for compatibility/testing.
