import React, { useState, useEffect } from "react";
// Import directly for now to ensure visibility
import GeneratedUI from "./GeneratedComponent";

interface MetaData {
  status: string;
  lastUpdated: string;
}

export default function App() {
  const [meta, setMeta] = useState<MetaData>({
    status: "Waiting...",
    lastUpdated: "Never"
  });
  const [prompt, setPrompt] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await fetch("/api/status");
        if (response.ok) {
          const data: MetaData = await response.json();
          setMeta(data);
        }
      } catch (e) {
        // Silent fail
      }
    };

    const interval = setInterval(checkStatus, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleGenerate = async (e: React.FormEvent) => {
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

      await new Promise((resolve) => setTimeout(resolve, 1500));

      const statusResponse = await fetch("/api/status");
      if (statusResponse.ok) {
        const data: MetaData = await statusResponse.json();
        setMeta(data);
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Unknown error";
      console.error("Error generating component:", error);

      setMeta((prev) => ({
        ...prev,
        status: `Error: ${errorMessage}`
      }));
    } finally {
      setIsGenerating(false);
      setPrompt("");
    }
  };

  return (
    <div className="p-5 font-sans max-w-6xl mx-auto min-h-screen bg-slate-50">
      {/* Status Bar */}
      <div className="bg-slate-800 text-white px-5 py-3 rounded-lg flex justify-between mb-5 shadow-md">
        <span><strong className="text-slate-400 mr-2">Status:</strong> {meta.status}</span>
        <span><strong className="text-slate-400 mr-2">Last Update:</strong> {meta.lastUpdated}</span>
      </div>

      {/* Prompt Input Form */}
      <form onSubmit={handleGenerate} className="mb-5 p-4 bg-white rounded-lg border border-slate-200 shadow-sm">
        <label htmlFor="prompt-input" className="block mb-2 text-sm font-semibold text-slate-700">
          Agent Prompt
        </label>
        <div className="flex gap-3">
          <input
            id="prompt-input"
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="What should I build next?"
            disabled={isGenerating}
            className="flex-1 px-3 py-2 border border-slate-300 rounded-md text-sm outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-slate-100 transition-all"
          />
          <button
            type="submit"
            disabled={isGenerating || !prompt.trim()}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-400 text-white rounded-md text-sm font-bold transition-all shadow-sm active:scale-95"
          >
            {isGenerating ? "Generating..." : "Generate"}
          </button>
        </div>
      </form>

      {/* Main Preview Area */}
      <div
        key={meta.lastUpdated} // Forces re-render when data updates
        className="border-2 border-dashed border-slate-200 rounded-xl p-8 bg-white shadow-sm min-h-[500px] flex flex-col items-center justify-start"
      >
        <GeneratedUI />
      </div>
    </div>
  );
}
