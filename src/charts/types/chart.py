import json
from enum import Enum
from typing import Any, Literal

from pydantic import Field, field_validator, model_validator
from typing_extensions import Self

from charts.base_types import BaseComponent, CustomType
from charts.templates.chart import SHADCN_CHART_TEMPLATE


class ChartTypes(str, Enum):
    bar = "bar"
    line = "line"
    pie = "pie"
    area = "area"


class ChartMetadata(CustomType):
    """
    Metadata for given chart, containing elements like title, subtitle, description and others.
    """

    title: str | None = None
    subtitle: str | None = None
    description: str | None = None


class ChartConfig(CustomType):
    """
    Config for a chart. Maps data keys to labels and colors.
    Example: {"desktop": {"label": "Desktop", "color": "#2563eb"}}
    """

    config: dict[str, dict[str, str]]


class ChartData(CustomType):
    """
    The actual data points for the chart.
    Example: [{"month": "Jan", "desktop": 100}, {"month": "Feb", "desktop": 120}]
    """

    data: list[dict[str, str | int | float | Any]]


class Chart(BaseComponent):
    # Main elements
    component_type: Literal["chart"] = "chart"
    chart_type: ChartTypes

    # Chart metadata
    metadata: ChartMetadata

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


class ChartToolOutput(CustomType):
    text: str | None = None
    message: str | None = None
    ui: list[Chart]
    data: dict[str, Any] | None = None

    @field_validator("ui", mode="before")
    @classmethod
    def wrap_in_list(cls, v: Chart | list[Chart]) -> list[Chart] | Any:
        if isinstance(v, Chart):
            return [v]
        return v


class ChartToolOutputV2(CustomType):
    text: str | None = None
    message: str | None = None
    ui: list[Chart]
    ui_element: str
    data: dict[str, Any] | None = None

    @field_validator("ui", mode="before")
    @classmethod
    def wrap_in_list(cls, v: Chart | list[Chart]) -> list[Chart] | Any:
        if isinstance(v, Chart):
            return [v]
        return v

    @model_validator(mode="after")
    def build_ui_element(self) -> Self:
        if not self.ui:
            return self

        chart = self.ui[0]
        template = SHADCN_CHART_TEMPLATE
        data_keys = list(chart.chart_config.config.keys())

        self.ui_element = template.render(
            component_name=(
                chart.metadata.title.replace(" ", "") if chart.metadata.title else "MyChart"
            ),
            chart_config_json=json.dumps(chart.chart_config.config, indent=2),
            chart_data_json=json.dumps(chart.chart_data.data, indent=2),
            x_axis_key=chart.x_axis_key,
            data_keys=data_keys,
        )

        return self
