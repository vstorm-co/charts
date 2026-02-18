# Charts - Agentic UI Component Generation

Charts is a Python middleware library that connects Agentic AI libraries (specifically `pydantic-ai`) with frontend libraries. It enables AI agents to generate structured configurations for UI components that render to React/TSX code.

## Features

- **Pydantic Models** - Type-safe component definitions with validation
- **Engine Abstraction** - Render components to different formats (TSX, JSON)
- **MCP Server** - Model Context Protocol integration for AI agents
- **FastAPI Integration** - REST API for component generation
- **Jinja2 Templates** - Flexible React/TypeScript code generation

## Supported Components

| Component | Description |
|-----------|-------------|
| Chart | Bar, Line, Pie, Area, Radar charts via Recharts |
| Table | Data grid with headers, rows, and footer calculations |
| Card | Container with title, description, content, footer |
| Accordion | Single/Multiple expansion collapsible panels |
| Carousel | Horizontal/vertical scrolling with loop option |

## Quick Start

```python
from pydantic_ai import Agent
from charts.toolset import create_ui_toolset
from charts.engines.shadcn import Shadcn

# Create an agent with UI tools
agent = Agent(
    'openai:gpt-5.1',
    tools=create_ui_toolset(Shadcn())
)

# Run the agent
result = agent.run('Create a bar chart showing monthly sales')
print(result.data)  # Generated Chart component
```

## Architecture

The library follows a layered architecture:

1. **Base Types** - Abstract base classes for all components
2. **Types** - Concrete Pydantic models with validation
3. **Engine** - Converts models to TSX via Jinja2 templates
4. **Templates** - Jinja2 templates generating React components

## Installation

```bash
pip install charts
# Or with uv
uv add charts
```

For shadcn/ui integration:

```bash
npx shadcn@latest add accordion button card carousel chart select table
```

## Examples

See the [Examples](examples/basic-usage.md) section for ready-to-use code patterns.

## API Reference

Full API documentation available in the [API Reference](api/index.md) section.

## Integration Guides

- [Pydantic AI](integrations/pydantic-ai.md) - Agent setup
- [MCP Server](integrations/mcp-server.md) - Model Context Protocol
- [FastAPI Server](integrations/api-server.md) - REST API
- [Frontend](integrations/frontend.md) - Using generated components

## Project Links

- [GitHub Repository](https://github.com/vstorm-co/charts)
- [PyPI Package](https://pypi.org/project/charts/)
