import React, { useState, useEffect } from "react";
import { sentimentService } from "../services/api";

const SentimentDashboard = () => {
  const [sentiments, setSentiments] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 20000); // Refresh every 20 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [sentRes, alertRes] = await Promise.all([
        sentimentService.getAllSentiment(),
        sentimentService.getSentimentAlerts(),
      ]);

      setSentiments(sentRes.data.data || []);
      setAlerts(alertRes.data.alerts || []);
      setError(null);
    } catch (err) {
      // Only show error if sentiments were never loaded
      if (sentiments.length === 0) {
        setError("Failed to fetch sentiment data. Retrying...");
      }
      console.error("Sentiment fetch error:", err.message);
    } finally {
      setLoading(false);
    }
  };

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

  return (
    <div className="h-full flex flex-col bg-gray-50 p-6">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">💬 Sentiment Analysis</h1>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {loading && sentiments.length === 0 ? (
        <div className="flex justify-center items-center h-full">
          <div className="text-gray-500">Loading sentiment data...</div>
        </div>
      ) : (
        <>
          {/* Sentiment Cards */}
          <div className="grid grid-cols-2 gap-4 mb-6">
            {sentiments.map((sentiment) => {
              const distribution = sentiment.sentiment_distribution;
              return (
                <div
                  key={sentiment.fund}
                  className={`rounded-lg shadow p-4 border-2 ${getSentimentColor(
                    sentiment.overall_score
                  )}`}
                >
                  <div className="mb-3">
                    <h3 className="text-sm font-semibold text-gray-700">
                      {sentiment.fund.replace(/_/g, " ").toUpperCase()}
                    </h3>
                    <p className="text-2xl font-bold mt-1">
                      {getSentimentLabel(sentiment.overall_score)}
                    </p>
                  </div>

                  {/* Distribution Bars */}
                  <div className="space-y-2 text-sm">
                    <div>
                      <div className="flex justify-between mb-1">
                        <span className="text-green-700">Positive</span>
                        <span className="font-semibold">
                          {distribution.positive.toFixed(1)}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-300 rounded h-2">
                        <div
                          className="bg-green-500 h-2 rounded"
                          style={{
                            width: `${distribution.positive}%`,
                          }}
                        ></div>
                      </div>
                    </div>

                    <div>
                      <div className="flex justify-between mb-1">
                        <span className="text-yellow-700">Neutral</span>
                        <span className="font-semibold">
                          {distribution.neutral.toFixed(1)}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-300 rounded h-2">
                        <div
                          className="bg-yellow-500 h-2 rounded"
                          style={{
                            width: `${distribution.neutral}%`,
                          }}
                        ></div>
                      </div>
                    </div>

                    <div>
                      <div className="flex justify-between mb-1">
                        <span className="text-red-700">Negative</span>
                        <span className="font-semibold">
                          {distribution.negative.toFixed(1)}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-300 rounded h-2">
                        <div
                          className="bg-red-500 h-2 rounded"
                          style={{
                            width: `${distribution.negative}%`,
                          }}
                        ></div>
                      </div>
                    </div>
                  </div>

                  <p className="text-xs text-gray-600 mt-3">
                    {sentiment.source_count} mentions analyzed
                  </p>
                </div>
              );
            })}
          </div>

          {/* Alerts */}
          {alerts.length > 0 && (
            <div className="bg-white rounded-lg shadow p-4">
              <h2 className="text-lg font-semibold text-gray-800 mb-4">
                ⚠️ Sentiment Alerts
              </h2>

              <div className="space-y-2">
                {alerts.map((alert, idx) => (
                  <div
                    key={idx}
                    className="p-3 rounded bg-blue-50 border-l-4 border-blue-500"
                  >
                    <p className="font-semibold text-gray-800">
                      {alert.alert}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {alerts.length === 0 && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center text-blue-700">
              No significant sentiment changes detected
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default SentimentDashboard;
