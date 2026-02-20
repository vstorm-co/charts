# Color Palettes

Configure color schemes for light and dark modes.

## BaseColors

Base color palette object with the following default values:

| Property | Default | Description |
| ---------- | --------- | ------------- |
| `primary` | `#858586` | Primary brand color |
| `secondary` | `#0FB1E2` | Secondary accent color |
| `tertiary` | `#E9E040` | Tertiary highlight color |
| `success` | `#33C819` | Success indicator |
| `danger` | `#EE8A19` | Error/danger indicator |
| `warning` | `#D6E718` | Warning indicator |
| `error` | `#FF0000` | Error color |
| `background` | `#FFFFFF` | Main background color |
| `surface` | `#F4F4F5` | Card/modal surface color |
| `text` | `#09090B` | Default text color |

## BaseColorPalette

Contains both light and dark theme colors:

```python
from charts.base_types import BaseColors, BaseColorPalette

palette = BaseColorPalette(
    light=BaseColors(primary="#2563eb", background="#ffffff"),
    dark=BaseColors(primary="#60a5fa", background="#1f2937")
)
```

## ShadcnLightColors / ShadcnDarkColors

Pre-configured shadcn theme colors in `charts.engines.shadcn.config`.

## ShadcnColorPalette

Complete color palette for shadcn components:

```python
from charts.engines.shadcn import ShadcnColorPalette

palette = ShadcnColorPalette()
# Uses default light/dark colors matching shadcn/ui defaults
```

## Custom Theme Example

```python
from charts.engines.shadcn.config import (
    ShadcnUIConfig, ShadcnLibraryConfig, ShadcnAgentUIConfig,
    ShadcnColorPalette, ShadcnLightColors, ShadcnDarkColors
)

# Create custom palette
custom_palette = ShadcnColorPalette(
    light=ShadcnLightColors(
        primary="#6366f1",  # Indigo
        secondary="#ec4899",  # Pink
        background="#ffffff",
        text="#1e293b"
    ),
    dark=ShadcnDarkColors(
        primary="#818cf8",  # Lighter Indigo
        secondary="#f472b6",  # Lighter Pink
        background="#0f172a",  # Slate 900
        text="#f1f5f9"
    )
)

# Apply to UI config
ui_config = ShadcnUIConfig(color_palette=custom_palette, mode="system")

# Full agent config
config = ShadcnAgentUIConfig(
    theme=ui_config,
    lib=ShadcnLibraryConfig()
)
```

## Mode Options

- `light` - Force light mode
- `dark` - Force dark mode
- `system` - Use system preference (default)
