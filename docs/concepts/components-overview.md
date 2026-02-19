# Component Overview

Charts supports five component types for generating React UI elements.

## Chart

**File:** [`src/charts/types/shadcn/chart.py`](https://github.com/vstorm-co/charts/blob/main/src/charts/types/shadcn/chart.py)

Generates interactive charts using Recharts library.

### Chart Types

| Type | Use Case |
| ------ | ---------- |
| `bar` | Comparing values across categories |
| `line` | Showing trends over time |
| `pie` | Displaying proportions |
| `area` | Cumulative data visualization |
| `radar` | Multivariate data comparison |

### Example

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

## Table

**File:** [`src/charts/types/shadcn/table.py`](https://github.com/vstorm-co/charts/blob/main/src/charts/types/shadcn/table.py)

Displays data in a grid format with optional footer calculations.

### Example

```python
from charts.types.shadcn.table import Table, TableData, TableFooter

table_data = TableData(
    headers=["name", "position", "sales"],
    rows=[("Alice", "Manager", 1000), ("Bob", "Salesperson", 500)],
)

table_footer = TableFooter(
    keyword="Total",
    header_to_summarize="sales",
    value=1500,
)

table = Table(
    table_data=table_data,
    caption="Sales Team",
    footer=table_footer,
)
```

## Card

**File:** [`src/charts/types/shadcn/card.py`](https://github.com/vstorm-co/charts/blob/main/src/charts/types/shadcn/card.py)

Container component with title, description, content, and footer.

### Example

```python
from charts.types.shadcn.card import Card

card = Card(
    title="Random Space Fact",
    description="A quick, fascinating tidbit about our universe.",
    content="Neutron stars are so dense that a sugar-cube-sized amount of their material would weigh about 1 billion tons on Earth.",
    footer="Source: NASA & astrophysics research summaries"
)
```

## Accordion

**File:** [`src/charts/types/shadcn/accordion.py`](https://github.com/vstorm-co/charts/blob/main/src/charts/types/shadcn/accordion.py)

Collapsible content panels that can be expanded/collapsed.

### Example

```python
from charts.types.shadcn.accordion import Accordion, AccordionItem
from charts.base_types import BaseAccordionTypes

accordion = Accordion(
    items=[
        AccordionItem(
            value="item-1",
            trigger="What is Shadcn UI?",
            content="Shadcn UI is a collection of reusable components built using Radix UI and Tailwind CSS. It provides unstyled, accessible primitives that you can customize to match your design system."
        ),
        AccordionItem(
            value="item-2",
            trigger="Is this accordion accessible?",
            content="Yes. It follows WAI-ARIA accordion patterns, supports keyboard navigation (Tab, Enter, Space, Arrow keys), and is screen-reader friendly when implemented with the underlying Radix UI primitives."
        )
    ],
    list_type=BaseAccordionTypes.single
)
```

## Carousel

**File:** [`src/charts/types/shadcn/carousel.py`](https://github.com/vstorm-co/charts/blob/main/src/charts/types/shadcn/carousel.py)

Scrollable container for cards or text content.

### Example

```python
from charts.types.shadcn.carousel import Carousel, CarouselConfig, CarouselItem
from charts.base_types import CarouselOrientation

config = CarouselConfig(orientation=CarouselOrientation.horizontal)
carousel = Carousel(
    items=[
        CarouselItem(content="Item 1"),
        CarouselItem(content="Item 2"),
    ],
    config=config,
)
```
