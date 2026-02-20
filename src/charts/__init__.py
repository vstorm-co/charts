"""Agentic charts package for PydanticAI.

A middleware library connecting AI agents (pydantic-ai) with frontend libraries,
enabling AI-generated structured data for UI components like Charts, Accordions,
Cards, Carousels, and Tables.
"""

from importlib.metadata import version

# Base types
from charts.engines.shadcn import (
    SHADCN_TOOLSET_PROMPT,
    Shadcn,
    ShadcnAgentUIConfig,
    ShadcnColorPalette,
    ShadcnDarkColors,
    ShadcnLibraryConfig,
    ShadcnLightColors,
    ShadcnUIConfig,
)

# Engines
from charts.protocol import EngineProtocol

# Toolset
from charts.toolset import EngineDeps, create_ui_toolset

# Concrete types (via subpackage that already re-exports)
from charts.types.shadcn import (
    Accordion,
    AccordionItem,
    Card,
    Carousel,
    CarouselConfig,
    CarouselItem,
    Chart,
    ChartConfig,
    ChartData,
    ChartMetadata,
    Table,
    TableData,
    TableFooter,
)

# Helper functions
from charts.utils.helpers import get_config_data, get_ui_component

__all__ = [
    # === Toolset (AI Agent Integration) ===
    "create_ui_toolset",
    "EngineDeps",
    # === Engines (Rendering) ===
    "Shadcn",
    "EngineProtocol",
    # === Shadcn Types (Concrete Models) ===
    "Table",
    "TableData",
    "TableFooter",
    "Chart",
    "ChartData",
    "ChartConfig",
    "ChartMetadata",
    "Accordion",
    "AccordionItem",
    "Card",
    "Carousel",
    "CarouselItem",
    "CarouselConfig",
    # === Shadcn Config Classes ===
    "ShadcnAgentUIConfig",
    "ShadcnColorPalette",
    "ShadcnLightColors",
    "ShadcnDarkColors",
    "ShadcnLibraryConfig",
    "ShadcnUIConfig",
    # === Helper Functions ===
    "get_ui_component",
    "get_config_data",
    # === Prompts (Advanced Use) ===
    "SHADCN_TOOLSET_PROMPT",
]

__version__ = version("charts")
