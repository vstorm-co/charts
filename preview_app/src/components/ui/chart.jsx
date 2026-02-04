import React from "react"
import {
  BarChart as BChart,
  Bar as B,
  LineChart as LChart,
  Line as L,
  PieChart as PChart,
  Pie as Pi,
  AreaChart as AChart,
  Area as A,
  RadarChart as RChart,
  Radar as R,
  PolarGrid as PG,
  PolarAngleAxis as PAA,
  Cell as C,
  XAxis as X,
  YAxis as Y,
  CartesianGrid as CG,
  Tooltip as T,
  Legend as Le,
  ResponsiveContainer
} from "recharts"

import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "./card"

export {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent
}

// --- Re-exports for Recharts ---
export const BarChart = BChart
export const Bar = B
export const LineChart = LChart
export const Line = L
export const PieChart = PChart
export const Pie = Pi
export const AreaChart = AChart
export const Area = A
export const RadarChart = RChart
export const Radar = R
export const PolarGrid = PG
export const PolarAngleAxis = PAA
export const Cell = C
export const XAxis = X
export const YAxis = Y
export const CartesianGrid = CG
export const ChartTooltip = T
export const ChartLegend = Le

// --- Chart Container with CSS Variable Logic ---
export const ChartContainer = ({ config = {}, children, className = "" }) => {
  const style = React.useMemo(() => {
    return Object.entries(config || {}).reduce((acc, [key, value]) => {
      if (value && value.color) acc[`--color-${key}`] = value.color;
      return acc;
    }, {});
  }, [config]);

  return (
    <div 
      className={className} 
      style={{ 
        ...style, 
        width: "100%", 
        height: "350px", // Added a default height
        minHeight: "300px", // Ensures it respects your template's intent
        position: "relative" // Helps Recharts calculate dimensions
      }}
    >
      <ResponsiveContainer width="100%" height="100%">
        {children}
      </ResponsiveContainer>
    </div>
  )
}

// --- Tooltip & Legend Content ---
export const ChartTooltipContent = ({ active, payload, label }) => {
  if (!active || !payload) return null;
  return (
    <div style={{ background: "white", border: "1px solid #e4e4e7", padding: "8px 12px", borderRadius: "6px", boxShadow: "0 4px 6px -1px rgba(0,0,0,0.1)" }}>
      <div style={{ fontWeight: 600, marginBottom: "4px" }}>{label}</div>
      {payload.map((item, i) => (
        <div key={i} style={{ fontSize: "12px", display: "flex", alignItems: "center", gap: "8px" }}>
          <div style={{ width: "8px", height: "8px", borderRadius: "2px", background: item.color || item.payload.fill }} />
          <span>{item.name}: {item.value}</span>
        </div>
      ))}
    </div>
  );
};

export const ChartLegendContent = ({ payload }) => {
  if (!payload) return null;
  return (
    <div style={{ display: "flex", justifyContent: "center", gap: "16px", fontSize: "12px", marginTop: "16px" }}>
      {payload.map((entry, index) => (
        <div key={index} style={{ display: "flex", alignItems: "center", gap: "4px" }}>
          <div style={{ width: "10px", height: "10px", backgroundColor: entry.color, borderRadius: "2px" }} />
          <span>{entry.value}</span>
        </div>
      ))}
    </div>
  );
};