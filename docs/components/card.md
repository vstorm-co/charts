# Card Component

The `Card` component is a container with title, description, content, and footer sections.

## Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `title` | str | Yes | Card title |
| `description` | str | Yes | Subtitle or description |
| `content` | str \| BaseComponent | No | Main content (text or nested component) |
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

# Create a chart
chart = Chart(
    data=[
        ChartData(month='Jan', sales=400),
        ChartData(month='Feb', sales=300),
        ChartData(month='Mar', sales=600),
    ],
    config=ChartConfig(config={
        'sales': {'label': 'Sales ($)', 'color': '#858586'}
    }),
    metadata=ChartMetadata(title='Sales Trend'),
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

### Card with Multiple Components

```python
from charts.types.shadcn.card import Card
from charts.types.shadcn.table import Table, TableData

table = Table(
    data=[
        TableData(name='Product A', price=29.99),
        TableData(name='Product B', price=49.99),
    ],
    headers=['name', 'price'],
    column_labels={'name': 'Name', 'price': 'Price'},
    caption='Top Products'
)

card = Card(
    title='Top Selling Products',
    description='Best performers this month',
    content=[table, 'Other widgets would go here'],
    footer='Last updated: 2024-03-15'
)
```

### Status Card

```python
card = Card(
    title='Active Users',
    description='Current active session count',
    content='1,234',
    footer= 'Status: Running'
)
```
