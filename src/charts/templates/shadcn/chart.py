from jinja2 import Template

SHADCN_BAR_CHART_TEMPLATE = Template("""
"use client"
import { Bar, BarChart, CartesianGrid, XAxis, YAxis, ChartTooltip,
ChartTooltipContent, ChartLegend, ChartLegendContent, ChartContainer, Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/chart"

const chartConfig = {{ chart_config_json }}
const chartData = {{ chart_data_json }}

// Using 'export default' ensures App.jsx never loses the reference
export default function GeneratedComponent() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-black">{chartConfig.title}</CardTitle>
        <CardDescription>{chartConfig.description}</CardDescription>
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
            />
            <YAxis tickLine={false} axisLine={false} />
            <ChartTooltip content={<ChartTooltipContent />} />
            <ChartLegend content={<ChartLegendContent />} />
            {% for key in data_keys %}
            <Bar dataKey="{{ key }}" fill="var(--color-{{ key }})" radius={4} />
            {% endfor %}
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
""")

SHADCN_PIE_CHART_TEMPLATE = Template("""
"use client"
import { Pie, PieChart, ChartTooltip,
ChartTooltipContent, ChartLegend, ChartLegendContent, ChartContainer, Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/chart"

const chartConfig = {{ chart_config_json }}
const chartData = {{ chart_data_json }}

// Using 'export default' ensures App.jsx never loses the reference
export default function GeneratedComponent() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-black">{chartConfig.title}</CardTitle>
        <CardDescription>{chartConfig.description}</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig} className="min-h-[300px] w-full">
          <PieChart accessibilityLayer>
            <Pie data={chartData} dataKey="value" nameKey="{{ x_axis_key }}" />
            <ChartTooltip content={<ChartTooltipContent />} />
            <ChartLegend content={<ChartLegendContent />} />
          </PieChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
""")

SHADCN_LINE_CHART_TEMPLATE = Template("""
"use client"
import { Line, LineChart, CartesianGrid, XAxis, YAxis, ChartTooltip,
ChartTooltipContent, ChartLegend, ChartLegendContent, ChartContainer, Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/chart"

const chartConfig = {{ chart_config_json }}
const chartData = {{ chart_data_json }}

{% set left_brace = '{' %}
{% set right_brace = '}' %}

// Using 'export default' ensures App.jsx never loses the reference
export default function GeneratedComponent() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-black">{chartConfig.title}</CardTitle>
        <CardDescription>{chartConfig.description}</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig} className="min-h-[300px] w-full">
          <LineChart
            accessibilityLayer
            data={chartData}
            margin={{ left_brace }}{{ left_brace }} left: 12, right: 12 {{ right_brace }}{{ right_brace }}
          >
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="{{ x_axis_key }}"
              tickLine={false}
              axisLine={false}
              tickMargin={10}
            />
            <YAxis tickLine={false} axisLine={false} />
            <ChartTooltip content={<ChartTooltipContent />} />
            <ChartLegend content={<ChartLegendContent />} />
            {% for key in data_keys %}
            <Line
              dataKey="{{ key }}"
              type="monotone"
              stroke="var(--color-{{ key }})"
              strokeWidth={2}
              dot={true}
              activeDot={{ left_brace }}{{ left_brace }} r: 6 {{ right_brace }}{{ right_brace }}
            />
            {% endfor %}
          </LineChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
""")

SHADCN_RADAR_CHART_TEMPLATE = Template("""
"use client"
import { PolarAngleAxis, PolarGrid, Radar, RadarChart, ChartTooltip,
ChartTooltipContent, ChartLegend, ChartLegendContent, ChartContainer, Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/chart"

const chartConfig = {{ chart_config_json }}
const chartData = {{ chart_data_json }}

{% set lb = '{' %}
{% set rb = '}' %}

// Using 'export default' ensures App.jsx never loses the reference
export default function GeneratedComponent() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-black">{chartConfig.title}</CardTitle>
        <CardDescription>{chartConfig.description}</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig} className="mx-auto aspect-square max-h-[350px] w-full">
          <RadarChart
            data={chartData}
            margin={{ lb }}{{ lb }} top: 10, right: 10, bottom: 10, left: 10 {{ rb }}{{ rb }}
          >
            <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
            <ChartLegend content={<ChartLegendContent />} />
            <PolarGrid />
            <PolarAngleAxis dataKey="{{ x_axis_key }}" />

            {% for key in data_keys %}
            <Radar
              dataKey="{{ key }}"
              fill="var(--color-{{ key }})"
              fillOpacity={0.6}
              stroke="var(--color-{{ key }})"
            />
            {% endfor %}
          </RadarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
""")

SHADCN_AREA_CHART_TEMPLATE = Template("""
"use client"
import { Area, AreaChart, CartesianGrid, XAxis, YAxis, ChartTooltip,
ChartTooltipContent, ChartLegend, ChartLegendContent, ChartContainer, Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/chart"

const chartConfig = {{ chart_config_json }}
const chartData = {{ chart_data_json }}

{% set lb = '{' %}
{% set rb = '}' %}

export default function GeneratedComponent() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-black">{chartConfig.title}</CardTitle>
        <CardDescription>{chartConfig.description}</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig} className="min-h-[300px] w-full">
          <AreaChart
            accessibilityLayer
            data={chartData}
            margin={{ lb }}{{ lb }} left: 12, right: 12 {{ rb }}{{ rb }}
          >
            <defs>
              {% for key in data_keys %}
              <linearGradient id="fill{{ key }}" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="var(--color-{{ key }})" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="var(--color-{{ key }})" stopOpacity={0.1}/>
              </linearGradient>
              {% endfor %}
            </defs>
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="{{ x_axis_key }}"
              tickLine={false}
              axisLine={false}
              tickMargin={10}
              tickFormatter={(value) => value.slice(0, 3)}
            />
            <YAxis tickLine={false} axisLine={false} />
            <ChartTooltip cursor={false} content={<ChartTooltipContent indicator="dot" />} />
            <ChartLegend content={<ChartLegendContent />} />
            {% for key in data_keys %}
            <Area
              dataKey="{{ key }}"
              type="natural"
              fill="url(#fill{{ key }})"
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
""")
