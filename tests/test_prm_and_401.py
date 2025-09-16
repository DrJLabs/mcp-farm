from __future__ import annotations

import os

import pytest
from starlette.testclient import TestClient

from tests._utils import build_test_app, create_server_instance


@pytest.fixture()
def auth_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("KC_ISSUER", "https://auth.localhost/realms/mcp")
    monkeypatch.setenv("MCP_SERVER_URL", "https://mcp.localhost")
    monkeypatch.setenv("MCP_AUDIENCE", "https://mcp.localhost")
    monkeypatch.setenv(
        "KC_JWKS_URI", "https://auth.localhost/realms/mcp/protocol/openid-connect/certs"
    )
    yield
    for key in ("KC_ISSUER", "MCP_SERVER_URL", "MCP_AUDIENCE", "KC_JWKS_URI"):
        monkeypatch.delenv(key, raising=False)


def test_prm_route_returns_expected_payload(auth_env):
    app = build_test_app(enable_auth=True)
    with TestClient(app) as client:
        response = client.get("/.well-known/oauth-protected-resource")
        assert response.status_code == 200
        assert response.headers.get("cache-control") == "public, max-age=60"
        assert response.headers.get("content-type", "").split(";")[0] == "application/json"
        assert response.json() == {
            "resource": "https://mcp.localhost",
            "authorization_servers": ["https://auth.localhost/realms/mcp"],
            "scopes_supported": [],
            "bearer_methods_supported": ["header"],
            "resource_name": "Cupcake MCP",
        }


def test_unauthenticated_mcp_returns_401_with_prm_hint(auth_env):
    app = build_test_app(enable_auth=True)
    with TestClient(app) as client:
        response = client.get("/mcp")
        assert response.status_code == 401
        header = response.headers.get("www-authenticate", "")
        assert "resource_metadata=\"https://mcp.localhost/.well-known/oauth-protected-resource\"" in header


def test_health_is_public_when_auth_enabled(auth_env):
    app = build_test_app(enable_auth=True)
    with TestClient(app) as client:
        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.json() == {"ok": True}


def test_server_without_issuer_keeps_auth_disabled(monkeypatch: pytest.MonkeyPatch):
    for key in ("KC_ISSUER", "MCP_SERVER_URL", "MCP_AUDIENCE", "KC_JWKS_URI"):
        monkeypatch.delenv(key, raising=False)
    server = create_server_instance()
    assert server.auth is None
