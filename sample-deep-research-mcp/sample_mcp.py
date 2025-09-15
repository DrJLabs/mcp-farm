import os
import json
from pathlib import Path
from typing import Any

from fastmcp.server import FastMCP
# FastMCP auth import compatibility: fallback when module layout differs
try:  # fastmcp >=2.5 may expose auth at fastmcp.auth
    from fastmcp.server.auth import JWTVerifier, RemoteAuthProvider  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    try:
        from fastmcp.auth import JWTVerifier, RemoteAuthProvider  # type: ignore
    except Exception:  # keep app running without auth for S2
        JWTVerifier = None  # type: ignore
        RemoteAuthProvider = None  # type: ignore
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
        mcp.auth = RemoteAuthProvider(
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
    async def healthz(request: Request) -> Response:  # type: ignore[unused-variable]
        return JSONResponse({"ok": True})

    return mcp


if __name__ == "__main__":
    # Bind host/port + transport from env (default Streamable‑HTTP)
    host = _env("BIND_HOST", "127.0.0.1") or "127.0.0.1"
    port = int(_env("BIND_PORT", "8000") or 8000)
    transport = _env("TRANSPORT", "http") or "http"  # "http" (preferred) or "sse"

    create_server().run(transport=transport, host=host, port=port)
