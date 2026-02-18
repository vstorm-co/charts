# Shadcn Types

Concrete Pydantic models for shadcn component definitions.

## Chart Types

### ChartMetadata

::: charts.types.shadcn.ChartMetadata
:members:
:show-inheritance:

```

Metadata for given chart, containing elements like title, subtitle, description and others.

### ChartConfig

::: charts.types.shadcn.ChartConfig
:members:
:show-inheritance:
```

Config for a chart. Maps data keys to labels and colors.

**Example (Bar/Line/Area/Radar):**

```python
{
    "desktop": {"label": "Desktop", "color": "#2563eb"},
    "mobile": {"label": "Mobile", "color": "#60a5fa"}
}
```

**Example (Pie):**

```python
{
    "chrome": {"label": "Chrome", "color": "var(--chart-1)"},
    "safari": {"label": "Safari", "color": "var(--chart-2)"}
}
```

### ChartData

::: charts.types.shadcn.ChartData
:members:
:show-inheritance:

```

The actual data points for the chart.

**Example (Bar/Line/Area/Radar):**
```python
[
    {"month": "Jan", "desktop": 100, "mobile": 80},
    {"month": "Feb", "desktop": 120, "mobile": 90}
]
```

**Example (Pie):**

```python
[
    {"category": "Chrome", "value": 275},
    {"category": "Safari", "value": 200}
]
```

### Chart

::: charts.types.shadcn.Chart
:members:
:show-inheritance:

```

Basic object to store various charts for component rendering.

**Validation:**
- Ensures x_axis_key exists in the data keys

## Table Types

### TableFooter

::: charts.types.shadcn.TableFooter
:members:
:show-inheritance:
```

Footer configuration for tables with calculation support.

**Attributes:**

- `keyword` (str): Summarizing keyword like 'Total', 'Estimated'
- `header_to_summarize` (str): The header to perform calculation on
- `value` (str | int | float | None): Optional pre-calculated value

### Table

::: charts.types.shadcn.Table
:members:
:show-inheritance:

```

Table component model with headers, rows, and optional footer.

## Accordion Types

### AccordionItem

::: charts.types.shadcn.AccordionItem
:members:
:show-inheritance:
```

Individual accordion item with trigger and content.

**Attributes:**

- `value` (str): Identifier of the field
- `trigger` (str): Header of an accordion element
- `content` (str): Content of the accordion element

### Accordion

::: charts.types.shadcn.Accordion
:members:
:show-inheritance:

```

Accordion component with multiple expandable items.

## Card Types

### Card

::: charts.types.shadcn.Card
:members:
:show-inheritance:
```

Card component with title, description, content, and footer.

## Carousel Types

### CarouselItem

::: charts.types.shadcn.CarouselItem
:members:
:show-inheritance:

```

Individual carousel item with content.

**Attributes:**
- `content` (str | BaseCard): Content of the carousel element

### CarouselConfig

::: charts.types.shadcn.CarouselConfig
:members:
:show-inheritance:
```

Configuration for carousel component.

**Attributes:**

- `align` ("start" | None): Alignment setting
- `loop` ("true" | "false" | None): Loop mode
- `orientation` (CarouselOrientation): Orientation ("horizontal" | "vertical")
- `container_class` (str | None): CSS class for container

### Carousel

::: charts.types.shadcn.Carousel
:members:
:show-inheritance:

```

Carousel component with multiple items and configuration.
