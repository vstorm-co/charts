# Component Combinations

Create dashboards and layouts with multiple components.

## Dashboard Layout

Combine chart, table, and cards for a complete dashboard:

```python
from charts.engines.shadcn import Shadcn
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData
from charts.types.shadcn.table import Table
from charts.types.shadcn.card import Card

engine = Shadcn(return_mode='tsx')

# Create chart component
chart_data = [
    ChartData(month="Jan", sales=1200),
    ChartData(month="Feb", sales=1900),
    ChartData(month="Mar", sales=1500),
]

chart_config = {"sales": {"label": "Sales ($)", "color": "#10b981"}}

chart = Chart(
    title="Monthly Sales",
    description="Q1 2024 Performance",
    data=chart_data,
    config=chart_config,
)

# Create summary cards
cards = [
    Card(title="Total Sales", content="$4,600", footer="+15% from last quarter"),
    Card(title="New Customers", content="89", footer="+8% from last quarter"),
    Card(title="Avg Order Value", content="$127", footer="+3% from last quarter"),
]

# Create data table
table_data = [
    {"product": "Widget A", "sales": 450, "margin": "24%"},
    {"product": "Widget B", "sales": 380, "margin": "18%"},
    {"product": "Gadget X", "sales": 670, "margin": "31%"},
]

table = Table(
    caption="Product Sales Details",
    headers=["Product", "Sales", "Margin"],
    items=table_data,
)

# Render all components
tsx_chart = engine.render_chart_component(chart)
tsx_table = engine.render_table_component(table)
tsx_cards = [engine.render_card_component(card) for card in cards]
```

## Data Grid with Summary

Show detailed data with summary statistics:

```python
from charts.engines.shadcn import Shadcn
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData
from charts.types.shadcn.table import Table

engine = Shadcn(return_mode='tsx')

# Create data table with employee information
employees = [
    {"name": "Alice", "department": "Engineering", "score": 92},
    {"name": "Bob", "department": "Sales", "score": 85},
    {"name": "Carol", "department": "Engineering", "score": 88},
    {"name": "Dave", "department": "Marketing", "score": 79},
]

table = Table(
    caption="Employee Performance Scores",
    headers=["Name", "Department", "Score"],
    items=employees,
)

# Create bar chart showing scores by department
chart_data = [
    ChartData(department="Engineering", score=90),
    ChartData(department="Sales", score=85),
    ChartData(department="Marketing", score=79),
]

chart_config = {"score": {"label": "Average Score", "color": "#3b82f6"}}

chart = Chart(
    title="Department Performance",
    data=chart_data,
    config=chart_config,
)

tsx_table = engine.render_table_component(table)
tsx_chart = engine.render_chart_component(chart)
```

## Interactive Dashboard with Accordion

Combine visualizations with expandable sections:

```python
from charts.engines.shadcn import Shadcn
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData
from charts.types.shadcn.accordion import Accordion, AccordionItem
from charts.types.shadcn.card import Card

engine = Shadcn(return_mode='tsx')

# Main metrics card
metrics_card = Card(
    title="Key Metrics",
    content="""
- Revenue: $245K (+12%)
- Users: 12.5K (+8%)
- Churn: 2.3% (-0.5%)
""",
)

# Charts for visual context
revenue_data = [
    ChartData(quarter="Q1", revenue=60),
    ChartData(quarter="Q2", revenue=62),
    ChartData(quarter="Q3", revenue=64),
    ChartData(quarter="Q4", revenue=69),
]

revenue_config = {"revenue": {"label": "Revenue (K$)", "color": "#10b981"}}

revenue_chart = Chart(
    title="Quarterly Revenue Growth",
    data=revenue_data,
    config=revenue_config,
)

# Detailed breakdown in accordion
breakdown_items = [
    AccordionItem(
        title="Revenue by Region",
        content="North: $95K, South: $68K, East: $52K, West: $30K",
    ),
    AccordionItem(
        title="Top Performing Products",
        content="Product A ($89K), Product B ($76K), Product C ($54K)",
    ),
]

breakdown_accordion = Accordion(
    title="Detailed Breakdown",
    items=breakdown_items,
    type="single",
)

tsx_metrics = engine.render_card_component(metrics_card)
tsx_chart = engine.render_chart_component(revenue_chart)
tsx_accordion = engine.render_accordion_component(breakdown_accordion)
```

## Full Page Dashboard Template

Complete dashboard with all component types:

```python
from charts.engines.shadcn import Shadcn
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData
from charts.types.shadcn.table import Table
from charts.types.shadcn.card import Card
from charts.types.shadcn.accordion import Accordion, AccordionItem
from charts.types.shadcn.carousel import Carousel, CarouselItem

engine = Shadcn(return_mode='tsx')

# Header carousel
carousel_items = [
    CarouselItem(
        title="New Feature",
        description="Check out our latest analytics dashboard update",
        image_url="/images/feature1.jpg",
    ),
    CarouselItem(
        title="Upgrade Available",
        description="Pro plan now includes AI insights",
        image_url="/images/promo.jpg",
    ),
]

carousel = Carousel(items=carousel_items, loop=True)

# Top metrics row (cards)
top_cards = [
    Card(title="Total Users", content="15,243", footer="+2.5% this week"),
    Card(title="Active Sessions", content="8,921", footer="+5.2% this week"),
    Card(title="Revenue", content="$45.8K", footer="+3.1% this week"),
]

# Main chart
chart_data = [
    ChartData(day="Mon", visits=1200),
    ChartData(day="Tue", visits=1450),
    ChartData(day="Wed", visits=1380),
    ChartData(day="Thu", visits=1620),
    ChartData(day="Fri", visits=1790),
]

chart_config = {"visits": {"label": "Visitors", "color": "#6366f1"}}

traffic_chart = Chart(
    title="Weekly Website Traffic",
    description="Unique visitors per day",
    data=chart_data,
    config=chart_config,
)

# Detailed table
table_data = [
    {"page": "/home", "visits": 4521, "bounce_rate": "38%"},
    {"page": "/products", "visits": 3289, "bounce_rate": "42%"},
    {"page": "/pricing", "visits": 1876, "bounce_rate": "29%"},
]

traffic_table = Table(
    caption="Page Performance",
    headers=["Page", "Visits", "Bounce Rate"],
    items=table_data,
)

# FAQ accordion
faq_items = [
    AccordionItem(title="How is data calculated?", content="Data is updated hourly from our analytics pipeline."),
    AccordionItem(title="Can I export reports?", content="Yes, export to PDF or CSV available in Pro plan."),
]

faq_accordion = Accordion(
    title="Frequently Asked Questions",
    items=faq_items,
    type="single",
)

# Render all components for the dashboard
tsx_carousel = engine.render_carousel_component(carousel)
tsx_cards = [engine.render_card_component(card) for card in top_cards]
tsx_chart = engine.render_chart_component(traffic_chart)
tsx_table = engine.render_table_component(traffic_table)
tsx_accordion = engine.render_accordion_component(faq_accordion)
```

## Responsive Layout Components

Create components that work well together:

```python
from charts.engines.shadcn import Shadcn
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData
from charts.types.shadcn.card import Card

engine = Shadcn(return_mode='tsx')

# Small card for sidebar
sidebar_card = Card(
    title="Quick Stats",
    description="At a glance metrics",
    content="""
Total: 1,234
Active: 890
Pending: 123
Completed: 221
""",
)

# Large chart for main area
chart_data = [
    ChartData(date="Jan", value=100),
    ChartData(date="Feb", value=150),
    ChartData(date="Mar", value=180),
    ChartData(date="Apr", value=220),
]

chart_config = {"value": {"label": "Value", "color": "#ec4899"}}

main_chart = Chart(
    title="Main Performance Metric",
    description="January through April",
    data=chart_data,
    config=chart_config,
)

tsx_sidebar_card = engine.render_card_component(sidebar_card)
tsx_main_chart = engine.render_chart_component(main_chart)
```
