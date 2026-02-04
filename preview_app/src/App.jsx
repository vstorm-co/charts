import React, { useState, useEffect } from "react";
import GeneratedUI from "./GeneratedComponent";

export default function App() {
  const [meta, setMeta] = useState({ status: "Waiting...", lastUpdated: "Never" });
  const [prompt, setPrompt] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);

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

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    setIsGenerating(true);

    try {
      const response = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        throw new Error(`Generation failed: ${response.statusText}`);
      }

      // Wait a bit for the backend to process and update status.json
      await new Promise((resolve) => setTimeout(resolve, 1500));

      // Trigger a status refresh
      const statusResponse = await fetch("/src/status.json");
      if (statusResponse.ok) {
        const data = await statusResponse.json();
        setMeta(data);
      }
    } catch (error) {
      console.error("Error generating chart:", error);
      // Still refresh status to show any error state
      try {
        const statusResponse = await fetch("/src/status.json");
        if (statusResponse.ok) {
          const data = await statusResponse.json();
          setMeta(data);
        }
      } catch (e) {
        // Update status to show error
        setMeta((prev) => ({ ...prev, status: `Error: ${error.message}` }));
      }
    } finally {
      setIsGenerating(false);
      setPrompt(""); // Clear input after submission
    }
  };

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

      {/* Prompt Input Form */}
      <form onSubmit={handleGenerate} style={{
        marginBottom: "20px",
        padding: "15px",
        background: "#f9fafb",
        borderRadius: "8px",
        border: "1px solid #e5e7eb"
      }}>
        <label htmlFor="prompt-input" style={{
          display: "block",
          marginBottom: "8px",
          fontSize: "14px",
          fontWeight: "600",
          color: "#374151"
        }}>
          Agent Prompt
        </label>
        <div style={{ display: "flex", gap: "10px" }}>
          <input
            id="prompt-input"
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Enter a prompt to generate a chart (e.g., 'Show monthly subscriptions and revenue')..."
            disabled={isGenerating}
            style={{
              flex: 1,
              padding: "10px 12px",
              border: "1px solid #d1d5db",
              borderRadius: "6px",
              fontSize: "14px",
              outline: "none",
              disabled: { backgroundColor: "#e5e7eb", cursor: "not-allowed" }
            }}
          />
          <button
            type="submit"
            disabled={isGenerating || !prompt.trim()}
            style={{
              padding: "10px 20px",
              background: isGenerating ? "#9ca3af" : "#2563eb",
              color: "#fff",
              border: "none",
              borderRadius: "6px",
              fontSize: "14px",
              fontWeight: "600",
              cursor: isGenerating ? "not-allowed" : "pointer",
              transition: "background-color 0.2s"
            }}
          >
            {isGenerating ? "Generating..." : "Generate"}
          </button>
        </div>
      </form>

      <div style={{ border: "2px solid #eee", borderRadius: "12px", padding: "20px" }}>
        <React.Suspense fallback={<div>Loading Component...</div>}>
          <GeneratedUI />
        </React.Suspense>
      </div>
    </div>
  );
}
