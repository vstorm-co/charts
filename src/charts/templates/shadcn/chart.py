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

// These come from your local card file
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
  CardFooter } from "@/components/ui/card"

import { Cell } from "recharts"

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
        <CardTitle>{{ title | default('') }}</CardTitle>
        <CardDescription>{{ description | default('') }}</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig} className="min-h-[300px] w-full">
          <BarChart accessibilityLayer data={chartData}>
            <CartesianGrid vertical={false} />
            <XAxis
                dataKey="{{ x_axis_key }}"
                tickLine={false}
                axisLine={false}
                tickMargin={10}
                tickFormatter={(value) => value.toString().slice(0, 3)}
            />
            <ChartTooltip content={<ChartTooltipContent hideLabel />} />
            <ChartLegend content={<ChartLegendContent />} />
            {% for key in data_keys %}
            {% if key != x_axis_key %}
            <Bar
              dataKey="{{ key }}"
              fill="var(--color-{{ key }})"
              radius={4}
            />
            {% endif %}
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
        <CardTitle>{{ title | default('') }}</CardTitle>
        <CardDescription>{{ description | default('') }}</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig} className="min-h-[300px] w-full">
          <LineChart
            data={chartData}
            margin={ { left: 12, right: 12, top: 12 } }
          >
            <CartesianGrid vertical={false} strokeDasharray="3 3" opacity={0.4} />
            <XAxis
              dataKey="{{ x_axis_key }}"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
            />
            {/* Hidden YAxis to maintain scale without taking space */}
            <YAxis hide />
            <ChartTooltip content={<ChartTooltipContent />} />
            <ChartLegend content={<ChartLegendContent />} />
            {% for key in data_keys %}
            <Line
              key="{{ key }}"
              dataKey="{{ key }}"
              type="monotone"
              stroke="var(--color-{{ key }})"
              strokeWidth={2}
              dot={false}
              activeDot={ { r: 4, strokeWidth: 2 } }
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
  // Generate a unique ID prefix to avoid gradient collisions in carousels
  const idPrefix = React.useId().replace(/:/g, "");

  return (
    <Card className="w-full shadow-none border-none">
      <CardHeader>
        <CardTitle>{{ title | default('') }}</CardTitle>
        <CardDescription>{{ description | default('') }}</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig} className="min-h-[300px] w-full">
          <AreaChart data={chartData} margin={ { left: 12, right: 12, top: 12 } }>
            <defs>
              {% for key in data_keys %}
              <linearGradient id={`${idPrefix}fill{{ key }}`} x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor="var(--color-{{ key }})"
                  stopOpacity={0.8}
                />
                <stop
                  offset="95%"
                  stopColor="var(--color-{{ key }})"
                  stopOpacity={0.1}
                />
              </linearGradient>
              {% endfor %}
            </defs>
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="{{ x_axis_key }}"
              tickLine={false}
              axisLine={false}
              tickMargin={10}
            />
            <YAxis hide />
            <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
            <ChartLegend content={<ChartLegendContent />} />
            {% for key in data_keys %}
            <Area
              key="{{ key }}"
              dataKey="{{ key }}"
              type="monotone"
              fill={`url(#${idPrefix}fill{{ key }})`}
              stroke="var(--color-{{ key }})"
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
import { TrendingUp } from "lucide-react"

const chartConfig = {{ chart_config_json }} satisfies ChartConfig
const chartData = {{ chart_data_json }}

export default function GeneratedComponent() {
  // Logic: Use the value_key passed from Python
  const dataKey = "{{ value_key }}";
  const nameKey = "{{ x_axis_key }}";

  return (
    <Card className="flex flex-col shadow-none border-none bg-transparent">
      <CardHeader className="items-center pb-0">
        <CardTitle>{{ title | default('Data Distribution') }}</CardTitle>
        <CardDescription>{{ description | default('Categorical breakdown') }}</CardDescription>
      </CardHeader>
      <CardContent className="flex-1 pb-0">
        <ChartContainer
          config={chartConfig}
          className="mx-auto aspect-square max-h-[250px]"
        >
          <PieChart>
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent hideLabel />}
            />
            <Pie
              data={chartData}
              dataKey={dataKey}
              nameKey={nameKey}
              innerRadius={60}
              strokeWidth={5}
            >
              {chartData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={entry.fill || `var(--chart-${(index % 5) + 1})`}
                />
              ))}
            </Pie>
          </PieChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="flex-col gap-2 text-sm text-center pt-4">
        <div className="flex items-center justify-center gap-2 leading-none font-medium">
          Data synchronized successfully <TrendingUp className="h-4 w-4" />
        </div>
        <div className="text-muted-foreground leading-none">
          Showing distribution based on latest metrics
        </div>
      </CardFooter>
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
    <Card className="w-full shadow-none border-none bg-transparent">
      <CardHeader className="items-center pb-4">
        <CardTitle>{{ title | default('') }}</CardTitle>
        <CardDescription>{{ description | default('') }}</CardDescription>
      </CardHeader>
      <CardContent className="pb-0">
        <ChartContainer
          config={chartConfig}
          className="mx-auto aspect-square w-full max-h-[350px]"
        >
          {/* Added margin to prevent axis labels from being cut off at the edges */}
          <RadarChart
            data={chartData}
            margin={ { top: 20, right: 20, bottom: 20, left: 20 } }
          >
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent />}
            />
            <PolarGrid className="stroke-muted opacity-50" />
            <PolarAngleAxis
              dataKey="{{ x_axis_key }}"
              tick={ { fill: "hsl(var(--muted-foreground))", fontSize: 12 } }
            />

            {% for key in data_keys %}
            {# Only render Radar shapes for keys that are NOT the X-axis label #}
            {% if key != x_axis_key %}
            <Radar
              key="{{ key }}"
              name={chartConfig["{{ key }}"]?.label || "{{ key }}"}
              dataKey="{{ key }}"
              fill="var(--color-{{ key }})"
              fillOpacity={0.5}
              stroke="var(--color-{{ key }})"
              strokeWidth={2}
              dot={ { r: 3, fillOpacity: 1, fill: "var(--color-{{ key }})" } }
            />
            {% endif %}
            {% endfor %}

            <ChartLegend content={<ChartLegendContent />} className="mt-6" />
          </RadarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
""",
)
