"""Configuration classes for the shadcn rendering engine.

This module provides concrete implementations of the base configuration types
defined in `charts.base_types`. These classes define the default theme, color
palettes, and library settings used by the Shadcn engine for component generation.

Key classes:
    ShadcnLightColors: Light theme color palette with semantic colors
    ShadcnDarkColors: Dark theme color palette with accessible contrasts
    ShadcnColorPalette: Combined light/dark color definitions
    ShadcnLibraryConfig: Library-specific settings (framework, paths, imports)
    ShadcnUIConfig: UI appearance configuration (mode, radius, density)
    ShadcnAgentUIConfig: Master configuration passed to AI agents

Example:
    ```python
    from charts.engines.shadcn.config import ShadcnAgentUIConfig

    config = ShadcnAgentUIConfig()
    engine = Shadcn(return_mode="tsx", config=config)
    ```
"""

from typing import Literal

from pydantic import Field

from charts.base_types import (
    BaseAgentUIConfig,
    BaseColorPalette,
    BaseColors,
    BaseLibraryConfig,
    BaseUIConfig,
)


class ShadcnLightColors(BaseColors):
    """A `shadcn` light theme color palette."""

    ...


class ShadcnDarkColors(BaseColors):
    """A `shadcn` dark theme color palette."""

    ...


class ShadcnColorPalette(BaseColorPalette):
    """Color palettes used by the `shadcn` components."""

    light: ShadcnLightColors = Field(default_factory=lambda: ShadcnLightColors())
    dark: ShadcnDarkColors = Field(default_factory=lambda: ShadcnDarkColors())


class ShadcnLibraryConfig(BaseLibraryConfig):
    """A `shadcn` library config for agentic component creation."""

    framework: Literal["react"] = "react"
    library: Literal["shadcn"] = "shadcn"
    import_alias: str = "@/components"
    component_path: str = "@/components/ui"
    use_typescript: bool = True
    styling_strategy: Literal["tailwind"] = "tailwind"
    is_package: bool = False


class ShadcnUIConfig(BaseUIConfig):
    """A `shadcn` UI configuration for agentic component creation."""

    color_palette: ShadcnColorPalette = Field(default_factory=lambda: ShadcnColorPalette())
    mode: Literal["light", "dark", "system"] = "system"


class ShadcnAgentUIConfig(BaseAgentUIConfig):
    """A `shadcn` complete config for agentic component creation."""

    theme: ShadcnUIConfig = Field(default_factory=lambda: ShadcnUIConfig())
    lib: ShadcnLibraryConfig = Field(default_factory=lambda: ShadcnLibraryConfig())
