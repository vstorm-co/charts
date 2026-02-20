# Card Component

The `Card` component is a container with title, description, content, and footer sections.

## Properties

| Property | Type | Required | Description |
| ---------- | ------ | ---------- | ------------- |
| `title` | str | Yes | Card title |
| `description` | str | Yes | Subtitle or description |
| `content` | str \| BaseComponent \| list[BaseComponent] | No | Main content |
| `footer` | str | Yes | Footer text |

## Examples

### Simple Text Card

```python
from charts.types.shadcn.card import Card

card = Card(
    title='Revenue',
    description='Total sales this quarter',
    content='$125,430',
    footer='Updated today at 10:30 AM'
)
```

### Nested Chart in Card

```python
from charts.types.shadcn.card import Card
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData, ChartMetadata
from charts.base_types import BaseChartTypes

# Create a chart
chart = Chart(
    chart_data=ChartData(data=[
        {"month": "Jan", "sales": 400},
        {"month": "Feb", "sales": 300},
        {"month": "Mar", "sales": 600},
    ]),
    chart_config=ChartConfig(config={
        'sales': {'label': 'Sales ($)', 'color': '#858586'}
    }),
    metadata=ChartMetadata(title='Sales Trend'),
    chart_type=BaseChartTypes.line,
    x_axis_key='month'
)

# Use it in a card
card = Card(
    title='Sales Performance',
    description='Quarterly sales overview',
    content=chart,
    footer='Source: Sales Database'
)
```
