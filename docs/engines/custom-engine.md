# Custom Engine

Create your own engine to render components for different targets.

## Overview

To create a custom engine, implement the `EngineProtocol` interface.

## Implementation

```python
from typing import Literal
from pydantic import BaseModel
from charts.protocol import EngineProtocol
from charts.base_types import (
    BaseTable, BaseAccordion, BaseCard,
    BaseCarousel, BaseChart, BaseAgentUIConfig
)

class MyCustomEngine(EngineProtocol):
    """Custom engine for rendering components."""

    name: str = "my-engine"
    return_mode: Literal["json", "tsx"] = "tsx"
    config: BaseAgentUIConfig

    def __init__(self, return_mode: Literal["json", "tsx"] = "tsx"):
        self.return_mode = return_mode
        self.config = BaseAgentUIConfig(
            theme=type('Theme', (), {'mode': 'light'})(),
            lib=type('Lib', (), {})()
        )

    async def render_table_component(self, table: BaseTable) -> str:
        if self.return_mode == "json":
            return table.model_dump_json()

        # Custom TSX generation
        headers = ", ".join(table.table_data.headers)
        rows_count = len(table.table_data.rows)

        return f"""
        <MyTable caption="{table.caption}">
            <thead><tr>{headers}</tr></thead>
            <tbody>{rows_count} rows</tbody>
        </MyTable>
        """

    async def render_accordion_component(self, accordion: BaseAccordion) -> str:
        if self.return_mode == "json":
            return accordion.model_dump_json()

        return f"<MyAccordion items={len(accordion.items)} />"

    async def render_card_component(self, card: BaseCard) -> str:
        if self.return_mode == "json":
            return card.model_dump_json()

        return f'<MyCard title="{card.title}" />'

    async def render_carousel_component(self, carousel: BaseCarousel) -> str:
        if self.return_mode == "json":
            return carousel.model_dump_json()

        return f"<MyCarousel items={len(carousel.items)} />"

    async def render_chart_component(self, chart: BaseChart) -> str:
        if self.return_mode == "json":
            return chart.model_dump_json()

        return f'<MyChart type="{chart.chart_type}" />'
```

## Using Custom Engine

```python
from pydantic_ai import Agent
from charts.toolset import create_ui_toolset

engine = MyCustomEngine(return_mode='tsx')

agent = Agent(
    'openai:gpt-5.1',
    tools=create_ui_toolset(engine)
)

result = await agent.run('Create a table')
```

## Key Requirements

1. **Implement all 5 render methods** - Table, Accordion, Card, Carousel, Chart
2. **Handle both return modes** - Return JSON when `return_mode == "json"`
3. **Return strings** - All methods must return string output
4. **Async functions** - Render methods should be async

## Integration with pydantic-ai

The engine works seamlessly with pydantic-ai agents:

```python
agent = Agent(
    'openai:gpt-5.1',
    tools=create_ui_toolset(MyCustomEngine())
)

# Agent will automatically use your custom engine
result = await agent.run('Generate a dashboard with components')
```
