"""Tests for protocol module."""

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
    CarouselOrientation,
)
from charts.engines.shadcn import Shadcn
from charts.protocol import EngineProtocol


class TestEngineProtocol:
    """Tests for the EngineProtocol class."""

    def test_protocol_has_name_attribute(self):
        """Test that EngineProtocol has a name attribute."""
        assert hasattr(EngineProtocol, "__annotations__")

    def test_protocol_has_return_mode_attribute(self):
        """Test that EngineProtocol has a return_mode attribute."""
        annotations = EngineProtocol.__annotations__
        # Check that the protocol defines required attributes
        assert "name" in annotations or hasattr(EngineProtocol, "name")
        assert "return_mode" in annotations

    def test_protocol_has_config_attribute(self):
        """Test that EngineProtocol has a config attribute."""
        annotations = EngineProtocol.__annotations__
        assert "config" in annotations or hasattr(EngineProtocol, "config")

    def test_protocol_has_render_table_component_method(self):
        """Test that EngineProtocol defines render_table_component method."""
        assert hasattr(EngineProtocol, "render_table_component")
        import inspect

        sig = inspect.signature(EngineProtocol.render_table_component)
        assert "table" in sig.parameters
        assert sig.return_annotation is str

    def test_protocol_has_render_accordion_component_method(self):
        """Test that EngineProtocol defines render_accordion_component method."""
        assert hasattr(EngineProtocol, "render_accordion_component")
        import inspect

        sig = inspect.signature(EngineProtocol.render_accordion_component)
        assert "accordion" in sig.parameters
        assert sig.return_annotation is str

    def test_protocol_has_render_card_component_method(self):
        """Test that EngineProtocol defines render_card_component method."""
        assert hasattr(EngineProtocol, "render_card_component")
        import inspect

        sig = inspect.signature(EngineProtocol.render_card_component)
        assert "card" in sig.parameters
        assert sig.return_annotation is str

    def test_protocol_has_render_carousel_component_method(self):
        """Test that EngineProtocol defines render_carousel_component method."""
        assert hasattr(EngineProtocol, "render_carousel_component")
        import inspect

        sig = inspect.signature(EngineProtocol.render_carousel_component)
        assert "carousel" in sig.parameters
        assert sig.return_annotation is str

    def test_protocol_has_render_chart_component_method(self):
        """Test that EngineProtocol defines render_chart_component method."""
        assert hasattr(EngineProtocol, "render_chart_component")
        import inspect

        sig = inspect.signature(EngineProtocol.render_chart_component)
        assert "chart" in sig.parameters
        assert sig.return_annotation is str


class TestShadcnImplementation:
    """Tests to verify Shadcn implements EngineProtocol."""

    @pytest.mark.asyncio
    async def test_shadcn_implements_render_table(self):
        """Test that Shadcn implements render_table_component."""

        shadcn = Shadcn("tsx")
        assert hasattr(shadcn, "render_table_component")

        table = BaseTable(
            component_type="table",
            table_data=BaseTableData(headers=["col1"], rows=[(1,)]),
            caption="Test Table",
        )
        result = await shadcn.render_table_component(table)
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_shadcn_implements_render_accordion(self):
        """Test that Shadcn implements render_accordion_component."""

        shadcn = Shadcn("tsx")
        assert hasattr(shadcn, "render_accordion_component")

        accordion = BaseAccordion(
            component_type="accordion",
            items=[
                BaseAccordionItem(
                    component_type="accordion_item",
                    value="item-1",
                    trigger="Trigger 1",
                    content="Content 1",
                )
            ],
            list_type=BaseAccordionTypes.single,
        )
        result = await shadcn.render_accordion_component(accordion)
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_shadcn_implements_render_card(self):
        """Test that Shadcn implements render_card_component."""

        shadcn = Shadcn("tsx")
        assert hasattr(shadcn, "render_card_component")

        card = BaseCard(
            component_type="card",
            title="Test Card",
            description="Description",
            content="Content",
            footer="Footer",
        )
        result = await shadcn.render_card_component(card)
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_shadcn_implements_render_carousel(self):
        """Test that Shadcn implements render_carousel_component."""

        shadcn = Shadcn("tsx")
        assert hasattr(shadcn, "render_carousel_component")

        carousel = BaseCarousel(
            component_type="carousel",
            items=[BaseCarouselItem(component_type="carousel_item", content="Slide 1")],
            config=BaseCarouselConfig(orientation=CarouselOrientation.vertical),
        )
        result = await shadcn.render_carousel_component(carousel)
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_shadcn_implements_render_chart(self):
        """Test that Shadcn implements render_chart_component."""

        shadcn = Shadcn("tsx")
        assert hasattr(shadcn, "render_chart_component")

        chart = BaseChart(
            component_type="chart",
            chart_type=BaseChartTypes.bar,
            metadata=BaseChartMetadata(),
            chart_config=BaseChartConfig(),
            chart_data=BaseChartData(),
            x_axis_key="month",
        )
        result = await shadcn.render_chart_component(chart)
        assert isinstance(result, str)
