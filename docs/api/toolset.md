# Toolset API

The `FunctionToolset` provides UI component creation tools for AI agents.

## create_ui_toolset()

::: charts.toolset.create_ui_toolset
:members:
:show-inheritance:

```

Create a toolset for chosen engine for component creation.

**Parameters:**
- `id` (str | None): Optional toolset ID

**Returns:** FunctionToolset[EngineDeps] - Toolset with UI component tools

## EngineDeps

Dependencies for the UI translator component creation engine.

::: charts.toolset.EngineDeps
:members:
:show-inheritance:
```

### Attributes

- `engine` (Annotated[EngineProtocol, SkipValidation]): A UI engine to base components on, e.g. `shadcn`
- `id` (str | None): Optional dependency ID

## Tools

The toolset includes the following tools:

### create_table(ctx: RunContext[EngineDeps], table: Table) -> ToolReturn

Create a Table component based on chosen translator engine.

**Parameters:**

- `ctx` (RunContext[EngineDeps]): The run context with engine dependencies
- `table` (Table): The Table model with data and configuration

**Returns:** ToolReturn - Contains the rendered component and metadata

### create_accordion(ctx: RunContext[EngineDeps], accordion: Accordion) -> ToolReturn

Create an Accordion component based on chosen translator engine.

**Parameters:**

- `ctx` (RunContext[EngineDeps]): The run context with engine dependencies
- `accordion` (Accordion): The Accordion model with items and configuration

**Returns:** ToolReturn - Contains the rendered component and metadata

### create_card(ctx: RunContext[EngineDeps], card: Card) -> ToolReturn

Create a Card component based on chosen translator engine.

**Parameters:**

- `ctx` (RunContext[EngineDeps]): The run context with engine dependencies
- `card` (Card): The Card model with title, description, content

**Returns:** ToolReturn - Contains the rendered component and metadata

### create_carousel(ctx: RunContext[EngineDeps], carousel: Carousel) -> ToolReturn

Create a Carousel component based on chosen translator engine.

**Parameters:**

- `ctx` (RunContext[EngineDeps]): The run context with engine dependencies
- `carousel` (Carousel): The Carousel model with items and configuration

**Returns:** ToolReturn - Contains the rendered component and metadata

### create_chart(ctx: RunContext[EngineDeps], chart: Chart) -> ToolReturn

Create a Chart component based on chosen translator engine.

**Parameters:**

- `ctx` (RunContext[EngineDeps]): The run context with engine dependencies
- `chart` (Chart): The Chart model with data and configuration

**Returns:** ToolReturn - Contains the rendered component and metadata

## Example Usage

```python
from pydantic_ai import Agent
from charts.toolset import create_ui_toolset
from charts.engines.shadcn import Shadcn, BaseAgentUIConfig

engine = Shadcn(return_mode='tsx')
toolset = create_ui_toolset(engine)

agent = Agent('openai:gpt-4o', tools=[toolset])

result = await agent.run('Create a bar chart of monthly sales')
print(result.output.return_value)
```
