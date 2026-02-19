# Carousel Component

The `Carousel` component displays scrollable content horizontally or vertically.

## Properties

| Property | Type | Required | Description |
| ---------- | ------ | ---------- | ------------- |
| `items` | list[CarouselItem] | Yes | Collection of carousel slides |
| `config` | CarouselConfig | Yes | Behavior configuration |

## CarouselConfig

Configuration for carousel behavior.

| Property | Type | Default | Description |
| ---------- | ------ | --------- | ------------- |
| `align` | 'start' \| None | 'start' | Alignment of slides |
| `loop` | 'true' \| 'false' \| None | 'true' | Infinite loop mode |
| `orientation` | CarouselOrientation | horizontal | Scroll direction |
| `container_class` | str \| None | 'max-w-xs' | CSS class for container |

## CarouselItem

Single slide in the carousel.

| Property | Type | Required | Description |
| ---------- | ------ | ---------- | ------------- |
| `content` | str \| Card | Yes | Slide content (text or Card) |

## Examples

### Basic Horizontal Carousel

```python
from charts.types.shadcn.carousel import Carousel, CarouselItem, CarouselConfig
from charts.base_types import CarouselOrientation

carousel = Carousel(
    items=[
        CarouselItem(content='Slide 1: Welcome to our app'),
        CarouselItem(content='Slide 2: Features overview'),
        CarouselItem(content='Slide 3: Getting started guide')
    ],
    config=CarouselConfig(
        align='start',
        loop='true',
        orientation=CarouselOrientation.horizontal
    )
)
```

### Carousel with Card Content

```python
from charts.types.shadcn.carousel import Carousel, CarouselItem, CarouselConfig
from charts.types.shadcn.card import Card

carousel = Carousel(
    items=[
        CarouselItem(content=Card(
            title='Product A',
            description='Premium quality',
            content='$29.99',
            footer='In Stock'
        )),
        CarouselItem(content=Card(
            title='Product B',
            description='Bestseller',
            content='$49.99',
            footer='Limited Offer'
        ))
    ],
    config=CarouselConfig(align='start', loop='true')
)
```
