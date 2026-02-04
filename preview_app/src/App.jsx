import React, { useState, useEffect } from "react";
import GeneratedUI from "./GeneratedComponent";

export default function App() {
  const [meta, setMeta] = useState({ status: "Waiting...", lastUpdated: "Never" });

  // Poll for the status.json file manually so it doesn't crash the build
  useEffect(() => {
    const checkStatus = async () => {
      try {
        // We fetch from /src/status.json (Vite serves this)
        const response = await fetch("/src/status.json");
        if (response.ok) {
          const data = await response.json();
          setMeta(data);
        }
      } catch (e) {
        // Silent fail if file doesn't exist yet
      }
    };

    const interval = setInterval(checkStatus, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
      <div style={{
        background: "#333",
        color: "#fff",
        padding: "10px 20px",
        borderRadius: "8px",
        display: "flex",
        justifyContent: "space-between",
        marginBottom: "20px"
      }}>
        <span><strong>Status:</strong> {meta.status}</span>
        <span><strong>Last Update:</strong> {meta.lastUpdated}</span>
      </div>

      <div style={{ border: "2px solid #eee", borderRadius: "12px", padding: "20px" }}>
        <React.Suspense fallback={<div>Loading Component...</div>}>
          <GeneratedUI />
        </React.Suspense>
      </div>
    </div>
  );
}
