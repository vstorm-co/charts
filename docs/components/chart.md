# Chart Component

The `Chart` component generates interactive charts using Recharts library.

## Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `data` | list[ChartData] | Yes | Array of data points for the chart |
| `config` | ChartConfig | Yes | Configuration for keys, labels, and colors |
| `metadata` | ChartMetadata | No | Title, subtitle, description |
| `x_axis_key` | str | Yes | Key used for the x-axis labels |

## ChartConfig

Configuration that maps data keys to visual properties.

| Property | Type | Description |
|----------|------|-------------|
| `config` | dict[str, dict] | Maps column names to {label, color} |

### Bar/Line/Area/Radar Config Example
```python
{
    "desktop": {"label": "Desktop", "color": "#2563eb"},
    "mobile": {"label": "Mobile", "color": "#60a5fa"}
}
```

### Pie Chart Config Example
```python
{
    "chrome": {"label": "Chrome", "color": "var(--chart-1)"},
    "safari": {"label": "Safari", "color": "var(--chart-2)"}
}
```

## Supported Chart Types

| Type | Use Case |
|------|----------|
| `bar` | Comparing values across categories |
| `line` | Showing trends over time |
| `pie` | Displaying proportions |
| `area` | Cumulative data visualization |
| `radar` | Multivariate data comparison |

## Examples

### Basic Bar Chart

```python
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData, ChartMetadata

chart = Chart(
    data=[
        ChartData(month='Jan', sales=400),
        ChartData(month='Feb', sales=300),
        ChartData(month='Mar', sales=600),
    ],
    config=ChartConfig(config={
        'sales': {'label': 'Sales ($)', 'color': '#858586'}
    }),
    metadata=ChartMetadata(title='Monthly Sales'),
    x_axis_key='month'
)
```

### Multi-Series Line Chart

```python
chart = Chart(
    data=[
        ChartData(month='Jan', desktop=100, mobile=80),
        ChartData(month='Feb', desktop=120, mobile=90),
        ChartData(month='Mar', desktop=150, mobile=110),
    ],
    config=ChartConfig(config={
        'desktop': {'label': 'Desktop Users', 'color': '#2563eb'},
        'mobile': {'label': 'Mobile Users', 'color': '#60a5fa'}
    }),
    metadata=ChartMetadata(
        title='User Analytics',
        subtitle='Active users by device type'
    ),
    x_axis_key='month'
)
```

### Pie Chart

```python
chart = Chart(
    data=[
        ChartData(browser='Chrome', value=275),
        ChartData(browser='Safari', value=200),
        ChartData(browser='Firefox', value=180),
    ],
    config=ChartConfig(config={
        'Chrome': {'label': 'Chrome', 'color': 'var(--chart-1)'},
        'Safari': {'label': 'Safari', 'color': 'var(--chart-2)'},
        'Firefox': {'label': 'Firefox', 'color': 'var(--chart-3)'}
    }),
    metadata=ChartMetadata(title='Browser Usage'),
    x_axis_key='browser'
)
```
