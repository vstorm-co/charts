# Engine Protocol

The `EngineProtocol` defines the interface for rendering components to different formats.

## Interface Definition

Located in [`src/charts/protocol.py`](https://github.com/vstorm-co/charts/blob/main/src/charts/protocol.py):

```python
class EngineProtocol(Protocol):
    name: str
    return_mode: Literal["json", "tsx"]
    config: BaseAgentUIConfig

    async def render_table_component(self, table: BaseTable) -> str
    async def render_accordion_component(self, accordion: BaseAccordion) -> str
    async def render_card_component(self, card: BaseCard) -> str
    async def render_carousel_component(self, carousel: BaseCarousel) -> str
    async def render_chart_component(self, chart: BaseChart) -> str
```

## Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | str | Engine identifier (e.g., 'shadcn') |
| `return_mode` | 'json' \| 'tsx' | Output format mode |
| `config` | BaseAgentUIConfig | Agent configuration for rendering |

## Return Modes

### `tsx` Mode

Returns fully rendered React/TypeScript code:

```python
engine = Shadcn(return_mode='tsx')
tsx_code = await engine.render_chart_component(chart)
# Returns: "<BarChart data={...}><XAxis dataKey=\"name\" /></BarChart>"
```

### `json` Mode

Returns JSON serialization of component data:

```python
engine = Shadcn(return_mode='json')
json_data = await engine.render_chart_component(chart)
# Returns: '{"component_type": "chart", "data": [...]}'
```

## Custom Engine Implementation

To create a custom engine, implement `EngineProtocol`:

```python
from typing import Literal
from charts.protocol import EngineProtocol
from charts.base_types import (
    BaseTable, BaseAccordion, BaseCard, BaseCarousel, BaseChart,
    BaseAgentUIConfig
)

class MyCustomEngine(EngineProtocol):
    name = "my-engine"
    return_mode: Literal["json", "tsx"] = "tsx"
    config: BaseAgentUIConfig

    async def render_table_component(self, table: BaseTable) -> str:
        # Implementation here
        return "<MyTableComponent />"

    async def render_accordion_component(self, accordion: BaseAccordion) -> str:
        # Implementation here
        return "<MyAccordionComponent />"

    async def render_card_component(self, card: BaseCard) -> str:
        # Implementation here
        return "<MyCardComponent />"

    async def render_carousel_component(self, carousel: BaseCarousel) -> str:
        # Implementation here
        return "<MyCarouselComponent />"

    async def render_chart_component(self, chart: BaseChart) -> str:
        # Implementation here
        return "<MyChartComponent />"
```

## Built-in Engine

The `Shadcn` engine is the built-in implementation located in
[`src/charts/engines/shadcn.py`](https://github.com/vstorm-co/charts/blob/main/src/charts/engines/shadcn.py).

It uses Jinja2 templates to generate React components with shadcn/ui styling.
