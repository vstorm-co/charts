from typing import Any

from pydantic import field_validator

from charts.base_types import BaseChart, BaseChartConfig, BaseChartData, BaseChartMetadata


class ChartMetadata(BaseChartMetadata):
    """Metadata for given chart, containing elements like title,
    subtitle, description and others.
    """


class ChartConfig(BaseChartConfig):
    """Config for a chart. Maps data keys to labels and colors.

    Example (Bar/Line/Area/Radar):
    {
        "desktop": {"label": "Desktop", "color": "#2563eb"},
        "mobile": {"label": "Mobile", "color": "#60a5fa"}
    }

    Example (Pie):
    {
        "chrome": {"label": "Chrome", "color": "var(--chart-1)"},
        "safari": {"label": "Safari", "color": "var(--chart-2)"}
    }
    """


class ChartData(BaseChartData):
    """The actual data points for the chart.

    Example (Bar/Line/Area/Radar):
    [{"month": "Jan", "desktop": 100, "mobile": 80}, {"month": "Feb", "desktop": 120, "mobile": 90}]

    Example (Pie):
    [{"category": "Chrome", "value": 275}, {"category": "Safari", "value": 200}]
    """


class Chart(BaseChart):
    """Basic object to store various charts for component rendering."""

    component_type: str = "chart"

    @field_validator("x_axis_key")
    @classmethod
    def validate_x_axis_key(cls, v: str, info: Any) -> str:
        # Pydantic V2 stores sibling fields in info.data
        chart_data_obj = info.data.get("chart_data")

        if chart_data_obj and hasattr(chart_data_obj, "data") and chart_data_obj.data:
            # Check the keys of the first dictionary in the list
            available_keys = chart_data_obj.data[0].keys()
            if v not in available_keys:
                raise ValueError(
                    f"x_axis_key '{v}' must be one of the data keys: {list(available_keys)}",
                )
        return v
