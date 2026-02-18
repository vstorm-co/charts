# Pydantic AI Integration

Integrate Charts with Pydantic AI agents.

## Overview

The `FunctionToolset` provides UI component creation tools for your agent.

## Basic Setup

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
result = await agent.run('Create a bar chart showing monthly sales')
print(result.output)  # ToolReturn with generated component
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
from charts.toolset import create_ui_toolset, SHADCN_TOOLSET_PROMPT
from charts.engines.shadcn import Shadcn

engine = Shadcn(return_mode='tsx')

agent = Agent(
    'openai:gpt-5.1',
    system_prompt=SHADCN_TOOLSET_PROMPT,
    tools=create_ui_toolset(engine)
)

result = await agent.run('Create a dashboard with a chart and table')
```

## Tool Return Structure

Each tool returns a `ToolReturn`:

```python
ToolReturn(
    return_value="Successfully created table: Monthly Sales",
    metadata={
        "ui_element": "<Table>...</Table>",  # Rendered TSX
        "config": {...},                      # Agent configuration
        "component_type": "table",            # Component type
        "data_summary": {"rows": 12}          # Data summary
    }
)
```

## Complete Example

```python
import asyncio
from pydantic_ai import Agent
from charts.toolset import create_ui_toolset
from charts.engines.shadcn import Shadcn
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData

async def main():
    engine = Shadcn(return_mode='tsx')

    agent = Agent(
        'openai:gpt-5.1',
        tools=create_ui_toolset(engine)
    )

    # Ask for a chart
    result = await agent.run('Show me a line chart of website traffic')

    print(result.output.return_value)
    print(result.output.metadata['ui_element'])

asyncio.run(main())
```

## Custom Output Types

You can also specify custom output types:

```python
from charts.types.shadcn.chart import ChartToolOutput

result = await agent.run(
    'Create a pie chart of browser usage',
    output_type=ChartToolOutput
)
```
