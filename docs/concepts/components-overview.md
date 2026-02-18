# Component Overview

Charts supports five component types for generating React UI elements.

## Chart

**File:** [`src/charts/types/shadcn/chart.py`](https://github.com/vstorm-co/charts/blob/main/src/charts/types/shadcn/chart.py)

Generates interactive charts using Recharts library.

### Chart Types

| Type | Use Case |
|------|----------|
| `bar` | Comparing values across categories |
| `line` | Showing trends over time |
| `pie` | Displaying proportions |
| `area` | Cumulative data visualization |
| `radar` | Multivariate data comparison |

### Example

```python
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData

chart = Chart(
    data=[
        ChartData(name='Jan', sales=400),
        ChartData(name='Feb', sales=300),
    ],
    config=ChartConfig(
        type='bar',
        x_key='name',
        y_keys=['sales'],
        title='Monthly Sales'
    )
)
```

## Table

**File:** [`src/charts/types/shadcn/table.py`](https://github.com/vstorm-co/charts/blob/main/src/charts/types/shadcn/table.py)

Displays data in a grid format with optional footer calculations.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `data` | list[TableData] | Row data as dictionaries |
| `headers` | list[str] | Column header names |
| `column_labels` | dict | Human-readable column names |
| `caption` | str | Table caption |
| `footer` | TableFooter | Optional summary row |

### Example

```python
from charts.types.shadcn.table import Table, TableData

table = Table(
    data=[
        TableData(name='Product A', price=29.99, stock=100),
        TableData(name='Product B', price=49.99, stock=50),
    ],
    headers=['name', 'price', 'stock'],
    column_labels={'name': 'Name', 'price': 'Price ($)', 'stock': 'Stock'},
    caption='Product Inventory'
)
```

## Card

**File:** [`src/charts/types/shadcn/card.py`](https://github.com/vstorm-co/charts/blob/main/src/charts/types/shadcn/card.py)

Container component with title, description, content, and footer.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `title` | str | Card title |
| `description` | str | Subtitle/description |
| `content` | str \| BaseComponent | Main content (text or nested component) |
| `footer` | str | Footer text |

### Example

```python
from charts.types.shadcn.card import Card

card = Card(
    title='Revenue',
    description='Total sales this quarter',
    content='$125,430',
    footer='Updated today at 10:30 AM'
)
```

## Accordion

**File:** [`src/charts/types/shadcn/accordion.py`](https://github.com/vstorm-co/charts/blob/main/src/charts/types/shadcn/accordion.py)

Collapsible content panels that can be expanded/collapsed.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `items` | list[AccordionItem] | Accordion panel items |
| `list_type` | 'single' \| 'multiple' | Single or multiple expansion |

### AccordionItem Properties

| Property | Type | Description |
|----------|------|-------------|
| `value` | str | Unique identifier |
| `trigger` | str | Header text |
| `content` | str | Expandable content |

### Example

```python
from charts.types.shadcn.accordion import Accordion, AccordionItem

accordion = Accordion(
    items=[
        AccordionItem(value='item1', trigger='Section 1', content='Content for section 1'),
        AccordionItem(value='item2', trigger='Section 2', content='Content for section 2'),
    ],
    list_type='single'
)
```

## Carousel

**File:** [`src/charts/types/shadcn/carousel.py`](https://github.com/vstorm-co/charts/blob/main/src/charts/types/shadcn/carousel.py)

Scrollable container for cards or text content.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `items` | list[CarouselItem] | Carousel slide items |
| `config` | CarouselConfig | Carousel behavior settings |

### CarouselConfig Properties

| Property | Type | Description |
|----------|------|-------------|
| `align` | 'start' | Alignment of slides |
| `loop` | 'true' \| 'false' | Infinite loop mode |
| `orientation` | 'horizontal' \| 'vertical' | Scroll direction |

### Example

```python
from charts.types.shadcn.carousel import Carousel, CarouselItem, CarouselConfig
from charts.types.shadcn.card import Card

card = Card(title='Slide 1', description='First slide', content='Content', footer='Footer')

carousel = Carousel(
    items=[CarouselItem(content=card)],
    config=CarouselConfig(align='start', loop='true', orientation='horizontal')
)
```
