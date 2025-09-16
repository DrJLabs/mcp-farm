# Performance & SLOs (MVP Targets)
- Availability: 99.5% monthly.
- TTFB (stream start): < 2s p95 via Traefik.
- Stream cadence: ≥ 10 chunks for representative long tools; keep‑alive every ≤ 30s.
- Error budget: 0.5% server 5xx.
- Capacity: Single container handles ≥ 50 concurrent sessions on 1 vCPU / 512 MB RAM.
- Timeouts: Client idle 90s; request timeout 120s; JWKS cache TTL 60m.
