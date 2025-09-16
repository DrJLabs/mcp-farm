# Bind Policy: 127.0.0.1 for Local; 0.0.0.0 in Containers

- Status: Accepted
- Deciders: Architect, PM
- Date: 2025-09-15
- ID: 005

## Context and Problem Statement
The sample MCP server must bind differently in local and containerized environments. Binding to `127.0.0.1` prevents container-to-container access; binding to `0.0.0.0` locally can be unsafe.

## Decision Drivers
- Safe local defaults; predictable container networking behind Traefik
- Minimize foot‑guns for new contributors

## Considered Options
- Always `0.0.0.0`
- Always `127.0.0.1`
- Environment‑driven policy (`BIND_HOST`), defaulting per environment

## Decision Outcome
- Chosen: Environment‑driven policy; default `127.0.0.1` locally and `0.0.0.0` in containers (compose/Dockerfile env). Document in `.env.example`.

## Positive Consequences
- Traefik can reach the container service; local runs stay private

## Negative Consequences
- Requires clear docs to avoid confusion when switching contexts

## Pros and Cons of the Options
- Always `0.0.0.0`
  - Pros: Works everywhere
  - Cons: Exposes local dev ports unnecessarily
- Always `127.0.0.1`
  - Pros: Safe locally
  - Cons: Breaks container networking

## Links and References
- PRD: ../prd.md (Networking notes)
- Architecture: ../brownfield-architecture.md (Networking assumptions)
