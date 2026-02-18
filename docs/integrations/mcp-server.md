# MCP Server

Use Charts through the Model Context Protocol (MCP).

## Overview

The MCP server exposes tools for component generation that can be used by any MCP-compatible client.

## Available Tools

| Tool | Description |
|------|-------------|
| `show_chart` | Display a sample chart component |
| `show_table` | Display a sample table component |
| `show_card` | Display a sample card component |
| `show_accordion` | Display a sample accordion component |
| `show_carousel` | Display a sample carousel component |
| `show_all_components` | Display all components in a single view |

## Running the MCP Server

```bash
uv run python -m preview_app.mcp.server
```

Or with custom port:

```bash
uv run python -m preview_app.mcp.server --port 8000
```

## Example: Using with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": [
    {
      "name": "charts",
      "command": "uv",
      "args": ["run", "python", "-m", "preview_app.mcp.server"],
      "env": {}
    }
  ]
}
```

## Example: Using with Anthropic SDK

```python
from anthropic import Anthropic
from anthropic.types.mcp_tool import MCPParentTool

client = Anthropic()

# List available tools
tools = client.beta.tools.list(
    model="claude-3-5-sonnet-20241022"
)

# Use a charts tool
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=[],
    messages=[
        {
            "role": "user",
            "content": "Show me a bar chart of monthly sales"
        }
    ]
)
```

## Example: Using with mcp-py

```python
from mcp import Client, StdioServerParameters, create_client
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "preview_app.mcp.server"]
    )

    async with stdio_client(server_params) as (read, write):
        async with Client(read, write) as client:
            # List tools
            tools = await client.list_tools()

            # Call a tool
            result = await client.call_tool("show_chart", {
                "chart_type": "bar",
                "title": "Monthly Sales"
            })

            print(result)

# asyncio.run(main())
```

## Tool Parameters

### show_chart

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `chart_type` | string | "bar" | bar, line, pie, area, radar |
| `title` | string | "Sample Chart" | Chart title |
| `subtitle` | string \| null | null | Optional subtitle |
| `description` | string \| null | null | Optional description |
| `x_axis_key` | string | "category" | Key for X-axis labels |

### show_table

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `caption` | string | "Sample Data Table" | Table caption |
| `headers` | array[string] | ["Name", "Value", "Status"] | Column headers |
| `rows` | array[array] | Sample data | Data rows |

### show_card

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | string | "Sample Card" | Card title |
| `description` | string \| null | null | Optional description |
| `content` | string \| null | null | Main content |
| `footer` | string \| null | null | Footer text |

### show_accordion

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `items` | array[object] | Sample items | Accordion items |
| `list_type` | string | "single" | "single" or "multiple" |

### show_carousel

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `items` | array[object] | Sample items | Carousel items |
| `orientation` | string | "horizontal" | "vertical" or "horizontal" |
| `loop` | boolean | true | Infinite loop |
