"""Shared text fixtures and helpers for charts package."""

from typing import Any

from pydantic_ai import FunctionToolset, Tool
from pydantic_ai.models.test import TestModel

from charts.base_types import (
    BaseAccordion,
    BaseAccordionItem,
    BaseAccordionTypes,
    BaseTable,
    BaseTableData,
    BaseTableFooter,
)
from charts.toolset import EngineDeps

MODEL = TestModel()


def get_tool(toolset: FunctionToolset[EngineDeps], name: str) -> Tool[Any]:
    """Retrieve a specific tool from a toolset by name."""
    tools = toolset.tools if isinstance(toolset.tools, list) else toolset.tools.values()
    return next(t for t in tools if t.name == name)


def table() -> BaseTable:
    return BaseTable(
        component_type="table",
        table_data=BaseTableData(headers=["1", "2", "3"], rows=[(1, 2, 3), (4, 5, 6), (7, 8, 9)]),
        caption="Table caption",
        footer=BaseTableFooter(keyword="Table keyword", header_to_summarize="1", value=10),
    )


def table_invalid_footer() -> BaseTable:
    return BaseTable(
        component_type="table",
        table_data=BaseTableData(
            headers=["1", "2"],
            rows=[("a", 2), ("b", 3)],  # non-numeric values
        ),
        caption="Invalid footer table",
        footer=BaseTableFooter(
            keyword="Sum",
            header_to_summarize="X",
        ),
    )


def accordion() -> BaseAccordion:
    return BaseAccordion(
        component_type="accordion",
        items=[
            BaseAccordionItem(
                component_type="accordion_item",
                value="some value 1",
                trigger="some trigger 1",
                content="some content 1",
            )
        ],
        list_type=BaseAccordionTypes.single,
    )
