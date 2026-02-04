import json
from enum import Enum
from typing import Any, Literal

from pydantic import Field, field_validator, model_validator
from typing_extensions import Self

from charts.base_types import BaseComponent, CustomType
from charts.templates.shadcn.chart import (
    SHADCN_BAR_CHART_TEMPLATE,
    SHADCN_PIE_CHART_TEMPLATE,
    SHADCN_LINE_CHART_TEMPLATE,
    SHADCN_RADAR_CHART_TEMPLATE,
    SHADCN_AREA_CHART_TEMPLATE,
)


class ChartTypes(str, Enum):
    bar = "bar"
    line = "line"
    pie = "pie"
    area = "area"
    radar = "radar"


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

    Example for bar chart: {"desktop": {"label": "Desktop", "color": "#2563eb"}}

    Example for pie chart: {"category": "subscriptions", "value": 1224,
    "fill": "var(--color-subscriptions)"}

    Example for line chart: desktop: {"label": "Desktop", "color": "var(--chart-1)"}

    Example for radar chart: { "desktop": { "label": "Desktop", "color": "var(--chart-1)"}

    Example for area chart: {visitors: {label: "Visitors",}, desktop: { label: "Desktop", color: "var(--chart-1)",}}
    """

    config: dict[str, dict[str, str]]


class ChartData(CustomType):
    """
    The actual data points for the chart.

    Example for bar chart: [{"month": "Jan", "desktop": 100}, {"month": "Feb", "desktop": 120}]

    Example for line chart: [{ month: "January", desktop: 186, mobile: 80 }]

    Example for radar chart: [{ month: "January", desktop: 186, mobile: 80 }]

    Example for area chart: [{ date: "2024-04-01", desktop: 222, mobile: 150 }]
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

    # Helpful for the frontend to know which key is X-axis
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
            self.ui_element = ""  # Or a placeholder component string
            return self

        chart = self.ui[0]

        # Select template based on chart type
        if chart.chart_type == "pie":
            template = SHADCN_PIE_CHART_TEMPLATE
        elif chart.chart_type == "line":
            template = SHADCN_LINE_CHART_TEMPLATE
        elif chart.chart_type == "radar":
            template = SHADCN_RADAR_CHART_TEMPLATE
        elif chart.chart_type == "bar":
            template = SHADCN_BAR_CHART_TEMPLATE
        elif chart.chart_type == "area":
            template = SHADCN_AREA_CHART_TEMPLATE
        else:
            raise KeyError("Unknown chart type")

        # Get the keys from the config (e.g., ['subscriptions', 'revenue'])
        data_keys = list(chart.chart_config.config.keys())

        # Build a chart_config object that includes both series config
        # and optional metadata (title/subtitle/description). This keeps
        # templates backward-compatible while exposing metadata to the
        # frontend via the same `chart_config` prop.
        series_config = dict(chart.chart_config.config or {})
        merged_config: dict = dict(series_config)
        if getattr(chart, "metadata", None):
            if chart.metadata.title:
                merged_config["title"] = chart.metadata.title
            if chart.metadata.subtitle:
                merged_config["subtitle"] = chart.metadata.subtitle
            if chart.metadata.description:
                merged_config["description"] = chart.metadata.description

        # Sanitize component name for the internal function
        # Remove non-alphanumeric characters and fall back to a default
        import re

        raw_name = (chart.metadata.title or "GeneratedChart") if getattr(chart, "metadata", None) else "GeneratedChart"
        safe_name = re.sub(r"[^0-9A-Za-z_]", "", raw_name.replace(" ", "")) or "GeneratedChart"

        # 3. Render the template
        self.ui_element = template.render(
            component_name=safe_name,
            chart_config_json=json.dumps(merged_config, ensure_ascii=False, indent=2),
            chart_data_json=json.dumps(chart.chart_data.data, ensure_ascii=False, indent=2),
            x_axis_key=chart.x_axis_key or "category",  # Fallback for X Axis
            data_keys=data_keys,
        )

        return self
