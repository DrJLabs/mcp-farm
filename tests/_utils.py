from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

from fastmcp.server.http import create_streamable_http_app

REPO_ROOT = Path(__file__).resolve().parents[1]
_FASTMCP_SRC = REPO_ROOT / "fastmcp" / "src"
_SAMPLE_PATH = REPO_ROOT / "sample-deep-research-mcp" / "sample_mcp.py"


def load_sample_module():
    """Load the sample MCP server module with local fastmcp sources on sys.path."""
    if str(_FASTMCP_SRC) not in sys.path:
        sys.path.insert(0, str(_FASTMCP_SRC))

    spec = importlib.util.spec_from_file_location("sample_mcp", _SAMPLE_PATH)
    assert spec and spec.loader, "Unable to locate sample_mcp.py"
    module = importlib.util.module_from_spec(spec)
    sys.modules["sample_mcp"] = module
    spec.loader.exec_module(module)
    return module


def build_test_app(*, enable_auth: bool, stream_path: str = "/mcp"):
    """Instantiate the FastMCP HTTP app for testing.

    Args:
        enable_auth: When True, pass the server's auth provider to the HTTP app.
        stream_path: Path to mount the Streamable HTTP endpoint (default: /mcp).
    """
    sample = load_sample_module()
    server = sample.create_server()
    auth_provider = server.auth if enable_auth else None
    # create_streamable_http_app accepts `auth` (alias for auth provider) in fastmcp>=2.5.
    return create_streamable_http_app(
        server=server,
        streamable_http_path=stream_path,
        auth=auth_provider,
        json_response=False,
        stateless_http=True,
        debug=False,
    )


def create_server_instance() -> Any:
    """Convenience helper to get a configured FastMCP server instance."""
    sample = load_sample_module()
    return sample.create_server()
