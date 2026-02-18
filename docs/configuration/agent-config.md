# Agent Configuration

The master configuration for AI agent component generation.

## BaseAgentUIConfig

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `theme` | BaseUIConfig | Required | Visual theme settings |
| `lib` | BaseLibraryConfig | Required | Library-specific settings |
| `overrides` | dict[str, Any] | {} | Global component overrides |
| `config_version` | "0.1" | "0.1" | Config version |

## ShadcnAgentUIConfig

Complete shadcn configuration with defaults:

```python
from charts.engines.shadcn.config import ShadcnAgentUIConfig

config = ShadcnAgentUIConfig()
```

This creates:

- `theme`: ShadcnUIConfig with default colors, system mode, radius 0.5
- `lib`: ShadcnLibraryConfig with react/shadcn settings

## Custom Agent Configuration

```python
from charts.engines.shadcn.config import (
    ShadcnAgentUIConfig,
    ShadcnUIConfig,
    ShadcnLibraryConfig,
    ShadcnColorPalette
)

config = ShadcnAgentUIConfig(
    theme=ShadcnUIConfig(
        color_palette=ShadcnColorPalette(),
        mode="dark",
        radius=0.75
    ),
    lib=ShadcnLibraryConfig(
        import_alias="@/components",
        use_typescript=True,
        styling_strategy="tailwind"
    ),
    overrides={
        "Button": {"variant": "outline"},
        "Card": {"className": "shadow-lg"}
    }
)
```

## Using the Config

### With Engine

```python
from charts.engines.shadcn import Shadcn

engine = Shadcn(
    return_mode="tsx",
    config=config
)
```

### With Agent

```python
from pydantic_ai import Agent
from charts.toolset import create_ui_toolset

agent = Agent(
    'openai:gpt-5.1',
    tools=create_ui_toolset(engine),
    deps_type=type('Deps', (), {'config': config})
)

result = await agent.run('Create a dashboard')
```

## Helper Method: get_active_colors()

Get the current color palette based on mode:

```python
colors = config.get_active_colors()
# Returns BaseColors for light or dark based on current mode
print(colors.primary)  # Primary color for active theme
print(colors.text)     # Text color for active theme
```
