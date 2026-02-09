<div align="center">

# 📊 Agentic Charts

**AI-Powered UI Component Generation for Modern Applications**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Checked with pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)

</div>

---

## 🚀 Overview

**Agentic Charts** serves as a powerful middleware connecting Agentic AI frameworks (specifically `pydantic-ai`) with modern frontend libraries. It empowers AI agents to autonomously generate structured configurations and data for complex UI components. These structures are then seamlessly transformed into production-ready React code, tailored for **Shadcn UI** and **Recharts**.

Whether you need dynamic data visualizations, interactive dashboards, or content-rich layouts, Agentic Charts bridges the gap between AI reasoning and frontend implementation.

## ✨ Features

- **🤖 AI-Driven UI**: Agents generate complete component specifications (data + config) based on natural language prompts.
- **🎨 Shadcn UI & Recharts Native**: Outputs clean, idiomatic React code compatible with the popular Shadcn ecosystem.
- **🧩 Rich Component Library**:
  - **Charts**: Bar, Line, Pie, Area, Radar.
  - **Layouts**: Accordions, Cards, Carousels, Tables.
- **⚡ Automated Workflow**: From agent thought to rendered component in seconds.
- **🛠️ Preview Application**: Includes a full-stack preview environment (FastAPI + React/Vite) for immediate testing and iteration.
- **📐 Type-Safe**: Built with strict typing (Pydantic, Mypy, Pyright) for robustness.

## 📋 Requirements

- **Python**: >= 3.10
- **Node.js**: >= 18 (for the preview app)
- **Package Manager**: [uv](https://github.com/astral-sh/uv) **(Required Standard)** - We use `uv` for all dependency management and tool execution.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd charts
   ```

2. **Install `uv`:**
   If you haven't installed `uv` yet, follow the [official installation guide](https://github.com/astral-sh/uv#installation).

3. **Install dependencies:**
   We use `make` to streamline setup, which internally uses `uv` to sync dependencies and set up pre-commit hooks.
   ```bash
   make install
   ```

3. **Configure Environment:**
   Copy the example environment file and add your API keys (e.g., OpenAI).
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

## 🚀 Quickstart: Running the Preview App

The fastest way to see Agentic Charts in action is via the included Preview App. This standalone application lets you chat with the agent and see generated components update in real-time.

### 1. Start the Backend (API Server)

The backend handles the AI logic and component generation.

```bash
# Terminal 1
cd preview_app
npm run api-server
# OR directly via python: python api_server.py --run server
```

### 2. Start the Frontend (Vite Dev Server)

The frontend provides the chat interface and renders the generated components.

```bash
# Terminal 2
cd preview_app
npm install
npm run dev
```

Visit `http://localhost:5173` in your browser. Type a prompt like:
> "Create a bar chart showing monthly revenue for the last 6 months."
> "Generate a card with a title 'Project Alpha' and a description of its status."

## 🧑‍💻 Development

We enforce high code quality standards. Use the provided `Makefile` commands to keep your code clean and tested.

| Command | Description |
|---------|-------------|
| `make sync` | Sync dependencies with `uv.lock`. |
| `make test` | Run tests with coverage reports. |
| `make lint` | Run `ruff` linting on `src` and `preview_app`. |
| `make format` | Auto-format code using `ruff`. |
| `make typecheck` | Run static type checking with `pyright`. |
| `make typecheck-mypy` | Run strict type checking with `mypy`. |
| `make all` | Run all checks (format, lint, typecheck, test). |
| `make clear` | Clean up build artifacts and caches. |

## 📂 Project Structure

```bash
charts/
├── src/charts/             # Core Library
│   ├── base_types.py       # Base classes for components
│   ├── templates/shadcn/   # Jinja2 templates for React generation
│   └── types/shadcn/       # Pydantic models for component schemas
├── preview_app/            # Interactive Demo Application
│   ├── api_server.py       # FastAPI backend for the agent and development
│   └── src/                # React frontend source
├── tests/                  # Test suite
├── pyproject.toml          # Project configuration
└── Makefile                # Task automation
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
