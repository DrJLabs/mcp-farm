# Source Tree and Module Organization

```text
./
├─ docs/
│  ├─ prd.md
│  └─ brownfield-architecture.md (this file)
└─ sample-deep-research-mcp/
   ├─ sample_mcp.py          # FastMCP server with tools (SSE transport)
   ├─ requirements.txt       # python deps (fastmcp, mcp, pydantic, etc.)
   ├─ records.json           # sample data
   └─ README.md
```

## Key Modules and Their Purpose
- `sample_mcp.py`
  - `create_server()` builds a `FastMCP` named "Cupcake MCP" with two tools:
    - `search(query: str) -> SearchResultPage` (keyword search over `records.json`)
    - `fetch(id: str) -> FetchResult` (lookup by id)
  - Main guard runs the server: `create_server().run(transport="sse", host="127.0.0.1", port=8000)`
- Pydantic models: `SearchResult`, `SearchResultPage`, `FetchResult` model tool inputs/outputs.
