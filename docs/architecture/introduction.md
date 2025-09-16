# Introduction
This document captures the current state of the mcp-farm repository with emphasis on the MVP defined in the PRD: securing the included sample MCP server with OAuth 2.1 behind Traefik/Keycloak and preferring Streamable‑HTTP transport (SSE as fallback). It is written to support AI agents implementing Epic 1.

## Document Scope
Focused on areas relevant to: Epic 1 “OAuth‑Secured Sample MCP” (PRM + 401 hint, OAuth 2.1 + PKCE, JWKS validation, Traefik routing/TLS, Streamable‑HTTP preferred, SSE fallback).

## Change Log
| Date       | Version | Description                                    | Author |
|------------|---------|------------------------------------------------|--------|
| 2025-09-15 | 1.1     | ADRs accepted; elicitation applied; Ready for Implementation | Arch   |
| 2025-09-15 | 1.0     | Initial brownfield analysis                    | Arch   |
