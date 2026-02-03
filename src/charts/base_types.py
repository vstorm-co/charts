from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


class CustomType(BaseModel):
    """
    Base class for custom Pydantic models in the sql-toolset-pydantic-ai library.

    This class provides a common configuration for all custom models in the library,
    allowing arbitrary types to be used in Pydantic models.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)


class BaseComponent(CustomType):
    """Base class for all UI components"""

    component_type: Literal["chart", "table"]


# TODO switch to default chart component?
class TableComponent(BaseComponent):
    """Standard table fallback if a chart isn't appropriate"""

    component_type: Literal["table"] = "table"
    headers: list[str]
    rows: list[dict[str, Any]]


# class ToolOutput(CustomType):
#     text: str
#     message: str | None
#     ui: BaseComponent | list[BaseComponent]
#     data: Any = None

#     @field_validator("ui")
#     @classmethod
#     def validate_ui(
#         cls, v: BaseComponent | list[BaseComponent]
#     ) -> BaseComponent | list[BaseComponent]:
#         """Validate that ui contains only valid component types"""
#         if isinstance(v, list):
#             for item in v:
#                 if not isinstance(item, BaseComponent):
#                     raise ValueError(
#                         f"UI list can only contain BaseComponent instances, got {type(item)}"
#                     )
#         return v
