# Pydantic AI Integration

Integrate Charts with Pydantic AI agents.

## Overview

The `FunctionToolset` provides UI component creation tools for your agent.

## Basic Setup

```python
from pydantic_ai import Agent
from charts.toolset import create_ui_toolset, EngineDeps
from charts.engines.shadcn import Shadcn

# Create engine and toolset
engine = Shadcn(return_mode='json')
toolset = create_ui_toolset()
deps = EngineDeps(engine=engine)

# Create agent with UI toolset
agent = Agent(
    'openai:gpt-5.1',
    toolsets=[toolset],
    deps_type=EngineDeps
)

# Run the agent with dependencies
# result = await agent.run('Create a bar chart showing monthly sales', deps=deps)

# Extract the component
# component = get_ui_component(result)
```

## Agent System Prompt

The library provides a default system prompt that guides the AI to create components:

```python
SHADCN_TOOLSET_PROMPT = """
You are an expert UI/UX developer using the Shadcn UI library.
Your goal is to create beautiful, functional, and accessible components
based on user requirements.

You have access to tools that render components using a specific engine.

When asked to create a UI element:
1. Gather or generate the necessary data for the component.
2. Structure the data according to the component's model (Table, Chart, Card, etc.).
3. Call the appropriate rendering tool (e.g., `create_table`, `create_chart`)
   to get the final React component code.

Always aim for high-quality data and sensible defaults for colors and labels.
"""
```

## Custom Agent with System Prompt

```python
from pydantic_ai import Agent
from charts.toolset import create_ui_toolset, EngineDeps
from charts.engines.shadcn import Shadcn, SHADCN_TOOLSET_PROMPT

engine = Shadcn(return_mode='tsx')
toolset = create_ui_toolset()
deps = EngineDeps(engine=engine)

agent = Agent(
    'openai:gpt-5.1',
    system_prompt=SHADCN_TOOLSET_PROMPT,
    toolsets=[toolset],
    deps_type=EngineDeps
)

# result = await agent.run('Create a dashboard with a chart and table', deps=deps)
# component = get_ui_component(result)
```

## Tool Return Structure

Each tool returns a `ToolReturn`. The generated UI component is stored in the `metadata`:

```python
# The ToolReturn structure
# return_value: "Successfully created table: Monthly Sales"
# metadata: {
#     "ui_component": "<Table>...</Table>",  # Rendered TSX or JSON
#     "config": {...},                      # UI configuration
#     "component_type": "table",            # Component type
#     "data_summary": {"rows": 12}          # Data summary
# }
```

## Complete Example

```python
import asyncio
from pydantic_ai import Agent
from charts.toolset import create_ui_toolset, EngineDeps
from charts.engines.shadcn import Shadcn
from charts.utils.helpers import get_ui_component, get_config_data

async def main():
    engine = Shadcn(return_mode='tsx')
    toolset = create_ui_toolset()
    deps = EngineDeps(engine=engine)

    agent = Agent(
        'openai:gpt-5.1',
        toolsets=[toolset],
        deps_type=EngineDeps
    )

    # Ask for a chart
    result = await agent.run('Show me a line chart of website traffic', deps=deps)

    # Access metadata for the UI component
    component = get_ui_component(result)

    # Extract the UI config
    config_data = get_config_data(result)

    # For FunctionToolset, the output might be in messages if using multiple tools
    # or you can inspect result.all_messages()

# asyncio.run(main())
```
