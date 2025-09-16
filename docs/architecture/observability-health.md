# Observability & Health

- Add `/healthz` returning 200 and a minimal body `{ "ok": true }` (unauthenticated) — used by Traefik/docker healthchecks.
- Logs: JSON lines; include `request_id`, `user_agent`, `remote_addr`, `transport` (sse|http-stream), and `latency_ms` for each request.
- Startup banner: dump effective transport(s) enabled and PRM URL.

Monitoring (MVP)
- Logs to stdout; container logs aggregated by platform.
- Optional: enable Traefik Prometheus metrics; no app metrics for MVP.
