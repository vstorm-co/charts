.PHONY: install sync test lint format typecheck all clean postgres-down

# Install dependencies
install:
	uv sync --all-extras
	uv run pre-commit install

# Sync dependencies
sync:
	uv sync --all-extras

# Run tests with coverage
test:
	uv run coverage run -m pytest -v
	uv run coverage report
	@$(MAKE) postgres-down

# Run tests without coverage
test-fast:
	uv run pytest -v
	@$(MAKE) postgres-down

# Run linter
lint:
	uv run ruff check src

# Format code
format:
	uv run ruff format src
	uv run ruff check --fix src
	uv run ruff check src --select I --fix

# Type checking
typecheck:
	uv run pyright

typecheck-mypy:
	uv run mypy src

# Run all checks
all: format lint typecheck typecheck-mypy typecheck test

# Run examples
#TODO

actions:
	act push

# Clean build artifacts
clear:
	rm -rf build dist *.egg-info .venv
	rm -rf .coverage htmlcov .pytest_cache .ruff_cache .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
