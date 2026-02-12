"""Alert-related tools for Datto RMM."""

import json

from mcp.server.fastmcp import FastMCP

from ..client import DattoRMMClient, get_client


def register_alert_tools(mcp: FastMCP, client: DattoRMMClient | None = None) -> None:
    """Register alert-related tools with the MCP server."""
    client = client or get_client()

    @mcp.tool()
    async def dattormm_alert_get(alert_uid: str) -> str:
        """Get alert details by UID.

        Args:
            alert_uid: The unique identifier of the alert

        Returns:
            JSON with alert details including type, priority, device, timestamp, and message.
        """
        result = await client.get(f"/v2/alert/{alert_uid}")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_alert_resolve(alert_uid: str) -> str:
        """Resolve an open alert.

        Args:
            alert_uid: The unique identifier of the alert to resolve

        Returns:
            JSON confirmation of alert resolution.
        """
        result = await client.post(f"/v2/alert/{alert_uid}/resolve")
        return json.dumps(result, indent=2)
