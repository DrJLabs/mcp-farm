# Data Models and APIs

## Pydantic Models (tool schemas)
- `SearchResult { id, title, text }`
- `SearchResultPage { results: list[SearchResult] }`
- `FetchResult { id, title, text, url?, metadata? }`

## MCP Transport Endpoints (Current)
- SSE transport exposed by FastMCP runner on `http://127.0.0.1:8000` (per README).
- No Streamable‑HTTP endpoint configured yet.
- No PRM route; unauthenticated requests do not advertise PRM metadata.
