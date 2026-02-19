# Engines

The Charts library includes the built-in Shadcn engine for TSX rendering.

## Shadcn Engine

::: charts.engines.shadcn.Shadcn
:members:
:show-inheritance:

### Constructor

```python
Shadcn(
    return_mode: Literal["json", "tsx"],
    config: BaseAgentUIConfig = CONFIG
)
```

**Parameters:**

- `return_mode` ("json" | "tsx"): Output format for rendered components
- `config` (BaseAgentUIConfig): Configuration for component generation

### Methods

#### render_table_component(table: BaseTable) -> str

Transform the Table object into a shadcn component.

#### render_accordion_component(accordion: BaseAccordion) -> str

Transform the Accordion object into a shadcn component.

#### render_card_component(card: BaseCard) -> str

Transform the Card object into a shadcn component.

#### render_carousel_component(carousel: BaseCarousel) -> str

Transform the Carousel object into a shadcn component.

#### render_chart_component(chart: BaseChart) -> str

Transform the Chart object into a shadcn component.

### Supported Chart Types

The Shadcn engine supports these chart types:

- `"bar"` - Bar charts
- `"line"` - Line charts
- `"pie"` - Pie charts
- `"area"` - Area charts
- `"radar"` - Radar charts

## Example Usage

```python
from charts.engines.shadcn import Shadcn
from charts.base_types import BaseAgentUIConfig, BaseUIConfig, BaseColorPalette

# Create config (or use default)
config = BaseAgentUIConfig(
    theme=BaseUIConfig(color_palette=BaseColorPalette()),
)

# Create engine with TSX output
engine = Shadcn(return_mode='tsx', config=config)

# Or use the default config
engine = Shadcn(return_mode='tsx')
```
