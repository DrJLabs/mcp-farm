import os
import json
from pathlib import Path
from typing import Any

from fastmcp.server import FastMCP
# FastMCP auth import compatibility: fallback when module layout differs
try:  # fastmcp >=2.5 may expose auth at fastmcp.auth
    from fastmcp.server.auth import JWTVerifier, RemoteAuthProvider  # type: ignore
    from mcp.server.auth.routes import cors_middleware
    from starlette.routing import Route

    class CupcakeRemoteAuthProvider(RemoteAuthProvider):
        """Remote auth provider that keeps PRM metadata aligned with MCP_SERVER_URL."""

        def __init__(self, *args, base_url: Any | None = None, **kwargs):  # type: ignore[override]
            self._cupcake_resource_url = None
            if base_url is not None:
                base_url_str = str(base_url)
                self._cupcake_resource_url = base_url_str.rstrip("/") or base_url_str
            super().__init__(*args, base_url=base_url, **kwargs)

        def get_routes(self, mcp_path: str | None = None, mcp_endpoint: Any | None = None):  # type: ignore[override]
            routes = [
                route
                for route in super().get_routes(mcp_path, mcp_endpoint)
                if not (
                    isinstance(route, Route)
                    # Filter the base provider's PRM route so we control cache headers.
                    and getattr(route, "path", None) == "/.well-known/oauth-protected-resource"
                )
            ]
            resource_value = self._cupcake_resource_url
            if resource_value:
                auth_servers = [str(url) for url in self.authorization_servers]

                async def prm_endpoint(_request):
                    payload = {
                        "resource": resource_value,
                        "authorization_servers": auth_servers,
                        "scopes_supported": self.token_verifier.required_scopes,
                        "bearer_methods_supported": ["header"],
                    }
                    if self.resource_name:
                        payload["resource_name"] = self.resource_name
                    if self.resource_documentation:
                        payload["resource_documentation"] = str(self.resource_documentation)

                    response = JSONResponse(payload)
                    response.headers["Cache-Control"] = "public, max-age=60"
                    return response

                endpoint = prm_endpoint
                if cors_middleware:
                    endpoint = cors_middleware(prm_endpoint, ["GET", "OPTIONS"])

                routes.append(
                    Route(
                        "/.well-known/oauth-protected-resource",
                        endpoint=endpoint,
                        methods=["GET", "OPTIONS"],
                    )
                )

            return routes

except ModuleNotFoundError:  # pragma: no cover
    try:
        from fastmcp.auth import JWTVerifier, RemoteAuthProvider  # type: ignore
        cors_middleware = None  # type: ignore
        Route = None  # type: ignore
        CupcakeRemoteAuthProvider = RemoteAuthProvider  # type: ignore
    except ImportError:  # keep app running without auth for S2
        JWTVerifier = None  # type: ignore
        RemoteAuthProvider = None  # type: ignore
        cors_middleware = None  # type: ignore
        Route = None  # type: ignore
        CupcakeRemoteAuthProvider = None  # type: ignore
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

RECORDS = json.loads(Path(__file__).with_name("records.json").read_text())
LOOKUP = {r["id"]: r for r in RECORDS}

class SearchResult(BaseModel):
    id: str
    title: str
    text: str

class SearchResultPage(BaseModel):
    results: list[SearchResult]

class FetchResult(BaseModel):
    id: str
    title: str
    text: str
    url: str | None = None
    metadata: dict[str, str] | None = None

def _env(name: str, default: str | None = None) -> str | None:
    v = os.environ.get(name)
    return v if v is not None and v != "" else default


def create_server() -> FastMCP:
    """Build and configure the FastMCP server with optional OAuth protection.

    Env vars (see .env.example):
      - MCP_SERVER_URL (external URL for PRM + audience)
      - KC_ISSUER (Keycloak realm issuer URL)
      - KC_JWKS_URI (optional override; defaults to {KC_ISSUER}/protocol/openid-connect/certs)
      - MCP_AUDIENCE (expected aud; defaults to MCP_SERVER_URL)
      - MCP_ALT_AUDIENCE (optional fallback aud)
    """

    mcp = FastMCP(name="Cupcake MCP", instructions="Search cupcake orders")
    # Default to auth disabled; conditional below may replace with provider instance
    mcp.auth = None  # type: ignore[attr-defined]

    # Configure auth (PRM + 401 + JWT verify) when issuer is provided
    issuer = _env("KC_ISSUER")
    server_url = _env("MCP_SERVER_URL", "http://127.0.0.1:8000")
    audience_primary = _env("MCP_AUDIENCE", server_url)
    audience_alt = _env("MCP_ALT_AUDIENCE")

    if issuer and server_url and JWTVerifier and RemoteAuthProvider:
        jwks_uri = _env("KC_JWKS_URI", issuer.rstrip("/") + "/protocol/openid-connect/certs")

        audiences: list[str] | str
        if audience_alt:
            audiences = [audience_primary, audience_alt]
        else:
            audiences = audience_primary or ""

        jwt = JWTVerifier(
            jwks_uri=jwks_uri,
            issuer=issuer,
            audience=audiences,
            required_scopes=[],
            base_url=server_url,
        )
        provider_cls = (
            CupcakeRemoteAuthProvider if CupcakeRemoteAuthProvider is not None else RemoteAuthProvider
        )
        mcp.auth = provider_cls(
            token_verifier=jwt,
            authorization_servers=[issuer],
            base_url=server_url,
            resource_name="Cupcake MCP",
        )

    @mcp.tool()
    async def search(query: str) -> SearchResultPage:
        """
        Search for cupcake orders – keyword match.

        Returns a SearchResultPage containing a list of SearchResult items.
        """
        toks = query.lower().split()
        results: list[SearchResult] = []
        for r in RECORDS:
            hay = " ".join(
                [
                    r.get("title", ""),
                    r.get("text", ""),
                    " ".join(r.get("metadata", {}).values()),
                ]
            ).lower()
            if any(t in hay for t in toks):
                results.append(
                    SearchResult(id=r["id"], title=r.get("title", ""), text=r.get("text", ""))
                )

        # Return the Pydantic model (FastMCP will serialise it for us)
        return SearchResultPage(results=results)

    @mcp.tool()
    async def fetch(id: str) -> FetchResult:
        """
        Fetch a cupcake order by ID.

        Returns a FetchResult model.
        """
        if id not in LOOKUP:
            raise ValueError("unknown id")

        r = LOOKUP[id]
        return FetchResult(
            id=r["id"],
            title=r.get("title", ""),
            text=r.get("text", ""),
            url=r.get("url"),
            metadata=r.get("metadata"),
        )

    # Health endpoint (unauthenticated)
    @mcp.custom_route("/healthz", methods=["GET"])
    async def healthz(_request: Request) -> Response:
        return JSONResponse({"ok": True})

    return mcp


if __name__ == "__main__":
    # Bind host/port + transport from env (default Streamable‑HTTP)
    host = _env("BIND_HOST", "127.0.0.1") or "127.0.0.1"
    port = int(_env("BIND_PORT", "8000") or 8000)
    transport = _env("TRANSPORT", "http") or "http"  # "http" (preferred) or "sse"

    create_server().run(transport=transport, host=host, port=port)
