# Deployment Parameters (To Be Confirmed)
- MCP Hostname (prod): <mcp.example.com>
- Auth Hostname (prod): <auth.example.com>
- ACME Contact Email: <ops@example.com>
- TLS: Traefik with certificate resolver (DNS/TLS challenge); SANs must match hostnames above
- DNS: A/AAAA records to Traefik ingress; internal networking unchanged
