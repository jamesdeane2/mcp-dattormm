"""Activity log tools for Datto RMM."""

import json

from mcp.server.fastmcp import FastMCP

from ..client import DattoRMMClient, get_client


def register_activity_tools(mcp: FastMCP, client: DattoRMMClient | None = None) -> None:
    """Register activity log tools with the MCP server."""
    client = client or get_client()

    @mcp.tool()
    async def dattormm_activity_logs(
        from_date: str | None = None,
        until_date: str | None = None,
        entities: str | None = None,
        categories: str | None = None,
        actions: str | None = None,
        site_ids: str | None = None,
        user_ids: str | None = None,
        page: int = 1,
        max_results: int = 250
    ) -> str:
        """Get activity logs with optional filters.

        Args:
            from_date: Start date filter (ISO format: YYYY-MM-DDTHH:MM:SSZ)
            until_date: End date filter (ISO format: YYYY-MM-DDTHH:MM:SSZ)
            entities: Comma-separated entity types (e.g., 'device,site,user')
            categories: Comma-separated categories (e.g., 'security,system')
            actions: Comma-separated actions (e.g., 'create,update,delete')
            site_ids: Comma-separated site IDs to filter by
            user_ids: Comma-separated user IDs to filter by
            page: Page number (1-indexed)
            max_results: Maximum results per page (max 250)

        Returns:
            JSON array of activity log entries with timestamp, user, action, and details.
        """
        params = {"page": page, "max": min(max_results, 250)}
        if from_date:
            params["from"] = from_date
        if until_date:
            params["until"] = until_date
        if entities:
            params["entities"] = entities
        if categories:
            params["categories"] = categories
        if actions:
            params["actions"] = actions
        if site_ids:
            params["siteIds"] = site_ids
        if user_ids:
            params["userIds"] = user_ids

        result = await client.get("/v2/activity-logs", params=params)
        return json.dumps(result, indent=2)
