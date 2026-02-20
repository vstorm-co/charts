"""Agentic charts package for PydanticAI.

#TODO fill description and examples
"""
# Example usage is now documented in the docstring above

from importlib.metadata import version

from charts.base_types import BaseComponent, CustomType
from charts.engines.shadcn import Shadcn
from charts.protocol import EngineProtocol
from charts.toolset import EngineDeps, create_ui_toolset
from charts.types.shadcn.chart import Chart, ChartConfig, ChartData

__all__ = [
    # Base types
    "CustomType",
    "BaseComponent",
    # Chart Types
    "ChartData",
    "ChartConfig",
    "Chart",
    # Toolset
    "EngineDeps",
    "create_ui_toolset",
    # Engines
    "EngineProtocol",
    "Shadcn",
]

__version__ = version("charts")
