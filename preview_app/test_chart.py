import asyncio
import json
import os
import time

from dotenv import load_dotenv
from icecream import ic
from pydantic_ai import Agent, RunContext

from charts.types.shadcn.chart import Chart, ChartConfig, ChartData, ChartToolOutput

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
You are assistant in querying and structuring data.
Use provided tools to perform various tasks.
Fill in the missing fields where it's necessary or needed.
Chart has to be be an area chart.
Filling colors are dark brown for subscriptions and light teal for revenue.
There should be no legend on the chart.
"""


load_dotenv(override=True)

agent = Agent("openai:gpt-5.1", output_type=Chart, system_prompt=system_prompt)


@agent.tool
async def query(ctx: RunContext) -> ChartData:
    """Query to get the relevant data."""
    return ChartData(data=data)


@agent.tool
async def config(ctx: RunContext) -> ChartConfig:
    """Get the configuration for the plot."""
    return ChartConfig(config=config_instance)


async def send_component(result: ChartToolOutput) -> None:
    ui_element = result.ui_element

    with open("preview_app/src/GeneratedComponent.tsx", "w") as f:
        f.write(ui_element)

    with open("preview_app/src/status.json", "w") as f:
        json.dump({"lastUpdated": time.strftime("%H:%M:%S"), "status": "Rendered Successfully"}, f)


async def initialize():
    # Ensure the directory exists
    os.makedirs("src", exist_ok=True)

    # Create placeholder component if it doesn't exist
    if not os.path.exists("src/GeneratedComponent.tsx"):
        with open("preview_app/src/GeneratedComponent.tsx", "w") as f:
            f.write("export default function GeneratedUI() { return <div>Waiting for AI...</div> }")

    # Create placeholder status
    if not os.path.exists("src/status.json"):
        with open("preview_app/src/status.json", "w") as f:
            json.dump({"status": "Initialized", "lastUpdated": "N/A"}, f)


async def main() -> None:
    await initialize()
    result = await agent.run(
        "Query the data and the config, return values needed to create the chart.",
        output_type=ChartToolOutput,
    )

    if result:
        ic(result.output.text)
        ic(result.output.ui_element)

    await send_component(result.output)


if __name__ == "__main__":
    asyncio.run(main())
