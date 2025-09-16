# Ops Runbook (MVP)
- Health: `GET /healthz` (200 `{ok:true}`).
- Logs: JSON lines with `request_id`, `transport`, `latency_ms`, `client_id?`.
- JWKS: Cache and refresh on key rotation; restart not required.
- TLS: Managed by Traefik; ensure SANs cover hosts; renewals via ACME.
- Deploy: `docker compose up -d`; rollbacks by image pin.
- Incident: Capture request_id and timeframe; verify JWKS and Traefik health; tail logs by service.
