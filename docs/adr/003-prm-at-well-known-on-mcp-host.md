# PRM at `/.well-known/oauth-protected-resource` on MCP Host

- Status: Accepted
- Deciders: Architect, PM
- Date: 2025-09-15
- ID: 003

## Context and Problem Statement
Clients discover protected resource metadata (PRM) per RFC 9728 to learn which authorization servers issue valid tokens and how to authenticate. We need to define where PRM is served in this deployment.

## Decision Drivers
- Align with spec and client expectations for 401 hint resolution
- Keep discovery local to the resource server hostname
- Simple operator mental model and fewer cross‑host dependencies

## Considered Options
- Serve PRM at `/.well-known/oauth-protected-resource` on the MCP host
- Serve PRM on the auth host instead
- Omit PRM and rely on docs only

## Decision Outcome
- Chosen: Serve PRM on the MCP host. 401 responses reference this PRM URL in `WWW-Authenticate`.

## Positive Consequences
- Predictable for clients; straightforward PRM URL
- Clear separation: MCP host advertises its protected resource

## Negative Consequences
- One more public endpoint on MCP host (must be safe and cacheable)

## Pros and Cons of the Options
- PRM on MCP host
  - Pros: Spec‑aligned; enables 401 hint flow
  - Cons: Additional route to maintain
- PRM on Auth host
  - Pros: Centralizes metadata
  - Cons: Cross‑host indirection; breaks 401 hint expectations

## Links and References
- PRD: ../prd.md (FR1, FR2)
- Architecture: ../brownfield-architecture.md (PRM and 401 ownership)
