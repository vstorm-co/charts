from typing import Literal

from pydantic import field_validator

from charts.base_types import BaseCarousel, BaseCarouselConfig, BaseCarouselItem


class CarouselItem(BaseCarouselItem):
    """A single element that is used in the Carousel component."""

    component_type: Literal["carousel_item"] = "carousel_item"


class CarouselConfig(BaseCarouselConfig):
    """A config for the Carousel component."""


class Carousel(BaseCarousel):
    """A complete Carousel component with items."""

    component_type: Literal["carousel"] = "carousel"

    @field_validator("items", mode="before")
    @classmethod
    def wrap_in_list(cls, v: CarouselItem | list[CarouselItem]) -> list[CarouselItem]:
        """Wrap items in a list object."""
        if isinstance(v, CarouselItem):
            return [v]
        return v
