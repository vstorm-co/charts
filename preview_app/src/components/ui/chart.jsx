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

// Explicitly define and export each component
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

// The Container (No changes needed here, height/width logic remains same)
export const ChartContainer = ({ config, children, className }) => {
  const style = React.useMemo(() => {
    return Object.entries(config).reduce((acc, [key, value]) => {
      acc[`--color-${key}`] = value.color;
      return acc;
    }, {});
  }, [config]);

  return (
    <div className={className} style={{ ...style, width: "100%", height: "400px" }}>
      <ResponsiveContainer width="100%" height="100%">
        {children}
      </ResponsiveContainer>
    </div>
  )
}

// Tooltip and Legend Content (No changes needed, Recharts passes payload same way)
export const ChartTooltipContent = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div style={{
        background: "white",
        border: "1px solid #ccc",
        padding: "8px",
        borderRadius: "4px",
        fontSize: "12px",
        boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
      }}>
        <p style={{ margin: 0, fontWeight: "bold", marginBottom: "4px" }}>{label}</p>
        {payload.map((item, i) => (
          <div key={i} style={{ color: item.color || item.payload.fill || "#333" }}>
            {item.name}: {item.value}
          </div>
        ))}
      </div>
    );
  }
  return null;
};

export const ChartLegendContent = ({ payload }) => {
  if (!payload) return null;
  return (
    <div style={{ display: "flex", justifyContent: "center", gap: "16px", fontSize: "12px", marginTop: "10px" }}>
      {payload.map((entry, index) => (
        <span key={index} style={{ display: "flex", alignItems: "center", gap: "4px" }}>
          <span style={{ width: "10px", height: "10px", backgroundColor: entry.color, borderRadius: "2px" }} />
          {entry.value}
        </span>
      ))}
    </div>
  );
};
