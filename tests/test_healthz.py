from __future__ import annotations

from starlette.testclient import TestClient

from tests._utils import build_test_app


def test_healthz_returns_json_ok():
    app = build_test_app(enable_auth=False)
    with TestClient(app) as client:
        r = client.get("/healthz")
        assert r.status_code == 200
        # Enforce exact content type contract (no charset suffix)
        assert r.headers.get("content-type", "").split(";")[0] == "application/json"
        assert r.json() == {"ok": True}
