"""API Server for the preview app.
Handles component generation requests from the frontend.

This variant uses pydantic-ai's FunctionToolset for structured component creation,
providing a cleaner separation between data querying and component rendering.

To run:
    uvicorn api_server_adv_tools:app --host 127.0.0.1 --port 8000 --reload
"""

import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

from charts.engines.shadcn import SHADCN_TOOLSET_PROMPT, Shadcn
from charts.protocol import EngineProtocol
from charts.toolset import EngineDeps, create_ui_toolset
from charts.types.shadcn.chart import ChartData
from charts.types.shadcn.table import TableData

# Add the project root to the path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(override=True)

app = FastAPI(title="Chart Generation API", version="0.0.1")


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

# Mockup for Pie/Distribution specific views
pie_config = {
    "Direct": {"label": "Direct Traffic", "color": "#2563eb"},  # Blue
    "Social": {"label": "Social Media", "color": "#ec4899"},  # Pink
    "Referral": {"label": "Referral", "color": "#facc15"},  # Yellow
    "Organic": {"label": "Organic Search", "color": "#10b981"},  # Green
    "Other": {"label": "Other Channels", "color": "#94a3b8"},  # Slate
}

pie_data = [
    {"channel": "Direct", "visitors": 4500},
    {"channel": "Social", "visitors": 2800},
    {"channel": "Referral", "visitors": 1500},
    {"channel": "Organic", "visitors": 5200},
    {"channel": "Other", "visitors": 800},
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

### Agent preparation & dependencies
SHADCN_TRANSLATOR_DEPS = EngineProtocol

# Toolset usage for structured component creation
toolset = create_ui_toolset()
engine = Shadcn("json")
deps = EngineDeps(engine=engine)

toolset_agent = Agent(
    "openai:gpt-5.1",
    retries=3,
    system_prompt=SHADCN_TOOLSET_PROMPT,
    toolsets=[toolset],
    deps_type=EngineDeps,
)


@toolset_agent.tool
def query_for_table_data(ctx: RunContext[EngineDeps]) -> TableData:
    """Query for data that will be used to create the table.

    Args:
        ctx: The RunContext containing engine dependencies.

    Returns:
        Sample TableData with month, subscriptions, and revenue columns.
    """
    return TableData(headers=headers, rows=rows)


@toolset_agent.tool
async def query_for_chart_data(ctx: RunContext[EngineDeps]) -> ChartData:
    """Query to get the latest database data.

    Args:
        ctx: The RunContext containing engine dependencies.

    Returns:
        Sample ChartData with monthly subscription and revenue information.
    """
    return ChartData(data=data)


@toolset_agent.tool
async def query_data_for_pie_chart(ctx: RunContext[EngineDeps]) -> ChartData:
    """Query to get the latest database data for the pie chart.

    Args:
        ctx: The RunContext containing engine dependencies.

    Returns:
        Sample ChartData with channel distribution and visitor counts.
    """
    return ChartData(data=pie_data)


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
        result = await toolset_agent.run(prompt, deps=deps)

        if result and result.output:
            messages = json.loads(result.all_messages_json())

            for msg in messages:
                if "parts" in msg:
                    for part in msg["parts"]:
                        if (
                            "metadata" in part
                            and part["metadata"]
                            and "ui_component" in part["metadata"]
                        ):
                            ui_component = part["metadata"]["ui_component"]
                            config = part["metadata"].get("config", {})

                if "usage" in msg:
                    logger.info(f"Partial usage: {msg['usage']}")

            status_msg = result.output or "Component generated successfully"

            # Log the output
            logger.info("Generated component successfully")
            logger.info(f"Status message: {status_msg}")
            logger.info(f"Config used: {config}")
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
        logger.error(f"Request failed: {e}")
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
