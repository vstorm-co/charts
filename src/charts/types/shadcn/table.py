import json
from typing import Any, Literal

from pydantic import Field, model_validator
from typing_extensions import Self

from charts.base_types import BaseComponent, BaseToolOutput, CustomType
from charts.templates.shadcn.table import SHADCN_TABLE_TEMPLATE


class TableData(CustomType):
    """Collection of data to present in the table.

    Exemplary format:
    headers = ["month", "price", "id", ...]
    rows = [
        ("september", "19.99", "asd21331", ...),
        ("may", "109.99", "d2134sdf", ...),
        ...
    ]

    """

    headers: list[str] = Field(..., description="A collection of headers corresponding to the data")
    rows: list[tuple[Any, ...]] = Field(
        ..., description="A collection of data stored in the form of rows",
    )


class TableFooter(CustomType):
    """A footer of the table."""

    keyword: str = Field(
        ...,
        description="A summarizing keyword like: 'Total', 'All', 'Estimated'. The proper keyword should be chosen based on the content of the data in the table.",
    )
    header_to_summarize: str = Field(..., description="A table header that has to be summarized.")
    value: str | int | float | None = None


class Table(BaseComponent):
    """A Table component."""

    component_type: Literal["table"] = "table"

    table_data: TableData
    caption: str = Field(..., description="Caption for the table")
    footer: TableFooter | None


class TableOutputTool(BaseToolOutput):
    """An output of Agentic component workflow creation."""

    text: str | None = None
    message: str | None = None
    ui: Table
    ui_element: str
    data: dict[str, Any] | None = None

    @model_validator(mode="after")
    def build_ui_element(self) -> Self:
        """Create a formatted UI element based on provided template."""
        if not self.ui:
            self.ui_element = ""  # Placeholder?
            return self

        # Format the data for table
        items_data = []
        headers = self.ui.table_data.headers

        for row in self.ui.table_data.rows:
            item = dict(zip(headers, row))
            items_data.append(item)
        items_json = json.dumps(items_data)

        # Get the total for footer
        footer_value = None
        footer_keyword = ""

        if self.ui.footer:
            footer_keyword = self.ui.footer.keyword
            if self.ui.footer.header_to_summarize in headers:
                try:
                    footer_value = sum(
                        float(item[self.ui.footer.header_to_summarize])
                        for item in items_data
                        if item[self.ui.footer.header_to_summarize] is not None
                    )
                except (ValueError, TypeError):
                    footer_value = None  # Fallback if data isn't numeric

        template = SHADCN_TABLE_TEMPLATE
        self.ui_element = template.render(
            items_json=items_json,
            headers=self.ui.table_data.headers,
            caption=self.ui.caption,
            footer_text=footer_keyword,
            footer_value=footer_value,
        )

        return self
