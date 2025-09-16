# Development and Deployment (Current Reality)

## Local Development Setup
1. `cd sample-deep-research-mcp`
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python sample_mcp.py` (starts SSE on `127.0.0.1:8000`)

## Build and Deployment Process
- No Dockerfile/compose in this folder at present; Traefik labels and containerization to be added during Epic 1.
