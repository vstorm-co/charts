"""API Server for the preview app.
Handles component generation requests from the frontend.

To run:
    uvicorn api_server:app --host 127.0.0.1 --port 8000 --reload
"""

import json
import os
import sys
import time
import uuid
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

from charts.types import BaseComponent
from charts.types.shadcn.accordion import (
    Accordion,
    AccordionList,
    AccordionToolOutput,
    AccordionTypes,
)
from charts.types.shadcn.card import Card, CardOutputTool
from charts.types.shadcn.carousel import (
    Carousel,
    CarouselConfig,
    CarouselItem,
    CarouselOrientation,
    CarouselToolOutput,
)
from charts.types.shadcn.chart import (
    Chart,
    ChartConfig,
    ChartData,
    ChartMetadata,
    ChartToolOutput,
    ChartTypes,
)
from charts.types.shadcn.table import Table, TableData, TableFooter, TableOutputTool

# Add the project root to the path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(override=True)

app = FastAPI(title="Chart Generation API", version="0.0.1")

COMPONENT_SCHEMAS = {
    "chart": Chart.model_json_schema(),
    "accordion": AccordionList.model_json_schema(),
    "accordion_list": AccordionList.model_json_schema(),
    "card": Card.model_json_schema(),
    "carousel_item": CarouselItem.model_json_schema(),
    "carousel": Carousel.model_json_schema(),
    "table": Table.model_json_schema(),
}

COMPONENT_LIST = list(COMPONENT_SCHEMAS.keys())

ComponentOutput = (
    AccordionToolOutput | ChartToolOutput | CardOutputTool | CarouselToolOutput | TableOutputTool
)


# Pydantic models for request/response validation
class GenerateRequest(BaseModel):
    prompt: str


class GenerateResponse(BaseModel):
    success: bool
    message: str
    lastUpdated: str


# Data for the chart tools
config_instance = {
    "subscriptions": {"label": "New Subscriptions", "color": "#2563eb"},
    "revenue": {"label": "Monthly Revenue", "color": "#10b981"},
}

data = [
    {"month": "January", "subscriptions": 186, "revenue": 450},
    {"month": "February", "subscriptions": 305, "revenue": 52},
    {"month": "March", "subscriptions": 237, "revenue": 480},
    {"month": "April", "subscriptions": 73, "revenue": 210},
    {"month": "May", "subscriptions": 209, "revenue": 59},
    {"month": "June", "subscriptions": 214, "revenue": 610},
]

# Data for the table tools
headers = ["month", "subscriptions", "revenue"]
rows = [
    ("January", 186, 450),
    ("February", 305, 52),
    ("March", 237, 480),
    ("April", 73, 210),
    ("May", 209, 59),
    ("June", 214, 610),
]

# Global status storage
current_status = {"status": "Waiting...", "lastUpdated": "Never"}

system_prompt = """
You are an assistant for frontend component creation.
You will query for needed data and structure the final component as per user's request.

Split user requests into smaller steps and use the provided tools to complete those steps.
Use provided tools proactively to perform tasks.
Fill in the missing fields where it's necessary or needed.
Do not hesitate to ask for more data if you think it's necessary for the final component.

You must always finish by calling a ToolOutput function
(CardOutputTool, TableOutputTool, ChartToolOutput, etc.) that produces the final UI element.
Do not end without returning a final output.
"""

agent = Agent("openai:gpt-5.1", system_prompt=system_prompt, retries=3)


### Main tools
@agent.tool
async def available_components(ctx: RunContext) -> list[str]:
    """Choose component relevant to the User's query"""
    return COMPONENT_LIST


@agent.tool
async def get_component_schema(ctx: RunContext, component_name: str) -> dict[str, Any]:
    """Get component's schema based on the component's type"""
    # Normalize naming: common LLM behavior is to use underscores
    normalized_name = component_name.lower().replace(" ", "_")

    if normalized_name in COMPONENT_SCHEMAS:
        return COMPONENT_SCHEMAS[normalized_name]

    # Returning this helps the LLM realize it made a typo
    return {
        "error": f"Component '{component_name}' not found.",
        "available_components": COMPONENT_LIST,
    }


### Card
@agent.tool
async def create_card(
    ctx: RunContext,
    title: str,
    description: str,
    content: str | BaseComponent | list[BaseComponent],
    footer: str,
) -> Card:
    """Create a Card component with given data."""
    return Card(title=title, description=description, content=content, footer=footer)


@agent.tool
async def finalize_card_creation(ctx: RunContext, ui: Card) -> CardOutputTool:
    """Finalize the creation of the card component by wrapping it in the output tool."""
    return CardOutputTool(ui=ui, ui_component="")


### Accordion
@agent.tool
async def create_accordion(ctx: RunContext, header: str, content: str) -> Accordion:
    """Create an Accordion component with header and content"""
    return Accordion(value=str(uuid.uuid4()), trigger=header, content=content)


@agent.tool
async def merge_accordions(
    ctx: RunContext,
    accordions: list[Accordion],
    list_type: AccordionTypes,
) -> AccordionList:
    """Generate a list of Accordion components with"""
    return AccordionList(items=accordions, list_type=list_type)


@agent.tool
async def finalize_accordion_creation(ctx: RunContext, ui: AccordionList) -> AccordionToolOutput:
    """Finalize the creation of the accordion component by wrapping it in the output tool."""
    return AccordionToolOutput(ui=ui, ui_component="")


### Carousel
@agent.tool
async def create_carousel_item(ctx: RunContext, content: str | Card) -> CarouselItem:
    """Generate a CarouselItem for further usage in Carousel component"""
    return CarouselItem(content=content)


@agent.tool
async def create_carousel_config(
    ctx: RunContext,
    orientation: CarouselOrientation,
) -> CarouselConfig:
    """Create a CarouselConfig item to determine the behavior of final component."""
    return CarouselConfig(orientation=orientation)


@agent.tool
async def create_complete_carousel(
    ctx: RunContext,
    items: list[CarouselItem],
    config: CarouselConfig,
) -> Carousel:
    """Create a complete Carousel component with items and config."""
    return Carousel(items=items, config=config)


@agent.tool
async def finalize_carousel_creation(ctx: RunContext, ui: Carousel) -> CarouselToolOutput:
    """Finalize the creation of the carousel component by wrapping it in the output tool."""
    return CarouselToolOutput(ui=ui, ui_component="")


# Table
@agent.tool
async def query_for_table_data(ctx: RunContext) -> TableData:
    """Query for data that will be used to create the table."""
    return TableData(headers=headers, rows=rows)


@agent.tool
async def create_table(
    ctx: RunContext,
    table_data: TableData,
    caption: str | None = None,
    footer: TableFooter | None = None,
) -> Table:
    """Create a Table component based on the provided data, caption, and optional footer."""
    return Table(table_data=table_data, caption=caption, footer=footer)


@agent.tool
async def finalize_table_creation(ctx: RunContext, ui: Table) -> TableOutputTool:
    """Finalize the creation of the table component by wrapping it in the output tool."""
    return TableOutputTool(ui=ui, ui_component="")


### Charts
@agent.tool
async def query_for_chart_data(ctx: RunContext) -> ChartData:
    """Query to get the latest database data."""
    return ChartData(data=data)


@agent.tool
async def get_chart_config(ctx: RunContext) -> ChartConfig:
    """Get the configuration for the chart."""
    return ChartConfig(config=config_instance)


@agent.tool
async def create_chart_metadata(
    ctx: RunContext,
    title: str,
    subtitle: str,
    description: str,
) -> ChartMetadata:
    """Create metadata for the chart component."""
    return ChartMetadata(title=title, subtitle=subtitle, description=description)


@agent.tool
async def create_chart(
    ctx: RunContext,
    chart_type: ChartTypes,
    data: ChartData,
    config: ChartConfig,
    metadata: ChartMetadata,
    x_axis_key: str,
) -> Chart:
    """Create a Chart component based on the provided data and configuration."""
    return Chart(
        chart_type=chart_type,
        chart_data=data,
        chart_config=config,
        metadata=metadata,
        x_axis_key=x_axis_key,
    )


@agent.tool
async def finalize_chart_creation(ctx: RunContext, ui: Chart) -> ChartToolOutput:
    """Finalize the creation of the chart component by wrapping it in the output tool."""
    return ChartToolOutput(ui=[ui], ui_component="")


### Methods
def update_status(status: str, last_updated: str) -> None:
    """Update the status.json file and global state.

    Args:
        status: Current status message (e.g., "Generating...", "Rendered Successfully")
        last_updated: Timestamp string for when the status was updated.
    """
    # Update in-memory state
    global current_status
    current_status["status"] = status
    current_status["lastUpdated"] = last_updated

    # Update file (optional, but kept for compatibility)
    status_path = Path(__file__).parent / "src" / "status.json"
    os.makedirs(status_path.parent, exist_ok=True)
    with open(status_path, "w") as f:
        json.dump(current_status, f)


def update_component(ui_component: str) -> None:
    """Update the GeneratedComponent.tsx file.

    Args:
        ui_component: The generated TSX/React code to write to disk.
    """
    component_path = Path(__file__).parent / "src" / "GeneratedComponent.tsx"
    os.makedirs(component_path.parent, exist_ok=True)
    with open(component_path, "w") as f:
        f.write(ui_component)


async def generate_component(prompt: str) -> tuple[str, str]:
    """Generate a component based on the prompt.

    Args:
        prompt: User's natural language description of desired component.

    Returns:
        Tuple of (status_message, ui_component).
    """
    logger.info(f"Received prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")

    try:
        result = await agent.run(
            prompt,
            output_type=ComponentOutput,
        )

        if result and result.output:
            print(result.output)
            ui_component = result.output.ui_component or ""
            status_msg = result.output.text or "Component generated successfully"

            # Log the output
            logger.info("Generated component successfully")
            logger.info(f"Status message: {status_msg}")
            logger.info(f"UI element length: {len(ui_component)} characters")
            logger.info(f"Usage: {result.usage()}")

            return status_msg, ui_component
        logger.warning("No output received from agent")
        return "No output received", ""

    except Exception as e:
        logger.error(f"Error generating component: {e!s}", exc_info=True)
        return f"Error: {e!s}", ""


async def handle_generate_request(prompt: str) -> dict:
    """Handle a component generation request.

    Updates both status.json and GeneratedComponent.tsx with the results.
    Returns the response dict for the API endpoint.

    Args:
        prompt: User's natural language description of desired component.

    Returns:
        Dict with success, message, and lastUpdated fields.
    """
    last_updated = time.strftime("%H:%M:%S")
    logger.info(f"Starting chart generation request at {last_updated}")

    # Update status to showing generating
    update_status("Generating...", last_updated)

    try:
        status_msg, ui_component = await generate_component(prompt)

        if ui_component:
            update_component(ui_component)
            status = "Rendered Successfully"
            logger.info("Component updated successfully")
        else:
            status = "Generation Failed"
            logger.warning("No UI element generated")

        update_status(status, last_updated)

        response = {
            "success": True,
            "message": status_msg or status,
            "lastUpdated": last_updated,
        }
        logger.info(f"Request completed: {response['message']}")
        return response

    except Exception as e:
        update_status(f"Error: {e!s}", last_updated)
        logger.error(f"Request failed: {e!s}", exc_info=True)
        return {
            "success": False,
            "message": str(e),
            "lastUpdated": last_updated,
        }


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint for API status monitoring.

    Returns:
        {"status": "ok"} when the service is running.
    """
    return {"status": "ok"}


@app.get("/api/status")
async def get_status() -> dict[str, str]:
    """Get current component generation status.

    Returns:
        Dict with 'status' and 'lastUpdated' fields showing
        the most recent generation operation state.
    """
    return current_status


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_component_endpoint(request: GenerateRequest) -> dict:
    """Generate a UI component from natural language prompt.

    Args:
        request: GenerateRequest with 'prompt' field containing
                user's natural language description of desired component.

    Returns:
        Dict with success status, message, and lastUpdated timestamp.
    """
    result = await handle_generate_request(request.prompt)
    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
