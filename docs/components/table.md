# Table Component

The `Table` component displays data in a grid format with optional footer calculations.

## Properties

| Property | Type | Required | Description |
| ---------- | ------ | ---------- | ------------- |
| `table_data` | TableData | Yes | Headers and row data |
| `caption` | str | Yes | Table caption |
| `footer` | TableFooter | No | Optional summary row |

## TableFooter

Optional footer for calculations.

| Property | Type | Required | Description |
| ---------- | ------ | ---------- | ------------- |
| `keyword` | str | Yes | Summary label (e.g., "Total", "Estimated") |
| `header_to_summarize` | str | Yes | Column header to calculate |
| `value` | str \| int \| float \| None | No | Pre-calculated value or None |

## Examples

### Basic Table

```python
from charts.types.shadcn.table import Table, TableData

table = Table(
    table_data=TableData(
        headers=['name', 'price', 'stock'],
        rows=[
            ('Product A', 29.99, 100),
            ('Product B', 49.99, 50),
            ('Product C', 19.99, 200),
        ]
    ),
    caption='Product Inventory'
)
```

### Table with Footer Calculation

```python
from charts.types.shadcn.table import Table, TableData, TableFooter

table = Table(
    table_data=TableData(
        headers=['product', 'cost', 'quantity'],
        rows=[
            ('Widget', 10.00, 5),
            ('Gadget', 25.00, 3),
            ('Gizmo', 5.00, 10),
        ]
    ),
    caption='Order Summary',
    footer=TableFooter(
        keyword='Total Items',
        header_to_summarize='quantity',
        value=None
    )
)
```

### Table with Pre-calculated Footer

```python
from charts.types.shadcn.table import Table, TableData, TableFooter

table = Table(
    table_data=TableData(
        headers=['item', 'price'],
        rows=[
            ('Laptop', 999.99),
            ('Mouse', 29.99),
            ('Keyboard', 79.99),
        ]
    ),
    caption='Shopping Cart',
    footer=TableFooter(
        keyword='Total',
        header_to_summarize='price',
        value=1109.97  # Pre-calculated
    )
)
```
