# Deployment & CI/CD (MVP)
- Environments: local (venv), compose (staging/prod style). Single image artifact.
- Release: update image and compose; rollback via previous image tag.
- CI: Lint + minimal smoke (build image, run `python -m pyflakes` if configured). Full CI deferred.
