"""Site-related tools for Datto RMM."""

import json

from mcp.server.fastmcp import FastMCP

from ..client import DattoRMMClient, get_client


def register_site_tools(mcp: FastMCP, client: DattoRMMClient | None = None) -> None:
    """Register site-related tools with the MCP server."""
    client = client or get_client()

    @mcp.tool()
    async def dattormm_site_get(site_uid: str) -> str:
        """Get site details by UID.

        Args:
            site_uid: The unique identifier of the site

        Returns:
            JSON with site details including name, description, and device counts.
        """
        result = await client.get(f"/v2/site/{site_uid}")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_site_create(
        name: str,
        description: str | None = None,
        notes: str | None = None,
        on_demand: bool = False
    ) -> str:
        """Create a new site.

        Args:
            name: Site name
            description: Site description (optional)
            notes: Site notes (optional)
            on_demand: Whether this is an on-demand site

        Returns:
            JSON with created site details including new UID.
        """
        data = {"name": name, "onDemand": on_demand}
        if description:
            data["description"] = description
        if notes:
            data["notes"] = notes
        result = await client.put("/v2/site", json=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_site_update(
        site_uid: str,
        name: str | None = None,
        description: str | None = None,
        notes: str | None = None,
        on_demand: bool | None = None
    ) -> str:
        """Update an existing site.

        Args:
            site_uid: The site UID to update
            name: New site name (optional)
            description: New site description (optional)
            notes: New site notes (optional)
            on_demand: Whether this is an on-demand site (optional)

        Returns:
            JSON with updated site details.
        """
        data = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if notes is not None:
            data["notes"] = notes
        if on_demand is not None:
            data["onDemand"] = on_demand
        result = await client.post(f"/v2/site/{site_uid}", json=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_site_devices(
        site_uid: str,
        page: int = 1,
        max_results: int = 250
    ) -> str:
        """List all devices at a site.

        Args:
            site_uid: The site UID
            page: Page number (1-indexed)
            max_results: Maximum results per page (max 250)

        Returns:
            JSON array of devices at this site.
        """
        params = {"page": page, "max": min(max_results, 250)}
        result = await client.get(f"/v2/site/{site_uid}/devices", params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_site_devices_network(
        site_uid: str,
        page: int = 1,
        max_results: int = 250
    ) -> str:
        """List network interface information for all devices at a site.

        Args:
            site_uid: The site UID
            page: Page number (1-indexed)
            max_results: Maximum results per page (max 250)

        Returns:
            JSON array of network interfaces with IP, MAC, and adapter details.
        """
        params = {"page": page, "max": min(max_results, 250)}
        result = await client.get(f"/v2/site/{site_uid}/devices/network-interface", params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_site_alerts_open(
        site_uid: str,
        page: int = 1,
        max_results: int = 250
    ) -> str:
        """List open alerts for a site.

        Args:
            site_uid: The site UID
            page: Page number (1-indexed)
            max_results: Maximum results per page (max 250)

        Returns:
            JSON array of open alerts at this site.
        """
        params = {"page": page, "max": min(max_results, 250)}
        result = await client.get(f"/v2/site/{site_uid}/alerts/open", params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_site_alerts_resolved(
        site_uid: str,
        page: int = 1,
        max_results: int = 250
    ) -> str:
        """List resolved alerts for a site.

        Args:
            site_uid: The site UID
            page: Page number (1-indexed)
            max_results: Maximum results per page (max 250)

        Returns:
            JSON array of resolved alerts at this site.
        """
        params = {"page": page, "max": min(max_results, 250)}
        result = await client.get(f"/v2/site/{site_uid}/alerts/resolved", params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_site_settings(site_uid: str) -> str:
        """Get site settings.

        Args:
            site_uid: The site UID

        Returns:
            JSON with site settings including proxy configuration.
        """
        result = await client.get(f"/v2/site/{site_uid}/settings")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_site_filters(site_uid: str) -> str:
        """List filters available for a site.

        Args:
            site_uid: The site UID

        Returns:
            JSON array of filters available at this site.
        """
        result = await client.get(f"/v2/site/{site_uid}/filters")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_site_variables(site_uid: str) -> str:
        """List all site-level variables.

        Args:
            site_uid: The site UID

        Returns:
            JSON array of site variables with id, name, and value.
        """
        result = await client.get(f"/v2/site/{site_uid}/variables")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_site_variable_create(
        site_uid: str,
        name: str,
        value: str,
        masked: bool = False
    ) -> str:
        """Create a new site-level variable.

        Args:
            site_uid: The site UID
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
        result = await client.put(f"/v2/site/{site_uid}/variable", json=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_site_variable_update(
        site_uid: str,
        variable_id: str,
        name: str | None = None,
        value: str | None = None,
        masked: bool | None = None
    ) -> str:
        """Update an existing site-level variable.

        Args:
            site_uid: The site UID
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
        result = await client.post(f"/v2/site/{site_uid}/variable/{variable_id}", json=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_site_variable_delete(site_uid: str, variable_id: str) -> str:
        """Delete a site-level variable.

        Args:
            site_uid: The site UID
            variable_id: The variable ID to delete

        Returns:
            JSON confirmation of deletion.
        """
        result = await client.delete(f"/v2/site/{site_uid}/variable/{variable_id}")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_site_proxy_update(
        site_uid: str,
        proxy_host: str,
        proxy_port: int,
        proxy_type: str = "HTTP",
        proxy_username: str | None = None,
        proxy_password: str | None = None
    ) -> str:
        """Update proxy settings for a site.

        Args:
            site_uid: The site UID
            proxy_host: Proxy server hostname or IP
            proxy_port: Proxy server port
            proxy_type: Proxy type (HTTP or SOCKS5)
            proxy_username: Proxy authentication username (optional)
            proxy_password: Proxy authentication password (optional)

        Returns:
            JSON confirmation of proxy update.
        """
        data = {
            "proxyHost": proxy_host,
            "proxyPort": proxy_port,
            "proxyType": proxy_type
        }
        if proxy_username:
            data["proxyUsername"] = proxy_username
        if proxy_password:
            data["proxyPassword"] = proxy_password
        result = await client.post(f"/v2/site/{site_uid}/settings/proxy", json=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_site_proxy_delete(site_uid: str) -> str:
        """Delete proxy settings for a site.

        Args:
            site_uid: The site UID

        Returns:
            JSON confirmation of proxy deletion.
        """
        result = await client.delete(f"/v2/site/{site_uid}/settings/proxy")
        return json.dumps(result, indent=2)
