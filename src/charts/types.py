from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


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


class ChartConfig(CustomType):
    """
    Config for a chart. Maps data keys to labels and colors.
    Example: {"desktop": {"label": "Desktop", "color": "#2563eb"}}
    """

    config: dict[str, dict[str, Any]]


class ChartData(CustomType):
    """
    The actual data points for the chart.
    Example: [{"month": "Jan", "desktop": 100}, {"month": "Feb", "desktop": 120}]
    """

    data: list[dict[str, Any]]


class Chart(BaseComponent):
    component_type: Literal["chart"] = "chart"
    chart_type: Literal["bar", "line", "pie", "area"]
    title: str | None
    description: str | None = Field(None, description="Subtitle or description of the chart")
    
    # Match `shadcn` variable naming
    chart_config: ChartConfig = Field(..., alias="chartConfig")
    chart_data: ChartData = Field(..., alias="chartData")
    
    # Helpful fot the frontend to know which key is X-axis
    x_axis_key: str = Field(..., description="The key in data used for the X-axis (e.g., 'month')")

    @field_validator("x_axis_key")
    @classmethod
    def validate_x_axis_key(cls, v: str, info: Any) -> str:
        """Validate that x_axis_key exists in chart_data keys"""
        if "data" in info.data and info.data["data"]:
            data_keys = info.data["data"][0].keys()
            if v not in data_keys:
                raise ValueError(
                    f"x_axis_key '{v}' must be one of the data keys: {list(data_keys)}"
                )
        return v


class TableComponent(BaseComponent):
    """Standard table fallback if a chart isn't appropriate"""
    
    component_type: Literal["table"] = "table"
    headers: list[str]
    rows: list[dict[str, Any]]


class ToolOutput(CustomType):
    text: str
    message: str | None
    ui: BaseComponent | list[BaseComponent]
    data: Any = None

    @field_validator("ui")
    @classmethod
    def validate_ui(
        cls, v: BaseComponent | list[BaseComponent]
    ) -> BaseComponent | list[BaseComponent]:
        """Validate that ui contains only valid component types"""
        if isinstance(v, list):
            for item in v:
                if not isinstance(item, BaseComponent):
                    raise ValueError(
                        f"UI list can only contain BaseComponent instances, got {type(item)}"
                    )
        return v
