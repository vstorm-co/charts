# Engine Protocol

The `EngineProtocol` defines the interface for component rendering engines.

## EngineProtocol

::: charts.protocol.EngineProtocol
:members:
:show-inheritance:

### Required Methods

#### render_table_component(table: BaseTable) -> str

Transform the Table object into a working component string.

**Parameters:**

- `table` (BaseTable): The table data model

**Returns:** str - Rendered component (TSX or JSON based on return_mode)

#### render_accordion_component(accordion: BaseAccordion) -> str

Transform the Accordion object into a working component string.

**Parameters:**

- `accordion` (BaseAccordion): The accordion data model

**Returns:** str - Rendered component

#### render_card_component(card: BaseCard) -> str

Transform BaseCard object into a working component string.

**Parameters:**

- `card` (BaseCard): The card data model

**Returns:** str - Rendered component

#### render_carousel_component(carousel: BaseCarousel) -> str

Transform BaseCarousel object into a working component string.

**Parameters:**

- `carousel` (BaseCarousel): The carousel data model

**Returns:** str - Rendered component

#### render_chart_component(chart: BaseChart) -> str

Transform BaseChart object into a working component string.

**Parameters:**

- `chart` (BaseChart): The chart data model

**Returns:** str - Rendered component

### Return Modes

Engines support two return modes:

- `"json"` - Returns JSON serialization of the component
- `"tsx"` - Returns fully rendered React/TSX code
