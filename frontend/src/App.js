import React, { useState } from "react";
import PriceMonitor from "./components/PriceMonitor";
import SentimentDashboard from "./components/SentimentDashboard";
import "./index.css";

function App() {
  const [activeTab, setActiveTab] = useState("split");

  return (
    <div className="h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-4 shadow-lg">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">🚀 Halan Invest Orchestrator</h1>
            <p className="text-blue-100 text-sm">
              Real-time Fund Monitoring & Sentiment Analysis
            </p>
          </div>

          <div className="space-x-2">
            <button
              onClick={() => setActiveTab("split")}
              className={`px-4 py-2 rounded ${
                activeTab === "split"
                  ? "bg-white text-blue-600 font-semibold"
                  : "bg-blue-500 hover:bg-blue-400"
              }`}
            >
              Split View
            </button>
            <button
              onClick={() => setActiveTab("prices")}
              className={`px-4 py-2 rounded ${
                activeTab === "prices"
                  ? "bg-white text-blue-600 font-semibold"
                  : "bg-blue-500 hover:bg-blue-400"
              }`}
            >
              Prices
            </button>
            <button
              onClick={() => setActiveTab("sentiment")}
              className={`px-4 py-2 rounded ${
                activeTab === "sentiment"
                  ? "bg-white text-blue-600 font-semibold"
                  : "bg-blue-500 hover:bg-blue-400"
              }`}
            >
              Sentiment
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="h-[calc(100%-80px)]">
        {activeTab === "split" && (
          <div className="flex h-full">
            <div className="w-1/2 border-r border-gray-300 overflow-auto">
              <PriceMonitor />
            </div>
            <div className="w-1/2 overflow-auto">
              <SentimentDashboard />
            </div>
          </div>
        )}

        {activeTab === "prices" && (
          <div className="overflow-auto">
            <PriceMonitor />
          </div>
        )}

        {activeTab === "sentiment" && (
          <div className="overflow-auto">
            <SentimentDashboard />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
