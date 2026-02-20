"""Tests for base types module."""

from charts.base_types import (
    BaseAccordion,
    BaseAccordionItem,
    BaseAccordionTypes,
    BaseAgentUIConfig,
    BaseCard,
    BaseCarousel,
    BaseCarouselConfig,
    BaseCarouselItem,
    BaseChart,
    BaseChartConfig,
    BaseChartData,
    BaseChartMetadata,
    BaseChartTypes,
    BaseColorPalette,
    BaseColors,
    BaseComponent,
    BaseLibraryConfig,
    BaseTable,
    BaseTableData,
    BaseTableFooter,
    BaseUIConfig,
    CarouselOrientation,
    CustomType,
)


class TestCustomType:
    """Tests for the CustomType base class."""

    def test_custom_type_instantiation(self):
        """Test that CustomType can be instantiated."""
        instance = CustomType()
        assert instance is not None

    def test_custom_type_config_dict(self):
        """Test that CustomType has the expected config dict settings."""
        instance = CustomType()
        # Check that arbitrary_types_allowed is True
        assert instance.model_config.get("arbitrary_types_allowed") is True
        # Check that populate_by_name is True
        assert instance.model_config.get("populate_by_name") is True


class TestBaseColors:
    """Tests for the BaseColors class."""

    def test_default_colors(self):
        """Test default color values."""
        colors = BaseColors()
        assert colors.primary == "#858586"
        assert colors.secondary == "#0FB1E2"
        assert colors.tertiary == "#E9E040"
        assert colors.success == "#33C819"
        assert colors.danger == "#EE8A19"
        assert colors.warning == "#D6E718"
        assert colors.error == "#FF0000"

    def test_default_neutral_colors(self):
        """Test default neutral color values."""
        colors = BaseColors()
        assert colors.background == "#FFFFFF"
        assert colors.surface == "#F4F4F5"
        assert colors.text == "#09090B"

    def test_custom_colors(self):
        """Test custom color values."""
        colors = BaseColors(
            primary="#FF0000",
            secondary="#00FF00",
            background="#000000",
        )
        assert colors.primary == "#FF0000"
        assert colors.secondary == "#00FF00"
        assert colors.background == "#000000"


class TestBaseColorPalette:
    """Tests for the BaseColorPalette class."""

    def test_default_palette(self):
        """Test default color palette."""
        palette = BaseColorPalette(
            light=BaseColors(),
            dark=BaseColors(),
        )
        assert palette.light is not None
        assert palette.dark is not None

    def test_custom_palette(self):
        """Test custom color palette."""
        light_colors = BaseColors(primary="#FF0000")
        dark_colors = BaseColors(primary="#0000FF")
        palette = BaseColorPalette(light=light_colors, dark=dark_colors)
        assert palette.light.primary == "#FF0000"
        assert palette.dark.primary == "#0000FF"


class TestBaseLibraryConfig:
    """Tests for the BaseLibraryConfig class."""

    def test_default_config(self):
        """Test default library configuration."""
        config = BaseLibraryConfig()
        assert config.framework == "react"
        assert config.library == "shadcn"
        assert config.is_package is False
        assert config.import_alias == "@/components"
        assert config.component_path == "ui"
        assert config.use_typescript is True
        assert config.styling_strategy == "tailwind"

    def test_custom_config(self):
        """Test custom library configuration."""
        config = BaseLibraryConfig(
            framework="react",
            library="shadcn",
            is_package=True,
            import_alias="@/ui",
            component_path="components/ui",
            use_typescript=False,
            styling_strategy="css-in-js",
        )
        assert config.framework == "react"
        assert config.library == "shadcn"
        assert config.is_package is True
        assert config.import_alias == "@/ui"
        assert config.component_path == "components/ui"
        assert config.use_typescript is False
        assert config.styling_strategy == "css-in-js"


class TestBaseUIConfig:
    """Tests for the BaseUIConfig class."""

    def test_default_config(self):
        """Test default UI configuration."""
        config = BaseUIConfig(
            color_palette=BaseColorPalette(light=BaseColors(), dark=BaseColors()),
        )
        assert config.mode == "system"
        assert config.radius == 0.5
        assert config.density == "comfortable"

    def test_custom_config(self):
        """Test custom UI configuration."""
        palette = BaseColorPalette(light=BaseColors(), dark=BaseColors())
        config = BaseUIConfig(
            color_palette=palette,
            mode="dark",
            radius=1.0,
            density="compact",
        )
        assert config.mode == "dark"
        assert config.radius == 1.0
        assert config.density == "compact"


class TestBaseAgentUIConfig:
    """Tests for the BaseAgentUIConfig class."""

    def test_default_config(self):
        """Test default agent UI configuration."""
        palette = BaseColorPalette(light=BaseColors(), dark=BaseColors())
        ui_config = BaseUIConfig(color_palette=palette)
        lib_config = BaseLibraryConfig()
        config = BaseAgentUIConfig(theme=ui_config, lib=lib_config)

        assert config.config_version == "0.1"
        assert config.overrides == {}

    def test_get_active_colors_light_mode(self):
        """Test get_active_colors in light mode."""
        palette = BaseColorPalette(light=BaseColors(), dark=BaseColors())
        ui_config = BaseUIConfig(color_palette=palette, mode="light")
        lib_config = BaseLibraryConfig()
        config = BaseAgentUIConfig(theme=ui_config, lib=lib_config)

        active_colors = config.get_active_colors()
        assert active_colors == palette.light

    def test_get_active_colors_dark_mode(self):
        """Test get_active_colors in dark mode."""
        light_colors = BaseColors(primary="#FFFFFF")
        dark_colors = BaseColors(primary="#000000")
        palette = BaseColorPalette(light=light_colors, dark=dark_colors)
        ui_config = BaseUIConfig(color_palette=palette, mode="dark")
        lib_config = BaseLibraryConfig()
        config = BaseAgentUIConfig(theme=ui_config, lib=lib_config)

        active_colors = config.get_active_colors()
        assert active_colors == palette.dark
        assert active_colors.primary == "#000000"

    def test_get_active_colors_system_mode(self):
        """Test get_active_colors in system mode (defaults to light)."""
        palette = BaseColorPalette(light=BaseColors(), dark=BaseColors())
        ui_config = BaseUIConfig(color_palette=palette, mode="system")
        lib_config = BaseLibraryConfig()
        config = BaseAgentUIConfig(theme=ui_config, lib=lib_config)

        active_colors = config.get_active_colors()
        assert active_colors == palette.light


class TestBaseComponent:
    """Tests for the BaseComponent class."""

    def test_component_type(self):
        """Test component type field."""
        component = BaseComponent(component_type="test")
        assert component.component_type == "test"


class TestBaseTableData:
    """Tests for the BaseTableData class."""

    def test_default_data(self):
        """Test default table data."""
        data = BaseTableData(headers=["col1", "col2"], rows=[(1, 2), (3, 4)])
        assert data.headers == ["col1", "col2"]
        assert len(data.rows) == 2
        assert data.rows[0] == (1, 2)

    def test_empty_rows(self):
        """Test table data with empty rows."""
        data = BaseTableData(headers=["col1"], rows=[])
        assert data.headers == ["col1"]
        assert len(data.rows) == 0


class TestBaseTableFooter:
    """Tests for the BaseTableFooter class."""

    def test_default_footer(self):
        """Test default table footer."""
        footer = BaseTableFooter(
            keyword="Total",
            header_to_summarize="amount",
            value=100,
        )
        assert footer.keyword == "Total"
        assert footer.header_to_summarize == "amount"
        assert footer.value == 100

    def test_none_value(self):
        """Test table footer with None value."""
        footer = BaseTableFooter(
            keyword="Sum",
            header_to_summarize="count",
            value=None,
        )
        assert footer.keyword == "Sum"
        assert footer.header_to_summarize == "count"
        assert footer.value is None


class TestBaseTable:
    """Tests for the BaseTable class."""

    def test_default_table(self):
        """Test default table."""
        data = BaseTableData(headers=["col1"], rows=[(1,)])
        footer = BaseTableFooter(keyword="Total", header_to_summarize="col1", value=1)
        table = BaseTable(
            component_type="table",
            table_data=data,
            caption="Test Table",
            footer=footer,
        )
        assert table.component_type == "table"
        assert table.caption == "Test Table"
        assert table.footer == footer

    def test_table_without_footer(self):
        """Test table without footer."""
        data = BaseTableData(headers=["col1"], rows=[(1,)])
        table = BaseTable(
            component_type="table",
            table_data=data,
            caption="Test Table",
        )
        assert table.footer is None


class TestBaseChartTypes:
    """Tests for the BaseChartTypes enum."""

    def test_chart_types(self):
        """Test all chart type values."""
        assert BaseChartTypes.bar.value == "bar"
        assert BaseChartTypes.line.value == "line"
        assert BaseChartTypes.pie.value == "pie"
        assert BaseChartTypes.area.value == "area"
        assert BaseChartTypes.radar.value == "radar"


class TestBaseChartMetadata:
    """Tests for the BaseChartMetadata class."""

    def test_default_metadata(self):
        """Test default chart metadata."""
        metadata = BaseChartMetadata()
        assert metadata.title is None
        assert metadata.subtitle is None
        assert metadata.description is None

    def test_custom_metadata(self):
        """Test custom chart metadata."""
        metadata = BaseChartMetadata(
            title="Sales Chart",
            subtitle="Q1 2024",
            description="Quarterly sales performance",
        )
        assert metadata.title == "Sales Chart"
        assert metadata.subtitle == "Q1 2024"
        assert metadata.description == "Quarterly sales performance"


class TestBaseChartConfig:
    """Tests for the BaseChartConfig class."""

    def test_default_config(self):
        """Test default chart config."""
        config = BaseChartConfig(config={})
        assert config.config == {}

    def test_custom_config(self):
        """Test custom chart config."""
        config = BaseChartConfig(
            config={
                "desktop": {"label": "Desktop", "color": "#2563eb"},
                "mobile": {"label": "Mobile", "color": "#60a5fa"},
            }
        )
        assert len(config.config) == 2
        assert config.config["desktop"]["label"] == "Desktop"


class TestBaseChartData:
    """Tests for the BaseChartData class."""

    def test_default_data(self):
        """Test default chart data."""
        data = BaseChartData(data=[])
        assert data.data == []

    def test_custom_data(self):
        """Test custom chart data."""
        data = BaseChartData(
            data=[
                {"month": "Jan", "value": 100},
                {"month": "Feb", "value": 200},
            ]
        )
        assert len(data.data) == 2
        assert data.data[0]["month"] == "Jan"


class TestBaseChart:
    """Tests for the BaseChart class."""

    def test_default_chart(self):
        """Test default chart."""
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
        assert chart.component_type == "chart"
        assert chart.chart_type == BaseChartTypes.bar
        assert chart.x_axis_key == "month"


class TestBaseAccordionTypes:
    """Tests for the BaseAccordionTypes enum."""

    def test_accordion_types(self):
        """Test accordion type values."""
        assert BaseAccordionTypes.single.value == "single"
        assert BaseAccordionTypes.multiple.value == "multiple"


class TestBaseAccordionItem:
    """Tests for the BaseAccordionItem class."""

    def test_default_item(self):
        """Test default accordion item."""
        item = BaseAccordionItem(
            component_type="accordion_item",
            value="item-1",
            trigger="Trigger text",
            content="Content text",
        )
        assert item.component_type == "accordion_item"
        assert item.value == "item-1"
        assert item.trigger == "Trigger text"
        assert item.content == "Content text"


class TestBaseAccordion:
    """Tests for the BaseAccordion class."""

    def test_default_accordion(self):
        """Test default accordion."""
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
        assert accordion.component_type == "accordion"
        assert len(accordion.items) == 1
        assert accordion.list_type == BaseAccordionTypes.single


class TestCarouselOrientation:
    """Tests for the CarouselOrientation enum."""

    def test_orientation_values(self):
        """Test orientation values."""

        assert CarouselOrientation.vertical.value == "vertical"
        assert CarouselOrientation.horizontal.value == "horizontal"


class TestBaseCarouselItem:
    """Tests for the BaseCarouselItem class."""

    def test_default_item(self):
        """Test default carousel item with text content."""
        item = BaseCarouselItem(
            component_type="carousel_item",
            content="Slide content",
        )
        assert item.component_type == "carousel_item"
        assert item.content == "Slide content"

    def test_item_with_card_content(self):
        """Test carousel item with card content."""
        card = BaseCard(
            component_type="card",
            title="Card Title",
            description="Card Description",
            content="Card Content",
            footer="Card Footer",
        )
        item = BaseCarouselItem(
            component_type="carousel_item",
            content=card,
        )
        assert item.content == card


class TestBaseCarouselConfig:
    """Tests for the BaseCarouselConfig class."""

    def test_default_config(self):
        """Test default carousel config."""
        config = BaseCarouselConfig(orientation=CarouselOrientation.horizontal)
        assert config.align == "start"
        assert config.loop == "true"
        assert config.orientation.value == "horizontal"
        assert config.container_class == "max-w-xs"

    def test_custom_config(self):
        """Test custom carousel config."""
        config = BaseCarouselConfig(
            align=None,
            loop="false",
            orientation=CarouselOrientation.vertical,
            container_class="max-w-md",
        )
        assert config.align is None
        assert config.loop == "false"
        assert config.orientation.value == "vertical"
        assert config.container_class == "max-w-md"


class TestBaseCarousel:
    """Tests for the BaseCarousel class."""

    def test_default_carousel(self):
        """Test default carousel."""
        items = [
            BaseCarouselItem(
                component_type="carousel_item",
                content="Slide 1",
            )
        ]
        config = BaseCarouselConfig(orientation=CarouselOrientation.vertical)
        carousel = BaseCarousel(
            component_type="carousel",
            items=items,
            config=config,
        )
        assert carousel.component_type == "carousel"
        assert len(carousel.items) == 1
        assert carousel.config == config
