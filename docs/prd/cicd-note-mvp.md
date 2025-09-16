# CI/CD Note (MVP)
- CI: Lint + build image + minimal smoke (health endpoint curl via ephemeral container).
- Artifacts: Docker image tagged per commit; compose-driven release.
- Rollback: Re-deploy previous image tag; revert compose labels if needed.
