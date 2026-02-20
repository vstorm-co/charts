# Shadcn Engine

The built-in engine for rendering components to React/TSX code.

## Overview

Located in [`src/charts/engines/shadcn.py`](https://github.com/vstorm-co/charts/blob/main/src/charts/engines/shadcn.py).

The `Shadcn` class implements the `EngineProtocol` and uses Jinja2 templates to generate React components with shadcn/ui styling.

## Initialization

```python
from charts.engines.shadcn import Shadcn
from charts.engines.shadcn.config import ShadcnAgentUIConfig

# Basic usage - tsx mode
engine = Shadcn(return_mode='tsx')

# With custom configuration
config = ShadcnAgentUIConfig()
engine = Shadcn(return_mode='tsx', config=config)

# JSON mode for data-only output
engine_json = Shadcn(return_mode='json')
```

## Chart Templates

The engine includes templates for:

| Template | Variable |
| ---------- | ---------- |
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
