import React, { useState, useEffect } from "react";
import PriceMonitor from "./components/PriceMonitor";
import SentimentDashboard from "./components/SentimentDashboard";
import { priceService, sentimentService } from "./services/api";

function App() {
  const [activeTab, setActiveTab] = useState("split");

  // Data State
  const [prices, setPrices] = useState([]);
  const [opportunities, setOpportunities] = useState([]);
  const [sentiments, setSentiments] = useState([]);
  const [alerts, setAlerts] = useState([]);

  // Loading/Error State
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchGlobalData = async () => {
    try {
      // Parallel fetching for performance
      const [pricesRes, oppRes, sentRes, alertRes] = await Promise.all([
        priceService.getCurrentPrices(),
        priceService.getPriceOpportunities(),
        sentimentService.getAllSentiment(),
        sentimentService.getSentimentAlerts()
      ]);

      setPrices(pricesRes.data.data || []);
      setOpportunities(oppRes.data.opportunities || []);
      setSentiments(sentRes.data.data || []);
      setAlerts(alertRes.data.alerts || []);
      setLoading(false);
      setError(null);
    } catch (err) {
      console.error("Global fetch error:", err);
      setError("Disconnected from Live Feed. Retrying...");
      // Don't clear data immediately to allow offline viewing
    }
  };

  useEffect(() => {
    fetchGlobalData();
    const interval = setInterval(fetchGlobalData, 10000); // 10s refresh
    return () => clearInterval(interval);
  }, []);

  const sharedProps = { prices, opportunities, sentiments, alerts, loading, error };

  return (
    <div className="flex flex-col h-screen text-gray-100 overflow-hidden">
      {/* Glass Header */}
      <header className="glass-header px-8 py-4 flex justify-between items-center z-50">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/30">
            <span className="text-white font-bold text-lg">H</span>
          </div>
          <h1 className="text-xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
            HALAN <span className="font-light">INVEST</span>
          </h1>
        </div>

        {/* Navigation Pills */}
        <nav className="flex bg-black/20 p-1 rounded-full border border-white/5">
          {['split', 'prices', 'sentiment'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-6 py-1.5 rounded-full text-sm font-medium transition-all duration-300 ${activeTab === tab
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/40'
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </nav>

        {/* Status Indicator */}
        <div className="flex items-center space-x-2">
          <span className={`w-2 h-2 rounded-full ${!error ? 'bg-emerald-400 animate-pulse-glow' : 'bg-red-500'}`}></span>
          <span className="text-xs font-medium text-gray-400">
            {error ? 'RECONNECTING' : 'SYSTEM ONLINE'}
          </span>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 overflow-hidden relative">
        {/* Background decorative blobs */}
        <div className="absolute top-0 left-0 w-96 h-96 bg-purple-600/20 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2 pointer-events-none"></div>
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-indigo-600/20 rounded-full blur-3xl translate-x-1/2 translate-y-1/2 pointer-events-none"></div>

        <div className="h-full p-6 overflow-hidden">
          {activeTab === "split" && (
            <div className="grid grid-cols-2 gap-6 h-full overflow-hidden">
              <div className="glass-panel rounded-2xl overflow-hidden relative border-t border-l border-white/10">
                <PriceMonitor {...sharedProps} />
              </div>
              <div className="glass-panel rounded-2xl overflow-y-auto relative border-t border-l border-white/10">
                <SentimentDashboard {...sharedProps} />
              </div>
            </div>
          )}

          {activeTab === "prices" && (
            <div className="glass-panel rounded-2xl h-full overflow-hidden border-t border-l border-white/10">
              <PriceMonitor {...sharedProps} />
            </div>
          )}

          {activeTab === "sentiment" && (
            <div className="glass-panel rounded-2xl h-full overflow-hidden border-t border-l border-white/10">
              <SentimentDashboard {...sharedProps} />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
