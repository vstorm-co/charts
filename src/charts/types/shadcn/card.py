from typing import Literal

from charts.base_types import BaseCard


class Card(BaseCard):
    """Card component can be either standalone of can contain some other components inside."""

    component_type: Literal["card"] = "card"
