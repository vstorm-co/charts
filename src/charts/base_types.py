from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class CustomType(BaseModel):
    """Base class for custom Pydantic models in the library."""

    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)


class BaseComponent(CustomType):
    """Base class for all UI components."""

    component_type: str


class BaseToolOutput(CustomType):
    """Base class for all tool output data from Agents."""

    text: str | None = None
    message: str | None = None
    ui: BaseComponent | list[BaseComponent]
    ui_element: str
    data: dict[str, Any] | None = None


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
    config: dict[str, dict[str, str]]


class BaseChartData(CustomType):
    data: list[dict[str, Any]]


class BaseChart(BaseComponent):
    component_type: Literal["chart"] = "chart"
    chart_type: BaseChartTypes
    metadata: BaseChartMetadata
    chart_config: BaseChartConfig
    chart_data: BaseChartData
    x_axis_key: str = Field(..., description="Key used for labels")


# --- Accordion Base Types ---


class BaseAccordionTypes(str, Enum):
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
    orientation: CarouselOrientation
    container_class: str | None = "max-w-xs"


class BaseCarousel(BaseComponent):
    component_type: Literal["carousel"] = "carousel"
    items: list[BaseCarouselItem]
    config: BaseCarouselConfig
