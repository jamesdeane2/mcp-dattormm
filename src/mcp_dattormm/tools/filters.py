"""Filter-related tools for Datto RMM."""

import json

from mcp.server.fastmcp import FastMCP

from ..client import DattoRMMClient, get_client


def register_filter_tools(mcp: FastMCP, client: DattoRMMClient | None = None) -> None:
    """Register filter-related tools with the MCP server."""
    client = client or get_client()

    @mcp.tool()
    async def dattormm_filters_default() -> str:
        """List all default (built-in) device filters.

        Returns:
            JSON array of default filters with id, name, and criteria.
        """
        result = await client.get("/v2/filter/default-filters")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_filters_custom() -> str:
        """List all custom (user-created) device filters.

        Returns:
            JSON array of custom filters with id, name, criteria, and owner.
        """
        result = await client.get("/v2/filter/custom-filters")
        return json.dumps(result, indent=2)
