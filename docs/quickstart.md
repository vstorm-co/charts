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
from charts.toolset import create_ui_toolset
from charts.engines.shadcn import Shadcn

async def main():
    # Create the engine with TSX output
    engine = Shadcn(return_mode='tsx')

    # Create agent with UI tools
    agent = Agent(
        'openai:gpt-5.1',
        tools=create_ui_toolset(engine),
        deps_type=type('Deps', (), {'engine': engine})
    )

    # Ask the agent to create a component
    result = await agent.run('Show me a bar chart of monthly sales')

    print(result.text)  # Generated TSX code

if __name__ == '__main__':
    asyncio.run(main())
```

## Step 3: Run Your Agent

```bash
python agent.py
```

You'll see the generated React component in the console.

## Create a Chart Component

The `create_chart` tool accepts:

```python
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData

chart = Chart(
    data=[
        ChartData(name='Jan', sales=400),
        ChartData(name='Feb', sales=300),
        ChartData(name='Mar', sales=600),
    ],
    config=ChartConfig(
        type='bar',
        x_key='name',
        y_keys=['sales'],
        title='Monthly Sales'
    )
)
```

## Create a Table Component

```python
from charts.types.shadcn.table import Table, TableData

table = Table(
    data=[
        TableData(name='Product A', price=29.99, stock=100),
        TableData(name='Product B', price=49.99, stock=50),
    ],
    headers=['name', 'price', 'stock'],
    column_labels={'name': 'Product Name', 'price': 'Price ($)', 'stock': 'Stock'}
)
```

## What's Next?

- [Component Reference](components/chart.md) - Learn about all component types
- [Configuration](configuration/color-palettes.md) - Customize colors and themes
- [Examples](examples/basic-usage.md) - More code examples
