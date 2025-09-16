# In‑App JWT Verification vs Traefik ForwardAuth (MVP)

- Status: Accepted
- Deciders: Architect, PM (Security review required)
- Date: 2025-09-15
- ID: 002

## Context and Problem Statement
We need to decide where OAuth access token verification occurs. Traefik offers ForwardAuth middleware; FastMCP provides JWT verification and PRM/401 behaviors in‑app. PRD specifies Traefik for TLS+routing only for MVP.

## Decision Drivers
- Simplicity and debuggability for a single service MVP
- Full control over PRM and 401 hint behaviors at the app layer
- Avoid externalizing critical auth logic until multi‑service scale is needed

## Considered Options
- In‑app JWT verify (JWKS, `iss`, `aud`), PRM and 401 handled by server
- Traefik ForwardAuth to an auth service (external auth)
- Sidecar auth proxy per service

## Decision Outcome
- Chosen: In‑app JWT verification for MVP; Traefik remains TLS+router only. Revisit ForwardAuth/sidecar when multiple services are onboarded.

## Positive Consequences
- Fewer moving parts; easier local and container debugging
- Precise control over `WWW-Authenticate` PRM hints

## Negative Consequences
- App is responsible for auth patches/updates
- Some cross‑cutting policies (rate limits) remain at proxy layer, not unified auth

## Pros and Cons of the Options
- In‑app
  - Pros: Control; simplicity; PRM/401 handled coherently
  - Cons: Duplicates logic across services if we scale out
- ForwardAuth
  - Pros: Central policy; easier multi‑service enforcement
  - Cons: More infra; 401/PRM alignment requires coordination

## Links and References
- PRD: ../prd.md (notes on Traefik as TLS/routing)
- Architecture: ../brownfield-architecture.md (PRM/401 ownership, JWT sections)
