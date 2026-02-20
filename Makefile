.PHONY: install sync test test-fast lint format typecheck typecheck-mypy all clear actions

# Install & Setup
install:
	uv sync --all-extras
	uv run pre-commit install

sync:
	uv sync --all-extras

# Testing
test:
	uv run coverage run -m pytest -v
	uv run coverage report

test-fast:
	uv run pytest -v

# Linting & Formatting
lint:
	uv run ruff check src tests

format:
	uv run ruff format src tests
	uv run ruff check --fix src tests

# Type Checking
typecheck:
	uv run pyright

typecheck-mypy:
	uv run mypy src tests

# CI/Check All
all: format lint typecheck-mypy typecheck test

# Tools
actions:
	act push

# Clean up
clear:
	rm -rf build dist *.egg-info .venv .coverage/
	rm -rf htmlcov .pytest_cache .ruff_cache .mypy_cache .pyright_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
