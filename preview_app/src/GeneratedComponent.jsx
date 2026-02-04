
"use client"
import { Bar, BarChart, CartesianGrid, XAxis, YAxis, ChartTooltip,
ChartTooltipContent, ChartLegend, ChartLegendContent, ChartContainer } from "@/components/ui/chart"

const chartConfig = {
  "subscriptions": {
    "label": "New Subscriptions",
    "color": "#0000FF"
  },
  "revenue": {
    "label": "Monthly Revenue",
    "color": "#FF00FF"
  }
}
const chartData = [
  {
    "month": "Jan",
    "subscriptions": 120,
    "revenue": 3200
  },
  {
    "month": "Feb",
    "subscriptions": 150,
    "revenue": 4100
  },
  {
    "month": "Mar",
    "subscriptions": 90,
    "revenue": 2800
  },
  {
    "month": "Apr",
    "subscriptions": 170,
    "revenue": 4600
  },
  {
    "month": "May",
    "subscriptions": 140,
    "revenue": 3900
  }
]

// Using 'export default' ensures App.jsx never loses the reference
export default function GeneratedComponent() {
  return (
    <ChartContainer config={chartConfig} className="min-h-[300px] w-full">
      <BarChart accessibilityLayer data={chartData}>
        <CartesianGrid vertical={false} />
        <XAxis
            dataKey="month"
            tickLine={false}
            axisLine={false}
            tickMargin={10}
        />
        <YAxis tickLine={false} axisLine={false} />
        <ChartTooltip content={<ChartTooltipContent />} />
        <ChartLegend content={<ChartLegendContent />} />

        <Bar dataKey="subscriptions" fill="var(--color-subscriptions)" radius={4} />

        <Bar dataKey="revenue" fill="var(--color-revenue)" radius={4} />

      </BarChart>
    </ChartContainer>
  )
}
