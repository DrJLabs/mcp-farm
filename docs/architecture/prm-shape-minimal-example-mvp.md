# PRM Shape — Minimal Example (MVP)

The PRD requires a PRM endpoint at `/.well-known/oauth-protected-resource`. The minimal shape we will expose for MVP is:

```json
{
  "resource": "https://mcp.localhost",
  "authorization_servers": [
    "https://auth.localhost/realms/mcp"
  ]
}
```

Notes
- The exact metadata fields are validated via our acceptance script; the above is a minimal, practical payload for clients to discover the AS and correlate the resource.
- Return `application/json; charset=utf-8` and cache for a short TTL (e.g., 60s) to allow config changes during bring‑up.
