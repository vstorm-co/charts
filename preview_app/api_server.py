"""
API Server for the preview app.
Handles chart generation requests from the frontend.

To run:
    uvicorn api_server:app --host 127.0.0.1 --port 8000 --reload
"""

import json
import logging
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Add the project root to the path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from charts.types.chart import Chart, ChartConfig, ChartData, ChartToolOutputV2

load_dotenv(override=True)

app = FastAPI(title="Chart Generation API", version="0.0.1")


# Pydantic models for request/response validation
class GenerateRequest(BaseModel):
    prompt: str


class GenerateResponse(BaseModel):
    success: bool
    message: str
    lastUpdated: str


# Data for the tools
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

system_prompt = """
You are an assistant in querying and structuring data.
Use provided tools to perform various tasks.
Fill in the missing fields where it's necessary or needed.
Create appropriate charts based on the user's request.
Use the provided data and configuration to generate meaningful visualizations.
"""

agent = Agent("openai:gpt-5.1", output_type=Chart, system_prompt=system_prompt)


@agent.tool
async def query(ctx: RunContext) -> ChartData:
    "Query to get the relevant data"
    return ChartData(data=data)


@agent.tool
async def config(ctx: RunContext) -> ChartConfig:
    "Get the configuration for the plot"
    return ChartConfig(config=config_instance)


def update_status(status: str, last_updated: str) -> None:
    """Update the status.json file."""
    status_path = Path(__file__).parent / "src" / "status.json"
    os.makedirs(status_path.parent, exist_ok=True)
    with open(status_path, "w") as f:
        json.dump({"lastUpdated": last_updated, "status": status}, f)


def update_component(ui_element: str) -> None:
    """Update the GeneratedComponent.jsx file."""
    component_path = Path(__file__).parent / "src" / "GeneratedComponent.jsx"
    os.makedirs(component_path.parent, exist_ok=True)
    with open(component_path, "w") as f:
        f.write(ui_element)


async def generate_chart(prompt: str) -> tuple[str, str]:
    """
    Generate a chart based on the prompt.
    Returns (status_message, ui_element)
    """
    logger.info(f"Received prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")

    try:
        result = await agent.run(
            prompt,
            output_type=ChartToolOutputV2,
        )

        if result and result.output:
            ui_element = result.output.ui_element or ""
            status_msg = result.output.text or "Chart generated successfully"

            # Log the output
            logger.info(f"Generated chart successfully")
            logger.info(f"Status message: {status_msg}")
            logger.info(f"UI element length: {len(ui_element)} characters")

            return status_msg, ui_element
        else:
            logger.warning("No output received from agent")
            return "No output received", ""

    except Exception as e:
        logger.error(f"Error generating chart: {str(e)}", exc_info=True)
        return f"Error: {str(e)}", ""


async def handle_generate_request(prompt: str) -> dict:
    """
    Handle a chart generation request.
    Updates both status.json and GeneratedComponent.jsx
    Returns the response dict.
    """
    last_updated = time.strftime("%H:%M:%S")
    logger.info(f"Starting chart generation request at {last_updated}")

    # Update status to showing generating
    update_status("Generating...", last_updated)

    try:
        status_msg, ui_element = await generate_chart(prompt)

        if ui_element:
            update_component(ui_element)
            status = "Rendered Successfully"
            logger.info(f"Chart component updated successfully")
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
        update_status(f"Error: {str(e)}", last_updated)
        logger.error(f"Request failed: {str(e)}", exc_info=True)
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
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_chart_endpoint(request: GenerateRequest):
    """
    Generate a chart based on the prompt.
    """
    result = await handle_generate_request(request.prompt)
    status_code = 200 if result.get("success", False) else 500
    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
