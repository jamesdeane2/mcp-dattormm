# MCP Datto RMM Server

FastMCP server for Datto RMM API v2 integration with Claude Desktop.

## Installation

```bash
cd mcp-dattormm
uv pip install -e .
```

## Configuration

Create `.env` file:

```
DATTORMM_API_KEY=your-api-key
DATTORMM_API_SECRET=your-api-secret
```

## Claude Desktop Integration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

## Available Tools

### Account
- `dattormm_account_get` - Get account details
- `dattormm_account_sites` - List all sites
- `dattormm_account_devices` - List all devices with filters
- `dattormm_account_users` - List account users
- `dattormm_account_components` - List available components
- `dattormm_account_alerts_open` - List open alerts
- `dattormm_account_alerts_resolved` - List resolved alerts
- `dattormm_account_variables` - List account variables
- `dattormm_account_variable_create` - Create account variable
- `dattormm_account_variable_update` - Update account variable
- `dattormm_account_variable_delete` - Delete account variable
- `dattormm_account_dnet_mappings` - Get D-Net site mappings
- `dattormm_user_reset_api_keys` - Reset API keys

### Sites
- `dattormm_site_get` - Get site by UID
- `dattormm_site_create` - Create new site
- `dattormm_site_update` - Update site
- `dattormm_site_devices` - List site devices
- `dattormm_site_devices_network` - List site network interfaces
- `dattormm_site_alerts_open` - List site open alerts
- `dattormm_site_alerts_resolved` - List site resolved alerts
- `dattormm_site_settings` - Get site settings
- `dattormm_site_filters` - List site filters
- `dattormm_site_variables` - List site variables
- `dattormm_site_variable_create` - Create site variable
- `dattormm_site_variable_update` - Update site variable
- `dattormm_site_variable_delete` - Delete site variable
- `dattormm_site_proxy_update` - Update site proxy settings
- `dattormm_site_proxy_delete` - Delete site proxy settings

### Devices
- `dattormm_device_get` - Get device by UID
- `dattormm_device_get_by_id` - Get device by numeric ID
- `dattormm_device_get_by_mac` - Get device by MAC address
- `dattormm_device_alerts_open` - List device open alerts
- `dattormm_device_alerts_resolved` - List device resolved alerts
- `dattormm_device_udf_set` - Set device UDF fields (1-30)
- `dattormm_device_warranty_set` - Set device warranty info
- `dattormm_device_move` - Move device to different site
- `dattormm_device_quickjob` - Run quick job on device

### Alerts
- `dattormm_alert_get` - Get alert details
- `dattormm_alert_resolve` - Resolve an alert

### Audit
- `dattormm_audit_device` - Get device audit data
- `dattormm_audit_device_software` - Get device software inventory
- `dattormm_audit_device_by_mac` - Get audit by MAC address
- `dattormm_audit_printer` - Get printer audit data
- `dattormm_audit_esxi` - Get ESXi host audit data

### Jobs
- `dattormm_job_get` - Get job details
- `dattormm_job_components` - Get job components
- `dattormm_job_results` - Get job results for device
- `dattormm_job_stdout` - Get job stdout output
- `dattormm_job_stderr` - Get job stderr output

### Filters
- `dattormm_filters_default` - List default filters
- `dattormm_filters_custom` - List custom filters

### Activity
- `dattormm_activity_logs` - Get activity logs with filters

### System
- `dattormm_system_status` - Get system status
- `dattormm_system_rate` - Get current request rate
- `dattormm_system_pagination` - Get pagination settings

## API Limits

- Rate Limit: 600 requests per 60 seconds
- Max Results: 250 per page
- Token Expiry: 100 hours (auto-refresh at 90 hours)
