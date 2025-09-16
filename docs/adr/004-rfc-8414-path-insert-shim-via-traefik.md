# RFC 8414 Path‑Insert Shim via Traefik

- Status: Accepted
- Deciders: Architect, PM
- Date: 2025-09-15
- ID: 004

## Context and Problem Statement
Keycloak exposes OIDC/OAuth discovery under `/realms/<realm>/.well-known/...`. Some clients probe `/.well-known/...` at the host root. We need compatibility without changing the realm structure.

## Decision Drivers
- Client compatibility with root `/.well-known` discovery
- Avoid Keycloak reconfiguration or custom images
- Keep behavior explicit and auditable at the proxy layer

## Considered Options
- Traefik `ReplacePathRegex` to map `/.well-known/*` → `/realms/mcp/.well-known/*`
- Document-only: require clients to call the realm-first paths
- Reverse proxy under a separate vhost/path managed by Keycloak

## Decision Outcome
- Chosen: Traefik rewrite on `auth.localhost` with explicit `service=kc` and higher router priority to map root `/.well-known` to realm-first metadata.

## Positive Consequences
- Seamless discovery across clients; no Keycloak customization

## Negative Consequences
- Potential confusion if multiple realms are later required; must revisit mapping

## Pros and Cons of the Options
- Traefik rewrite
  - Pros: Minimal; infrastructure-only; reversible
  - Cons: One-off mapping per realm/host
- Document-only
  - Pros: Zero config
  - Cons: Fragile; breaks clients that assume root well-known

## Links and References
- Architecture: ../brownfield-architecture.md (Compose labels)
- Validation: ../validation.md (2b)
