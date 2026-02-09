import json
from enum import Enum
from typing import Any, Literal

from pydantic import Field, model_validator
from typing_extensions import Self

from charts.base_types import BaseComponent, CustomType
from charts.templates.shadcn.accordion import SHADCN_ACCORDION_TEMPLATE


class AccordionTypes(str, Enum):
    single = "single"
    multiple = "multiple"


class Accordion(BaseComponent):
    """Accordion element to be rendered on the frontend.

    Example:
    {
        value: "item-1",
        trigger: "How do I reset my password?",
        content: "Click on 'Forgot Password' on the login page, enter
        your email address, and we'll send you a link to reset your
        password. The link will expire in 24 hours."
    }

    """

    component_type: Literal["accordion"] = "accordion"
    value: str = Field(..., description="Identifier of the field")
    trigger: str = Field(..., description="Header of an accordion element")
    content: str = Field(..., description="Content of the accordion element")


class AccordionList(BaseComponent):
    """A list-type collection of Accordion objects for rendering purposes.

    Example:
    { items: [
        { value: "item-1",
        trigger: "How do I reset my password?",
        content: "Click on 'Forgot Password' on the login page, enter your
            email address, and we'll send you a link to reset your password.
            The link will expire in 24 hours."
        },
        { value: "item-2",
        trigger: "Can I change my subscription plan?",
        content: "Yes, you can upgrade or downgrade your plan at any time
        from your account settings. Changes will be reflected in your
        next billing cycle."
        }],
    list_type: "multiple"
    }

    """

    component_type: str = "accordion_list"
    items: list[Accordion]
    list_type: AccordionTypes = Field(
        ...,
        description="""Determine whether single or multiple
            elements can be expanded at the same time""",
    )


class AccordionToolOutput(CustomType):
    """An output of Agentic component workflow creation."""

    text: str | None = None
    message: str | None = None
    ui: AccordionList
    ui_element: str
    data: dict[str, Any] | None = None

    @model_validator(mode="after")
    def build_ui_element(self) -> Self:
        """Create a formatted UI element based on provided template."""
        if not self.ui:
            self.ui_element = ""  # Placeholder?
            return self

        template = SHADCN_ACCORDION_TEMPLATE
        items_data = [item.model_dump() for item in self.ui.items]
        items_json = json.dumps(items_data)
        self.ui_element = template.render(
            items=self.ui.items,
            items_json=items_json,
            list_type=self.ui.list_type.value,
        )

        return self
