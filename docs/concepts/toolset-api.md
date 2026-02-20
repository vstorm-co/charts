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

## Creating an Agent with a Toolset

```python
from pydantic_ai import Agent
from charts.toolset import create_ui_toolset, EngineDeps
from charts.engines.shadcn import Shadcn, SHADCN_TOOLSET_PROMPT
from charts.utils.helpers import get_ui_component

# Create engine with TSX output
engine = Shadcn(return_mode='tsx')

# Create agent with UI tools
toolset = create_ui_toolset()
engine = Shadcn("json")
deps = EngineDeps(engine=engine)

agent = Agent(
    "openai:gpt-5.1",
    retries=3,
    system_prompt=SHADCN_TOOLSET_PROMPT,
    toolsets=[toolset],
    deps_type=EngineDeps,
)

# Run the agent
result = await agent.run('Create a bar chart of monthly sales')

# Get the result
component = get_ui_component(result)
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
        "ui_component": "<BarChart>...</BarChart>",  # Rendered component in TSX or JSON
        "config": {...},                            # UI configuration
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
