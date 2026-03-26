<!-- badges -->
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![MCP](https://img.shields.io/badge/MCP-FastMCP-purple)

# MCP Datto RMM Server

A comprehensive [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server for the [Datto RMM](https://www.datto.com/products/rmm/) API v2. Gives AI assistants like Claude full access to your RMM platform — query devices, manage sites, resolve alerts, run jobs, pull audit data, and control variables, all through natural language.

## Features

- **55 tools** covering the full Datto RMM API v2 surface
- **OAuth 2.0 authentication** with automatic token management (100-hour tokens, auto-refresh at 90 hours)
- **Structured error handling** — typed exceptions for auth, validation, rate-limit, not-found, and server errors
- **Automatic retry** with exponential backoff on rate limits (429) and transient server errors (5xx)
- **Pagination support** on all list endpoints (up to 250 results per page)
- **Modular architecture** — one file per API domain, easy to extend
- **Async throughout** — built on `httpx` with full async/await support

## Installation

```bash
git clone https://github.com/jamesdeane2/mcp-dattormm.git
cd mcp-dattormm
uv pip install -e .
```

## Configuration

Create a `.env` file in the project root:

```env
DATTORMM_API_KEY=your-api-key
DATTORMM_API_SECRET=your-api-secret
```

| Variable | Description | Default |
|----------|-------------|---------|
| `DATTORMM_API_KEY` | Datto RMM API key (required) | — |
| `DATTORMM_API_SECRET` | Datto RMM API secret (required) | — |
| `DATTORMM_API_URL` | API base URL | `https://merlot-api.centrastage.net/api` |
| `DATTORMM_AUTH_URL` | OAuth token endpoint | `https://merlot-api.centrastage.net/auth/oauth/token` |
| `DATTORMM_TIMEOUT` | Request timeout (seconds) | `30.0` |
| `DATTORMM_MAX_RETRIES` | Max retry attempts | `3` |

### Getting API Credentials

1. Log in to your Datto RMM portal
2. Navigate to **Setup > Global Settings > API**
3. Generate an API key and secret pair
4. Store them securely — the secret is shown only once

### Regional API URLs

The default URL targets the **Merlot** (US) region. If your account is on a different platform:

| Region | API URL |
|--------|---------|
| Merlot (US) | `https://merlot-api.centrastage.net/api` |
| Concord (US) | `https://concord-api.centrastage.net/api` |
| Pinotage (EU) | `https://pinotage-api.centrastage.net/api` |
| Vidal (AU) | `https://vidal-api.centrastage.net/api` |
| Zinfandel (US) | `https://zinfandel-api.centrastage.net/api` |
| Syrah (US) | `https://syrah-api.centrastage.net/api` |

## Claude Desktop Integration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "dattormm": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-dattormm",
        "run",
        "mcp-dattormm"
      ]
    }
  }
}
```

Restart Claude Desktop after updating the configuration.

## Available Tools (55)

### Account (13 tools)

| Tool | Description |
|------|-------------|
| `dattormm_account_get` | Get account details |
| `dattormm_account_sites` | List all sites with optional name filter |
| `dattormm_account_devices` | List all devices with filters (hostname, type, OS, site) |
| `dattormm_account_users` | List account users |
| `dattormm_account_components` | List available components (scripts/monitors) |
| `dattormm_account_alerts_open` | List all open alerts |
| `dattormm_account_alerts_resolved` | List all resolved alerts |
| `dattormm_account_variables` | List account-level variables |
| `dattormm_account_variable_create` | Create account variable (supports masked values) |
| `dattormm_account_variable_update` | Update account variable |
| `dattormm_account_variable_delete` | Delete account variable |
| `dattormm_account_dnet_mappings` | Get Datto Networking site mappings |
| `dattormm_user_reset_api_keys` | Reset API keys for current user |

### Sites (15 tools)

| Tool | Description |
|------|-------------|
| `dattormm_site_get` | Get site details by UID |
| `dattormm_site_create` | Create a new site |
| `dattormm_site_update` | Update site properties |
| `dattormm_site_devices` | List devices at a site |
| `dattormm_site_devices_network` | List network interfaces for site devices |
| `dattormm_site_alerts_open` | List open alerts for a site |
| `dattormm_site_alerts_resolved` | List resolved alerts for a site |
| `dattormm_site_settings` | Get site settings |
| `dattormm_site_filters` | List saved filters for a site |
| `dattormm_site_variables` | List site-level variables |
| `dattormm_site_variable_create` | Create site variable |
| `dattormm_site_variable_update` | Update site variable |
| `dattormm_site_variable_delete` | Delete site variable |
| `dattormm_site_proxy_update` | Update site proxy settings |
| `dattormm_site_proxy_delete` | Delete site proxy settings |

### Devices (9 tools)

| Tool | Description |
|------|-------------|
| `dattormm_device_get` | Get device by UID |
| `dattormm_device_get_by_id` | Get device by numeric ID |
| `dattormm_device_get_by_mac` | Get device by MAC address |
| `dattormm_device_alerts_open` | List open alerts for a device |
| `dattormm_device_alerts_resolved` | List resolved alerts for a device |
| `dattormm_device_udf_set` | Set user-defined fields (UDF 1-30) |
| `dattormm_device_warranty_set` | Set warranty date, vendor, and notes |
| `dattormm_device_move` | Move device to a different site |
| `dattormm_device_quickjob` | Run a quick job (component) on a device |

### Alerts (2 tools)

| Tool | Description |
|------|-------------|
| `dattormm_alert_get` | Get alert details by UID |
| `dattormm_alert_resolve` | Resolve an open alert |

### Audit (5 tools)

| Tool | Description |
|------|-------------|
| `dattormm_audit_device` | Get device audit data (hardware, OS, network) |
| `dattormm_audit_device_software` | Get software inventory for a device |
| `dattormm_audit_device_by_mac` | Get audit data by MAC address |
| `dattormm_audit_printer` | Get printer audit data |
| `dattormm_audit_esxi` | Get ESXi host audit data |

### Jobs (5 tools)

| Tool | Description |
|------|-------------|
| `dattormm_job_get` | Get job details by UID |
| `dattormm_job_components` | Get components used in a job |
| `dattormm_job_results` | Get job results for a specific device |
| `dattormm_job_stdout` | Get stdout output from a job |
| `dattormm_job_stderr` | Get stderr output from a job |

### Filters (2 tools)

| Tool | Description |
|------|-------------|
| `dattormm_filters_default` | List default (built-in) filters |
| `dattormm_filters_custom` | List custom filters |

### Activity (1 tool)

| Tool | Description |
|------|-------------|
| `dattormm_activity_logs` | Get activity logs with date/user/action filters |

### System (3 tools)

| Tool | Description |
|------|-------------|
| `dattormm_system_status` | Get API system status |
| `dattormm_system_rate` | Get current request rate usage |
| `dattormm_system_pagination` | Get pagination settings |

## Error Handling

The client provides structured exception types:

```python
from mcp_dattormm.client import (
    DattoRMMError,            # Base error
    DattoRMMAuthError,        # 401/403 — Invalid credentials or forbidden
    DattoRMMNotFoundError,    # 404 — Resource not found
    DattoRMMValidationError,  # 400/422 — Bad request parameters
    DattoRMMRateLimitError,   # 429 — Rate limit exceeded (includes retry_after)
    DattoRMMServerError,      # 5xx — Server-side failure
)
```

Rate-limited requests automatically retry with exponential backoff, respecting `Retry-After` headers when provided.

## Project Structure

```
mcp-dattormm/
├── pyproject.toml                 # Project config (hatchling build)
├── README.md
├── LICENSE                        # MIT
└── src/
    └── mcp_dattormm/
        ├── __init__.py
        ├── server.py              # FastMCP server entry point
        ├── client.py              # Async HTTP client with OAuth + retry
        ├── config.py              # Pydantic settings (env vars / .env)
        └── tools/
            ├── __init__.py        # Tool registration dispatcher
            ├── account.py         # Account, users, components, variables
            ├── sites.py           # Site CRUD, settings, proxy, variables
            ├── devices.py         # Device lookup, UDFs, warranty, jobs
            ├── alerts.py          # Alert details and resolution
            ├── audit.py           # Device/printer/ESXi audit data
            ├── jobs.py            # Job tracking and output retrieval
            ├── filters.py         # Default and custom filters
            ├── activity.py        # Activity log queries
            └── system.py          # API status, rate, pagination
```

## API Limits

| Limit | Value |
|-------|-------|
| Rate limit | 600 requests per 60 seconds |
| Max results per page | 250 |
| Token lifetime | 100 hours (auto-refreshed at 90 hours) |

## Tech Stack

- **Python 3.10+**
- **[FastMCP](https://github.com/modelcontextprotocol/python-sdk)** — MCP server framework
- **[httpx](https://www.python-httpx.org/)** — Async HTTP client
- **[Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)** — Configuration management
- **[Hatchling](https://hatch.pypa.io/)** — Build backend

## Adding New Tools

1. Create a new file in `src/mcp_dattormm/tools/` (e.g., `patches.py`)
2. Define a `register_*_tools(mcp, client)` function
3. Import and call it in `tools/__init__.py`

```python
# src/mcp_dattormm/tools/patches.py
import json
from mcp.server.fastmcp import FastMCP
from ..client import DattoRMMClient, get_client

def register_patch_tools(mcp: FastMCP, client: DattoRMMClient | None = None) -> None:
    client = client or get_client()

    @mcp.tool()
    async def dattormm_list_patches(device_uid: str) -> str:
        """List available patches for a device."""
        result = await client.get(f"/v2/device/{device_uid}/patches")
        return json.dumps(result, indent=2)
```

## License

MIT License — see [LICENSE](LICENSE) for details.

## Resources

- [Datto RMM API Documentation](https://rmm-api-doc.datto.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
