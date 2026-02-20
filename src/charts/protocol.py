"""Engine Protocol for UI component rendering.

This module defines the EngineProtocol interface that all rendering engines must implement.
Engines transform Pydantic model objects (Chart, Table, Card, etc.) into target format
code (TSX/React or JSON).

The protocol ensures consistent component generation across different frontend frameworks
and styling systems while maintaining type safety through Pydantic models.

Example:
    ```python
    from charts.protocol import EngineProtocol
    from charts.engines.shadcn import Shadcn

    engine: EngineProtocol = Shadcn(return_mode="tsx")
    tsx_code = await engine.render_chart_component(chart)
    ```
"""

from typing import Literal, Protocol

from charts.base_types import (
    BaseAccordion,
    BaseAgentUIConfig,
    BaseCard,
    BaseCarousel,
    BaseChart,
    BaseTable,
)


class EngineProtocol(Protocol):
    """Interface contract for UI rendering engines.

    All engine implementations must provide methods to convert base component
    types into target format code (TSX/React or JSON data).

    Attributes:
        name: Unique engine identifier
        return_mode: Default output format ("json" or "tsx")
        config: Agent UI configuration for rendering options

    Methods:
        render_table_component: Convert Table model to component string
        render_accordion_component: Convert Accordion model to component string
        render_card_component: Convert Card model to component string
        render_carousel_component: Convert Carousel model to component string
        render_chart_component: Convert Chart model to component string
    """

    name: str
    return_mode: Literal["json", "tsx"]
    config: BaseAgentUIConfig

    async def render_table_component(self, table: BaseTable) -> str:
        """Transform the BaseTable object into a working component string.

        Args:
            table: The Table model containing data, caption, and optional footer.

        Returns:
            TSX/React code or JSON string depending on engine return_mode.
        """
        ...

    async def render_accordion_component(self, accordion: BaseAccordion) -> str:
        """Transform the BaseAccordion object into a working component string.

        Args:
            accordion: The Accordion model with items and list_type configuration.

        Returns:
            TSX/React code or JSON string depending on engine return_mode.
        """
        ...

    async def render_card_component(self, card: BaseCard) -> str:
        """Transform BaseCard object into a working component string.

        Args:
            card: The Card model with title, description, content, and footer.

        Returns:
            TSX/React code or JSON string depending on engine return_mode.
        """
        ...

    async def render_carousel_component(self, carousel: BaseCarousel) -> str:
        """Transform BaseCarousel object into a working component string.

        Args:
            carousel: The Carousel model with items and configuration.

        Returns:
            TSX/React code or JSON string depending on engine return_mode.
        """
        ...

    async def render_chart_component(self, chart: BaseChart) -> str:
        """Transform BaseChart object into a working component string.

        Args:
            chart: The Chart model with data, config, metadata, and axis configuration.

        Returns:
            TSX/React code or JSON string depending on engine return_mode.
        """
        ...
