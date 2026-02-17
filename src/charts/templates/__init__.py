"""Jinja2 templates for component generation."""

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

__all__ = [
    # Accordion template
    "SHADCN_ACCORDION_TEMPLATE",
    # Card template
    "SHADCN_CARD_TEMPLATE",
    # Carousel template
    "SHADCN_CAROUSEL_TEMPLATE",
    # Chart templates
    "SHADCN_AREA_CHART_TEMPLATE",
    "SHADCN_BAR_CHART_TEMPLATE",
    "SHADCN_LINE_CHART_TEMPLATE",
    "SHADCN_PIE_CHART_TEMPLATE",
    "SHADCN_RADAR_CHART_TEMPLATE",
    # Table template
    "SHADCN_TABLE_TEMPLATE",
]
