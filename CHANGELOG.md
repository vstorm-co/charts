# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - 2026-02-20

### Added

*   Core components: Chart (Bar, Line, Pie, Area, Radar), Table, Accordion, Card, Carousel
*   Engine abstraction with `EngineProtocol` and `Shadcn` implementation for rendering components to TSX/JSON
*   Jinja2 templates for React/TSX component generation via Recharts UI library
*   Toolset API (`create_ui_toolset`) for AI agent integration with pydantic-ai
*   Pydantic models with validation (e.g., Chart's `x_axis_key` validation)
*   JSON return mode for tools in addition to rendered TSX output
*   Configuration classes (`ShadcnAgentUIConfig`, color palettes, library config)
*   Preview app with FastAPI backend and React frontend for real-time component display
*   Comprehensive MkDocs documentation with architecture concepts, component guides, and API reference

### Changed

*   Switched output format from `.jsx` to `.tsx` for TypeScript support
*   Updated README.md multiple times throughout development

### Chore

*   CI/CD workflows (linting, type checking, testing with coverage)
*   Pre-commit hooks configuration
*   Makefile commands for common tasks (install, sync, test, lint, format, typecheck)
*   100% test coverage requirement enforced

### Docs

*   Architecture concepts documentation
*   Component reference guides
*   Configuration options documentation
*   API reference documentation
