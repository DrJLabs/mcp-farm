# Reference Deployment — Docker + Traefik (Proposed)

This section provides a minimal, copy‑pasteable baseline for Epic 1. It is intentionally simple and label‑driven so it can be adapted per host.

## Dockerfile (sample‑deep‑research‑mcp)
```dockerfile
# ./sample-deep-research-mcp/Dockerfile
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Default dev bind; override via env in compose
ENV BIND_HOST=0.0.0.0 BIND_PORT=8000
CMD ["python", "sample_mcp.py"]
```

## Compose with Traefik Labels
```yaml
# ./compose.yaml (reference)
version: "3.9"
services:
  traefik:
    image: traefik:v3.1
    command:
      - --providers.docker=true
      - --entrypoints.web.address=:80
      - --entrypoints.websecure.address=:443
      - --certificatesresolvers.dev.acme.tlschallenge=true
      - --certificatesresolvers.dev.acme.email=you@example.com
      - --certificatesresolvers.dev.acme.storage=/letsencrypt/acme.json
    ports: ["80:80", "443:443"]
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - traefik_data:/letsencrypt

  mcp:
    build:
      context: ./sample-deep-research-mcp
    environment:
      MCP_SERVER_URL: https://mcp.localhost
      KC_ISSUER: https://auth.localhost/realms/mcp
      MCP_AUDIENCE: https://mcp.localhost
      MCP_ALT_AUDIENCE: ""  # optional fallback; leave empty by default
      BIND_HOST: 0.0.0.0
      BIND_PORT: 8000
      LOG_LEVEL: info
    expose: ["8000"]
    labels:
      - traefik.enable=true
      - traefik.http.routers.mcp.rule=Host(`mcp.localhost`)
      - traefik.http.routers.mcp.entrypoints=websecure
      - traefik.http.routers.mcp.tls=true
      - traefik.http.routers.mcp.tls.certresolver=dev
      - traefik.http.services.mcp.loadbalancer.server.port=8000
      # Optional: RFC 8414 path‑insert shim on the auth host
      # Map /.well-known/openid-configuration → /realms/mcp/.well-known/openid-configuration
      # Requires the Keycloak service to be attached to the same network and reachable as "keycloak".

  keycloak:
    image: quay.io/keycloak/keycloak:25.0
    command: ["start"]
    environment:
      KC_PROXY: edge
      KC_HOSTNAME: auth.localhost
      KC_HTTP_ENABLED: "true"
    expose: ["8080"]
    labels:
      - traefik.enable=true
      - traefik.http.routers.kc.rule=Host(`auth.localhost`)
      - traefik.http.routers.kc.entrypoints=websecure
      - traefik.http.routers.kc.tls=true
      - traefik.http.routers.kc.tls.certresolver=dev
      - traefik.http.services.kc.loadbalancer.server.port=8080
      # Optional RFC 8414 path‑insert shim (ReplacePathRegex)
      - traefik.http.routers.kc-discovery.rule=Host(`auth.localhost`) && PathPrefix(`/.well-known/`)
      - traefik.http.routers.kc-discovery.entrypoints=websecure
      - traefik.http.routers.kc-discovery.tls=true
      - traefik.http.routers.kc-discovery.middlewares=kc-discovery-rewrite
      - traefik.http.middlewares.kc-discovery-rewrite.replacepathregex.regex=^/\.well-known/(.*)
      - traefik.http.middlewares.kc-discovery-rewrite.replacepathregex.replacement=/realms/mcp/.well-known/$${1}

volumes:
  traefik_data: {}
```

Notes
- For production, replace `mcp.localhost` and `auth.localhost` with real FQDNs and use a DNS‑validated resolver. The above is suitable for local testing with hosts entries.
- The MCP container binds `0.0.0.0:8000` so Traefik can reach it. Local non‑container runs may keep `127.0.0.1`.
