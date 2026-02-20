# Accordion Component

The `Accordion` component displays collapsible content panels.

## Properties

| Property | Type | Required | Description |
| ---------- | ------ | ---------- | ------------- |
| `items` | list[AccordionItem] | Yes | Collection of accordion items |
| `list_type` | BaseAccordionTypes | Yes | Expansion mode (single or multiple) |

## AccordionItem

Individual panel in the accordion.

| Property | Type | Required | Description |
| ---------- | ------ | ---------- | ------------- |
| `value` | str | Yes | Unique identifier for the item |
| `trigger` | str | Yes | Header text displayed when collapsed |
| `content` | str | Yes | Content displayed when expanded |

## Examples

### Single Expansion Accordion

```python
from charts.types.shadcn.accordion import Accordion, AccordionItem
from charts.base_types import BaseAccordionTypes

accordion = Accordion(
    items=[
        AccordionItem(
            value='payment',
            trigger='How do I make a payment?',
            content='Payments can be made using credit card, PayPal, or bank transfer.'
        ),
        AccordionItem(
            value='shipping',
            trigger='What are shipping rates?',
            content='Shipping costs depend on your location and order total.'
        )
    ],
    list_type=BaseAccordionTypes.single
)
```

### Multiple Expansion Accordion

```python
from charts.types.shadcn.accordion import Accordion, AccordionItem
from charts.base_types import BaseAccordionTypes

accordion = Accordion(
    items=[
        AccordionItem(
            value='feature1',
            trigger='Real-time analytics',
            content='View your data as it arrives with sub-second latency.'
        ),
        AccordionItem(
            value='feature2',
            trigger='Export capabilities',
            content='Export reports to PDF, CSV, or JSON formats.'
        )
    ],
    list_type=BaseAccordionTypes.multiple
)
```
