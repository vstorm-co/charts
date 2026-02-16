import asyncio
import json

import pytest
import pytest_asyncio

from collections.abc import AsyncGenerator
from typing import Any, Literal
from pydantic_ai import RunContext, RunUsage, ToolReturn

import pytest_asyncio
from tests.conftest import MODEL, get_tool, table, table_invalid_footer, accordion

from charts.engines.shadcn import Shadcn
from charts.toolset import EngineDeps, create_ui_toolset
from charts.types import shadcn


# Setup fixture fot toolset
@pytest_asyncio.fixture
async def shadcn_client_json() -> AsyncGenerator[Shadcn, Any]:
    """An instance of Shadcn engine object."""

    shadcn = Shadcn("json")
    yield shadcn


@pytest_asyncio.fixture
async def shadcn_client_tsx() -> AsyncGenerator[Shadcn, Any]:
    """An instance of Shadcn engine object."""

    shadcn = Shadcn("tsx")
    yield shadcn


@pytest.fixture
def deps_json(shadcn_client_json: Shadcn) -> EngineDeps:
    """An instance of dependencies used in the real object."""
    return EngineDeps(engine=shadcn_client_json)


@pytest.fixture
def deps_tsx(shadcn_client_tsx: Shadcn) -> EngineDeps:
    """An instance of dependencies used in the real object."""
    return EngineDeps(engine=shadcn_client_tsx)


@pytest.fixture
def context_json(deps_json: EngineDeps) -> RunContext[EngineDeps]:
    """An instance of context used in th real object."""
    return RunContext(model=MODEL, usage=RunUsage(), deps=deps_json)


@pytest.fixture
def context_tsx(deps_tsx: EngineDeps) -> RunContext[EngineDeps]:
    """An instance of context used in th real object."""
    return RunContext(model=MODEL, usage=RunUsage(), deps=deps_tsx)


### TESTS ###
def test_toolset_creation() -> None:
    toolset = create_ui_toolset()
    tools_list = list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools

    assert len(tools_list) > 1
    assert len(tools_list) == 5
    tool_names = {t.name for t in tools_list}
    assert tool_names == {
        "create_table",
        "create_accordion",
        "create_card",
        "create_carousel",
        "create_chart",
    }


## TABLE ##
# JSON #
@pytest.mark.asyncio
async def test_json_tool_create_table(
    context_json: RunContext[EngineDeps], shadcn_client_json: Shadcn
) -> None:
    toolset = create_ui_toolset()
    tool = get_tool(toolset, "create_table")

    # Make calls manually
    engine_response = await shadcn_client_json.render_table_component(table())
    tool_result = await tool.function(context_json, table())

    # Assert
    assert isinstance(tool_result, ToolReturn)
    ui_element = tool_result.metadata.get("ui_element")
    assert ui_element is not None, "ToolResult metadata should contain 'ui_element'"

    # Differentiate assertions based on the fixture's internal state
    assert isinstance(ui_element, str)
    assert json.loads(ui_element)


@pytest.mark.asyncio
async def test_json_tool_create_table_invalid_footer(
    context_json: RunContext[EngineDeps], shadcn_client_json: Shadcn
) -> None:
    toolset = create_ui_toolset()
    tool = get_tool(toolset, "create_table")

    # Make calls manually
    result = await shadcn_client_json.render_table_component(table_invalid_footer())
    assert result  # just ensure it doesn't crash


@pytest.mark.asyncio
async def test_json_tool_create_accordion(
    context_json: RunContext[EngineDeps], shadcn_client_json: Shadcn
) -> None:
    toolset = create_ui_toolset()
    tool = get_tool(toolset, "create_accordion")

    # Make calls manually
    engine_response = await shadcn_client_json.render_accordion_component(accordion())
    tool_result = await tool.function(context_json, accordion())

    # Assert
    assert isinstance(tool_result, ToolReturn)
    ui_element = tool_result.metadata.get("ui_element")
    assert ui_element is not None, "ToolResult metadata should contain 'ui_element'"

    # Differentiate assertions based on the fixture's internal state
    assert isinstance(ui_element, str)
    assert json.loads(ui_element)
