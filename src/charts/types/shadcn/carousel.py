import json
from enum import Enum
from typing import Any, Literal

from pydantic import Field, field_validator, model_validator
from typing_extensions import Self

from charts.base_types import BaseComponent, BaseToolOutput, CustomType
from charts.templates.shadcn.carousel import SHADCN_CAROUSEL_TEMPLATE


class CarouselOrientation(str, Enum):
    vertical = "vertical"
    horizontal = "horizontal"


class CarouselItem(BaseComponent):
    """A single element that is used in the Carousel component."""

    component_type: Literal["carousel_item"] = "carousel_item"
    content: str | BaseComponent = Field(
        ...,
        description="Content of the carousel element - either a text or BaseComponent type object",
    )


class CarouselConfig(CustomType):
    """A config for the Carousel component."""

    align: Literal["start"] | None = "start"
    loop: Literal["true", "false"] | None = "true"
    orientation: CarouselOrientation
    container_class: Literal["max-w-xs"] | None = "max-w-xs"


class Carousel(BaseComponent):
    """A complete Carousel component with items."""

    component_type: Literal["carousel"] = "carousel"
    items: list[CarouselItem]
    config: CarouselConfig

    @field_validator("items", mode="before")
    @classmethod
    def wrap_in_list(cls, v: CarouselItem | list[CarouselItem]) -> list[CarouselItem]:
        """Wrap items in a list object."""
        if isinstance(v, CarouselItem):
            return [v]
        return v


class CarouselToolOutput(BaseToolOutput):
    """An output of Agentic component workflow creation."""

    text: str | None = None
    message: str | None = None
    ui: Carousel
    ui_element: str
    data: dict[str, Any] | None = None

    @model_validator(mode="after")
    def build_ui_element(self) -> Self:
        """Create a formatted UI element based on provided template."""
        if not self.ui:
            self.ui_element = ""
            return self

        items_data = [i.model_dump() for i in self.ui.items]
        items_json = json.dumps(items_data)

        template = SHADCN_CAROUSEL_TEMPLATE
        self.ui_element = template.render(
            items_json=items_json,
            align=self.ui.config.align,
            loop=self.ui.config.loop,
            orientation=self.ui.config.orientation.value,
            container_class=self.ui.config.container_class,
        )
        return self
