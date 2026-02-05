from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


class CustomType(BaseModel):
    """Base class for custom Pydantic models in the sql-toolset-pydantic-ai library.

    This class provides a common configuration for all custom models in the library,
    allowing arbitrary types to be used in Pydantic models.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)


class BaseComponent(CustomType):
    """Base class for all UI components."""

    component_type: str


class BaseToolOutput(CustomType):
    """Base class for all tool output data from Agents."""

    text: str | None = None
    message: str | None = None
    ui: list[BaseComponent]
    ui_element: str
    data: dict[str, Any] | None = None


# TODO switch to default chart component?
class TableComponent(BaseComponent):
    """Standard table fallback if a chart isn't appropriate."""

    component_type: Literal["table"] = "table"
    headers: list[str]
    rows: list[dict[str, Any]]
