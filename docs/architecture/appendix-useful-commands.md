# Appendix – Useful Commands
```bash
# Local sample server
python sample_mcp.py

# Skeleton for validation (to be implemented during Epic 1)
curl -sS https://<mcp-host>/.well-known/oauth-protected-resource | jq
curl -i  https://<mcp-host>/mcp/... # expect 401 with WWW-Authenticate PRM hint
# Streamable‑HTTP smoke (expect 200 and streamed chunks)
```
