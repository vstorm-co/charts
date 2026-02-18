# Accordion Component

The `Accordion` component displays collapsible content panels.

## Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `items` | list[AccordionItem] | Yes | Collection of accordion items |
| `list_type` | 'single' \| 'multiple' | Yes | Expansion mode |

## AccordionItem

Individual panel in the accordion.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `value` | str | Yes | Unique identifier for the item |
| `trigger` | str | Yes | Header text displayed when collapsed |
| `content` | str | Yes | Content displayed when expanded |

## Examples

### Single Expansion Accordion

```python
from charts.types.shadcn.accordion import Accordion, AccordionItem

accordion = Accordion(
    items=[
        AccordionItem(
            value='payment',
            trigger='How do I make a payment?',
            content='Payments can be made using credit card, PayPal, or bank transfer. '
                    'Please visit the billing page to view your options.'
        ),
        AccordionItem(
            value='shipping',
            trigger='What are shipping rates?',
            content='Shipping costs depend on your location and order total. '
                    'Standard shipping is $5.99 for orders under $50.'
        ),
        AccordionItem(
            value='returns',
            trigger='What is your return policy?',
            content='We offer a 30-day money-back guarantee. Items must be '
                    'unopened and in original packaging.'
        )
    ],
    list_type='single'  # Only one item expands at a time
)
```

### Multiple Expansion Accordion

```python
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
        ),
        AccordionItem(
            value='feature3',
            trigger='API access',
            content='Full REST API for programmatic data access.'
        )
    ],
    list_type='multiple'  # Multiple items can be expanded
)
```

### Nested Content

```python
from charts.types.shadcn.card import Card

accordion = Accordion(
    items=[
        AccordionItem(
            value='detailed',
            trigger='View Detailed Statistics',
            content=Card(
                title='Performance Metrics',
                description='Current quarter performance',
                content='CPU: 45% | Memory: 62% | Disk: 38%',
                footer='Updated every 5 minutes'
            )
        )
    ],
    list_type='single'
)
```
