"""Jinja2 templates for UI component generation.

This package provides Jinja2 templates that convert Pydantic model objects into
React/TypeScript code using the shadcn/ui component library. The templates support
five major component types:

- **Accordion**: Collapsible content panels with single/multiple expansion modes
- **Card**: Container components with header, body, and footer sections
- **Carousel**: Horizontal or vertical scrolling displays with navigation controls
- **Chart**: Five chart types (Bar, Line, Pie, Area, Radar) via Recharts library
- **Table**: Data grids with headers, rows, optional footers for calculations

All templates generate client-side React components ("use client") that integrate
with shadcn/ui primitives and Recharts for visualization.
"""

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
