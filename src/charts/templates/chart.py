from jinja2 import Template

SHADCN_CHART_TEMPLATE = Template("""
"use client"
import { Bar, BarChart, CartesianGrid, XAxis, YAxis, ChartTooltip, 
ChartTooltipContent, ChartLegend, ChartLegendContent, ChartContainer } from "@/components/ui/chart"

const chartConfig = {{ chart_config_json }}
const chartData = {{ chart_data_json }}

export function {{ component_name }}() {
  return (
    <ChartContainer config={chartConfig} className="min-h-[200px] w-full">
      <BarChart accessibilityLayer data={chartData}>
        <CartesianGrid vertical={false} />
        <XAxis dataKey="{{ x_axis_key }}" tickLine={false} axisLine={false} />
        <YAxis tickLine={false} axisLine={false} />
        <ChartTooltip content={<ChartTooltipContent />} />
        <ChartLegend content={<ChartLegendContent />} />
        {% for key in data_keys %}
        <Bar dataKey="{{ key }}" fill="var(--color-{{ key }})" radius={4} />
        {% endfor %}
      </BarChart>
    </ChartContainer>
  )
}
""")
