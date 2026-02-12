"""System status tools for Datto RMM."""

import json

from mcp.server.fastmcp import FastMCP

from ..client import DattoRMMClient, get_client


def register_system_tools(mcp: FastMCP, client: DattoRMMClient | None = None) -> None:
    """Register system status tools with the MCP server."""
    client = client or get_client()

    @mcp.tool()
    async def dattormm_system_status() -> str:
        """Get current system status.

        Returns:
            JSON with system health status and any ongoing issues.
        """
        result = await client.get("/v2/system/status")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_system_rate() -> str:
        """Get current API request rate information.

        Returns:
            JSON with current request count, limit (600/60s), and reset time.
        """
        result = await client.get("/v2/system/request_rate")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_system_pagination() -> str:
        """Get pagination settings for the API.

        Returns:
            JSON with default and maximum page sizes (max 250 per page).
        """
        result = await client.get("/v2/system/pagination")
        return json.dumps(result, indent=2)
