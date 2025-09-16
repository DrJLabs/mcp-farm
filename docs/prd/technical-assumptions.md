# Technical Assumptions
- Tech stack: FastMCP framework.
- AuthN/AuthZ: OAuth 2.1 Authorization Code with PKCE (S256) via Keycloak; Authorization Server exposes RFC 8414 metadata.
- Host OS: Linux for development; containerized deployment via Docker.
- Target client: ChatGPT MCP Developer Mode connectors (must interoperate cleanly).
- Transport: Streamable‑HTTP preferred; SSE supported as fallback for compatibility.
- JWT validation occurs in‑app for MVP (no Traefik ForwardAuth); Traefik provides TLS termination and routing only.
- Scope restraint: No additional feature work beyond securing and validating the sample server.
 - Local reference: `fastmcp/` repository is included for implementation details (transports, examples) to inform Epic 1.
