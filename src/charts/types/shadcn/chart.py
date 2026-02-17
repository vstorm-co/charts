from typing import Literal

from pydantic import model_validator

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

    component_type: Literal["chart"] = "chart"

    @model_validator(mode="after")
    def validate_keys_exist_in_data(self) -> "Chart":
        # Ensure we have data to check against
        if not self.chart_data.data:
            raise ValueError("chart_data must contain at least one row of data.")

        available_keys = self.chart_data.data[0].keys()

        if self.x_axis_key not in available_keys:
            raise ValueError(
                f"x_axis_key '{self.x_axis_key}' not found in data keys: {list(available_keys)}",
            )

        return self
