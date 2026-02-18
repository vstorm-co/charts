# Table Component

The `Table` component displays data in a grid format with optional footer calculations.

## Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `data` | list[TableData] | Yes | Row data as dictionaries |
| `headers` | list[str] | Yes | Column header names (keys) |
| `column_labels` | dict | No | Human-readable column names |
| `caption` | str | Yes | Table caption |
| `footer` | TableFooter | No | Optional summary row |

## TableFooter

Optional footer for calculations.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `keyword` | str | Yes | Summary label (e.g., "Total", "Estimated") |
| `header_to_summarize` | str | Yes | Column header to calculate |
| `value` | int \| float \| None | No | Pre-calculated value or None |

## Examples

### Basic Table

```python
from charts.types.shadcn.table import Table, TableData

table = Table(
    data=[
        TableData(name='Product A', price=29.99, stock=100),
        TableData(name='Product B', price=49.99, stock=50),
        TableData(name='Product C', price=19.99, stock=200),
    ],
    headers=['name', 'price', 'stock'],
    column_labels={
        'name': 'Product Name',
        'price': 'Price ($)',
        'stock': 'Stock'
    },
    caption='Product Inventory'
)
```

### Table with Footer Calculation

```python
from charts.types.shadcn.table import Table, TableData, TableFooter

table = Table(
    data=[
        TableData(product='Widget', cost=10.00, quantity=5),
        TableData(product='Gadget', cost=25.00, quantity=3),
        TableData(product='Gizmo', cost=5.00, quantity=10),
    ],
    headers=['product', 'cost', 'quantity'],
    column_labels={'product': 'Product', 'cost': 'Cost', 'quantity': 'Qty'},
    caption='Order Summary',
    footer=TableFooter(
        keyword='Total Items',
        header_to_summarize='quantity',
        value=None  # Calculated automatically
    )
)
```

### Table with Pre-calculated Footer

```python
table = Table(
    data=[
        TableData(item='Laptop', price=999.99),
        TableData(item='Mouse', price=29.99),
        TableData(item='Keyboard', price=79.99),
    ],
    headers=['item', 'price'],
    column_labels={'item': 'Item', 'price': 'Price'},
    caption='Shopping Cart',
    footer=TableFooter(
        keyword='Total',
        header_to_summarize='price',
        value=1109.97  # Pre-calculated
    )
)
```
