from typing import Any, Literal

from pydantic import Field, model_validator
from typing_extensions import Self

from charts.base_types import BaseComponent, BaseToolOutput
from charts.templates.shadcn.card import SHADCN_CARD_TEMPLATE


class Card(BaseComponent):
    """Card component can be either standalone of can contain some other components inside."""

    component_type: Literal["card"] = "card"
    title: str = Field(..., description="Title of the card")
    description: str = Field(..., description="Description or subtitle")
    content: str | BaseComponent | list[BaseComponent] | None = Field(
        default=None,
        description="Content of the card component: text, other component or list of them.",
    )
    footer: str = Field(..., description="Footer of the card component")


class CardOutputTool(BaseToolOutput):
    """An output of Agentic component workflow creation."""

    text: str | None = None
    message: str | None = None
    ui: Card
    ui_element: str
    data: dict[str, Any] | None = None

    @model_validator(mode="after")
    def build_ui_element(self) -> Self:
        """Create a formatted UI element based on provided template."""
        if not self.ui:
            self.ui_element = ""  # Placeholder?
            return self

        template = SHADCN_CARD_TEMPLATE
        self.ui_element = template.render(
            title=self.ui.title,
            description=self.ui.description,
            content=self.ui.content,
            footer=self.ui.footer,
        )
        return self
