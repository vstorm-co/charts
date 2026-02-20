# UI Theme Configuration

Configure visual appearance of components.

## BaseUIConfig

| Property | Type | Default | Description |
| ---------- | ------ | --------- | ------------- |
| `color_palette` | BaseColorPalette | Required | Light/dark color scheme |
| `mode` | "light" \| "dark" \| "system" | "system" | Theme mode |
| `radius` | float | 0.5 | Border radius multiplier (0=sharp, 1+=rounded) |
| `density` | "compact" \| "comfortable" \| "spacious" | "comfortable" | Spacing density |

## Radius Values

The `radius` property controls border rounding:

| Value | Effect |
| ------- | -------- |
| `0` | Sharp corners |
| `0.5` | Slightly rounded (default) |
| `1` | Fully rounded |

## Density Options

- `compact` - Reduced spacing, more content visible
- `comfortable` - Standard spacing (default)
- `spacious` - Increased spacing, airy layout

## ShadcnUIConfig

Shadcn-specific UI configuration:

```python
from charts.engines.shadcn.config import ShadcnUIConfig, ShadcnColorPalette

config = ShadcnUIConfig(
    color_palette=ShadcnColorPalette(),
    mode="system",
    radius=0.5,
    density="comfortable"
)
```

## Example: Compact Dark Theme

```python
from charts.engines.shadcn.config import (
    ShadcnLightColors, ShadcnDarkColors, ShadcnColorPalette,
    ShadcnUIConfig
)

config = ShadcnUIConfig(
    color_palette=ShadcnColorPalette(
        light=ShadcnLightColors(),
        dark=ShadcnDarkColors()
    ),
    mode="dark",
    radius=0.25,  # More compact
    density="compact"
)
```

## Example: Spacious Light Theme

```python
config = ShadcnUIConfig(
    color_palette=ShadcnColorPalette(),
    mode="light",
    radius=1,  # Fully rounded
    density="spacious"
)
```
