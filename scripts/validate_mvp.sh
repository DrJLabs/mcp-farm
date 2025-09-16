#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${MCP_SERVER_URL:-"https://mcp.localhost"}

echo "# PRM"
curl -sS "$BASE_URL/.well-known/oauth-protected-resource" | jq || true

echo
echo "# OIDC (realm-first)"
curl -sS https://auth.localhost/realms/mcp/.well-known/openid-configuration | jq '.issuer,.jwks_uri'

echo
echo "# Shimmed well-known (root)"
curl -sS https://auth.localhost/.well-known/openid-configuration | jq '.issuer,.jwks_uri'
curl -sS https://auth.localhost/.well-known/oauth-authorization-server | jq '.issuer,.jwks_uri'

echo
echo "# 401 + PRM hint"
curl -isk "$BASE_URL/mcp" | sed -n '1,20p'

echo
echo "# Health"
curl -sS "$BASE_URL/healthz" | jq

echo
echo "# Streamable-HTTP smoke (requires BEARER_TOKEN env when auth enabled)"
python scripts/stream_smoke.py || true

