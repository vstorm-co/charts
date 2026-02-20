# Frontend Integration

Use generated components in your React project.

## shadcn/ui Setup

First, install the required shadcn components:

```bash
npx shadcn@latest add accordion button card carousel chart select table
```

This installs:
- `accordion` - For Accordion component
- `button` - Required by many components
- `card` - For Card component
- `carousel` - For Carousel component
- `chart` - For Chart component (Recharts wrappers)
- `select` - Optional, for dropdowns
- `table` - For Table component

## Component File Structure

Generated components go in your project's UI directory:

```bash
src/
├── components/
│   └── ui/                # Generated components
│       ├── accordion.tsx
│       ├── button.tsx     # shadcn dependency
│       ├── card.tsx
│       ├── carousel.tsx
│       ├── chart.tsx      # Recharts wrapper
│       └── table.tsx
```

## Using the Preview App

The preview app provides a live preview of generated components:

```bash
# Terminal 1: Start API server
cd preview_app && npm run api-server

# Terminal 2: Start Vite dev server
npm install && npm run dev
```

Visit `http://localhost:5173` to see the agent in action.

## Manual Integration

### 1. Copy Generated TSX

Copy the generated component code from the tool output:

```tsx
// src/components/ui/MyChart.tsx
"use client"

import { Bar, BarChart, CartesianGrid, XAxis } from "recharts"
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import {
    ChartConfig,
    ChartContainer,
    ChartTooltip,
    ChartTooltipContent,
} from "@/components/ui/chart"

const chartData = [
    { month: "January", desktop: 186, mobile: 80 },
    { month: "February", desktop: 305, mobile: 90 },
]

const chartConfig = {
    desktop: { label: "Desktop", color: "#2563eb" },
    mobile: { label: "Mobile", color: "#60a5fa" },
}

export function MyChart() {
    return (
        <Card>
            <CardHeader>
                <CardTitle>Monthly Sales</CardTitle>
                <CardDescription>January - June 2024</CardDescription>
            </CardHeader>
            <CardContent>
                <ChartContainer config={chartConfig}>
                    <BarChart data={chartData} xKey="month">
                        <CartesianGrid vertical={false} />
                        <XAxis
                            dataKey="month"
                            tickLine={false}
                            axisLine={false}
                        />
                        <ChartTooltip
                            cursor={false}
                            content={<ChartTooltipContent />}
                        />
                        <Bar dataKey="desktop" fill="var(--color-desktop)" radius={4} />
                        <Bar dataKey="mobile" fill="var(--color-mobile)" radius={4} />
                    </BarChart>
                </ChartContainer>
            </CardContent>
        </Card>
    )
}
```

### 2. Import and Use

```tsx
// src/App.tsx
import { MyChart } from './components/ui/MyChart'

function App() {
    return (
        <div className="container mx-auto p-4">
            <h1>Dashboard</h1>
            <MyChart />
        </div>
    )
}

export default App
```

## Dynamic Component Loading

For projects where components are generated at runtime:

```tsx
// src/components/DynamicComponent.tsx
interface DynamicComponentProps {
    componentType: string
    props: Record<string, any>
}

export function DynamicComponent({ componentType, props }: DynamicComponentProps) {
    // Import component dynamically based on type
    switch (componentType) {
        case 'chart':
            return import('./ui/GeneratedChart').then(m => <m.GeneratedChart {...props} />)
        case 'table':
            return import('./ui/GeneratedTable').then(m => <m.GeneratedTable {...props} />)
        default:
            return null
    }
}
```

## TypeScript Configuration

Ensure your `tsconfig.json` includes the UI components:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/ui": ["./src/components/ui"]
    }
  }
}
```
