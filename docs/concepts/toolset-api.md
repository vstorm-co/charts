# Toolset API

The `FunctionToolset` provides AI agents with tools for creating UI components.

## Overview

Located in [`src/charts/toolset.py`](https://github.com/vstorm-co/charts/blob/main/src/charts/toolset.py).

The toolset exposes five tools:

- `create_table` - Create Table component
- `create_accordion` - Create Accordion component
- `create_card` - Create Card component
- `create_carousel` - Create Carousel component
- `create_chart` - Create Chart component

## Creating a Toolset

```python
from pydantic_ai import Agent
from charts.toolset import create_ui_toolset
from charts.engines.shadcn import Shadcn

# Create engine with TSX output
engine = Shadcn(return_mode='tsx')

# Create agent with UI tools
agent = Agent(
    'openai:gpt-5.1',
    tools=create_ui_toolset(engine)
)

# Run the agent
result = await agent.run('Create a bar chart of monthly sales')
```

## EngineDeps

Dependencies passed to tool functions:

```python
class EngineDeps(BaseModel):
    engine: EngineProtocol  # The rendering engine
    id: str | None          # Optional dependency ID
```

## Tool Return Value

Each tool returns a `ToolReturn` with metadata:

```python
ToolReturn(
    return_value="Successfully created chart: Monthly Sales",
    metadata={
        "ui_component": "<BarChart>...</BarChart>",  # Rendered component
        "config": {...},                            # Agent configuration
        "component_type": "chart",                  # Component type
        "data_summary": {"num_elements": 12}        # Data summary
    }
)
```

## Tool Metadata Fields

| Field | Description |
| ------- | ------------- |
| `ui_component` | Rendered component (TSX or JSON) |
| `config` | Full agent configuration dump |
| `component_type` | One of: table, chart, card, accordion, carousel |
| `data_summary` | Component-specific data summary |

## Custom Toolset ID

You can assign an ID to the toolset:

```python
toolset = create_ui_toolset(id='my-toolset')

agent = Agent(
    'openai:gpt-5.1',
    tools=toolset
)
```

The ID appears in tool metadata for tracking purposes.
