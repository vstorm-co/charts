"""Pydantic AI toolset for AI agents used to create and stylize UI components."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, SkipValidation
from pydantic_ai import FunctionToolset, RunContext, ToolReturn

from charts.protocol import EngineProtocol
from charts.types.shadcn.accordion import Accordion
from charts.types.shadcn.card import Card
from charts.types.shadcn.carousel import Carousel
from charts.types.shadcn.chart import Chart
from charts.types.shadcn.table import Table

SHADCN_TOOLSET_PROMPT = """
You are an expert UI/UX developer using the Shadcn UI library.
Your goal is to create beautiful, functional, and accessible components
based on user requirements.

You have access to tools that render components using a specific engine.

When asked to create a UI element:
1. Gather or generate the necessary data for the component.
2. Structure the data according to the component's model (Table, Chart, Card, etc.).
3. Call the appropriate rendering tool (e.g., `create_table`, `create_chart`)
to get the final React component code.

Always aim for high-quality data and sensible defaults for colors and labels.
"""


class EngineDeps(BaseModel):
    """Dependencies for the UI translator component creation engine.

    Attributes:
        engine: A UI engine to base components on, e.g. `shadcn`
        id: Optional dependency ID

    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    engine: Annotated[EngineProtocol, SkipValidation]
    id: str | None = None


def create_ui_toolset(*, id: str | None = None) -> FunctionToolset[EngineDeps]:
    """Create a toolset for chosen engine for component creation.

    Args:
        id: Optional toolset ID.

    Returns:
        FunctionToolset with UI component tools.

    """
    toolset = FunctionToolset[EngineDeps](id=id)

    # Table
    @toolset.tool
    async def create_table(ctx: RunContext[EngineDeps], table: Table) -> ToolReturn:
        """Create a Table component based on chosen translator engine."""
        component = await ctx.deps.engine.render_table_component(table)

        return ToolReturn(
            return_value=f"Successfully created table: {table.caption}",
            metadata={
                "ui_element": component,
                "component_type": table.component_type,
                "data_summary": {"rows": len(table.table_data.rows)},
            },
        )

    # Accordion
    @toolset.tool
    async def create_accordion(ctx: RunContext[EngineDeps], accordion: Accordion) -> ToolReturn:
        """Create an Accordion component based on chosen translator engine."""
        component = await ctx.deps.engine.render_accordion_component(accordion)

        return ToolReturn(
            return_value=f"Successfully created an accordion with {len(accordion.items)} items",
            metadata={
                "ui_element": component,
                "component_type": accordion.component_type,
                "data_summary": {"num_elements": len(accordion.items)},
            },
        )

    # Card
    @toolset.tool
    async def create_card(ctx: RunContext[EngineDeps], card: Card) -> ToolReturn:
        """Create a Card component based on chosen translator engine."""
        component = await ctx.deps.engine.render_card_component(card)

        return ToolReturn(
            return_value=f"Successfully created card component with title: {card.title}",
            metadata={
                "ui_element": component,
                "component_type": card.component_type,
                "data_summary": {"content_type": f"{type(card.content)}"},
            },
        )

    # Carousel
    @toolset.tool
    async def create_carousel(ctx: RunContext[EngineDeps], carousel: Carousel) -> ToolReturn:
        """Create a Carousel component based on chosen translator engine."""
        component = await ctx.deps.engine.render_carousel_component(carousel)

        return ToolReturn(
            return_value=(
                f"""Successfully created carousel component
                with {len(carousel.items)} elements."""
            ),
            metadata={
                "ui_element": component,
                "component_type": carousel.component_type,
                "data_summary": {"num_elements": len(carousel.items)},
            },
        )

    # Chart
    @toolset.tool
    async def create_chart(ctx: RunContext[EngineDeps], chart: Chart) -> ToolReturn:
        """Create a Chart component based on chosen translator engine."""
        component = await ctx.deps.engine.render_chart_component(chart)

        return ToolReturn(
            return_value=f"Successfully created chart: {chart.metadata.title}",
            metadata={
                "ui_element": component,
                "component_type": chart.component_type,
                "data_summary": {"num_elements": (len(chart.chart_data.data))},
            },
        )

    return toolset
