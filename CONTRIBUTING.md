# Contributing to Charts

Thanks for your interest in contributing to Charts! This document provides guidelines for setting up the development environment and contributing code.

## Table of Contents

- [Development Setup](#development-setup)
- [Local CI Testing with act](#local-ci-testing-with-act)
- [Running Tests](#running-tests)
- [Requirements](#requirements)
- [Quick Commands Reference](#quick-commands-reference)
- [Code Style](#code-style)
- [Pull Request Process](#pull-request-process)

## Development Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/vstorm-co/charts.git
   cd charts
   ```

2. **Install dependencies**

   ```bash
   make install
   ```

   This will:
   - Create a virtual environment with `uv sync`
   - Install all dependencies including dev tools
   - Set up pre-commit hooks

3. **Prerequisites**

   - Python >= 3.10
   - Node.js >= 18 (for preview app)
   - uv (Python package manager)

4. **Preview App Setup**

   The preview app is a separate React application for testing component generation:

   ```bash
   cd preview_app
   npm install
   npm run dev
   ```

## Local CI Testing with act

You can test GitHub Actions workflows locally using [act](https://github.com/nektos/act):

```bash
make actions
```

### Prerequisites for act

- Docker must be running
- On M1/M2 Macs, ensure Docker is configured for ARM64 containers

The `.actrc` file configures act to use:
- Full Ubuntu image for compatibility
- Root user in containers
- Host network mode
- Docker socket mounting for CI tasks

## Running Tests

### With Coverage (Recommended)

```bash
make test
```

This runs pytest with coverage reporting. The project requires **100% code coverage**.

### Without Coverage

```bash
make test-fast
```

### Run All Checks

```bash
make all
```

This runs the full suite: formatting, linting, type checking, and tests.

## Requirements

Before your contribution can be merged:

- [ ] 100% test coverage maintained
- [ ] All Pyright checks pass (`make typecheck`)
- [ ] All MyPy checks pass (`make typecheck-mypy`)
- [ ] All Ruff checks pass (`make lint` / `make format`)
- [ ] Tests pass with coverage (`make test`)

## Quick Commands Reference

| Command | Description |
|---------|-------------|
| `make install` | Install dependencies + pre-commit hooks |
| `make sync` | Sync dependencies with uv.lock |
| `make test` | Run tests with coverage reports |
| `make test-fast` | Run tests without coverage |
| `make lint` | Run ruff check on src |
| `make format` | Auto-format code and fix issues |
| `make typecheck` | Run pyright static type checking |
| `make typecheck-mypy` | Run mypy strict type checking |
| `make all` | Run formatting, linting, type checks, and tests |
| `make actions` | Run GitHub Actions locally with act |
| `make clear` | Clean up build artifacts and caches |

## Code Style

### Python

- **Formatter/Linter:** Ruff
- **Line length:** 100 characters
- **Quote style:** Double quotes
- **Target version:** py310

Run formatting before committing:

```bash
make format
```

### Type Checking

We use two type checkers:

- **Pyright** (basic mode) - Fast, integrated with editors
- **MyPy** (strict mode) - Comprehensive checking for src directory

Run both before PR submission:

```bash
make typecheck
make typecheck-mypy
```

### TypeScript/React

- Follow existing component patterns in `preview_app/src/`
- Use functional components with hooks
- Maintain consistent prop typing

## Pull Request Process

1. **Fork the repository**

2. **Create a branch from main**

   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**

   - Follow the code style above
   - Add tests for new functionality
   - Ensure existing tests pass

4. **Run the full check suite**

   ```bash
   make all
   ```

5. **Commit and push**

   ```bash
   git add .
   git commit -m "Descriptive commit message"
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**

   Include:
   - Clear description of changes
   - Related issues (if any)
   - Any breaking changes or migration notes

## Questions?

Check the [README.md](README.md) for project overview and usage examples. For specific implementation questions, review the source code comments and type hints.
