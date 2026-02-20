# Component Combinations

Create dashboards and layouts with multiple components.

## Dashboard Layout

Combine chart, table, and cards for a complete dashboard:

```python
from charts.engines.shadcn import Shadcn
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData, ChartMetadata
from charts.types.shadcn.table import Table, TableData
from charts.types.shadcn.card import Card
from charts.base_types import BaseChartTypes

engine = Shadcn(return_mode='tsx')

# 1. Create chart component
chart = Chart(
    chart_type=BaseChartTypes.bar,
    metadata=ChartMetadata(title="Monthly Sales"),
    chart_data=ChartData(data=[
        {"month": "Jan", "sales": 1200},
        {"month": "Feb", "sales": 1900},
        {"month": "Mar", "sales": 1500},
    ]),
    chart_config=ChartConfig(config={"sales": {"label": "Sales ($)", "color": "#10b981"}}),
    x_axis_key="month"
)

# 2. Create summary cards
cards = [
    Card(title="Total Sales", description="Q1 summary", content="$4,600", footer="+15% from last quarter"),
    Card(title="New Customers", description="Growth", content="89", footer="+8% from last quarter"),
]

# 3. Create data table
table = Table(
    caption="Product Sales Details",
    table_data=TableData(
        headers=["Product", "Sales", "Margin"],
        rows=[
            ("Widget A", 450, "24%"),
            ("Widget B", 380, "18%"),
        ]
    )
)

# 4. Render all components (async context required)
# tsx_chart = await engine.render_chart_component(chart)
# tsx_table = await engine.render_table_component(table)
# tsx_cards = [await engine.render_card_component(card) for card in cards]
```
