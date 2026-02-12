"""Job-related tools for Datto RMM."""

import json

from mcp.server.fastmcp import FastMCP

from ..client import DattoRMMClient, get_client


def register_job_tools(mcp: FastMCP, client: DattoRMMClient | None = None) -> None:
    """Register job-related tools with the MCP server."""
    client = client or get_client()

    @mcp.tool()
    async def dattormm_job_get(job_uid: str) -> str:
        """Get job details by UID.

        Args:
            job_uid: The unique identifier of the job

        Returns:
            JSON with job details including status, target devices, and execution info.
        """
        result = await client.get(f"/v2/job/{job_uid}")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_job_components(job_uid: str) -> str:
        """Get components associated with a job.

        Args:
            job_uid: The unique identifier of the job

        Returns:
            JSON array of components in the job with their execution order and settings.
        """
        result = await client.get(f"/v2/job/{job_uid}/components")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_job_results(job_uid: str, device_uid: str) -> str:
        """Get job results for a specific device.

        Args:
            job_uid: The unique identifier of the job
            device_uid: The unique identifier of the device

        Returns:
            JSON with job results including status, exit codes, and timing.
        """
        result = await client.get(f"/v2/job/{job_uid}/results/{device_uid}")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_job_stdout(job_uid: str, device_uid: str) -> str:
        """Get stdout output from a job execution on a device.

        Args:
            job_uid: The unique identifier of the job
            device_uid: The unique identifier of the device

        Returns:
            JSON with stdout content from the job execution.
        """
        result = await client.get(f"/v2/job/{job_uid}/results/{device_uid}/stdout")
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def dattormm_job_stderr(job_uid: str, device_uid: str) -> str:
        """Get stderr output from a job execution on a device.

        Args:
            job_uid: The unique identifier of the job
            device_uid: The unique identifier of the device

        Returns:
            JSON with stderr content from the job execution.
        """
        result = await client.get(f"/v2/job/{job_uid}/results/{device_uid}/stderr")
        return json.dumps(result, indent=2)
