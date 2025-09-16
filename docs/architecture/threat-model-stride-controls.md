# Threat Model (STRIDE) & Controls
- Spoofing: JWT verification (JWKS, iss/aud), TLS, header‑only Bearer.
- Tampering: TLS 1.2+; reject tokens with invalid signature or claims.
- Repudiation: JSON audit logs (request_id, sub, client_id, outcome, reason).
- Information Disclosure: Redact Authorization; avoid logging bodies by default; CORS deny by default.
- DoS: Configure server timeouts, max body size, and connection limits at Traefik; document rate‑limit plan.
- Elevation of Privilege: Optional scopes; least‑privilege tool set; no token in URL.
