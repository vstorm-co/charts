# Agent Workflows

Advanced patterns for using Charts with AI agents.

## Multi-Step Data Collection

Agents can gather data through conversation before rendering components:

```python
import asyncio
from typing import Any

from pydantic_ai import Agent, RunContext
from charts.toolset import create_ui_toolset, EngineDeps
from charts.engines.shadcn import Shadcn, SHADCN_TOOLSET_PROMPT
from charts.utils.helpers import get_ui_component

from dotenv import load_dotenv

load_dotenv(override=True)

engine = Shadcn(return_mode='json')
toolset = create_ui_toolset()
deps = EngineDeps(engine=engine)

# Enhance the toolset with a custom tool to gather data from a database
# Here we simulate this behavior returning static results
@toolset.tool
async def gather_db_data(ctx: RunContext) -> list[dict[str, Any]]:
    """Fetch the data from the database to use it in the chart creation."""
    # Simulate gathering data from a database
    return [
        {"month": "January", "sales": 100},
        {"month": "February", "sales": 150},
        {"month": "March", "sales": 200},
    ]

agent = Agent(
    'openai:gpt-5.1',
    system_prompt=SHADCN_TOOLSET_PROMPT,
    retries=3,
    toolsets=[toolset],
    deps_type=EngineDeps,
)

async def collect_sales_data() -> str:
    # Step 1: Ask for data (Simulated conversation)
    result1 = await agent.run(
        "Fetch some data to create the sales chart.",
        deps=deps
    )

    # Step 2: Generate the chart with collected data
    result2 = await agent.run(
        "Now create a table showing these sales figures",
        deps=deps,
        message_history=result1.all_messages() # Maintain the conversation history
    )

    component = get_ui_component(result2)
    return component

ui = asyncio.run(collect_sales_data())
print(ui)
```

Exemplary JSON output:

```json
{
    "component_type": "chart",
    "chart_type": "bar",
    "metadata": {
        "title": "Monthly Sales",
        "subtitle": "Q1 Performance",
        "description": "Sales data for the first quarter"
    },
    "chart_config": {
        "config": {}
    },
    "chart_data": {
        "data": [
            {
                "month": "January",
                "sales": 100
            },
            {
                "month": "February",
                "sales": 150
            },
            {
                "month": "March",
                "sales": 200
            }
        ]
    },
    "x_axis_key": "month"
}
```

Exemplary TSX output:

```tsx
"use client"

import * as React from "react"
import { Bar, BarChart, CartesianGrid, XAxis } from "recharts"

import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  ChartLegend,
  ChartLegendContent,
} from "@/components/ui/chart"

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card"

// 1. Data keys must match the keys in your data array
const chartData = [
  { month: "January", sales: 100 },
  { month: "February", sales: 150 },
  { month: "March", sales: 200 },
]

// 2. Config maps the 'sales' key to a label and a CSS variable color
const chartConfig = {
  sales: {
    label: "Sales",
    color: "#4F46E5",
  },
} satisfies ChartConfig

export default function GeneratedComponent() {
  return (
    <Card className="w-full shadow-none border-none">
      <CardHeader>
        <CardTitle>Monthly Sales</CardTitle>
        <CardDescription>Sales data for the first quarter</CardDescription>
      </CardHeader>
      <CardContent>
        {/* ChartContainer handles the CSS variables based on your config */}
        <ChartContainer config={chartConfig} className="min-h-[300px] w-full">
          <BarChart accessibilityLayer data={chartData}>
            <CartesianGrid vertical={false} strokeDasharray="3 3" verticalFill="none" />

            <XAxis
              dataKey="month"
              tickLine={false}
              axisLine={false}
              tickMargin={10}
              tickFormatter={(value) => value.toString().slice(0, 3)}
            />

            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent hideLabel />}
            />

            <ChartLegend content={<ChartLegendContent />} />

            {/* 3. Link the Bar to the "sales" data key */}
            <Bar
              dataKey="sales"
              fill="var(--color-sales)"
              radius={[4, 4, 0, 0]} // Slightly rounded top corners
            />
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
```

## Dashboard Generation Workflow

A complete multi-component dashboard workflow:

```python
import asyncio
from typing import Any

from pydantic_ai import Agent, RunContext
from charts.toolset import create_ui_toolset, EngineDeps
from charts.engines.shadcn import Shadcn, SHADCN_TOOLSET_PROMPT
from charts.utils.helpers import get_ui_component

from dotenv import load_dotenv

load_dotenv(override=True)

engine = Shadcn(return_mode='json')
toolset = create_ui_toolset()
deps = EngineDeps(engine=engine)

@toolset.tool
async def gather_db_data(ctx: RunContext) -> list[dict[str, Any]]:
    """Fetch the data from the database to use it in the chart creation."""
    # Simulate gathering data from a database
    return [
        {"month": "January", "sales": 100},
        {"month": "February", "sales": 150},
        {"month": "March", "sales": 200},
    ]

async def generate_complete_dashboard():
    agent = Agent(
        'openai:gpt-5.1',
        system_prompt=SHADCN_TOOLSET_PROMPT,
        toolsets=[toolset],
        retries=3,
        deps_type=EngineDeps
    )

    # Phase 1: Create individual components through tool calls
    chart_result = await agent.run(
        "Fetch latest data. Create a bar chart showing sales by month.",
        deps=deps,
    )

    table_result = await agent.run(
        "Now also create a table with detailed sales data.",
        deps=deps,
        message_history=chart_result.all_messages()
    )

    return {
        'chart': get_ui_component(chart_result),
        'table': get_ui_component(table_result),
    }

ui = asyncio.run(generate_complete_dashboard())

# Print the results
# for k, v in ui.items():
#     print(f" *** {k.upper()} ***")
#     print(v)
```
