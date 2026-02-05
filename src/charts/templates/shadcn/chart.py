from jinja2 import Template

# Shared Imports and Interfaces
TSX_BASE = """
"use client"
import * as React from "react"

// These come from the base library 'recharts'
import {
  Bar, BarChart, CartesianGrid, XAxis, YAxis, Line, LineChart,
  Area, AreaChart, Pie, PieChart, PolarAngleAxis, PolarGrid, Radar, RadarChart
} from "recharts"

// These come from your local shadcn file
import {
  ChartTooltip, ChartTooltipContent, ChartLegend, ChartLegendContent, ChartContainer
} from "@/components/ui/chart"

// 3. These come from your local card file
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"

interface ChartConfig {
  [key: string]: {
    label: string;
    color?: string;
  } | any;
}
"""

SHADCN_BAR_CHART_TEMPLATE = Template(
    TSX_BASE
    + """
const chartConfig = {{ chart_config_json }} satisfies ChartConfig
const chartData = {{ chart_data_json }}

export default function GeneratedComponent() {
  return (
    <Card className="w-full shadow-none border-none">
      <CardHeader>
        <CardTitle>{chartConfig.title}</CardTitle>
        <CardDescription>{chartConfig.description}</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig} className="min-h-[300px] w-full">
          <BarChart accessibilityLayer data={chartData}>
            <CartesianGrid vertical={false} strokeDasharray="3 3" opacity={0.4} />
            <XAxis
                dataKey="{{ x_axis_key }}"
                tickLine={false}
                axisLine={false}
                tickMargin={10}
            />
            <YAxis tickLine={false} axisLine={false} tick={false} width={0} />
            <ChartTooltip content={<ChartTooltipContent />} />
            <ChartLegend content={<ChartLegendContent />} />
            {% for key in data_keys %}
            <Bar
              dataKey="{{ key }}"
              fill={chartConfig["{{ key }}"]?.color || "var(--color-{{ key }})"}
              radius={4}
            />
            {% endfor %}
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
""",
)

SHADCN_LINE_CHART_TEMPLATE = Template(
    TSX_BASE
    + """
const chartConfig = {{ chart_config_json }} satisfies ChartConfig
const chartData = {{ chart_data_json }}

export default function GeneratedComponent() {
  return (
    <Card className="w-full shadow-none border-none">
      <CardHeader>
        <CardTitle>{chartConfig.title}</CardTitle>
        <CardDescription>{chartConfig.description}</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig} className="min-h-[300px] w-full">
          <LineChart data={chartData} margin={ {% raw %}{ left: 12, right: 12 }{% endraw %} }>
            <CartesianGrid vertical={false} strokeDasharray="3 3" opacity={0.4} />
            <XAxis
              dataKey="{{ x_axis_key }}"
              tickLine={false}
              axisLine={false}
              tickMargin={10}
            />
            <YAxis tickLine={false} axisLine={false} tick={false} width={0} />
            <ChartTooltip content={<ChartTooltipContent />} />
            <ChartLegend content={<ChartLegendContent />} />
            {% for key in data_keys %}
            <Line
              dataKey="{{ key }}"
              type="monotone"
              stroke={chartConfig["{{ key }}"]?.color || "var(--color-{{ key }})"}
              strokeWidth={2.5}
              dot={
              {% raw %}
              { fill: chartConfig["{% endraw %}{{ key }}{% raw %}"].color }
              {% endraw %} }
              activeDot={ {% raw %}{ r: 6 }{% endraw %} }
            />
            {% endfor %}
          </LineChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
""",
)

SHADCN_AREA_CHART_TEMPLATE = Template(
    TSX_BASE
    + """
const chartConfig = {{ chart_config_json }} satisfies ChartConfig
const chartData = {{ chart_data_json }}

export default function GeneratedComponent() {
  return (
    <Card className="w-full shadow-none border-none">
      <CardHeader>
        <CardTitle>{chartConfig.title}</CardTitle>
        <CardDescription>{chartConfig.description}</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig} className="min-h-[300px] w-full">
          <AreaChart data={chartData} margin={ {% raw %}{ left: 12, right: 12 }{% endraw %} }>
            <defs>
              {% for key in data_keys %}
              <linearGradient id="fill{{ key }}" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={chartConfig["{{ key }}"]?.color ||
                "var(--color-{{ key }})"} stopOpacity={0.8}/>
                <stop offset="95%" stopColor={chartConfig["{{ key }}"]?.color ||
                "var(--color-{{ key }})"} stopOpacity={0.1}/>
              </linearGradient>
              {% endfor %}
            </defs>
            <CartesianGrid vertical={false} strokeDasharray="3 3" opacity={0.4} />
            <XAxis
              dataKey="{{ x_axis_key }}"
              tickLine={false}
              axisLine={false}
              tickMargin={10}
            />
            <YAxis tickLine={false} axisLine={false} tick={false} width={0} />
            <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
            <ChartLegend content={<ChartLegendContent />} />
            {% for key in data_keys %}
            <Area
              dataKey="{{ key }}"
              type="natural"
              fill="url(#fill{{ key }})"
              stroke={chartConfig["{{ key }}"]?.color || "var(--color-{{ key }})"}
              stackId="a"
            />
            {% endfor %}
          </AreaChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
""",
)

SHADCN_PIE_CHART_TEMPLATE = Template(
    TSX_BASE
    + """
const chartConfig = {{ chart_config_json }} satisfies ChartConfig
const chartData = {{ chart_data_json }}

export default function GeneratedComponent() {
  return (
    <Card className="flex flex-col shadow-none border-none">
      <CardHeader className="items-center pb-0">
        <CardTitle>{chartConfig.title}</CardTitle>
        <CardDescription>{chartConfig.description}</CardDescription>
      </CardHeader>
      <CardContent className="flex-1 pb-0">
        <ChartContainer config={chartConfig} className="mx-auto aspect-square max-h-[300px]">
          <PieChart>
            <ChartTooltip cursor={false} content={<ChartTooltipContent hideLabel />} />
            <Pie
              data={chartData}
              dataKey="value"
              nameKey="{{ x_axis_key }}"
              innerRadius={60}
              strokeWidth={5}
            />
            <ChartLegend content={<ChartLegendContent nameKey="{{ x_axis_key }}" />}
            className="-translate-y-2" />
          </PieChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
""",
)

SHADCN_RADAR_CHART_TEMPLATE = Template(
    TSX_BASE
    + """
const chartConfig = {{ chart_config_json }} satisfies ChartConfig
const chartData = {{ chart_data_json }}

export default function GeneratedComponent() {
  return (
    <Card className="w-full shadow-none border-none">
      <CardHeader className="items-center pb-4">
        <CardTitle>{chartConfig.title}</CardTitle>
        <CardDescription>{chartConfig.description}</CardDescription>
      </CardHeader>
      <CardContent>
        {/* Force aspect-square to prevent the '0px height' collapse */}
        <ChartContainer config={chartConfig} className="mx-auto aspect-square w-full max-h-[400px]">
          <RadarChart data={chartData}>
            <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
            <PolarGrid strokeDasharray="3 3" />
            <PolarAngleAxis dataKey="{{ x_axis_key }}" />
            {% for key in data_keys %}
            <Radar
              dataKey="{{ key }}"
              fill={chartConfig["{{ key }}"]?.color || "var(--color-{{ key }})"}
              fillOpacity={0.6}
              stroke={chartConfig["{{ key }}"]?.color || "var(--color-{{ key }})"}
              strokeWidth={2}
            />
            {% endfor %}
            <ChartLegend content={<ChartLegendContent />} className="mt-4" />
          </RadarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
""",
)
