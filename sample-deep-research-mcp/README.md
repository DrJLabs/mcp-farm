# Cupcake MCP for Deep Research

This is a minimal example of a Deep Research style MCP server for searching and fetching cupcake orders.

## Set up & run

Python setup:

```shell
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Run the server (Streamable‑HTTP preferred):

```shell
# Defaults: TRANSPORT=http, BIND_HOST=127.0.0.1, BIND_PORT=8000
python sample_mcp.py
```

Endpoints:

- Streamable‑HTTP: `http://127.0.0.1:8000/mcp`
- Health: `http://127.0.0.1:8000/healthz`

SSE fallback (optional):

```shell
TRANSPORT=sse python sample_mcp.py
```

With OAuth (Keycloak): set envs per `.env.example` in repo root:

- `MCP_SERVER_URL`, `KC_ISSUER`, optional `KC_JWKS_URI`
- `MCP_AUDIENCE` and optional `MCP_ALT_AUDIENCE`

When configured, PRM is served at `/.well-known/oauth-protected-resource`, MCP endpoints require Bearer tokens, and 401 responses include a PRM hint.

## Files

- `sample_mcp.py`: Main server code
- `records.json`: Cupcake order data (must be present in the same directory)
