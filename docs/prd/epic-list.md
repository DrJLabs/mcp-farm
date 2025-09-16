# Epic List
- Epic 1: OAuth‑Secured Sample MCP
  - Deliver Streamable‑HTTP MCP behind Traefik with TLS.
  - Publish PRM and 401 `WWW-Authenticate` hint per RFC 9728.
  - Wire OAuth 2.1 + PKCE S256 to Keycloak (reuse existing realm/client; register redirect URIs if needed).
  - Validate JWT via JWKS; enforce `iss`/`aud`; header‑only bearer.
  - Add Traefik labels (incl. optional RFC 8414 path‑insert shims).
  - Provide validation docs/script and ensure ChatGPT Developer‑mode end‑to‑end works.

- Epic 2 (Post‑MVP, optional): Reusable Template & Bootstrap
  - Extract sample into a minimal template package.
  - Provide `.env.example`, compose, and tested Traefik label blocks.
  - “New server in ≤30 minutes” walkthrough + smoke test.

## Epic 1 Stories (Sequential)
- S1: Bootstrap env and healthcheck — Done (2025‑09‑15)
  - Output: `.env.example`; health endpoint routed via Traefik HTTPS.
- S2: Traefik routing + TLS labels — Done (2025‑09‑16)
  - Output: Host → container:port; smoke `200` on health; labels‑only with external Traefik.
- S3: PRM + 401 hint
  - Output: `/.well-known/oauth-protected-resource` valid; 401 includes `WWW-Authenticate` with PRM URL.
- S4: OAuth 2.1 validation
  - Output: JWKS verify; enforce `iss` and `aud`; header‑only bearer.
- S5: Streamable‑HTTP transport (preferred)
  - Output: Streamable‑HTTP round‑trip through Traefik (200 + streaming chunks); SSE fallback still works.
- S6: RFC 8414 path‑insert shims (conditional)
  - Output: Traefik replace‑path rules pass discovery smoke.
- S7: ChatGPT Developer‑mode onboarding + validation scripts
  - Output: Connector added; end‑to‑end tool calls succeed; scripts confirm PRM/AS/401/stream.

## Acceptance Gates (Map to FR/NFR)
- Gate A (after S3): FR1–FR2 satisfied.
- Gate B (after S4): FR3, NFR2 satisfied.
- Gate C (after S5): FR4, FR8 satisfied.
- Gate D (after S7): FR9 + Success Metrics “Done for MVP”.

References
- See docs/brownfield-architecture.md sections “FR/NFR → Gates & Evidence Map” and “Performance & SLOs (MVP Targets)” for detailed evidence and targets.
