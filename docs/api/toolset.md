# Toolset API

The `FunctionToolset` provides UI component creation tools for AI agents.

## create_ui_toolset()

::: charts.toolset.create_ui_toolset
    options:
      show_root_toc: true
      show_bases: true

## EngineDeps

Dependencies for the UI translator component creation engine.

::: charts.toolset.EngineDeps
    options:
      show_root_toc: true
      show_bases: true

### Attributes

- `engine` (Annotated[EngineProtocol, SkipValidation]): A UI engine to base components on, e.g. `shadcn`
- `id` (str | None): Optional dependency ID
