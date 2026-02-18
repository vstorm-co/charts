"""Comprehensive tests for toolset module."""

import pytest
from pydantic_ai import RunContext, RunUsage
from pydantic_ai.models.test import TestModel

from charts.engines.shadcn import Shadcn
from charts.toolset import EngineDeps, create_ui_toolset
from charts.types.shadcn.accordion import Accordion, AccordionItem
from charts.types.shadcn.card import Card
from charts.types.shadcn.carousel import Carousel, CarouselConfig, CarouselItem
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData, ChartMetadata
from charts.types.shadcn.table import Table, TableData, TableFooter


class TestToolOutputConfig:
    """Tests for config field in tool output metadata."""

    @pytest.mark.asyncio
    async def test_config_present_in_table_tool(self):
        """Test that table tool returns config in metadata."""
        MODEL = TestModel()
        shadcn = Shadcn("json")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        table_tool = next(t for t in tools_list if t.name == "create_table")

        data = TableData(headers=["Name"], rows=[("Item 1",)])
        table = Table(
            component_type="table",
            table_data=data,
            caption="Test",
        )

        result = await table_tool.function(context, table)

        assert "config" in result.metadata

    @pytest.mark.asyncio
    async def test_config_present_in_accordion_tool(self):
        """Test that accordion tool returns config in metadata."""
        MODEL = TestModel()
        shadcn = Shadcn("json")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        accordion_tool = next(t for t in tools_list if t.name == "create_accordion")

        items = [
            AccordionItem(
                component_type="accordion_item",
                value="item-1",
                trigger="Trigger",
                content="Content",
            )
        ]
        accordion = Accordion(
            component_type="accordion",
            items=items,
            list_type="single",
        )

        result = await accordion_tool.function(context, accordion)

        assert "config" in result.metadata

    @pytest.mark.asyncio
    async def test_config_present_in_card_tool(self):
        """Test that card tool returns config in metadata."""
        MODEL = TestModel()
        shadcn = Shadcn("json")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        card_tool = next(t for t in tools_list if t.name == "create_card")

        card = Card(
            component_type="card",
            title="Test Card",
            description="Description",
            content="Content",
            footer="Footer",
        )

        result = await card_tool.function(context, card)

        assert "config" in result.metadata

    @pytest.mark.asyncio
    async def test_config_present_in_carousel_tool(self):
        """Test that carousel tool returns config in metadata."""
        MODEL = TestModel()
        shadcn = Shadcn("json")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        carousel_tool = next(t for t in tools_list if t.name == "create_carousel")

        items = [
            CarouselItem(
                component_type="carousel_item",
                content="Slide 1",
            )
        ]
        config = CarouselConfig()
        carousel = Carousel(
            component_type="carousel",
            items=items,
            config=config,
        )

        result = await carousel_tool.function(context, carousel)

        assert "config" in result.metadata

    @pytest.mark.asyncio
    async def test_config_present_in_chart_tool(self):
        """Test that chart tool returns config in metadata."""
        MODEL = TestModel()
        shadcn = Shadcn("json")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        chart_tool = next(t for t in tools_list if t.name == "create_chart")

        config = ChartConfig(
            config={
                "desktop": {"label": "Desktop", "color": "#2563eb"},
            }
        )
        data = ChartData(data=[{"month": "Jan", "desktop": 100}])
        metadata = ChartMetadata(title="Test")
        chart = Chart(
            component_type="chart",
            chart_type="bar",
            metadata=metadata,
            chart_config=config,
            chart_data=data,
            x_axis_key="month",
        )

        result = await chart_tool.function(context, chart)

        assert "config" in result.metadata

    @pytest.mark.asyncio
    async def test_config_structure_has_theme_and_lib(self):
        """Test that config has expected top-level keys: theme and lib."""
        MODEL = TestModel()
        shadcn = Shadcn("json")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        table_tool = next(t for t in tools_list if t.name == "create_table")

        data = TableData(headers=["Name"], rows=[("Item 1",)])
        table = Table(
            component_type="table",
            table_data=data,
            caption="Test",
        )

        result = await table_tool.function(context, table)
        config = result.metadata["config"]

        assert "theme" in config
        assert "lib" in config

    @pytest.mark.asyncio
    async def test_config_theme_has_color_palette(self):
        """Test that theme contains color_palette with light and dark schemes."""
        MODEL = TestModel()
        shadcn = Shadcn("json")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        table_tool = next(t for t in tools_list if t.name == "create_table")

        data = TableData(headers=["Name"], rows=[("Item 1",)])
        table = Table(
            component_type="table",
            table_data=data,
            caption="Test",
        )

        result = await table_tool.function(context, table)
        config = result.metadata["config"]

        assert "color_palette" in config["theme"]
        assert "light" in config["theme"]["color_palette"]
        assert "dark" in config["theme"]["color_palette"]

    @pytest.mark.asyncio
    async def test_config_defaults_to_system_mode(self):
        """Test that default mode is 'system'."""
        MODEL = TestModel()
        shadcn = Shadcn("json")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        table_tool = next(t for t in tools_list if t.name == "create_table")

        data = TableData(headers=["Name"], rows=[("Item 1",)])
        table = Table(
            component_type="table",
            table_data=data,
            caption="Test",
        )

        result = await table_tool.function(context, table)
        config = result.metadata["config"]

        assert config["theme"]["mode"] == "system"

    @pytest.mark.asyncio
    async def test_config_color_palette_has_expected_colors(self):
        """Test that color palette contains expected color fields."""
        MODEL = TestModel()
        shadcn = Shadcn("json")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        table_tool = next(t for t in tools_list if t.name == "create_table")

        data = TableData(headers=["Name"], rows=[("Item 1",)])
        table = Table(
            component_type="table",
            table_data=data,
            caption="Test",
        )

        result = await table_tool.function(context, table)
        config = result.metadata["config"]
        palette = config["theme"]["color_palette"]["light"]

        # Check BaseColors fields
        assert "primary" in palette
        assert "secondary" in palette
        assert "background" in palette
        assert "text" in palette

    @pytest.mark.asyncio
    async def test_config_library_settings(self):
        """Test that lib config has expected fields."""
        MODEL = TestModel()
        shadcn = Shadcn("json")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        table_tool = next(t for t in tools_list if t.name == "create_table")

        data = TableData(headers=["Name"], rows=[("Item 1",)])
        table = Table(
            component_type="table",
            table_data=data,
            caption="Test",
        )

        result = await table_tool.function(context, table)
        config = result.metadata["config"]
        lib_config = config["lib"]

        assert "framework" in lib_config
        assert "library" in lib_config
        assert "import_alias" in lib_config

    @pytest.mark.asyncio
    async def test_config_is_json_serializable(self):
        """Test that config can be serialized to JSON."""
        import json

        MODEL = TestModel()
        shadcn = Shadcn("json")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        table_tool = next(t for t in tools_list if t.name == "create_table")

        data = TableData(headers=["Name"], rows=[("Item 1",)])
        table = Table(
            component_type="table",
            table_data=data,
            caption="Test",
        )

        result = await table_tool.function(context, table)
        config = result.metadata["config"]

        # Should not raise
        json.dumps(config)

    @pytest.mark.asyncio
    async def test_config_contains_overrides_field(self):
        """Test that config has overrides field."""
        MODEL = TestModel()
        shadcn = Shadcn("json")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        table_tool = next(t for t in tools_list if t.name == "create_table")

        data = TableData(headers=["Name"], rows=[("Item 1",)])
        table = Table(
            component_type="table",
            table_data=data,
            caption="Test",
        )

        result = await table_tool.function(context, table)
        config = result.metadata["config"]

        assert "overrides" in config

    @pytest.mark.asyncio
    async def test_config_contains_config_version(self):
        """Test that config has config_version field."""
        MODEL = TestModel()
        shadcn = Shadcn("json")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        table_tool = next(t for t in tools_list if t.name == "create_table")

        data = TableData(headers=["Name"], rows=[("Item 1",)])
        table = Table(
            component_type="table",
            table_data=data,
            caption="Test",
        )

        result = await table_tool.function(context, table)
        config = result.metadata["config"]

        assert "config_version" in config
        assert config["config_version"] == "0.1"


class TestCreateUiToolset:
    """Tests for the create_ui_toolset function."""

    def test_toolset_creation(self):
        """Test basic toolset creation."""
        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        assert len(tools_list) == 5

    def test_toolset_with_id(self):
        """Test toolset creation with custom ID."""
        toolset = create_ui_toolset(id="custom-toolset")
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        assert len(tools_list) == 5

    def test_all_expected_tools_present(self):
        """Test that all expected tools are present in the toolset."""
        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        tool_names = {t.name for t in tools_list}
        assert tool_names == {
            "create_table",
            "create_accordion",
            "create_card",
            "create_carousel",
            "create_chart",
        }


class TestCreateTableTool:
    """Tests for the create_table tool function."""

    @pytest.mark.asyncio
    async def test_create_table_tool_json_mode(self):
        """Test table creation tool in JSON mode."""
        MODEL = TestModel()
        shadcn = Shadcn("json")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        table_tool = next(t for t in tools_list if t.name == "create_table")

        data = TableData(headers=["Name", "Value"], rows=[("Item 1", 100)])
        footer = TableFooter(keyword="Total", header_to_summarize="Value", value=100)
        table = Table(
            component_type="table",
            table_data=data,
            caption="Sales Data",
            footer=footer,
        )

        result = await table_tool.function(context, table)

        assert result.return_value is not None
        assert "Successfully created table" in result.return_value
        assert "ui_element" in result.metadata
        assert result.metadata["component_type"] == "table"

    @pytest.mark.asyncio
    async def test_create_table_tool_tsx_mode(self):
        """Test table creation tool in TSX mode."""
        MODEL = TestModel()
        shadcn = Shadcn("tsx")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        table_tool = next(t for t in tools_list if t.name == "create_table")

        data = TableData(headers=["Name", "Value"], rows=[("Item 1", 100)])
        footer = TableFooter(keyword="Total", header_to_summarize="Value", value=100)
        table = Table(
            component_type="table",
            table_data=data,
            caption="Sales Data",
            footer=footer,
        )

        result = await table_tool.function(context, table)

        assert result.return_value is not None
        assert "ui_element" in result.metadata
        ui_element = result.metadata["ui_element"]
        assert isinstance(ui_element, str)
        assert "use client" in ui_element


class TestCreateAccordionTool:
    """Tests for the create_accordion tool function."""

    @pytest.mark.asyncio
    async def test_create_accordion_tool_json_mode(self):
        """Test accordion creation tool in JSON mode."""
        MODEL = TestModel()
        shadcn = Shadcn("json")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        accordion_tool = next(t for t in tools_list if t.name == "create_accordion")

        items = [
            AccordionItem(
                component_type="accordion_item",
                value="item-1",
                trigger="What is React?",
                content="React is a JavaScript library for building user interfaces.",
            )
        ]
        accordion = Accordion(
            component_type="accordion",
            items=items,
            list_type="single",
        )

        result = await accordion_tool.function(context, accordion)

        assert result.return_value is not None
        assert "Successfully created an accordion" in result.return_value
        assert "ui_element" in result.metadata

    @pytest.mark.asyncio
    async def test_create_accordion_tool_tsx_mode(self):
        """Test accordion creation tool in TSX mode."""
        MODEL = TestModel()
        shadcn = Shadcn("tsx")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        accordion_tool = next(t for t in tools_list if t.name == "create_accordion")

        items = [
            AccordionItem(
                component_type="accordion_item",
                value="item-1",
                trigger="What is React?",
                content="React is a JavaScript library for building user interfaces.",
            )
        ]
        accordion = Accordion(
            component_type="accordion",
            items=items,
            list_type="single",
        )

        result = await accordion_tool.function(context, accordion)

        assert result.return_value is not None
        ui_element = result.metadata["ui_element"]
        assert isinstance(ui_element, str)
        assert "Accordion" in ui_element


class TestCreateCardTool:
    """Tests for the create_card tool function."""

    @pytest.mark.asyncio
    async def test_create_card_tool_json_mode(self):
        """Test card creation tool in JSON mode."""
        MODEL = TestModel()
        shadcn = Shadcn("json")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        card_tool = next(t for t in tools_list if t.name == "create_card")

        card = Card(
            component_type="card",
            title="Welcome Card",
            description="This is a sample card",
            content="Card content goes here.",
            footer="Card footer text",
        )

        result = await card_tool.function(context, card)

        assert result.return_value is not None
        assert "Successfully created card component" in result.return_value
        assert "ui_element" in result.metadata

    @pytest.mark.asyncio
    async def test_create_card_tool_tsx_mode(self):
        """Test card creation tool in TSX mode."""
        MODEL = TestModel()
        shadcn = Shadcn("tsx")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        card_tool = next(t for t in tools_list if t.name == "create_card")

        card = Card(
            component_type="card",
            title="Welcome Card",
            description="This is a sample card",
            content="Card content goes here.",
            footer="Card footer text",
        )

        result = await card_tool.function(context, card)

        assert result.return_value is not None
        ui_element = result.metadata["ui_element"]
        assert isinstance(ui_element, str)
        assert "Card" in ui_element


class TestCreateCarouselTool:
    """Tests for the create_carousel tool function."""

    @pytest.mark.asyncio
    async def test_create_carousel_tool_json_mode(self):
        """Test carousel creation tool in JSON mode."""
        MODEL = TestModel()
        shadcn = Shadcn("json")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        carousel_tool = next(t for t in tools_list if t.name == "create_carousel")

        items = [
            CarouselItem(
                component_type="carousel_item",
                content="Slide 1: Welcome to our showcase",
            )
        ]
        config = CarouselConfig()
        carousel = Carousel(
            component_type="carousel",
            items=items,
            config=config,
        )

        result = await carousel_tool.function(context, carousel)

        assert result.return_value is not None
        assert "Successfully created carousel component" in result.return_value
        assert "ui_element" in result.metadata

    @pytest.mark.asyncio
    async def test_create_carousel_tool_tsx_mode(self):
        """Test carousel creation tool in TSX mode."""
        MODEL = TestModel()
        shadcn = Shadcn("tsx")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        carousel_tool = next(t for t in tools_list if t.name == "create_carousel")

        items = [
            CarouselItem(
                component_type="carousel_item",
                content="Slide 1: Welcome to our showcase",
            )
        ]
        config = CarouselConfig()
        carousel = Carousel(
            component_type="carousel",
            items=items,
            config=config,
        )

        result = await carousel_tool.function(context, carousel)

        assert result.return_value is not None
        ui_element = result.metadata["ui_element"]
        assert isinstance(ui_element, str)
        assert "Carousel" in ui_element


class TestCreateChartTool:
    """Tests for the create_chart tool function."""

    @pytest.mark.asyncio
    async def test_create_chart_tool_json_mode(self):
        """Test chart creation tool in JSON mode."""
        MODEL = TestModel()
        shadcn = Shadcn("json")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        chart_tool = next(t for t in tools_list if t.name == "create_chart")

        config = ChartConfig(
            config={
                "desktop": {"label": "Desktop", "color": "#2563eb"},
                "mobile": {"label": "Mobile", "color": "#60a5fa"},
            }
        )
        data = ChartData(
            data=[
                {"month": "January", "desktop": 186, "mobile": 80},
                {"month": "February", "desktop": 305, "mobile": 90},
            ]
        )
        metadata = ChartMetadata(title="Sales Overview")
        chart = Chart(
            component_type="chart",
            chart_type="bar",
            metadata=metadata,
            chart_config=config,
            chart_data=data,
            x_axis_key="month",
        )

        result = await chart_tool.function(context, chart)

        assert result.return_value is not None
        assert "Successfully created chart" in result.return_value
        assert "ui_element" in result.metadata

    @pytest.mark.asyncio
    async def test_create_chart_tool_tsx_mode(self):
        """Test chart creation tool in TSX mode."""
        MODEL = TestModel()
        shadcn = Shadcn("tsx")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        chart_tool = next(t for t in tools_list if t.name == "create_chart")

        config = ChartConfig(
            config={
                "desktop": {"label": "Desktop", "color": "#2563eb"},
                "mobile": {"label": "Mobile", "color": "#60a5fa"},
            }
        )
        data = ChartData(
            data=[
                {"month": "January", "desktop": 186, "mobile": 80},
                {"month": "February", "desktop": 305, "mobile": 90},
            ]
        )
        metadata = ChartMetadata(title="Sales Overview")
        chart = Chart(
            component_type="chart",
            chart_type="bar",
            metadata=metadata,
            chart_config=config,
            chart_data=data,
            x_axis_key="month",
        )

        result = await chart_tool.function(context, chart)

        assert result.return_value is not None
        ui_element = result.metadata["ui_element"]
        assert isinstance(ui_element, str)
        assert "BarChart" in ui_element

    @pytest.mark.asyncio
    async def test_create_pie_chart_tool(self):
        """Test pie chart creation tool."""
        MODEL = TestModel()
        shadcn = Shadcn("tsx")
        deps = EngineDeps(engine=shadcn)
        context = RunContext(model=MODEL, usage=RunUsage(), deps=deps)

        toolset = create_ui_toolset()
        tools_list = (
            list(toolset.tools.values()) if isinstance(toolset.tools, dict) else toolset.tools
        )
        chart_tool = next(t for t in tools_list if t.name == "create_chart")

        config = ChartConfig(
            config={
                "chrome": {"label": "Chrome", "color": "var(--chart-1)"},
                "safari": {"label": "Safari", "color": "var(--chart-2)"},
            }
        )
        data = ChartData(
            data=[
                {"browser": "Chrome", "value": 275},
                {"browser": "Safari", "value": 200},
            ]
        )
        metadata = ChartMetadata(title="Browser Usage")
        chart = Chart(
            component_type="chart",
            chart_type="pie",
            metadata=metadata,
            chart_config=config,
            chart_data=data,
            x_axis_key="browser",
        )

        result = await chart_tool.function(context, chart)

        assert result.return_value is not None
        ui_element = result.metadata["ui_element"]
        assert isinstance(ui_element, str)
        assert "PieChart" in ui_element
