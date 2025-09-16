# Technical Debt and Known Issues (Current)
1. No OAuth 2.1 integration: missing PRM route and JWT validation.
2. SSE‑only; Streamable‑HTTP not yet wired (required/preferred per PRD).
3. Binds to `127.0.0.1` for local development; when containerized behind Traefik, the app must bind `0.0.0.0` so Traefik can reach it over the bridge network.
4. No healthcheck endpoint; no restart policy; limited operational notes.
5. No log redaction policy; risk of leaking sensitive headers if added later.

## Workarounds and Gotchas
- Container networking: Inside containers, binding to 127.0.0.1 isolates the process from other containers. Bind `0.0.0.0` when running under Traefik; keep `127.0.0.1` only for local, non-container runs.
- Tool schemas are embedded; any auth layer must not alter tool I/O contracts.
