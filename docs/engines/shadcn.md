# Shadcn Engine

The built-in engine for rendering components to React/TSX code.

## Overview

Located in [`src/charts/engines/shadcn.py`](https://github.com/vstorm-co/charts/blob/main/src/charts/engines/shadcn.py).

The `Shadcn` class implements the `EngineProtocol` and uses Jinja2 templates to generate React components with shadcn/ui styling.

## Initialization

```python
from charts.engines.shadcn import Shadcn
from charts.engines.shadcn.config import ShadcnAgentUIConfig

# Basic usage - defaults to tsx mode
engine = Shadcn(return_mode='tsx')

# With custom configuration
config = ShadcnAgentUIConfig()
engine = Shadcn(return_mode='tsx', config=config)

# JSON mode for data-only output
engine_json = Shadcn(return_mode='json')
```

## Methods

### render_table_component(table: BaseTable) -> str

Renders a Table component to TSX or JSON.

```python
tsx = await engine.render_table_component(table)
```

### render_accordion_component(accordion: BaseAccordion) -> str

Renders an Accordion component to TSX or JSON.

```python
tsx = await engine.render_accordion_component(accordion)
```

### render_card_component(card: BaseCard) -> str

Renders a Card component to TSX or JSON.

```python
tsx = await engine.render_card_component(card)
```

### render_carousel_component(carousel: BaseCarousel) -> str

Renders a Carousel component to TSX or JSON.

```python
tsx = await engine.render_carousel_component(carousel)
```

### render_chart_component(chart: BaseChart) -> str

Renders a Chart component to TSX or JSON. Supports all chart types (bar, line, pie, area, radar).

```python
tsx = await engine.render_chart_component(chart)
```

## Return Modes

### tsx Mode (default)

Returns fully rendered React/TypeScript code:

```python
engine = Shadcn(return_mode='tsx')
result = await engine.render_chart_component(chart)
# Returns: "<BarChart data={...}><XAxis dataKey=\"name\" /></BarChart>"
```

### json Mode

Returns JSON serialization of component data:

```python
engine = Shadcn(return_mode='json')
result = await engine.render_chart_component(chart)
# Returns: '{"component_type": "chart", "data": [...]}'
```

## Chart Templates

The engine includes templates for:

| Template | Variable |
|----------|----------|
| Bar Chart | `SHADCN_BAR_CHART_TEMPLATE` |
| Line Chart | `SHADCN_LINE_CHART_TEMPLATE` |
| Pie Chart | `SHADCN_PIE_CHART_TEMPLATE` |
| Area Chart | `SHADCN_AREA_CHART_TEMPLATE` |
| Radar Chart | `SHADCN_RADAR_CHART_TEMPLATE` |

## Custom Engine Example

To create a custom engine, implement the same interface:

```python
from charts.protocol import EngineProtocol
from charts.base_types import BaseTable, BaseChart, BaseAgentUIConfig

class MyEngine(EngineProtocol):
    name = "my-engine"
    return_mode: Literal["json", "tsx"] = "tsx"
    config: BaseAgentUIConfig

    async def render_table_component(self, table: BaseTable) -> str:
        # Custom implementation
        pass

    async def render_chart_component(self, chart: BaseChart) -> str:
        # Custom implementation
        pass
```
