"""Tool registration for Datto RMM MCP server."""

from mcp.server.fastmcp import FastMCP

from .account import register_account_tools
from .sites import register_site_tools
from .devices import register_device_tools
from .alerts import register_alert_tools
from .audit import register_audit_tools
from .jobs import register_job_tools
from .filters import register_filter_tools
from .activity import register_activity_tools
from .system import register_system_tools


def register_all_tools(mcp: FastMCP) -> None:
    """Register all Datto RMM tools with the MCP server."""
    register_account_tools(mcp)
    register_site_tools(mcp)
    register_device_tools(mcp)
    register_alert_tools(mcp)
    register_audit_tools(mcp)
    register_job_tools(mcp)
    register_filter_tools(mcp)
    register_activity_tools(mcp)
    register_system_tools(mcp)
