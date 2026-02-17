"""Tests for shadcn type classes."""

import pytest

from charts.base_types import BaseChartTypes
from charts.types.shadcn.accordion import Accordion, AccordionItem
from charts.types.shadcn.card import Card
from charts.types.shadcn.carousel import Carousel, CarouselConfig, CarouselItem
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData, ChartMetadata
from charts.types.shadcn.table import Table, TableData, TableFooter


class TestChartMetadata:
    """Tests for the ChartMetadata class."""

    def test_custom_metadata(self):
        """Test custom chart metadata values."""
        metadata = ChartMetadata(
            title="Sales Report",
            subtitle="Q1 2024",
            description="Quarterly sales performance report",
        )
        assert metadata.title == "Sales Report"
        assert metadata.subtitle == "Q1 2024"
        assert metadata.description == "Quarterly sales performance report"


class TestChartConfig:
    """Tests for the ChartConfig class."""

    def test_bar_line_area_radar_config(self):
        """Test chart config format for bar/line/area/radar charts."""
        config = ChartConfig(
            config={
                "desktop": {"label": "Desktop", "color": "#2563eb"},
                "mobile": {"label": "Mobile", "color": "#60a5fa"},
            }
        )
        assert len(config.config) == 2
        assert config.config["desktop"]["label"] == "Desktop"
        assert config.config["desktop"]["color"] == "#2563eb"

    def test_pie_config(self):
        """Test chart config format for pie charts."""
        config = ChartConfig(
            config={
                "chrome": {"label": "Chrome", "color": "var(--chart-1)"},
                "safari": {"label": "Safari", "color": "var(--chart-2)"},
            }
        )
        assert len(config.config) == 2
        assert config.config["chrome"]["label"] == "Chrome"


class TestChartData:
    """Tests for the ChartData class."""

    def test_bar_line_area_radar_data(self):
        """Test chart data format for bar/line/area/radar charts."""
        data = ChartData(
            data=[
                {"month": "Jan", "desktop": 100, "mobile": 80},
                {"month": "Feb", "desktop": 120, "mobile": 90},
            ]
        )
        assert len(data.data) == 2
        assert data.data[0]["month"] == "Jan"
        assert data.data[0]["desktop"] == 100

    def test_pie_data(self):
        """Test chart data format for pie charts."""
        data = ChartData(
            data=[
                {"category": "Chrome", "value": 275},
                {"category": "Safari", "value": 200},
            ]
        )
        assert len(data.data) == 2
        assert data.data[0]["category"] == "Chrome"
        assert data.data[0]["value"] == 275


class TestChart:
    """Tests for the Chart class."""

    def test_x_axis_key_validation_valid(self):
        """Test that valid x_axis_key passes validation."""
        config = ChartConfig(
            config={
                "desktop": {"label": "Desktop", "color": "#2563eb"},
                "mobile": {"label": "Mobile", "color": "#60a5fa"},
            }
        )
        data = ChartData(
            data=[
                {"month": "Jan", "desktop": 100, "mobile": 80},
            ]
        )
        metadata = ChartMetadata()
        chart = Chart(
            component_type="chart",
            chart_type=BaseChartTypes.bar,
            metadata=metadata,
            chart_config=config,
            chart_data=data,
            x_axis_key="month",
        )
        assert chart.x_axis_key == "month"

    def test_x_axis_key_validation_invalid(self):
        """Test that invalid x_axis_key raises ValueError."""
        config = ChartConfig(
            config={
                "desktop": {"label": "Desktop", "color": "#2563eb"},
            }
        )
        data = ChartData(data=[{"month": "Jan", "desktop": 100}])
        metadata = ChartMetadata()

        with pytest.raises(ValueError) as exc_info:
            Chart(
                component_type="chart",
                chart_type=BaseChartTypes.bar,
                metadata=metadata,
                chart_config=config,
                chart_data=data,
                x_axis_key="invalid_key",
            )

        # Use a more flexible assertion
        error_msg = str(exc_info.value)
        assert "x_axis_key 'invalid_key'" in error_msg
        assert "data keys" in error_msg

    def test_no_chart_data(self):
        """Test absence of chart data in model."""
        config = ChartConfig(
            config={
                "desktop": {"label": "Desktop", "color": "#2563eb"},
            }
        )
        data = ChartData()
        metadata = ChartMetadata()
        with pytest.raises(ValueError) as exc_info:
            Chart(
                component_type="chart",
                chart_type=BaseChartTypes.bar,
                metadata=metadata,
                chart_config=config,
                chart_data=data,
                x_axis_key="invalid_key",
            )

        error_msg = str(exc_info.value)
        assert "chart_data must contain at least one row of data." in error_msg


class TestTableData:
    """Tests for the TableData class."""

    def test_custom_data(self):
        """Test custom table data."""
        data = TableData(
            headers=["Name", "Value", "Status"],
            rows=[
                ("Item 1", "100", "Active"),
                ("Item 2", "250", "Pending"),
            ],
        )
        assert len(data.headers) == 3
        assert len(data.rows) == 2
        assert data.headers[0] == "Name"


class TestTableFooter:
    """Tests for the TableFooter class."""

    def test_custom_footer(self):
        """Test custom table footer."""
        footer = TableFooter(
            keyword="Sum",
            header_to_summarize="count",
            value=None,
        )
        assert footer.keyword == "Sum"
        assert footer.header_to_summarize == "count"
        assert footer.value is None


class TestTable:
    """Tests for the Table class."""

    def test_component_type(self):
        """Test that Table has correct component type."""
        data = TableData(headers=["col1"], rows=[(1,)])
        table = Table(
            component_type="table",
            table_data=data,
            caption="Test Table",
        )
        assert table.component_type == "table"


class TestAccordionItem:
    """Tests for the AccordionItem class."""

    def test_custom_item(self):
        """Test custom accordion item."""
        item = AccordionItem(
            component_type="accordion_item",
            value="faq-1",
            trigger="What is React?",
            content="React is a JavaScript library for building user interfaces.",
        )
        assert item.value == "faq-1"
        assert item.trigger == "What is React?"


class TestAccordion:
    """Tests for the Accordion class."""

    def test_single_type(self):
        """Test accordion with single expansion type."""
        items = [
            AccordionItem(
                component_type="accordion_item",
                value="item-1",
                trigger="Trigger 1",
                content="Content 1",
            )
        ]
        accordion = Accordion(
            component_type="accordion",
            items=items,
            list_type="single",
        )
        assert accordion.list_type == "single"

    def test_multiple_type(self):
        """Test accordion with multiple expansion type."""
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
        assert accordion.list_type == "multiple"
        assert len(accordion.items) == 2


class TestCard:
    """Tests for the Card class."""

    def test_default_values(self):
        """Test card with minimal required fields."""
        card = Card(
            component_type="card",
            title="Title",
            description="Description",
            content=None,
            footer="Footer",
        )
        assert card.title == "Title"
        assert card.description == "Description"
        assert card.content is None
        assert card.footer == "Footer"


class TestCarouselItem:
    """Tests for the CarouselItem class."""

    def test_text_content(self):
        """Test carousel item with text content."""
        item = CarouselItem(
            component_type="carousel_item",
            content="Welcome to our showcase",
        )
        assert item.content == "Welcome to our showcase"

    def test_card_content(self):
        """Test carousel item with card content."""
        card = Card(
            component_type="card",
            title="Featured Product",
            description="Best seller",
            content="Product details here",
            footer="$99.99",
        )
        item = CarouselItem(
            component_type="carousel_item",
            content=card,
        )
        assert item.content == card


class TestCarouselConfig:
    """Tests for the CarouselConfig class."""

    def test_default_config(self):
        """Test default carousel configuration."""
        config = CarouselConfig()
        assert config.align == "start"
        assert config.loop == "true"

    def test_custom_config(self):
        """Test custom carousel configuration."""
        from charts.base_types import CarouselOrientation

        config = CarouselConfig(
            align=None,
            loop="false",
            orientation=CarouselOrientation.vertical,
            container_class="max-w-md",
        )
        assert config.align is None
        assert config.loop == "false"
        assert config.orientation.value == "vertical"


class TestCarousel:
    """Tests for the Carousel class."""

    def test_single_item_wrap_in_list(self):
        """Test that single item is wrapped in list."""
        item = CarouselItem(
            component_type="carousel_item",
            content="Single slide",
        )
        carousel = Carousel(
            component_type="carousel",
            items=item,  # Single item, not a list
            config=CarouselConfig(),
        )
        assert isinstance(carousel.items, list)
        assert len(carousel.items) == 1

    def test_multiple_items(self):
        """Test carousel with multiple items."""
        items = [
            CarouselItem(
                component_type="carousel_item",
                content="Slide 1",
            ),
            CarouselItem(
                component_type="carousel_item",
                content="Slide 2",
            ),
        ]
        carousel = Carousel(
            component_type="carousel",
            items=items,
            config=CarouselConfig(),
        )
        assert isinstance(carousel.items, list)
        assert len(carousel.items) == 2

    def test_loop_configuration(self):
        """Test carousel loop configuration."""
        items = [
            CarouselItem(
                component_type="carousel_item",
                content="Slide 1",
            )
        ]
        carousel = Carousel(
            component_type="carousel",
            items=items,
            config=CarouselConfig(loop="false"),
        )
        assert carousel.config.loop == "false"
