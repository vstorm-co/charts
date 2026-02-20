# Installation

## Prerequisites

- Python >= 3.10
- `uv` or `pip` package manager
- OpenAI API key (for AI agent integration)

## Installation Methods

### Using pip

```bash
pip install charts
```

### Using uv

```bash
uv add charts
```

### Development Installation

Clone the repository:

```bash
git clone https://github.com/vstorm-co/charts.git
cd charts
```

Install with `make`:

```bash
make install
```

Or using `uv` directly:

```bash
uv sync
```

## shadcn/ui Setup

To use generated components in a frontend project, install the required shadcn components:

```bash
npx shadcn@latest add accordion button card carousel chart select table
```

This installs:

- `accordion` - For Accordion component
- `button` - Required by many components
- `card` - For Card component
- `carousel` - For Carousel component
- `chart` - For Chart component (Recharts wrappers)
- `select` - Optional, for dropdowns
- `table` - For Table component

## Environment Setup

Copy `.env.example` to `.env` and add your OpenAI API key:

```bash
cp .env.example .env
# Edit .env and add:
OPENAI_API_KEY=your-api-key-here
```

## Verification

Create a test file `test_charts.py`:

```python
# Create a simple card component
from charts.types.shadcn.card import Card

card = Card(
    title="Random Space Fact",
    description="A quick, fascinating tidbit about our universe.",
    content="Neutron stars are so dense that a sugar-cube-sized amount of their material would weigh about 1 billion tons on Earth.",
    footer="Source: NASA & astrophysics research summaries"
)

print(f"Created {chart.component_type} component")
```

Run it:

```bash
uv run test_charts.py
```

## Troubleshooting

### Module not found

If you get `ModuleNotFoundError: No module named 'charts'`:

- Ensure you're in the correct virtual environment
- Check installation with `pip show charts` or `uv pip show charts`

### shadcn components missing

If generated components don't render:

- Verify shadcn is installed in your React project
- Run `npx shadcn@latest add` for each required component
