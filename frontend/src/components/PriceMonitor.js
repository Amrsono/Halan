import React from "react";

const PriceMonitor = ({ prices, sentiments, loading, error }) => {

  const getChangeColor = (change) => {
    return change < 0 ? "text-red-600" : "text-green-600";
  };

  const timeAgo = (dateString) => {
    if (!dateString) return "";
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);

    if (seconds < 60) return "just now";
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes}m ago`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="h-full flex flex-col p-6 overflow-y-auto">
      <h2 className="text-2xl font-bold text-white mb-6 flex-shrink-0 flex items-center">
        <span className="bg-indigo-500/20 p-2 rounded-lg mr-3 text-indigo-400">📊</span>
        Market Watch
      </h2>

      {error && (
        <div className="bg-red-500/10 border border-red-500/50 text-red-200 px-4 py-3 rounded mb-4 backdrop-blur-sm">
          {error}
        </div>
      )}

      {loading && prices.length === 0 ? (
        <div className="flex justify-center items-center h-full">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-2 gap-4 mb-6 flex-shrink-0">
            {prices.map((price) => (
              <div
                key={price.fund}
                className="glass-panel rounded-xl p-5 hover:scale-[1.02] transition-transform duration-300 border border-white/5"
              >
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-sm font-medium text-gray-400">
                    {price.ticker}
                  </h3>
                  <span
                    className={`text-xs font-bold px-2 py-1 rounded bg-opacity-20 ${price.change >= 0
                      ? "bg-green-500 text-green-400"
                      : "bg-red-500 text-red-400"
                      }`}
                  >
                    {price.change >= 0 ? "▲" : "▼"} {Math.abs(price.change)}%
                  </span>
                </div>

                <p className="text-3xl font-bold text-white mb-2 tracking-wide">
                  <span className="text-lg text-gray-500 mr-1">EGP</span>
                  {price.price.toFixed(2)}
                </p>

                {price.context_label && (
                  <div className="bg-indigo-500/10 border border-indigo-500/20 rounded px-2 py-1.5 mb-3">
                    <p className="text-xs text-indigo-300 font-medium flex items-center">
                      <span className="opacity-70 mr-1">ℹ️</span> {price.context_label}
                    </p>
                  </div>
                )}

                <div className="flex justify-between text-xs text-gray-500 border-t border-white/5 pt-3 mt-1">
                  <span>Vol: {(price.volume / 1000).toFixed(0)}K</span>
                  <span>
                    {new Date(price.timestamp).toLocaleTimeString()}
                  </span>
                </div>
              </div>
            ))}
          </div>

          {/* Market Feed */}
          <h3 className="text-lg font-semibold text-white mb-4 flex-shrink-0 flex items-center">
            <span className="text-purple-400 mr-2">📢</span>
            Market Feed
            <span className="ml-3 text-xs font-semibold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-1 rounded-full flex items-center shadow-[0_0_15px_rgba(16,185,129,0.2)]">
              <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full mr-1.5 animate-pulse-glow"></span>
              LIVE
            </span>
          </h3>

          <div className="flex-1 overflow-y-auto space-y-3 pr-2 custom-scrollbar">
            {sentiments.flatMap(s => s.recent_items || []).length === 0 ? (
              <p className="text-gray-500 italic text-center py-4">No recent market feed collected yet.</p>
            ) : (
              sentiments.flatMap(s =>
                (s.recent_items || []).map(item => ({ ...item, fund: s.fund }))
              )
                .sort((a, b) => (b.timestamp || "").localeCompare(a.timestamp || ""))
                .map((item, idx) => (
                  <div key={idx} className="group border-b border-white/5 pb-3 last:border-0 hover:bg-white/5 p-3 rounded-lg transition-colors">
                    <div className="flex justify-between items-start mb-1.5">
                      <span className={`inline-block text-[10px] px-2 py-0.5 rounded font-bold uppercase tracking-wide ${item.source.includes("Reddit") ? "bg-orange-500/20 text-orange-400 border border-orange-500/30" :
                          item.source.includes("Yahoo") ? "bg-blue-500/20 text-blue-400 border border-blue-500/30" :
                            item.source.includes("TradingView") ? "bg-purple-500/20 text-purple-400 border border-purple-500/30" :
                              item.source.includes("Investing") ? "bg-green-500/20 text-green-400 border border-green-500/30" :
                                "bg-indigo-500/20 text-indigo-400 border border-indigo-500/30"
                        }`}>
                        {item.source}
                      </span>
                      <span className="text-xs text-gray-500 font-mono">
                        {timeAgo(item.timestamp)}
                      </span>
                    </div>

                    <p className="text-gray-300 text-sm font-medium mb-2 leading-relaxed group-hover:text-white transition-colors">
                      "{item.text}"
                    </p>

                    <div className="flex justify-between items-center text-xs text-gray-500">
                      <span className="flex items-center">
                        <span className="w-1.5 h-1.5 rounded-full bg-gray-600 mr-2"></span>
                        {item.fund.replace(/_/g, " ").toUpperCase()}
                      </span>
                      {item.url && (
                        <a href={item.url} target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 hover:underline flex items-center transition-colors">
                          Source ↗
                        </a>
                      )}
                    </div>
                  </div>
                ))
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default PriceMonitor;
