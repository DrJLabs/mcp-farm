# Risks & Mitigations

- Streamable‑HTTP availability: If not fully supported by current FastMCP version, Gate C allows SSE fallback; document measured latency so we can upgrade later.
- Audience mismatch from ChatGPT: permit `MCP_ALT_AUDIENCE` for compatibility, but gate with audit logging and a 90‑day deprecation note.
- Path‑insert discovery differences: include the Traefik ReplacePathRegex shim for clients that expect RFC 8414 at `/.well-known/...` without realm prefix.
