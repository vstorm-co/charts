# Agent Workflows

Advanced patterns for using Charts with AI agents.

## Multi-Step Data Collection

Agents can gather data through conversation before rendering components:

```python
from pydantic_ai import Agent
from charts.toolset import create_ui_toolset
from charts.engines.shadcn import Shadcn
import asyncio

engine = Shadcn(return_mode='tsx')
agent = Agent(
    'openai:gpt-5.1',
    tools=create_ui_toolset(engine),
)

async def collect_sales_data():
    agent = Agent(
        'openai:gpt-5.1',
        tools=create_ui_toolset(engine),
    )

    # Step 1: Ask for data
    result1 = await agent.run(
        "I need to create a sales chart. What are the monthly sales figures?"
    )

    # Step 2: Generate the chart with collected data
    result2 = await agent.run(
        "Now create a bar chart showing these sales figures"
    )

    return result2

# asyncio.run(collect_sales_data())
```

## Context-Aware Chart Generation

Pass existing context to the agent for more relevant components:

```python
from pydantic_ai import Agent
from charts.toolset import create_ui_toolset
from charts.engines.shadcn import Shadcn

engine = Shadcn(return_mode='tsx')

async def generate_contextual_chart(user_preferences: dict):
    # Start with user context
    system_prompt = f"""
    You are a data visualization expert.
    User preferences: {user_preferences}

    When creating charts, consider these preferences for colors and styling.
    """

    agent = Agent(
        'openai:gpt-5.1',
        tools=create_ui_toolset(engine),
        system_prompt=system_prompt,
    )

    result = await agent.run(
        "Create a line chart of quarterly revenue growth"
    )

    return result.output

# asyncio.run(generate_contextual_chart({'color_scheme': 'dark', 'focus': 'growth'}))
```

## Conditional Component Rendering

Render different components based on data or user needs:

```python
from pydantic_ai import Agent
from charts.toolset import create_ui_toolset
from charts.engines.shadcn import Shadcn

engine = Shadcn(return_mode='tsx')
agent = Agent(
    'openai:gpt-5.1',
    tools=create_ui_toolset(engine),
)

async def generate_dashboard(data_summary: dict):
    """Generate appropriate components based on data characteristics."""

    # Determine component type based on data
    if data_summary.get('type') == 'time_series':
        prompt = "Create a line chart showing trends over time"
    elif data_summary.get('type') == 'categories':
        prompt = "Create a bar chart comparing different categories"
    elif data_summary.get('type') == 'distribution':
        prompt = "Create a pie chart showing distribution"
    else:
        prompt = "Create a table displaying the data"

    result = await agent.run(prompt)
    return result.output

# asyncio.run(generate_dashboard({'type': 'time_series'}))
```

## Dashboard Generation Workflow

A complete multi-component dashboard workflow:

```python
from pydantic_ai import Agent
from charts.toolset import create_ui_toolset
from charts.engines.shadcn import Shadcn

engine = Shadcn(return_mode='tsx')

async def generate_complete_dashboard():
    agent = Agent(
        'openai:gpt-5.1',
        tools=create_ui_toolset(engine),
    )

    # Phase 1: Collect requirements
    req_result = await agent.run(
        "What data should this dashboard show? What components would be most useful?"
    )

    # Phase 2: Generate individual components
    chart_result = await agent.run(
        "Create a bar chart showing sales by region"
    )

    table_result = await agent.run(
        "Create a table with detailed sales data"
    )

    card_result = await agent.run(
        "Create a summary card with key metrics"
    )

    return {
        'chart': chart_result.output,
        'table': table_result.output,
        'card': card_result.output,
    }

# asyncio.run(generate_complete_dashboard())
```

## Tool Call Chain

Chain multiple tool calls for complex component generation:

```python
from pydantic_ai import Agent
from charts.toolset import create_ui_toolset
from charts.engines.shadcn import Shadcn

engine = Shadcn(return_mode='tsx')
agent = Agent(
    'openai:gpt-5.1',
    tools=create_ui_toolset(engine),
)

async def chain_tool_calls():
    """Generate a chart, then add it to an existing dashboard."""

    # Step 1: Create base chart
    result1 = await agent.run(
        "Create a line chart of website traffic for the last month"
    )

    # Step 2: Modify or extend based on feedback
    result2 = await agent.run(
        "Add mobile vs desktop breakdown to this chart"
    )

    # Step 3: Package with additional elements
    result3 = await agent.run(
        "Put this chart in a card with title 'Website Traffic'"
    )

    return result3.output

# asyncio.run(chain_tool_calls())
```
