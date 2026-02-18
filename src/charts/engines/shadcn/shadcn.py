import json
from typing import Literal

from jinja2 import Template

from charts.base_types import (
    BaseAccordion,
    BaseAgentUIConfig,
    BaseCard,
    BaseCarousel,
    BaseChart,
    BaseChartTypes,
    BaseTable,
)
from charts.engines.shadcn.config import ShadcnAgentUIConfig
from charts.templates.shadcn.accordion import SHADCN_ACCORDION_TEMPLATE
from charts.templates.shadcn.card import SHADCN_CARD_TEMPLATE
from charts.templates.shadcn.carousel import SHADCN_CAROUSEL_TEMPLATE
from charts.templates.shadcn.chart import (
    SHADCN_AREA_CHART_TEMPLATE,
    SHADCN_BAR_CHART_TEMPLATE,
    SHADCN_LINE_CHART_TEMPLATE,
    SHADCN_PIE_CHART_TEMPLATE,
    SHADCN_RADAR_CHART_TEMPLATE,
)
from charts.templates.shadcn.table import SHADCN_TABLE_TEMPLATE
from charts.types.shadcn.table import TableFooter

CONFIG = ShadcnAgentUIConfig()


class Shadcn:
    name: str
    return_mode: Literal["json", "tsx"]
    config: BaseAgentUIConfig

    def __init__(
        self, return_mode: Literal["json", "tsx"], config: BaseAgentUIConfig = CONFIG
    ) -> None:

        self.name = "shadcn"
        self.return_mode = return_mode
        self.config = config

        self.CHART_TEMPLATES = {
            "pie": SHADCN_PIE_CHART_TEMPLATE,
            "line": SHADCN_LINE_CHART_TEMPLATE,
            "radar": SHADCN_RADAR_CHART_TEMPLATE,
            "bar": SHADCN_BAR_CHART_TEMPLATE,
            "area": SHADCN_AREA_CHART_TEMPLATE,
        }

    def __get_chart_template(self, chart_type: BaseChartTypes) -> Template | str:
        try:
            return self.CHART_TEMPLATES[chart_type]
        except KeyError:
            return "Unknown chart type"

    ### Table
    async def render_table_component(self, table: BaseTable) -> str:
        """Transform the Table object into `shadcn` component."""
        if self.return_mode == "json":
            return table.model_dump_json(indent=4, ensure_ascii=False)

        # Format the data
        headers = table.table_data.headers
        items_data = [dict(zip(headers, row, strict=True)) for row in table.table_data.rows]
        items_json = json.dumps(items_data)

        # Handle footer logic
        footer_value = None
        footer_keyword = ""
        if isinstance(table.footer, TableFooter):
            footer_keyword = table.footer.keyword
            if table.footer.header_to_summarize in headers:
                try:
                    footer_value = sum(
                        float(item[table.footer.header_to_summarize])
                        for item in items_data
                        if item.get(table.footer.header_to_summarize) is not None
                    )
                except (ValueError, TypeError):
                    footer_value = None

        # Render component template
        return SHADCN_TABLE_TEMPLATE.render(
            items_json=items_json,
            headers=headers,
            caption=table.caption,
            footer_text=footer_keyword,
            footer_value=footer_value,
        )

    ### Accordion
    async def render_accordion_component(self, accordion: BaseAccordion) -> str:
        """Transform the Accordion objects into `shadcn` component."""
        if self.return_mode == "json":
            return accordion.model_dump_json(indent=4, ensure_ascii=False)

        # Prepare data
        items_data = [item.model_dump() for item in accordion.items]
        items_json = json.dumps(items_data)

        # Structure and return
        return SHADCN_ACCORDION_TEMPLATE.render(
            items=accordion.items,
            items_json=items_json,
            list_type=accordion.list_type.value,
        )

    ### Card
    async def render_card_component(self, card: BaseCard) -> str:
        """Transform the Card object into a `shadcn` component."""
        if self.return_mode == "json":
            return card.model_dump_json(indent=4, ensure_ascii=False)

        return SHADCN_CARD_TEMPLATE.render(
            title=card.title,
            description=card.description,
            content=card.content,
            footer=card.footer,
        )

    ### Carousel
    async def render_carousel_component(self, carousel: BaseCarousel) -> str:
        """Transform the Carousel object into a `shadcn` component."""
        if self.return_mode == "json":
            return carousel.model_dump_json(indent=4, ensure_ascii=False)

        # Prepare data
        items_data = [i.model_dump(mode="json") for i in carousel.items]
        items_json = json.dumps(items_data, default=str)

        # Structure and return
        return SHADCN_CAROUSEL_TEMPLATE.render(
            items_json=items_json,
            align=carousel.config.align,
            loop=carousel.config.loop,
            orientation=carousel.config.orientation.value,
            container_class=carousel.config.container_class,
        )

    ### Chart
    async def render_chart_component(self, chart: BaseChart) -> str:
        """Transform the Chart object into a `shadcn` component."""
        if self.return_mode == "json":
            return chart.model_dump_json(indent=4, ensure_ascii=False)

        # Get proper template
        template = self.__get_chart_template(chart.chart_type)

        # Identify keys
        value_key = "value"

        data_keys = list(chart.chart_config.config.keys())
        data_keys = [k for k in chart.chart_config.config if k != chart.x_axis_key]

        ### PIE CHART SPECIFIC ###
        # If there are any keys in the config
        # the one that IS NOT a x_axis_key is the right value
        chart_data = chart.chart_data.data
        if chart.chart_type == BaseChartTypes.pie:
            first_row = chart_data[0] if chart_data else {}

            # Find the key that contains the numbers.
            # It's the key that is NOT the x_axis_key and NOT 'fill'
            detected_value_key = next(
                (k for k in first_row if k != chart.x_axis_key and k != "fill"),
                "value",
            )
            value_key = detected_value_key  # This will now correctly be "visitors"

            # Assign fills (Keep your existing fill logic)
            for i, row in enumerate(chart_data):
                label_value = row.get(chart.x_axis_key)
                if label_value in chart.chart_config.config:
                    row["fill"] = chart.chart_config.config[label_value].get("color")
                else:
                    row["fill"] = f"var(--chart-{(i % 5) + 1})"
        ### END PIE CHART SPECIFIC ###

        try:
            if template and isinstance(template, Template):
                return template.render(
                    chart_config_json=json.dumps(chart.chart_config.config),
                    chart_data_json=json.dumps(chart_data),
                    title=chart.metadata.title,
                    description=chart.metadata.description,
                    x_axis_key=chart.x_axis_key,
                    value_key=value_key,  # specific for pie chart
                    data_keys=data_keys,
                )
            return "Chart could not be created"

        except Exception as e:  # pragma: no cover
            return f"An error has occurred while creating a chart: {e}"
