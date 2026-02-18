# Library Configuration

Configure library-specific settings for component generation.

## ShadcnLibraryConfig

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `framework` | "react" | "react" | Target framework |
| `library` | "shadcn" | "shadcn" | UI library name |
| `is_package` | bool | False | Components in node_modules? |
| `import_alias` | str | "@/components" | Import alias for components |
| `component_path` | str | "@/components/ui" | Path to component files |
| `use_typescript` | bool | True | Generate TSX files |
| `styling_strategy` | "tailwind" \| "css-in-js" \| "inline" | "tailwind" | Styling approach |

## Example Configurations

### Default shadcn Configuration

```python
from charts.engines.shadcn.config import ShadcnLibraryConfig

config = ShadcnLibraryConfig()
# import_alias: "@/components"
# component_path: "@/components/ui"
```

### Custom Import Alias

```python
from charts.engines.shadcn.config import ShadcnLibraryConfig

config = ShadcnLibraryConfig(
    import_alias="@/ui",
    component_path="@/ui/components"
)
```

### Package-based Imports

If components are installed via npm:

```python
config = ShadcnLibraryConfig(
    is_package=True,
    import_alias="react"
)
```

## Integration with Agent Config

```python
from charts.engines.shadcn.config import (
    ShadcnLibraryConfig, ShadcnUIConfig, ShadcnAgentUIConfig
)

lib_config = ShadcnLibraryConfig(
    framework="react",
    library="shadcn",
    use_typescript=True,
    styling_strategy="tailwind"
)

ui_config = ShadcnUIConfig()

agent_config = ShadcnAgentUIConfig(
    theme=ui_config,
    lib=lib_config
)
```
