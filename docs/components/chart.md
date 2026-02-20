# Chart Component

The `Chart` component generates interactive charts using Recharts library.

## Properties

| Property | Type | Required | Description |
| ---------- | ------ | ---------- | ------------- |
| `chart_data` | ChartData | Yes | Object containing data points for the chart |
| `chart_config` | ChartConfig | Yes | Configuration for keys, labels, and colors |
| `metadata` | ChartMetadata | No | Title, subtitle, description |
| `chart_type` | BaseChartTypes | Yes | Type of chart (bar, line, pie, etc.) |
| `x_axis_key` | str | Yes | Key used for the x-axis labels |

## ChartConfig

Configuration that maps data keys to visual properties.

| Property | Type | Description |
| ---------- | ------ | ------------- |
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
| ------ | ---------- |
| `bar` | Comparing values across categories |
| `line` | Showing trends over time |
| `pie` | Displaying proportions |
| `area` | Cumulative data visualization |
| `radar` | Multivariate data comparison |

## Examples

### Basic Bar Chart

```python
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData, ChartMetadata
from charts.base_types import BaseChartTypes

chart = Chart(
    chart_data=ChartData(data=[
        {"month": "Jan", "sales": 400},
        {"month": "Feb", "sales": 300},
        {"month": "Mar", "sales": 600},
    ]),
    chart_config=ChartConfig(config={
        'sales': {'label': 'Sales ($)', 'color': '#858586'}
    }),
    metadata=ChartMetadata(title='Monthly Sales'),
    chart_type=BaseChartTypes.bar,
    x_axis_key='month'
)
```

### Multi-Series Line Chart

```python
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData, ChartMetadata
from charts.base_types import BaseChartTypes

chart = Chart(
    chart_data=ChartData(data=[
        {"month": "Jan", "desktop": 100, "mobile": 80},
        {"month": "Feb", "desktop": 120, "mobile": 90},
        {"month": "Mar", "desktop": 150, "mobile": 110},
    ]),
    chart_config=ChartConfig(config={
        'desktop': {'label': 'Desktop Users', 'color': '#2563eb'},
        'mobile': {'label': 'Mobile Users', 'color': '#60a5fa'}
    }),
    metadata=ChartMetadata(
        title='User Analytics',
        subtitle='Active users by device type'
    ),
    chart_type=BaseChartTypes.line,
    x_axis_key='month'
)
```

### Pie Chart

```python
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData, ChartMetadata
from charts.base_types import BaseChartTypes

chart = Chart(
    chart_data=ChartData(data=[
        {"browser": "Chrome", "visitors": 275},
        {"browser": "Safari", "visitors": 200},
        {"browser": "Firefox", "visitors": 180},
    ]),
    chart_config=ChartConfig(config={
        'Chrome': {'label': 'Chrome', 'color': 'var(--chart-1)'},
        'Safari': {'label': 'Safari', 'color': 'var(--chart-2)'},
        'Firefox': {'label': 'Firefox', 'color': 'var(--chart-3)'}
    }),
    metadata=ChartMetadata(title='Browser Usage'),
    chart_type=BaseChartTypes.pie,
    x_axis_key='browser'
)
```
