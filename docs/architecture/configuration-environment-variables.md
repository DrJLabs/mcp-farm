# Configuration — Environment Variables

| Variable            | Purpose                                   | Example                          |
|---------------------|-------------------------------------------|----------------------------------|
| `MCP_SERVER_URL`    | Canonical external URL of MCP             | `https://mcp.localhost`          |
| `KC_ISSUER`         | Keycloak Issuer (realm public URL)        | `https://auth.localhost/realms/mcp` |
| `KC_JWKS_URI`       | Optional explicit JWKS URI                | `https://auth.localhost/realms/mcp/protocol/openid-connect/certs` |
| `MCP_AUDIENCE`      | Expected `aud` claim                       | `https://mcp.localhost`          |
| `MCP_ALT_AUDIENCE`  | Optional fallback audience                 | `` (empty)                       |
| `BIND_HOST`         | Bind interface inside container            | `0.0.0.0`                        |
| `BIND_PORT`         | Bind port                                  | `8000`                           |
| `ALLOWED_ORIGINS`   | CORS allowlist if needed                   | `https://chat.openai.com`        |
| `LOG_LEVEL`         | App log level                              | `info`                           |

Implementation Guidance
- Validate envs at startup and emit a single structured line summarizing effective values (excluding secrets).
- Do not log tokens or Authorization headers; ensure redaction in both success and error paths.
