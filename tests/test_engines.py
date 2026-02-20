"""Tests for engines module."""

from typing import cast

import pytest

from charts.base_types import (
    BaseAccordion,
    BaseAccordionItem,
    BaseAccordionTypes,
    BaseCard,
    BaseCarousel,
    BaseCarouselConfig,
    BaseCarouselItem,
    BaseChart,
    BaseChartConfig,
    BaseChartData,
    BaseChartMetadata,
    BaseChartTypes,
    BaseTable,
    BaseTableData,
    BaseTableFooter,
    CarouselOrientation,
)
from charts.engines.shadcn import Shadcn
from charts.types.shadcn.accordion import Accordion, AccordionItem
from charts.types.shadcn.card import Card
from charts.types.shadcn.carousel import Carousel, CarouselConfig, CarouselItem
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData, ChartMetadata
from charts.types.shadcn.table import TableFooter


class TestShadcnInitialization:
    """Tests for Shadcn engine initialization."""

    def test_shadcn_json_mode(self) -> None:
        """Test Shadcn initialization in JSON mode."""
        shadcn = Shadcn("json")
        assert shadcn.name == "shadcn"
        assert shadcn.return_mode == "json"

    def test_shadcn_tsx_mode(self) -> None:
        """Test Shadcn initialization in TSX mode."""
        shadcn = Shadcn("tsx")
        assert shadcn.name == "shadcn"
        assert shadcn.return_mode == "tsx"

    def test_get_chart_template_error(self) -> None:
        """Test `_get_chart_template` error handling,"""
        shadcn = Shadcn("json")
        bad_type = cast(BaseChartTypes, "random")  # Force an invalid chart type
        result = shadcn._get_chart_template(bad_type)
        assert result == "Unknown chart type"


class TestShadcnRenderTableComponent:
    """Tests for Shadcn render_table_component method."""

    @pytest.mark.asyncio
    async def test_render_table_json_mode(self):
        """Test table rendering in JSON mode."""
        shadcn = Shadcn("json")
        data = BaseTableData(headers=["col1"], rows=[(1,)])
        footer = BaseTableFooter(keyword="Total", header_to_summarize="col1", value=1)
        table = BaseTable(
            component_type="table",
            table_data=data,
            caption="Test Table",
            footer=footer,
        )
        result = await shadcn.render_table_component(table)
        assert isinstance(result, str)
        import json

        parsed = json.loads(result)
        assert parsed["caption"] == "Test Table"

    @pytest.mark.asyncio
    async def test_render_table_tsx_mode(self):
        """Test table rendering in TSX mode."""
        shadcn = Shadcn("tsx")
        data = BaseTableData(headers=["Name", "Value"], rows=[("Item 1", 100)])
        footer = TableFooter(keyword="Total", header_to_summarize="Value", value=100)
        table = BaseTable(
            component_type="table",
            table_data=data,
            caption="Sales Data",
            footer=footer,
        )
        result = await shadcn.render_table_component(table)
        assert isinstance(result, str)
        assert "use client" in result
        assert "Table" in result

    @pytest.mark.asyncio
    async def test_render_table_with_footer_calculation(self):
        """Test table rendering with footer value calculation."""
        shadcn = Shadcn("tsx")
        data = BaseTableData(headers=["month", "amount"], rows=[("Jan", 100), ("Feb", 200)])
        footer = TableFooter(keyword="Total", header_to_summarize="amount", value=None)
        table = BaseTable(
            component_type="table",
            table_data=data,
            caption="Monthly Sales",
            footer=footer,
        )
        result = await shadcn.render_table_component(table)
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_render_table_invalid_footer_values(self):
        """Test table rendering with invalid footer values."""
        shadcn = Shadcn("tsx")
        data = BaseTableData(headers=["col1", "col2"], rows=[("a", "not_a_number"), ("b", "apple")])
        footer = TableFooter(keyword="Sum", header_to_summarize="XAZ", value=None)
        table = BaseTable(
            component_type="table",
            table_data=data,
            caption="Invalid Footer Table",
            footer=footer,
        )
        result = await shadcn.render_table_component(table)
        assert isinstance(result, str)
        assert "<TableFooter>" not in result

    @pytest.mark.asyncio
    async def test_render_table_invalid_sum_values(self):
        """Test table rendering with invalid footer values."""
        shadcn = Shadcn("tsx")
        data = BaseTableData(headers=["col1", "col2"], rows=[("a", "not_a_number"), ("b", "apple")])
        footer = TableFooter(keyword="Sum", header_to_summarize="col2", value=None)
        table = BaseTable(
            component_type="table",
            table_data=data,
            caption="Invalid Footer Table",
            footer=footer,
        )
        result = await shadcn.render_table_component(table)
        assert isinstance(result, str)


class TestShadcnRenderAccordionComponent:
    """Tests for Shadcn render_accordion_component method."""

    @pytest.mark.asyncio
    async def test_render_accordion_json_mode(self):
        """Test accordion rendering in JSON mode."""
        shadcn = Shadcn("json")
        items = [
            BaseAccordionItem(
                component_type="accordion_item",
                value="item-1",
                trigger="Trigger 1",
                content="Content 1",
            )
        ]
        accordion = BaseAccordion(
            component_type="accordion",
            items=items,
            list_type=BaseAccordionTypes.single,
        )
        result = await shadcn.render_accordion_component(accordion)
        assert isinstance(result, str)
        import json

        parsed = json.loads(result)
        assert len(parsed["items"]) == 1

    @pytest.mark.asyncio
    async def test_render_accordion_tsx_mode(self):
        """Test accordion rendering in TSX mode."""
        shadcn = Shadcn("tsx")
        items = [
            AccordionItem(
                component_type="accordion_item",
                value="faq-1",
                trigger="What is React?",
                content="React is a JavaScript library for building user interfaces.",
            )
        ]
        accordion = Accordion(
            component_type="accordion",
            items=items,
            list_type="single",
        )
        result = await shadcn.render_accordion_component(accordion)
        assert isinstance(result, str)
        assert "use client" in result
        assert "Accordion" in result

    @pytest.mark.asyncio
    async def test_render_accordion_multiple_items(self):
        """Test accordion rendering with multiple items."""
        shadcn = Shadcn("tsx")
        items = [
            AccordionItem(
                component_type="accordion_item",
                value="item-1",
                trigger="Trigger 1",
                content="Content 1",
            ),
            AccordionItem(
                component_type="accordion_item",
                value="item-2",
                trigger="Trigger 2",
                content="Content 2",
            ),
        ]
        accordion = Accordion(
            component_type="accordion",
            items=items,
            list_type="multiple",
        )
        result = await shadcn.render_accordion_component(accordion)
        assert isinstance(result, str)


class TestShadcnRenderCardComponent:
    """Tests for Shadcn render_card_component method."""

    @pytest.mark.asyncio
    async def test_render_card_json_mode(self):
        """Test card rendering in JSON mode."""
        shadcn = Shadcn("json")
        card = BaseCard(
            component_type="card",
            title="Test Card",
            description="Description",
            content="Content",
            footer="Footer",
        )
        result = await shadcn.render_card_component(card)
        assert isinstance(result, str)
        import json

        parsed = json.loads(result)
        assert parsed["title"] == "Test Card"

    @pytest.mark.asyncio
    async def test_render_card_tsx_mode(self):
        """Test card rendering in TSX mode."""
        shadcn = Shadcn("tsx")
        card = BaseCard(
            component_type="card",
            title="Welcome Card",
            description="This is a sample card",
            content="Card content goes here.",
            footer="Card footer text",
        )
        result = await shadcn.render_card_component(card)
        assert isinstance(result, str)
        assert "use client" in result
        assert "Card" in result

    @pytest.mark.asyncio
    async def test_render_card_with_none_content(self):
        """Test card rendering with None content."""
        shadcn = Shadcn("tsx")
        card = BaseCard(
            component_type="card",
            title="Minimal Card",
            description="Description",
            content=None,
            footer="Footer",
        )
        result = await shadcn.render_card_component(card)
        assert isinstance(result, str)


class TestShadcnRenderCarouselComponent:
    """Tests for Shadcn render_carousel_component method."""

    @pytest.mark.asyncio
    async def test_render_carousel_json_mode(self):
        """Test carousel rendering in JSON mode."""
        shadcn = Shadcn("json")
        items = [
            BaseCarouselItem(
                component_type="carousel_item",
                content="Slide 1",
            )
        ]
        config = BaseCarouselConfig()
        carousel = BaseCarousel(
            component_type="carousel",
            items=items,
            config=config,
        )
        result = await shadcn.render_carousel_component(carousel)
        assert isinstance(result, str)
        import json

        parsed = json.loads(result)
        assert len(parsed["items"]) == 1

    @pytest.mark.asyncio
    async def test_render_carousel_tsx_mode(self):
        """Test carousel rendering in TSX mode."""
        shadcn = Shadcn("tsx")
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
        result = await shadcn.render_carousel_component(carousel)
        assert isinstance(result, str)
        assert "use client" in result
        assert "Carousel" in result

    @pytest.mark.asyncio
    async def test_render_carousel_with_card_content(self):
        """Test carousel rendering with card content."""
        shadcn = Shadcn("tsx")
        card = Card(
            component_type="card",
            title="Featured Product",
            description="Best seller",
            content="Product details here",
            footer="$99.99",
        )
        items = [
            CarouselItem(
                component_type="carousel_item",
                content=card,
            )
        ]
        config = CarouselConfig()
        carousel = Carousel(
            component_type="carousel",
            items=items,
            config=config,
        )
        result = await shadcn.render_carousel_component(carousel)
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_render_carousel_vertical_orientation(self):
        """Test carousel rendering with vertical orientation."""

        shadcn = Shadcn("tsx")
        items = [
            CarouselItem(
                component_type="carousel_item",
                content="Slide 1",
            )
        ]
        config = CarouselConfig(orientation=CarouselOrientation.vertical)
        carousel = Carousel(
            component_type="carousel",
            items=items,
            config=config,
        )
        result = await shadcn.render_carousel_component(carousel)
        assert isinstance(result, str)


class TestShadcnRenderChartComponent:
    """Tests for Shadcn render_chart_component method."""

    @pytest.mark.asyncio
    async def test_render_chart_json_mode(self):
        """Test chart rendering in JSON mode."""
        shadcn = Shadcn("json")
        config = BaseChartConfig(config={})
        data = BaseChartData(data=[])
        metadata = BaseChartMetadata()
        chart = BaseChart(
            component_type="chart",
            chart_type=BaseChartTypes.bar,
            metadata=metadata,
            chart_config=config,
            chart_data=data,
            x_axis_key="month",
        )
        result = await shadcn.render_chart_component(chart)
        assert isinstance(result, str)
        import json

        parsed = json.loads(result)
        assert parsed["chart_type"] == "bar"

    @pytest.mark.asyncio
    async def test_render_bar_chart_tsx_mode(self):
        """Test bar chart rendering in TSX mode."""
        shadcn = Shadcn("tsx")
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
            chart_type=BaseChartTypes.bar,
            metadata=metadata,
            chart_config=config,
            chart_data=data,
            x_axis_key="month",
        )
        result = await shadcn.render_chart_component(chart)
        assert isinstance(result, str)
        assert "use client" in result
        assert "BarChart" in result

    @pytest.mark.asyncio
    async def test_render_line_chart_tsx_mode(self):
        """Test line chart rendering in TSX mode."""
        shadcn = Shadcn("tsx")
        config = ChartConfig(
            config={
                "desktop": {"label": "Desktop", "color": "#2563eb"},
            }
        )
        data = ChartData(data=[{"month": "Jan", "desktop": 100}])
        metadata = ChartMetadata()
        chart = Chart(
            component_type="chart",
            chart_type=BaseChartTypes.line,
            metadata=metadata,
            chart_config=config,
            chart_data=data,
            x_axis_key="month",
        )
        result = await shadcn.render_chart_component(chart)
        assert isinstance(result, str)
        assert "LineChart" in result

    @pytest.mark.asyncio
    async def test_render_pie_chart_tsx_mode(self):
        """Test pie chart rendering in TSX mode."""
        shadcn = Shadcn("tsx")
        config = ChartConfig(
            config={
                "chrome": {"label": "Chrome", "color": "var(--chart-1)"},
                "safari": {"label": "Safari", "color": "var(--chart-2)"},
            }
        )
        data = ChartData(
            data=[
                {"browser": "Chrome", "value": 275, "fill": "var(--chart-1)"},
                {"browser": "Safari", "value": 200, "fill": "var(--chart-2)"},
            ]
        )
        metadata = ChartMetadata(title="Browser Usage")
        chart = Chart(
            component_type="chart",
            chart_type=BaseChartTypes.pie,
            metadata=metadata,
            chart_config=config,
            chart_data=data,
            x_axis_key="browser",
        )
        result = await shadcn.render_chart_component(chart)
        assert isinstance(result, str)
        assert "PieChart" in result

    @pytest.mark.asyncio
    async def test_render_area_chart_tsx_mode(self):
        """Test area chart rendering in TSX mode."""
        shadcn = Shadcn("tsx")
        config = ChartConfig(
            config={
                "desktop": {"label": "Desktop", "color": "#2563eb"},
            }
        )
        data = ChartData(data=[{"month": "Jan", "desktop": 100}])
        metadata = ChartMetadata()
        chart = Chart(
            component_type="chart",
            chart_type=BaseChartTypes.area,
            metadata=metadata,
            chart_config=config,
            chart_data=data,
            x_axis_key="month",
        )
        result = await shadcn.render_chart_component(chart)
        assert isinstance(result, str)
        assert "AreaChart" in result

    @pytest.mark.asyncio
    async def test_render_radar_chart_tsx_mode(self):
        """Test radar chart rendering in TSX mode."""
        shadcn = Shadcn("tsx")
        config = ChartConfig(
            config={
                "desktop": {"label": "Desktop", "color": "#2563eb"},
            }
        )
        data = ChartData(data=[{"month": "Jan", "desktop": 100}])
        metadata = ChartMetadata()
        chart = Chart(
            component_type="chart",
            chart_type=BaseChartTypes.radar,
            metadata=metadata,
            chart_config=config,
            chart_data=data,
            x_axis_key="month",
        )
        result = await shadcn.render_chart_component(chart)
        assert isinstance(result, str)
        assert "RadarChart" in result

    @pytest.mark.asyncio
    async def test_render_chart_unknown_type(self):
        """Test chart rendering with unknown chart type."""
        shadcn = Shadcn("tsx")
        config = ChartConfig(config={})
        data = ChartData(data=[])
        metadata = ChartMetadata()
        # Create a chart with an invalid type (will use default)
        chart = BaseChart(
            component_type="chart",
            chart_type=BaseChartTypes.bar,
            metadata=metadata,
            chart_config=config,
            chart_data=data,
            x_axis_key="month",
        )
        result = await shadcn.render_chart_component(chart)
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_render_chart_with_error_handling(self):
        """Test chart rendering with error handling."""
        shadcn = Shadcn("tsx")
        # Create a chart that might cause issues
        config = ChartConfig(config={})
        data = ChartData(data=[])
        metadata = ChartMetadata()
        chart = BaseChart(
            component_type="chart",
            chart_type=BaseChartTypes.bar,
            metadata=metadata,
            chart_config=config,
            chart_data=data,
            x_axis_key="month",
        )
        result = await shadcn.render_chart_component(chart)
        # Should handle gracefully even with minimal data
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_render_pie_chart_with_matching_x_label_color(self):
        """Test that pie chart correctly picks up colors from config matching the data labels."""
        shadcn = Shadcn("tsx")

        # The config key must match the VALUE found in the data's x_axis_key column
        config = ChartConfig(config={"January": {"label": "Jan", "color": "#ff0000"}})

        # x_axis_key is "month". The value at data["month"] is "January".
        data = ChartData(data=[{"month": "January", "visitors": 275}])
        metadata = ChartMetadata()
        chart = Chart(  # Use your Chart class
            component_type="chart",
            chart_type=BaseChartTypes.pie,
            metadata=metadata,
            chart_config=config,
            chart_data=data,
            x_axis_key="month",
        )

        result = await shadcn.render_chart_component(chart)

        assert isinstance(result, str)
        # Verify the specific hex code from your config ended up in the output
        assert "#ff0000" in result

    @pytest.mark.asyncio
    async def test_render_chart_template_not_found(self):
        """Test that if no valid template is found, a fallback string is returned."""
        shadcn = Shadcn("tsx")

        # Ensure the internal template mapping is missing this chart type
        # We can temporarily clear it or use a type you haven't defined a template for
        shadcn.CHART_TEMPLATES = {}

        config = ChartConfig(config={"desktop": {"label": "D", "color": "#000"}})
        data = ChartData(data=[{"month": "Jan", "desktop": 100}])

        chart = Chart(
            component_type="chart",
            chart_type=BaseChartTypes.bar,  # Any type works since we cleared the dict
            metadata=ChartMetadata(),
            chart_config=config,
            chart_data=data,
            x_axis_key="month",
        )

        # Call the method
        result = await shadcn.render_chart_component(chart)

        # 3Verification
        # _get_chart_template will return "Unknown chart type" (a string)
        # isinstance(template, Template) will be False
        assert result == "Chart could not be created"
