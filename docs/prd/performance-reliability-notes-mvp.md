# Performance & Reliability Notes (MVP)
- Streaming: Streamable‑HTTP initial headers within ~2s; support long‑lived sessions (≥10 minutes) via Traefik timeouts/keep‑alive.
- SSE Fallback: If used, send keep‑alive events (e.g., every 15s) to prevent idle closure.
- Healthcheck: Expose `GET /healthz` (200) and container `HEALTHCHECK` probing that endpoint.
- Restart Policy: Container restart `unless-stopped` (or equivalent) with backoff.
- Observability: Include request ID correlation in logs; redact Authorization headers.
