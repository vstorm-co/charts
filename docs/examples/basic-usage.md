# Basic Usage Examples

Learn to create individual components with the Charts library.

## Chart Component

Create a bar chart showing monthly sales:

```python
from charts.engines.shadcn import Shadcn
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData

engine = Shadcn(return_mode='tsx')

# Create chart data
chart_data = [
    ChartData(month="January", desktop=186, mobile=80),
    ChartData(month="February", desktop=305, mobile=90),
    ChartData(month="March", desktop=237, mobile=120),
]

# Create chart config
chart_config = {
    "desktop": {"label": "Desktop", "color": "#2563eb"},
    "mobile": {"label": "Mobile", "color": "#60a5fa"},
}

# Create and render the chart
chart = Chart(
    title="Monthly Sales",
    description="January - March 2024",
    data=chart_data,
    config=chart_config,
)

tsx_code = engine.render_chart_component(chart)
```

## Table Component

Create a data table showing user information:

```python
from charts.engines.shadcn import Shadcn
from charts.types.shadcn.table import Table

engine = Shadcn(return_mode='tsx')

# Create table rows
table_data = [
    {"name": "Alice Johnson", "email": "alice@example.com", "status": "Active"},
    {"name": "Bob Smith", "email": "bob@example.com", "status": "Inactive"},
    {"name": "Carol White", "email": "carol@example.com", "status": "Active"},
]

# Create and render the table
table = Table(
    caption="User Management Table",
    headers=["Name", "Email", "Status"],
    items=table_data,
)

tsx_code = engine.render_table_component(table)
```

## Card Component

Create a card with title, description, and content:

```python
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

tsx_code = engine.render_card_component(card)
```

## Accordion Component

Create an accordion with multiple expandable sections:

```python
from charts.engines.shadcn import Shadcn
from charts.types.shadcn.accordion import Accordion, AccordionItem

engine = Shadcn(return_mode='tsx')

# Create accordion items
items = [
    AccordionItem(title="Getting Started", content="Learn the basics of our platform."),
    AccordionItem(title="Advanced Features", content="Explore power user capabilities."),
    AccordionItem(title="FAQ", content="Common questions and answers."),
]

# Create and render the accordion (multiple expansion)
accordion = Accordion(
    title="Help Center",
    items=items,
    type="multiple",
)

tsx_code = engine.render_accordion_component(accordion)
```

## Carousel Component

Create an image carousel with multiple slides:

```python
from charts.engines.shadcn import Shadcn
from charts.types.shadcn.carousel import Carousel, CarouselItem

engine = Shadcn(return_mode='tsx')

# Create carousel items
items = [
    CarouselItem(
        title="Product Alpha",
        description="Our flagship product",
        image_url="/images/alpha.jpg",
    ),
    CarouselItem(
        title="Product Beta",
        description="Best seller of the year",
        image_url="/images/beta.jpg",
    ),
]

# Create and render the carousel
carousel = Carousel(
    items=items,
    orientation="horizontal",
    loop=True,
)

tsx_code = engine.render_carousel_component(carousel)
```

## Complete Example with Pydantic AI

Combine component creation with an agent workflow:

```python
from pydantic_ai import Agent
from charts.toolset import create_ui_toolset
from charts.engines.shadcn import Shadcn

engine = Shadcn(return_mode='tsx')
agent = Agent(
    'openai:gpt-5.1',
    tools=create_ui_toolset(engine),
)

# Run the agent with a request for multiple components
result = await agent.run('Create a dashboard showing: 1) A bar chart of sales by region, 2) A table of top products')

print(result.output)
```
