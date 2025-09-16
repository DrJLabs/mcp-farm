# Goals and Background Context

## Goals
- Establish a repeatable framework for creating MCP servers secured with Keycloak‑provided OAuth 2.1, compatible with ChatGPT’s MCP Developer Mode connectors.
- Deliver a working OAuth-secured sample MCP server at `sample-deep-research-mcp` that remains fully functional when connected to ChatGPT.
- Keep scope minimal: prioritize OAuth compatibility and stability over additional features.

## Status & KPIs (MVP)
- Target readiness: Architecture “Ready for Implementation” by 2025-09-20.
- Bootstrap time: ≤ 30 minutes to bring up a new OAuth‑enabled MCP from the sample.
- Streaming TTFB: < 2s p95 through Traefik (see architecture SLOs).
- Error budget: ≤ 0.5% server 5xx during validation.

## Background Context

Problem Statement: Create a repeatable OAuth 2.1 framework for MCP servers behind Traefik/Keycloak so ChatGPT Developer‑mode can authenticate and reliably stream tool calls; MVP is the included sample server working end‑to‑end with OAuth.

This project aims to standardize how multiple MCP servers authenticate via OAuth (Keycloak) while remaining fully compatible with ChatGPT’s MCP Developer Mode connectors, including deep-research style connectors that require no tool-type limits and write capabilities. The immediate objective is to secure the included sample server and establish a pattern that can be reused for additional MCP servers with minimal effort. Primary user is the project maintainer (single-user scenario) running on Linux and ultimately deploying via Docker.

## Change Log
| Date       | Version | Description                     | Author |
|------------|---------|---------------------------------|--------|
| 2025-09-14 | 0.1     | Initial scaffold created        | PM     |
| 2025-09-15 | 0.2     | Populated goals/background; added constraints and metrics | PM |
| 2025-09-15 | 0.3     | Preferred Streamable‑HTTP; added Traefik ingress section; replaced FR/NFR; expanded risks | PM |
| 2025-09-15 | 0.4     | Added Epic List, sequenced stories, and acceptance gates | PM |
| 2025-09-15 | 0.5     | MVP clarifies in‑app JWT (no ForwardAuth); stronger Streamable‑HTTP acceptance; Traefik noted as router/TLS only | PM |
| 2025-09-15 | 0.6     | Added Problem Statement, Out‑of‑Scope, and Performance & Reliability notes | PM |
| 2025-09-15 | 0.7     | Noted local `fastmcp/` reference repo; clarified container bind (0.0.0.0) vs local (127.0.0.1) | PM |
| 2025-09-15 | 0.8     | Added explicit Out‑of‑Scope, Status & KPIs, and references to architecture SLOs/evidence map | PM |
