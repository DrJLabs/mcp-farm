# Security Controls

- Bearer in header only; reject tokens in query/path.
- Enforce `iss == KC_ISSUER` and `aud in {MCP_AUDIENCE, MCP_ALT_AUDIENCE?}` (if fallback configured, log usage once per minute max to avoid noise).
- Clock skew tolerance ≤ 60s; verify `exp` and `nbf`.
- Structured audit log for auth decisions: outcome, reason, subject (sub), truncated jti, client_id if present.
- CORS: default deny; allow only known MCP client origins if required (ChatGPT typically does not need CORS for SSE/HTTP from server‑side).

Rate Limiting & Request Limits
- Traefik rate limit (per source IP): average 50 rps, burst 25 (tune with evidence).
- Max body size: 2 MiB (Traefik middleware) for MCP endpoints.
