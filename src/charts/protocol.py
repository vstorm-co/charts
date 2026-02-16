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
    name: str
    return_mode: Literal["json", "tsx"]
    config: BaseAgentUIConfig

    async def render_table_component(self, table: BaseTable) -> str:
        """Transform the BaseTable object into a working component string."""
        ...

    async def render_accordion_component(self, accordion: BaseAccordion) -> str:
        """Transform the BaseAccordion object into a working component string."""
        ...

    async def render_card_component(self, card: BaseCard) -> str:
        """Transform BaseCard object into a working component string."""
        ...

    async def render_carousel_component(self, carousel: BaseCarousel) -> str:
        """Transform BaseCarousel object into a working component string."""
        ...

    async def render_chart_component(self, chart: BaseChart) -> str:
        """Transform BaseChart object into a working component string."""
        ...
