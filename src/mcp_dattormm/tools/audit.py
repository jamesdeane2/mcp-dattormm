"""Audit-related tools for Datto RMM."""

import json

from mcp.server.fastmcp import FastMCP

from ..client import DattoRMMClient, get_client


def register_audit_tools(mcp: FastMCP, client: DattoRMMClient | None = None) -> None:
    """Register audit-related tools with the MCP server."""
    client = client or get_client()

    @mcp.tool()
    async def dattormm_audit_device(device_uid: str) -> str:
        """Get full audit data for a device.

        Args:
            device_uid: The unique identifier of the device

        Returns:
            JSON with comprehensive hardware and software audit data including:
            - Hardware: CPU, RAM, disks, network adapters
            - Software: Installed applications, Windows features
            - Security: Antivirus status, firewall state
            - System: OS details, last boot time, uptime
        """
        result = await client.get(f"/v2/audit/device/{device_uid}")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_audit_device_software(
        device_uid: str,
        page: int = 1,
        max_results: int = 250
    ) -> str:
        """Get software inventory for a device.

        Args:
            device_uid: The unique identifier of the device
            page: Page number (1-indexed)
            max_results: Maximum results per page (max 250)

        Returns:
            JSON array of installed software with name, version, publisher, and install date.
        """
        params = {"page": page, "max": min(max_results, 250)}
        result = await client.get(f"/v2/audit/device/{device_uid}/software", params=params)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_audit_device_by_mac(mac_address: str) -> str:
        """Get audit data for a device by MAC address.

        Args:
            mac_address: The MAC address of the device (with or without colons)

        Returns:
            JSON with comprehensive hardware and software audit data.
        """
        result = await client.get(f"/v2/audit/device/macAddress/{mac_address}")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_audit_printer(device_uid: str) -> str:
        """Get printer audit data for a device.

        Args:
            device_uid: The unique identifier of the device

        Returns:
            JSON with printer information including name, driver, port, and status.
        """
        result = await client.get(f"/v2/audit/printer/{device_uid}")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_audit_esxi(device_uid: str) -> str:
        """Get ESXi host audit data.

        Args:
            device_uid: The unique identifier of the ESXi host device

        Returns:
            JSON with ESXi host information including version, VMs, datastores, and resources.
        """
        result = await client.get(f"/v2/audit/esxihost/{device_uid}")
        return json.dumps(result, indent=2)
