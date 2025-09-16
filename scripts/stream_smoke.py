#!/usr/bin/env python3
"""
Streamable-HTTP smoke test using FastMCP Client.

Requires:
  - fastmcp in the Python environment (installed via requirements)
  - MCP_SERVER_URL (base URL, e.g., https://mcp.localhost)
  - Optional: BEARER_TOKEN for Authorization header
"""

import asyncio
import os

from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport


async def main() -> None:
    base = os.environ.get("MCP_SERVER_URL", "http://127.0.0.1:8000")
    url = base.rstrip("/") + "/mcp"
    token = os.environ.get("BEARER_TOKEN")

    transport = StreamableHttpTransport(url, auth=(token or None))
    async with Client(transport=transport) as client:
        tools = await client.list_tools()
        print({"tools": [t.name for t in tools]})


if __name__ == "__main__":
    asyncio.run(main())
