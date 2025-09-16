# Responsibility Matrix (MVP)
| Task | Owner | When |
|------|-------|------|
| Register/confirm DNS for MCP/Auth | Human (Ops) | Before S2 |
| Configure ACME email/cert resolver | Human (Ops) | Before S2 |
| Create Keycloak realm + client; register redirect URIs | Human (Ops/Sec) | Before S3–S4 |
| Implement PRM/401/JWT/transport per FRs | Dev Agent | S3–S5 |
| Configure Traefik labels, TLS, and discovery shim | Dev Agent | S2, S6 |
| Run validation scripts and capture evidence | Dev Agent | Gates A–C |
| Add ChatGPT connector and authenticate | Human (User) | S7 |
