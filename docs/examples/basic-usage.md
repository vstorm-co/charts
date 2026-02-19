# Basic Usage Examples

Learn to create individual components with the Charts library.

## Chart Component

Create a bar chart showing monthly sales:

```python
import asyncio
from charts.engines.shadcn import Shadcn
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData, ChartMetadata
from charts.base_types import BaseChartTypes

engine = Shadcn(return_mode='tsx')

# Create chart data
chart_data = ChartData(data=[
    {"month": "January", "desktop": 186, "mobile": 80},
    {"month": "February", "desktop": 305, "mobile": 90},
    {"month": "March", "desktop": 237, "mobile": 120},
])

# Create chart config
chart_config = ChartConfig(config={
    "desktop": {"label": "Desktop", "color": "#2563eb"},
    "mobile": {"label": "Mobile", "color": "#60a5fa"},
})

# Create and render the chart
chart = Chart(
    chart_type=BaseChartTypes.bar,
    metadata=ChartMetadata(
        title="Monthly Sales",
        description="January - March 2024"
    ),
    chart_data=chart_data,
    chart_config=chart_config,
    x_axis_key="month"
)

tsx_code = asyncio.run(engine.render_chart_component(chart))

# See the results
# print(tsx_code)
```

## Table Component

Create a data table showing user information:

```python
import asyncio
from charts.engines.shadcn import Shadcn
from charts.types.shadcn.table import Table, TableData

engine = Shadcn(return_mode='tsx')

# Create table data
table_data = TableData(
    headers=["Name", "Email", "Status"],
    rows=[
        ("Alice Johnson", "alice@example.com", "Active"),
        ("Bob Smith", "bob@example.com", "Inactive"),
        ("Carol White", "carol@example.com", "Active"),
    ]
)

# Create and render the table
table = Table(
    caption="User Management Table",
    table_data=table_data,
)

tsx_code = asyncio.run(engine.render_table_component(table))

# See the results
# print(tsx_code)
```

## Card Component

Create a card with title, description, and content:

```python
import asyncio
from charts.engines.shadcn import Shadcn
from charts.types.shadcn.card import Card

engine = Shadcn(return_mode='tsx')

# Create and render the card
card = Card(
    title="Weekly Progress",
    description="Performance metrics for this week",
    content="Your team has completed 8 out of 10 tasks. Great job!",
    footer="Updated: Today at 5:30 PM",
)

tsx_code = asyncio.run(engine.render_card_component(card))

# See the results
# print(tsx_code)
```

## Accordion Component

Create an accordion with multiple expandable sections:

```python
import asyncio
from charts.engines.shadcn import Shadcn
from charts.types.shadcn.accordion import Accordion
from charts.base_types import BaseAccordionItem, BaseAccordionTypes

engine = Shadcn(return_mode='tsx')

# Create accordion items
items = [
    BaseAccordionItem(value="getting-started", trigger="Getting Started", content="Learn the basics of our platform."),
    BaseAccordionItem(value="advanced", trigger="Advanced Features", content="Explore power user capabilities."),
    BaseAccordionItem(value="faq", trigger="FAQ", content="Common questions and answers."),
]

# Create and render the accordion (multiple expansion)
accordion = Accordion(
    items=items,
    list_type=BaseAccordionTypes.multiple,
)

tsx_code = await engine.render_accordion_component(accordion)

# See the results
# print(tsx_code)
```

## Carousel Component

Create a carousel with multiple slides:

```python
import asyncio
from charts.engines.shadcn import Shadcn
from charts.types.shadcn.carousel import Carousel, CarouselItem, CarouselConfig

engine = Shadcn(return_mode='tsx')

# Create carousel items
items = [
    CarouselItem(
        content="Welcome to Product Alpha - our flagship product"
    ),
    CarouselItem(
        content="Product Beta - Best seller of the year"
    ),
]

# Create and render the carousel
carousel = Carousel(
    items=items,
    config=CarouselConfig(
        orientation="horizontal",
        loop="true"
    ),
)

tsx_code = await engine.render_carousel_component(carousel)

# See the results
# print(tsx_code)
```

## Complete Example with Pydantic AI

Combine component creation with an agent workflow:

```python
import asyncio

from pydantic_ai import Agent
from charts.toolset import create_ui_toolset, EngineDeps
from charts.engines.shadcn import Shadcn, SHADCN_TOOLSET_PROMPT
from charts.utils.helpers import get_ui_component

from dotenv import load_dotenv

load_dotenv(override=True)

# 1. Setup engine and toolset
engine = Shadcn(return_mode='tsx')
toolset = create_ui_toolset()
deps = EngineDeps(engine=engine)

# 2. Setup agent
agent = Agent(
    'openai:gpt-4o',
    system_prompt=SHADCN_TOOLSET_PROMPT,
    toolsets=[toolset],
    deps_type=EngineDeps
)

# 3. Run the agent
# result = asyncio.run(agent.run('Create a dashboard with sales chart', deps=deps))
# component = get_ui_component(result)
# print(component)
```
