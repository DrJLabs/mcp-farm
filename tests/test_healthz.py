from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
from starlette.testclient import TestClient


def load_sample_server_module():
    repo_root = Path(__file__).resolve().parents[1]

    # Ensure fastmcp package is importable from source
    fastmcp_src = repo_root / "fastmcp" / "src"
    sys.path.insert(0, str(fastmcp_src))

    # Dynamically load sample_deep_research_mcp/sample_mcp.py
    sample_path = repo_root / "sample-deep-research-mcp" / "sample_mcp.py"
    spec = importlib.util.spec_from_file_location("sample_mcp", sample_path)
    assert spec and spec.loader, "Unable to locate sample_mcp.py"
    module = importlib.util.module_from_spec(spec)
    sys.modules["sample_mcp"] = module
    spec.loader.exec_module(module)
    return module


def create_test_app():
    sample = load_sample_server_module()
    mcp = sample.create_server()

    # Build the Starlette app including custom routes (e.g., /healthz)
    from fastmcp.server.http import create_streamable_http_app

    app = create_streamable_http_app(
        server=mcp,
        streamable_http_path="/mcp",
        auth=None,
        json_response=False,
        stateless_http=True,
        debug=False,
    )
    return app


def test_healthz_returns_json_ok():
    app = create_test_app()
    with TestClient(app) as client:
        r = client.get("/healthz")
        assert r.status_code == 200
        # Enforce exact content type contract (no charset suffix)
        assert r.headers.get("content-type", "").split(";")[0] == "application/json"
        assert r.json() == {"ok": True}

