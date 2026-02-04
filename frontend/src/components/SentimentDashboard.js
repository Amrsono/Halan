import React from "react";

const SentimentDashboard = ({ sentiments, alerts, loading, error }) => {

  const getSentimentColor = (score) => {
    if (score > 0.3) return "bg-green-100 border-green-400";
    if (score < -0.3) return "bg-red-100 border-red-400";
    return "bg-yellow-100 border-yellow-400";
  };

  const getSentimentLabel = (score) => {
    if (score > 0.3) return "🟢 Positive";
    if (score < -0.3) return "🔴 Negative";
    return "🟡 Neutral";
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
    <div className="flex flex-col p-6 h-full overflow-y-auto">
      <h2 className="text-2xl font-bold text-white mb-6 flex-shrink-0 flex items-center">
        <span className="bg-purple-500/20 p-2 rounded-lg mr-3 text-purple-400">💬</span>
        Sentiment Analysis
      </h2>

      {error && (
        <div className="bg-red-500/10 border border-red-500/50 text-red-200 px-4 py-3 rounded mb-4 backdrop-blur-sm">
          {error}
        </div>
      )}

      {loading && sentiments.length === 0 ? (
        <div className="flex justify-center items-center h-full">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
        </div>
      ) : (
        <>
          {/* Sentiment Cards */}
          <div className="grid grid-cols-2 gap-4 mb-6 flex-shrink-0">
            {sentiments.map((sentiment) => {
              const distribution = sentiment.sentiment_distribution;
              const borderColor = sentiment.overall_score >= 0.5 ? 'border-emerald-500/50'
                : sentiment.overall_score <= -0.5 ? 'border-red-500/50'
                  : 'border-white/10';

              return (
                <div
                  key={sentiment.fund}
                  className={`glass-panel rounded-xl p-5 hover:scale-[1.02] transition-transform duration-300 border-l-4 ${borderColor}`}
                >
                  <div className="mb-4 flex justify-between items-start">
                    <div>
                      <h3 className="text-sm font-medium text-gray-400">
                        {sentiment.fund.replace(/_/g, " ").toUpperCase()}
                      </h3>
                      <p className="text-2xl font-bold mt-1 text-white">
                        {getSentimentLabel(sentiment.overall_score)}
                      </p>
                    </div>
                    <div className="text-right">
                      <span className="text-xs text-gray-500 block">Score</span>
                      <span className={`font-mono font-bold ${sentiment.overall_score > 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                        {sentiment.overall_score > 0 ? '+' : ''}{sentiment.overall_score}
                      </span>
                    </div>
                  </div>

                  {/* Distribution Bars */}
                  <div className="space-y-3 text-sm">
                    {/* Positive */}
                    <div>
                      <div className="flex justify-between mb-1 text-xs">
                        <span className="text-emerald-300">Positive</span>
                        <span className="text-gray-400">{distribution.positive.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-white/5 rounded-full h-1.5">
                        <div className="bg-emerald-500 h-1.5 rounded-full shadow-[0_0_10px_rgba(16,185,129,0.5)]" style={{ width: `${distribution.positive}%` }}></div>
                      </div>
                    </div>

                    {/* Neutral */}
                    <div>
                      <div className="flex justify-between mb-1 text-xs">
                        <span className="text-gray-300">Neutral</span>
                        <span className="text-gray-400">{distribution.neutral.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-white/5 rounded-full h-1.5">
                        <div className="bg-gray-500 h-1.5 rounded-full" style={{ width: `${distribution.neutral}%` }}></div>
                      </div>
                    </div>

                    {/* Negative */}
                    <div>
                      <div className="flex justify-between mb-1 text-xs">
                        <span className="text-red-300">Negative</span>
                        <span className="text-gray-400">{distribution.negative.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-white/5 rounded-full h-1.5">
                        <div className="bg-red-500 h-1.5 rounded-full shadow-[0_0_10px_rgba(239,68,68,0.5)]" style={{ width: `${distribution.negative}%` }}></div>
                      </div>
                    </div>
                  </div>

                  <p className="text-xs text-gray-500 mt-4 border-t border-white/5 pt-2 flex justify-between">
                    <span>{sentiment.source_count} sources</span>
                    <span>Confidence: High</span>
                  </p>
                </div>
              );
            })}
          </div>

          {/* Alerts */}
          {alerts.length > 0 && (
            <div className="glass-panel rounded-xl p-4 mb-6 border-l-4 border-yellow-500 flex-shrink-0">
              <h2 className="text-lg font-semibold text-white mb-3 flex items-center">
                ⚠️ Sentiment Alerts
              </h2>
              <div className="space-y-2">
                {alerts.map((alert, idx) => (
                  <div
                    key={idx}
                    className="p-3 rounded bg-yellow-500/10 border border-yellow-500/20 text-yellow-200 text-sm"
                  >
                    {alert.alert}
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default SentimentDashboard;
