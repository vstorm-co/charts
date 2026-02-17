from typing import Literal

from charts.base_types import (
    BaseAgentUIConfig,
    BaseColorPalette,
    BaseColors,
    BaseLibraryConfig,
    BaseUIConfig,
)


class ShadcnLightColors(BaseColors):
    """A `shadcn` light theme color palette."""


class ShadcnDarkColors(BaseColors):
    """A `shadcn` dark theme color palette."""


class ShadcnColorPalette(BaseColorPalette):
    """Color palettes used by the `shadcn` components."""

    light: ShadcnLightColors
    dark: ShadcnDarkColors


class ShadcnLibraryConfig(BaseLibraryConfig):
    """A `shadcn` library config for agentic component creation."""

    framework: Literal["react"] = "react"
    library: Literal["shadcn"] = "shadcn"
    import_alias: str = "@/components"
    component_path: str = "@/components/ui"
    use_typescript: bool = True
    styling_strategy: Literal["tailwind"] = "tailwind"


class ShadcnUIConfig(BaseUIConfig):
    """A `shadcn` UI configuration for agentic component creation."""

    color_palette: ShadcnColorPalette
    mode: Literal["light", "dark", "system"] = "system"


class ShadcnAgentUIConfig(BaseAgentUIConfig):
    """A `shadcn` complete config for agentic component creation."""

    theme: ShadcnUIConfig
    lib: ShadcnLibraryConfig
