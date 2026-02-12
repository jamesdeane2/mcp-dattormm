"""FastMCP server entry point for Datto RMM."""

from mcp.server.fastmcp import FastMCP

from .tools import register_all_tools

mcp = FastMCP("Datto RMM")


def main():
    """Run the MCP server."""
    register_all_tools(mcp)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
