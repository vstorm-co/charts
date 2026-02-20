# Architecture

Charts follows a layered architecture that separates concerns from abstract definitions to concrete rendering.

## Layered Architecture

```bash
┌─────────────────────────────────────────────────────────────┐
│                    Agent / API Layer                        │
│                       (pydantic-ai )                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Toolset Layer                              │
│           FunctionToolset with create_* tools               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              EngineProtocol (Interface)                     │
│                    render_*(component)                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 Concrete Engine (Shadcn)                    │
│           Implements EngineProtocol with Jinja2 or JSON     │
└─────────────────────────────────────────────────────────────┘
```

## Base Types Layer

Located in [`src/charts/base_types.py`](https://github.com/vstorm-co/charts/blob/main/src/charts/base_types.py)

This layer defines abstract base classes that all components inherit from:

| Class | Purpose |
| ------- | --------- |
| `BaseComponent` | Base class with `component_type` field |
| `BaseTable`, `BaseChart`, `BaseAccordion`, `BaseCard`, `BaseCarousel` | Component base classes |
| `BaseColors`, `BaseColorPalette` | Color configuration |
| `BaseLibraryConfig`, `BaseUIConfig`, `BaseAgentUIConfig` | Configuration hierarchy |

## Types Layer

Located in [`src/charts/types/shadcn/`](https://github.com/vstorm-co/charts/blob/main/src/charts/types/shadcn/)

Concrete Pydantic models that extend base types with:

- **Validation** - Custom validators (e.g., `x_axis_key` must exist in data)
- **Default Values** - Sensible defaults for shadcn components
- **Field Constraints** - Type hints and descriptions

Component models:

- `Table`, `Chart`, `Accordion`, `Card`, `Carousel`

## Engine Layer

The engine converts Pydantic models into rendered output.

### EngineProtocol Interface

Defined in [`src/charts/protocol.py`](https://github.com/vstorm-co/charts/blob/main/src/charts/protocol.py):

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

### Shadcn Engine

Located in [`src/charts/engines/shadcn.py`](https://github.com/vstorm-co/charts/blob/main/src/charts/engines/shadcn.py)

Implements `EngineProtocol` with two return modes:

- **`tsx`** - Returns fully rendered React component code
- **`json`** - Returns JSON serialization of component data

## Template Layer

Located in [`src/charts/templates/shadcn/`](https://github.com/vstorm-co/charts/blob/main/src/charts/templates/shadcn/)

Jinja2 templates that generate React/TypeScript code:

| Template | Generates |
| ---------- | ----------- |
| `table.py` | Table with headers, rows, footer |
| `chart.py` | Bar, Line, Pie, Area, Radar charts |
| `accordion.py` | Collapsible accordion panels |
| `card.py` | Card container with sections |
| `carousel.py` | Horizontal/vertical carousel |

## Data Flow

1. **Agent** calls a tool: `create_chart(chart=Chart(...))`
2. **Toolset** receives the call and passes to engine
3. **Engine** (Shadcn) selects appropriate template
4. **Template** renders TSX using Jinja2 variables from component data
5. **Output** returned as TSX string or JSON
