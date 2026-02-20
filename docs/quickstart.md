# Quick Start

Get started with Charts in under 5 minutes.

## Step 1: Install the Library

```bash
pip install charts
# or
uv add charts
```

## Step 2: Set Up Your Agent

Create a file `agent.py`:

```python
import asyncio
from pydantic_ai import Agent
from charts.toolset import create_ui_toolset, EngineDeps
from charts.engines.shadcn import Shadcn, SHADCN_TOOLSET_PROMPT
from charts.utils.helpers import get_ui_component
from dotenv import load_dotenv

load_dotenv(override=True)

async def main():
    # Create the engine with TSX output
    engine = Shadcn('tsx')
    toolset = create_ui_toolset()
    deps = EngineDeps(engine=engine)

    # Create agent with UI tools
    agent = Agent(
        "openai:gpt-5.1",
        retries=3,
        system_prompt=SHADCN_TOOLSET_PROMPT,
        toolsets=[toolset],
        deps_type=EngineDeps,
    )

    # Ask the agent to create a component
    result = await agent.run('Show me a bar chart of monthly sales', deps=deps)
    component = get_ui_component(result)
    print(component)  # Generated TSX code

if __name__ == '__main__':
    asyncio.run(main())
```

## Step 3: Run Your Agent

```bash
uv run agent.py
```

You'll see the generated React component in the console.

## Create a Chart Component

The `create_chart` tool accepts data as follows:

```python
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData, ChartMetadata
from charts.base_types import BaseChartTypes

chart_config = ChartConfig(
    config={
        "subscriptions": {"label": "New Subscriptions", "color": "#2563eb"},
        "revenue": {"label": "Monthly Revenue", "color": "#10b981"},
    }
)

chart_data = ChartData(data=[
    {"month": "January", "subscriptions": 186, "revenue": 450},
    {"month": "February", "subscriptions": 305, "revenue": 52},
    {"month": "March", "subscriptions": 237, "revenue": 480},
    {"month": "April", "subscriptions": 73, "revenue": 210},
    {"month": "May", "subscriptions": 209, "revenue": 59},
    {"month": "June", "subscriptions": 214, "revenue": 610},
])

chart_metadata = ChartMetadata(
        title="Monthly Revenue & Subscriptions",
        subtitle="Sales & revenue for the first quarter",
        description="This chart shows the subscriptions and revenue figures for January, February, and March."
    )

chart = Chart(
    chart_type=BaseChartTypes.bar,
    chart_data=chart_data,
    chart_config=chart_config,
    metadata=chart_metadata,
    x_axis_key="month"
)
```

You can also allow your Agent to reach the data by himself, e.g. via [database-pydantic-ai](https://github.com/vstorm-co/database-pydantic-ai) toolset that allows easy and effortless database connection and inference.

## What's Next?

- [Component Reference](components/chart.md) - Learn about all component types
- [Configuration](configuration/color-palettes.md) - Customize colors and themes
- [Examples](examples/basic-usage.md) - More code examples
