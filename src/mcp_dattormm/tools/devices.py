"""Device-related tools for Datto RMM."""

import json

from mcp.server.fastmcp import FastMCP

from ..client import DattoRMMClient, get_client


def register_device_tools(mcp: FastMCP, client: DattoRMMClient | None = None) -> None:
    """Register device-related tools with the MCP server."""
    client = client or get_client()

    @mcp.tool()
    async def dattormm_device_get(device_uid: str) -> str:
        """Get device details by UID.

        Args:
            device_uid: The unique identifier of the device

        Returns:
            JSON with device details including hostname, OS, site, status, and audit data.
        """
        result = await client.get(f"/v2/device/{device_uid}")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_device_get_by_id(device_id: int) -> str:
        """Get device details by numeric ID.

        Args:
            device_id: The numeric ID of the device

        Returns:
            JSON with device details including hostname, OS, site, status, and audit data.
        """
        result = await client.get(f"/v2/device/id/{device_id}")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_device_get_by_mac(mac_address: str) -> str:
        """Get device details by MAC address.

        Args:
            mac_address: The MAC address of the device (with or without colons)

        Returns:
            JSON with device details including hostname, OS, site, status, and audit data.
        """
        result = await client.get(f"/v2/device/macAddress/{mac_address}")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_device_alerts_open(
        device_uid: str,
        page: int = 1,
        max_results: int = 250
    ) -> str:
        """List open alerts for a device.

        Args:
            device_uid: The device UID
            page: Page number (1-indexed)
            max_results: Maximum results per page (max 250)

        Returns:
            JSON array of open alerts for this device.
        """
        params = {"page": page, "max": min(max_results, 250)}
        result = await client.get(f"/v2/device/{device_uid}/alerts/open", params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_device_alerts_resolved(
        device_uid: str,
        page: int = 1,
        max_results: int = 250
    ) -> str:
        """List resolved alerts for a device.

        Args:
            device_uid: The device UID
            page: Page number (1-indexed)
            max_results: Maximum results per page (max 250)

        Returns:
            JSON array of resolved alerts for this device.
        """
        params = {"page": page, "max": min(max_results, 250)}
        result = await client.get(f"/v2/device/{device_uid}/alerts/resolved", params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_device_udf_set(
        device_uid: str,
        udf1: str | None = None,
        udf2: str | None = None,
        udf3: str | None = None,
        udf4: str | None = None,
        udf5: str | None = None,
        udf6: str | None = None,
        udf7: str | None = None,
        udf8: str | None = None,
        udf9: str | None = None,
        udf10: str | None = None,
        udf11: str | None = None,
        udf12: str | None = None,
        udf13: str | None = None,
        udf14: str | None = None,
        udf15: str | None = None,
        udf16: str | None = None,
        udf17: str | None = None,
        udf18: str | None = None,
        udf19: str | None = None,
        udf20: str | None = None,
        udf21: str | None = None,
        udf22: str | None = None,
        udf23: str | None = None,
        udf24: str | None = None,
        udf25: str | None = None,
        udf26: str | None = None,
        udf27: str | None = None,
        udf28: str | None = None,
        udf29: str | None = None,
        udf30: str | None = None
    ) -> str:
        """Set user defined fields (UDF) on a device.

        Args:
            device_uid: The device UID
            udf1-udf30: User defined field values. Pass empty string to clear a field.

        Returns:
            JSON confirmation of UDF update.
        """
        data = {}
        local_vars = locals()
        for i in range(1, 31):
            key = f"udf{i}"
            if local_vars[key] is not None:
                data[key] = local_vars[key]

        if not data:
            return json.dumps({"error": "At least one UDF field must be provided"}, indent=2)

        result = await client.post(f"/v2/device/{device_uid}/udf", json=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_device_warranty_set(
        device_uid: str,
        warranty_date: str | None = None,
        warranty_vendor: str | None = None,
        warranty_notes: str | None = None
    ) -> str:
        """Set warranty information on a device.

        Args:
            device_uid: The device UID
            warranty_date: Warranty expiration date (ISO format: YYYY-MM-DD)
            warranty_vendor: Warranty vendor/provider name
            warranty_notes: Additional warranty notes

        Returns:
            JSON confirmation of warranty update.
        """
        data = {}
        if warranty_date is not None:
            data["warrantyDate"] = warranty_date
        if warranty_vendor is not None:
            data["warrantyVendor"] = warranty_vendor
        if warranty_notes is not None:
            data["warrantyNotes"] = warranty_notes

        if not data:
            return json.dumps({"error": "At least one warranty field must be provided"}, indent=2)

        result = await client.post(f"/v2/device/{device_uid}/warranty", json=data)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_device_move(device_uid: str, site_uid: str) -> str:
        """Move a device to a different site.

        Args:
            device_uid: The device UID to move
            site_uid: The target site UID

        Returns:
            JSON confirmation of device move.
        """
        result = await client.put(f"/v2/device/{device_uid}/site/{site_uid}")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_device_quickjob(
        device_uid: str,
        component_uid: str,
        variables: list[dict] | None = None
    ) -> str:
        """Run a quick job (component) on a device.

        Args:
            device_uid: The device UID
            component_uid: The component UID to run
            variables: Optional list of variable dictionaries with 'name' and 'value' keys

        Returns:
            JSON with job details including job UID.
        """
        data = {"componentUid": component_uid}
        if variables:
            data["variables"] = variables
        result = await client.put(f"/v2/device/{device_uid}/quickjob", json=data)
        return json.dumps(result, indent=2)
