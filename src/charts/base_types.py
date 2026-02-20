"""Base types and Pydantic models for UI component definitions.

This module provides abstract base classes that define the structure for all
UI components in the library. These base classes are extended by concrete
implementations in the `charts.types.shadcn` subpackage.

Key abstractions:
- BaseComponent: Root interface for all UI components
- BaseTable, BaseChart, BaseCard, BaseAccordion, BaseCarousel: Component-specific bases
- BaseAgentUIConfig: Configuration model passed to AI agents for component creation

All models use Pydantic's ConfigDict with arbitrary_types_allowed=True to support
Jinja2 Template objects and other non-serializable types.
"""

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


# --- MAIN CLASSES --- #$
class CustomType(BaseModel):
    """Base class for custom Pydantic models in the library."""

    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)


# --- CONFIG --- #
class BaseColors(CustomType):
    """A base color palette object."""

    primary: str = Field(default="#858586", description="Hex or CSS variable for primary color.")
    secondary: str = Field(
        default="#0FB1E2", description="Hex or CSS variable for secondary color."
    )
    tertiary: str = Field(default="#E9E040", description="Hex or CSS variable for tertiary color.")
    success: str = Field(default="#33C819", description="Hex or CSS variable for success color.")
    danger: str = Field(default="#EE8A19", description="Hex or CSS variable for danger color.")
    warning: str = Field(default="#D6E718", description="Hex or CSS variable for warning color.")
    error: str = Field(default="#FF0000", description="Hex or CSS variable for error color.")

    # Neutrals - Essential for MUI 'Paper' and Shadcn 'Card'
    background: str = Field(default="#FFFFFF", description="The main background color")
    surface: str = Field(default="#F4F4F5", description="Color for cards, modals, etc.")
    text: str = Field(default="#09090B", description="The default text color")


class BaseColorPalette(CustomType):
    """A base color palette fore light and dark settings."""

    light: BaseColors
    dark: BaseColors


class BaseLibraryConfig(CustomType):
    """A basic config for chosen library."""

    # Technical part
    framework: Literal["react"] = "react"
    library: Literal["shadcn"] = "shadcn"  # More libs in the future
    is_package: bool = Field(
        False,
        description="True if components are in node_modules, False if local files",
    )

    # Path & Import logic
    import_alias: str = Field("@/components", description="Alias used for local component imports")
    component_path: str = Field(
        "ui",
        description="Sub-directory for components (e.g. '@/components/ui')",
    )
    use_typescript: bool = True
    styling_strategy: Literal["tailwind", "css-in-js", "inline"] = "tailwind"


class BaseUIConfig(CustomType):
    """A base configuration to be used by agents for creating the components."""

    color_palette: BaseColorPalette
    mode: Literal["light", "dark", "system"] = "system"
    radius: float = Field(
        default=0.5, description="Border radius multiplier (0 for sharp, 1+ for rounded)"
    )
    density: Literal["compact", "comfortable", "spacious"] = "comfortable"


class BaseAgentUIConfig(CustomType):
    """A master config passed directly to the tools."""

    theme: BaseUIConfig
    lib: BaseLibraryConfig

    # Custom overrides
    overrides: dict[str, Any] = Field(
        default_factory=dict,
        description="Global overrides(e.g., {'Button': {'variant': 'outline'})",
    )

    # Misc
    config_version: Literal["0.1"] = "0.1"

    def get_active_colors(self) -> BaseColors:
        """Helper to the the correct color scheme based on current mode."""
        if self.theme.mode == "dark":
            return self.theme.color_palette.dark
        return self.theme.color_palette.light


# --- COMPONENTS --- #
class BaseComponent(CustomType):
    """Base class for all UI components."""

    component_type: str


# --- Table Base Types ---
class BaseTableData(CustomType):
    headers: list[str] = Field(..., description="A collection of headers corresponding to the data")
    rows: list[tuple[Any, ...]] = Field(
        ...,
        description="A collection of data stored in the form of rows",
    )


class BaseTableFooter(CustomType):
    keyword: str = Field(..., description="Summarizing keyword like: 'Total', 'Estimated'")
    header_to_summarize: str = Field(..., description="The header to perform calculation on")
    value: str | int | float | None = None


class BaseTable(BaseComponent):
    component_type: Literal["table"] = "table"
    table_data: BaseTableData
    caption: str = Field(..., description="Caption for the table")
    footer: BaseTableFooter | None = None


# --- Chart Base Types ---
class BaseChartTypes(str, Enum):
    """Available chart types for data visualization.

    Attributes:
        bar: Bar chart for categorical comparisons
        line: Line chart for time series trends
        pie: Pie chart for proportional distribution
        area: Area chart for stacked continuous data
        radar: Radar chart for multivariate comparisons
    """

    bar = "bar"
    line = "line"
    pie = "pie"
    area = "area"
    radar = "radar"


class BaseChartMetadata(CustomType):
    title: str | None = None
    subtitle: str | None = None
    description: str | None = None


class BaseChartConfig(CustomType):
    config: dict[str, dict[str, str]] = Field(default_factory=dict)


class BaseChartData(CustomType):
    data: list[dict[str, Any]] = Field(default_factory=list)


class BaseChart(BaseComponent):
    component_type: Literal["chart"] = "chart"
    chart_type: BaseChartTypes
    metadata: BaseChartMetadata
    chart_config: BaseChartConfig
    chart_data: BaseChartData
    x_axis_key: str = Field(..., description="Key used for labels")


# --- Accordion Base Types ---
class BaseAccordionTypes(str, Enum):
    """Accordion expansion modes.

    Attributes:
        single: Only one accordion panel can be open at a time
        multiple: Multiple accordion panels can be expanded simultaneously
    """

    single = "single"
    multiple = "multiple"


class BaseAccordionItem(BaseComponent):
    component_type: Literal["accordion_item"] = "accordion_item"
    value: str = Field(..., description="Identifier of the field")
    trigger: str = Field(..., description="Header of an accordion element")
    content: str = Field(..., description="Content of the accordion element")


class BaseAccordion(BaseComponent):
    component_type: Literal["accordion"] = "accordion"
    items: list[BaseAccordionItem]
    list_type: BaseAccordionTypes = Field(
        ...,
        description="""Determine whether single or multiple
            elements can be expanded at the same time""",
    )


# --- Card Base Types ---
class BaseCard(BaseComponent):
    component_type: Literal["card"] = "card"
    title: str = Field(..., description="Title of the card")
    description: str = Field(..., description="Description or subtitle")
    content: str | BaseComponent | list[BaseComponent] | None = Field(
        default=None,
        description="Content of the card component: text, other component or list of them.",
    )
    footer: str = Field(..., description="Footer of the card component")


# --- Carousel Base Types ---
class CarouselOrientation(str, Enum):
    """Carousel scrolling orientation.

    Attributes:
        horizontal: Items scroll left-to-right (default)
        vertical: Items scroll top-to-bottom
    """

    vertical = "vertical"
    horizontal = "horizontal"


class BaseCarouselItem(BaseComponent):
    component_type: Literal["carousel_item"] = "carousel_item"
    content: str | BaseCard = Field(
        ...,
        description="Content of the carousel element - either a text or Card type object",
    )


class BaseCarouselConfig(CustomType):
    align: Literal["start"] | None = "start"
    loop: Literal["true", "false"] | None = "true"
    orientation: CarouselOrientation = Field(default=CarouselOrientation.horizontal)
    container_class: str | None = "max-w-xs"


class BaseCarousel(BaseComponent):
    component_type: Literal["carousel"] = "carousel"
    items: list[BaseCarouselItem]
    config: BaseCarouselConfig
