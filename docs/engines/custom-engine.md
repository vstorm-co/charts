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

# Create a custom prompt for the engine
MY_CUSTOM_ENGINE_PROMPT = """..."""

class MyCustomEngine(EngineProtocol):
    """Custom engine for rendering components."""

    name: str = "my-engine"
    return_mode: Literal["json", "tsx"] = "tsx"
    config: BaseAgentUIConfig

    def __init__(self, return_mode: Literal["json", "tsx"] = "tsx"):
        self.return_mode = return_mode
        self.config = BaseAgentUIConfig()

    async def render_table_component(self, table: BaseTable) -> str:
        if self.return_mode == "json":
            return table.model_dump_json()

        # Custom TSX generation
        ...

    async def render_accordion_component(self, accordion: BaseAccordion) -> str:
        if self.return_mode == "json":
            return accordion.model_dump_json()

        # Custom TSX generation
        ...

    async def render_card_component(self, card: BaseCard) -> str:
        if self.return_mode == "json":
            return card.model_dump_json()

        # Custom TSX generation
        ...

    async def render_carousel_component(self, carousel: BaseCarousel) -> str:
        if self.return_mode == "json":
            return carousel.model_dump_json()

        # Custom TSX generation
        ...

    async def render_chart_component(self, chart: BaseChart) -> str:
        if self.return_mode == "json":
            return chart.model_dump_json()

        # Custom TSX generation
        ...
```

## Using Custom Engine

```python
from pydantic_ai import Agent
from charts.toolset import create_ui_toolset, EngineDeps
from charts.utils.helpers import get_ui_component

engine = MyCustomEngine(return_mode='tsx')
toolset = create_ui_toolset()
deps = EngineDeps(engine=engine)

agent = Agent(
    'openai:gpt-5.1',
    retries=3,
    system_prompt=MY_CUSTOM_ENGINE_PROMPT,
    toolsets=[toolset],
    deps_type=EngineDeps
)

# Get the agent to work
result = await agent.run('Create a table', deps=deps)

# Extract component
component = get_ui_component(result)
```

## Key Requirements

1. **Implement all 5 render methods** - Table, Accordion, Card, Carousel, Chart
2. **Handle both return modes** - Return JSON when `return_mode == "json"`
3. **Return strings** - All methods must return string output
4. **Async functions** - Render methods should be async
