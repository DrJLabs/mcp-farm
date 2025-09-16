# FR/NFR → Gates & Evidence Map
- FR1/FR2 (PRM + 401 hint) → Gate A → sample_deep_research_mcp (RemoteAuthProvider) + docs/validation.md steps 1 & 3.
- FR3 (JWT validation iss/aud/JWKS) → Gate B → JWTVerifier config via env; curl OIDC + signed token test.
- FR4/FR8 (Streamable‑HTTP preferred + streaming acceptance) → Gate C → scripts/stream_smoke.py, validate_mvp.sh.
- FR5/FR6 (Traefik TLS + discovery shim) → Gate C → compose.yaml labels; validation 2b.
- FR7 (Env config) → Gate A → .env.example + config table.
- FR9 (Tool functionality preserved) → Gate D → ChatGPT onboarding evidence.
- NFRs (SLOs, security) → Gate D → SLOs section and security controls.
