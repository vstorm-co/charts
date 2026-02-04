
"use client"
import { Pie, PieChart, ChartTooltip,
ChartTooltipContent, ChartLegend, ChartLegendContent, ChartContainer } from "@/components/ui/chart"

const chartConfig = {
  "category": {
    "label": "Category"
  },
  "value": {
    "label": "Value"
  }
}
const chartData = [
  {
    "category": "Subscriptions",
    "value": 1224,
    "fill": "magenta"
  },
  {
    "category": "Revenue",
    "value": 1861,
    "fill": "yellow"
  }
]

// Using 'export default' ensures App.jsx never loses the reference
export default function GeneratedComponent() {
  return (
    <ChartContainer config={chartConfig} className="min-h-[300px] w-full">
      <PieChart accessibilityLayer>
        <Pie data={chartData} dataKey="value" nameKey="category" />
        <ChartTooltip content={<ChartTooltipContent />} />
        <ChartLegend content={<ChartLegendContent />} />
      </PieChart>
    </ChartContainer>
  )
}
