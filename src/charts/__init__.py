"""
Agentic charts package for PydanticAI.

#TODO fill description and examples
"""
# Example usage is now documented in the docstring above

from importlib.metadata import version

from charts.base_types import CustomType, BaseComponent
from charts.types.chart import ChartData, ChartConfig, Chart, ChartToolOutput

__all__ = [
    # Base types
    "CustomType",
    "BaseComponent",
    # "ToolOutput",
    # Chart Types
    "ChartData",
    "ChartConfig",
    "Chart",
    "ChartToolOutput"
    
]

__version__ = version("charts")