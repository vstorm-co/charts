"""API Server for the preview app.
Handles component generation requests from the frontend.

To run:
    uvicorn api_server:app --host 127.0.0.1 --port 8000 --reload
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

from charts.engines.shadcn import ShadcnTranslator
from charts.protocol import EngineProtocol
from charts.toolset import SHADCN_TOOLSET_PROMPT, EngineDeps, create_ui_toolset
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
SHADCN_TRANSLATOR = ShadcnTranslator()

# Simplified agent
agent = Agent(
    "openai:gpt-5.1",
    system_prompt=system_prompt,
    retries=3,
    deps_type=SHADCN_TRANSLATOR_DEPS,
)

# Toolset usage
toolset = create_ui_toolset()
deps = EngineDeps(engine=ShadcnTranslator())

toolset_agent = Agent(
    "openai:gpt-5.1",
    retries=3,
    system_prompt=SHADCN_TOOLSET_PROMPT,
    toolsets=[toolset],
    deps_type=EngineDeps,
)

# @agent.tool
# async def query_for_table_data(ctx: RunContext[SHADCN_TRANSLATOR_DEPS]) -> TableData:
#     """Query for data that will be used to create the table."""
#     return TableData(headers=headers, rows=rows)

# @agent.tool
# async def query_for_chart_data(ctx: RunContext[SHADCN_TRANSLATOR_DEPS]) -> ChartData:
#     """Query to get the latest database data."""
#     return ChartData(data=data)

# @agent.tool
# async def query_data_for_pie_chart(ctx: RunContext[SHADCN_TRANSLATOR_DEPS]) -> ChartData:
#     """Query to get the latest database data for the pie chart."""
#     return ChartData(data=pie_data)


@toolset_agent.tool
def query_for_table_data(ctx: RunContext[EngineDeps]) -> TableData:
    """Query for data that will be used to create the table."""
    return TableData(headers=headers, rows=rows)


@toolset_agent.tool
async def query_for_chart_data(ctx: RunContext[EngineDeps]) -> ChartData:
    """Query to get the latest database data."""
    return ChartData(data=data)


@toolset_agent.tool
async def query_data_for_pie_chart(ctx: RunContext[EngineDeps]) -> ChartData:
    """Query to get the latest database data for the pie chart."""
    return ChartData(data=pie_data)


# @agent.tool
# async def create_table(
#     ctx: RunContext[SHADCN_TRANSLATOR_DEPS],
#     table_data: TableData,
#     caption: str,
#     footer: TableFooter | None = None
# ) -> ToolReturn:
#     """Create a Table component based on the provided data and configuration."""
#     # Instantiate the Table object
#     table_obj = Table(table_data=table_data, caption=caption, footer=footer)

#     # Transform the data
#     component_code = await ctx.deps.render_table_component(table_obj)
#     return ToolReturn(
#         return_value=f"Successfully created table: {caption}",
#         metadata={
#             "ui_element": component_code,
#             "component_type": table_obj.component_type,
#             "data_summary": {"rows": len(table_data.rows)}
#         }
#     )

# @agent.tool
# async def create_accordion(
#     ctx: RunContext[SHADCN_TRANSLATOR_DEPS],
#     accordions: list[Accordion],
#     list_type: BaseAccordionTypes
# ) -> ToolReturn:
#     """Create an Accordion component based on provided data and configuration."""
#     # Instantiate the AccordionList object
#     accordion_obj = Accordion(items=accordions, list_type=list_type)

#     # Transform the data
#     component_code = await ctx.deps.render_accordion_component(accordion_obj)
#     return ToolReturn(
#         return_value=f"Successfully created accordion with {len(accordions)} elements",
#         metadata={
#             "ui_element": component_code,
#             "component_type": accordion_obj.component_type,
#             "data_summary": {"num_elements": len(accordions)}
#         }
#     )

# @agent.tool
# async def create_card(
#     ctx: RunContext[SHADCN_TRANSLATOR_DEPS],
#     card: Card,
# ) -> ToolReturn:
#     """Create a Card component based on provided data and configuration."""
#     # Instantiate the Card object
#     card_obj = Card(
#         title=card.title,
#         description=card.description,
#         content=card.content,
#         footer=card.footer
#     )

#     # Transform the data
#     component_code = await ctx.deps.render_card_component(card_obj)
#     return ToolReturn(
#         return_value=f"Successfully created card component with title: {card_obj.title}",
#         metadata={
#             "ui_element": component_code,
#             "component_type": card_obj.component_type,
#             "data_summary": {"content_type": f"{type(card_obj.content)}"}
#         }
#     )

# @agent.tool
# async def create_carousel_component(
#     ctx: RunContext[SHADCN_TRANSLATOR_DEPS],
#     content: str | Card,
# ) -> ToolReturn:
#     """Create a CarouselItem component based on the user query and instructions."""
#     carousel_item_obj = CarouselItem(content=content)
#     return ToolReturn(
#         return_value=carousel_item_obj
#     )


# @agent.tool
# async def create_complete_carousel(
#     ctx: RunContext[SHADCN_TRANSLATOR_DEPS],
#     carousel_items: list[CarouselItem],
#     carousel_config: CarouselConfig,
# ) -> ToolReturn:
#     """Create a Carousel component based on provided data and configuration."""
#     # Instantiate the Carousel object
#     carousel_obj = Carousel(
#         items=carousel_items,
#         config=carousel_config
#     )

#     # Transform the data
#     component_code = await ctx.deps.render_carousel_component(carousel_obj)
#     return ToolReturn(
#         return_value=(
#                f"Successfully created carousel component with"
#                "{len(carousel_items)} elements."),
#         metadata={
#             "ui_element": component_code,
#             "component_type": carousel_obj.component_type,
#             "data_summary": {"num_elements": len(carousel_items)}
#         }
#     )

# @agent.tool
# async def create_chart_config(ctx: RunContext[SHADCN_TRANSLATOR_DEPS]) -> ChartConfig:
#     """Create a ChartConfig for a chart."""
#     return ChartConfig(config=config_instance) #TODO - this is a placeholder for tests

# @agent.tool
# async def create_pie_chart_config(ctx: RunContext[SHADCN_TRANSLATOR_DEPS]) -> ChartConfig:
#     """Create a ChartConfig for a pie chart."""
#     return ChartConfig(config=pie_config)

# @agent.tool
# async def create_chart_metadata(
#     ctx: RunContext[SHADCN_TRANSLATOR_DEPS],
#     title: str,
#     subtitle: str,
#     description: str
# ) -> ChartMetadata:
#     """Create a ChartMetadata describing the data used to present on the chart."""
#     return ChartMetadata(title=title, subtitle=subtitle, description=description)


# @agent.tool
# async def create_complete_chart(
#     ctx: RunContext[SHADCN_TRANSLATOR_DEPS],
#     chart_type: str,
#     metadata: ChartMetadata,
#     chart_config: ChartConfig,
#     chart_data: ChartData,
#     x_key_axis: str
# ) -> ToolReturn:
#     """
#     Create a Chart object based on provided data and configuration.
#     Be very precise about which type of chart the user wants since they can differ in
#     terms of needed configuration or data.
#     Before invoking this function, all previous configuration and query functions
#     providing data should be called in this order:
#     * query_for_chart_data / query_for_pie_chart_data
#     * create_chart_config / create_pie_chart_config
#     * create_chart_metadata
#     """
#     # Instantiate the Chart object
#     chart_obj = Chart(
#         chart_type=chart_type,
#         metadata=metadata,
#         chart_config=chart_config,
#         chart_data=chart_data,
#         x_axis_key=x_key_axis
#     )

#     # Transform the data
#     component_code = await ctx.deps.render_chart_component(chart_obj)
#     return ToolReturn(
#         return_value=f"Successfully created chart: {chart_obj.metadata.title}",
#         metadata={
#             "ui_element": component_code,
#             "component_type": chart_obj.component_type,
#             "data_summary": {"num_elements": (len(chart_data.data))}
#         }
#     )


### Methods
def update_status(status: str, last_updated: str) -> None:
    """Update the status.json file and global state."""
    # Update in-memory state
    global current_status
    current_status["status"] = status
    current_status["lastUpdated"] = last_updated

    # Update file (optional, but kept for compatibility)
    status_path = Path(__file__).parent / "src" / "status.json"
    os.makedirs(status_path.parent, exist_ok=True)
    with open(status_path, "w") as f:
        json.dump(current_status, f)


def update_component(ui_element: str) -> None:
    """Update the GeneratedComponent.tsx file."""
    component_path = Path(__file__).parent / "src" / "GeneratedComponent.tsx"
    os.makedirs(component_path.parent, exist_ok=True)
    with open(component_path, "w") as f:
        f.write(ui_element)


async def generate_component(prompt: str) -> tuple[str, str]:
    """Generate a component based on the prompt.
    Returns (status_message, ui_element)
    """
    logger.info(f"Received prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")

    try:
        # result = await agent.run(
        #     prompt, deps=SHADCN_TRANSLATOR
        # )

        result = await toolset_agent.run(prompt, deps=deps)

        if result and result.output:
            # logger.info(result.output)
            messages = json.loads(result.all_messages_json())
            # logger.info(messages)

            for msg in messages:
                if "parts" in msg:
                    for part in msg["parts"]:
                        if (
                            "metadata" in part
                            and part["metadata"]
                            and "ui_element" in part["metadata"]
                        ):
                            # if "ui_element" in part["metadata"].keys():
                            ui_element = part["metadata"]["ui_element"]

                if "usage" in msg:
                    logger.info(f"Partial usage: {msg['usage']}")

            ### TEST
            # create a table. add predictions to data for 6 upcoming months

            ### USAGE
            # Usage: RunUsage(
            # input_tokens=1771, output_tokens=184,
            # details={
            # 'accepted_prediction_tokens': 0,
            # 'audio_tokens': 0,
            # 'reasoning_tokens': 0,
            # 'rejected_prediction_tokens': 0},
            # requests=3, tool_calls=2)

            # ui_element = result.output.metadata.ui_element or ""
            status_msg = result.output or "Component generated successfully"

            # Log the output
            logger.info("Generated component successfully")
            logger.info(f"Status message: {status_msg}")
            logger.info(f"UI element length: {len(ui_element)} characters")
            logger.info(f"Usage: {result.usage()}")

            return status_msg, ui_element
        logger.warning("No output received from agent")
        return "No output received", ""

    except Exception as e:
        logger.error(f"Error generating component: {e!s}", exc_info=True)
        return f"Error: {e!s}", ""


async def handle_generate_request(prompt: str) -> dict:
    """Handle a component generation request.
    Updates both status.json and GeneratedComponent.tsx
    Returns the response dict.
    """
    last_updated = time.strftime("%H:%M:%S")
    logger.info(f"Starting chart generation request at {last_updated}")

    # Update status to showing generating
    update_status("Generating...", last_updated)

    try:
        status_msg, ui_element = await generate_component(prompt)

        if ui_element:
            update_component(ui_element)
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
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/api/status")
async def get_status():
    """Get the current generation status."""
    return current_status


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_component_endpoint(request: GenerateRequest):
    """Generate a component based on the prompt."""
    result = await handle_generate_request(request.prompt)
    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
