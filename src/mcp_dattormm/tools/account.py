"""Account-related tools for Datto RMM."""

import json

from mcp.server.fastmcp import FastMCP

from ..client import DattoRMMClient, get_client


def register_account_tools(mcp: FastMCP, client: DattoRMMClient | None = None) -> None:
    """Register account-related tools with the MCP server."""
    client = client or get_client()

    @mcp.tool()
    async def dattormm_account_get() -> str:
        """Get account details.

        Returns:
            JSON with account information including name, ID, and settings.
        """
        result = await client.get("/v2/account")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_account_sites(
        site_name: str | None = None,
        page: int = 1,
        max_results: int = 250
    ) -> str:
        """List all sites in the account.

        Args:
            site_name: Filter by site name (partial match)
            page: Page number (1-indexed)
            max_results: Maximum results per page (max 250)

        Returns:
            JSON array of sites with uid, name, and device counts.
        """
        params = {"page": page, "max": min(max_results, 250)}
        if site_name:
            params["siteName"] = site_name
        result = await client.get("/v2/account/sites", params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_account_devices(
        hostname: str | None = None,
        device_type: str | None = None,
        operating_system: str | None = None,
        site_name: str | None = None,
        filter_id: str | None = None,
        page: int = 1,
        max_results: int = 250
    ) -> str:
        """List all devices in the account with optional filters.

        Args:
            hostname: Filter by hostname (partial match)
            device_type: Filter by device type (e.g., 'desktop', 'laptop', 'server')
            operating_system: Filter by OS (partial match)
            site_name: Filter by site name (partial match)
            filter_id: Filter by saved filter ID
            page: Page number (1-indexed)
            max_results: Maximum results per page (max 250)

        Returns:
            JSON array of devices with uid, hostname, site, OS, and status.
        """
        params = {"page": page, "max": min(max_results, 250)}
        if hostname:
            params["hostname"] = hostname
        if device_type:
            params["deviceType"] = device_type
        if operating_system:
            params["operatingSystem"] = operating_system
        if site_name:
            params["siteName"] = site_name
        if filter_id:
            params["filterId"] = filter_id
        result = await client.get("/v2/account/devices", params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_account_users(
        page: int = 1,
        max_results: int = 250
    ) -> str:
        """List all users in the account.

        Args:
            page: Page number (1-indexed)
            max_results: Maximum results per page (max 250)

        Returns:
            JSON array of users with email, name, role, and permissions.
        """
        params = {"page": page, "max": min(max_results, 250)}
        result = await client.get("/v2/account/users", params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_account_components(
        page: int = 1,
        max_results: int = 250
    ) -> str:
        """List available components (scripts/monitors) in the account.

        Args:
            page: Page number (1-indexed)
            max_results: Maximum results per page (max 250)

        Returns:
            JSON array of components with uid, name, type, and category.
        """
        params = {"page": page, "max": min(max_results, 250)}
        result = await client.get("/v2/account/components", params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_account_alerts_open(
        page: int = 1,
        max_results: int = 250
    ) -> str:
        """List all open alerts across the account.

        Args:
            page: Page number (1-indexed)
            max_results: Maximum results per page (max 250)

        Returns:
            JSON array of open alerts with uid, device, priority, and timestamp.
        """
        params = {"page": page, "max": min(max_results, 250)}
        result = await client.get("/v2/account/alerts/open", params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_account_alerts_resolved(
        page: int = 1,
        max_results: int = 250
    ) -> str:
        """List all resolved alerts across the account.

        Args:
            page: Page number (1-indexed)
            max_results: Maximum results per page (max 250)

        Returns:
            JSON array of resolved alerts with uid, device, resolution details.
        """
        params = {"page": page, "max": min(max_results, 250)}
        result = await client.get("/v2/account/alerts/resolved", params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_account_variables() -> str:
        """List all account-level variables.

        Returns:
            JSON array of variables with id, name, and value.
        """
        result = await client.get("/v2/account/variables")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_account_variable_create(
        name: str,
        value: str,
        masked: bool = False
    ) -> str:
        """Create a new account-level variable.

        Args:
            name: Variable name
            value: Variable value
            masked: Whether to mask the value in UI (for secrets)

        Returns:
            JSON with created variable details.
        """
        data = {
            "name": name,
            "value": value,
            "masked": masked
        }
        result = await client.put("/v2/account/variable", json=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_account_variable_update(
        variable_id: str,
        name: str | None = None,
        value: str | None = None,
        masked: bool | None = None
    ) -> str:
        """Update an existing account-level variable.

        Args:
            variable_id: The variable ID to update
            name: New variable name (optional)
            value: New variable value (optional)
            masked: Whether to mask the value (optional)

        Returns:
            JSON with updated variable details.
        """
        data = {}
        if name is not None:
            data["name"] = name
        if value is not None:
            data["value"] = value
        if masked is not None:
            data["masked"] = masked
        result = await client.post(f"/v2/account/variable/{variable_id}", json=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_account_variable_delete(variable_id: str) -> str:
        """Delete an account-level variable.

        Args:
            variable_id: The variable ID to delete

        Returns:
            JSON confirmation of deletion.
        """
        result = await client.delete(f"/v2/account/variable/{variable_id}")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_account_dnet_mappings() -> str:
        """Get Datto Networking site mappings.

        Returns:
            JSON array of D-Net site mappings.
        """
        result = await client.get("/v2/account/dnet-site-mappings")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_user_reset_api_keys() -> str:
        """Reset the API keys for the current user.

        WARNING: This will invalidate current credentials and generate new ones.

        Returns:
            JSON with new API key and secret.
        """
        result = await client.post("/v2/user/resetApiKeys")
        return json.dumps(result, indent=2)
