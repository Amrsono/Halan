import React, { useState, useEffect } from "react";
import { priceService, recommendationService } from "../services/api";

const PriceMonitor = () => {
  const [prices, setPrices] = useState([]);
  const [opportunities, setOpportunities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 15000); // Refresh every 15 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [pricesRes, oppRes] = await Promise.all([
        priceService.getCurrentPrices(),
        priceService.getPriceOpportunities(),
      ]);

      setPrices(pricesRes.data.data || []);
      setOpportunities(oppRes.data.opportunities || []);
      setError(null);
    } catch (err) {
      // Only show error if prices were never loaded
      if (prices.length === 0) {
        setError("Failed to fetch price data. Retrying...");
      }
      console.error("Price fetch error:", err.message);
    } finally {
      setLoading(false);
    }
  };

  const getChangeColor = (change) => {
    return change < 0 ? "text-red-600" : "text-green-600";
  };

  return (
    <div className="h-full flex flex-col bg-gray-50 p-6">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">📊 Price Monitor</h1>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {loading && prices.length === 0 ? (
        <div className="flex justify-center items-center h-full">
          <div className="text-gray-500">Loading price data...</div>
        </div>
      ) : (
        <>
          {/* Price Cards */}
          <div className="grid grid-cols-2 gap-4 mb-6">
            {prices.map((price) => (
              <div
                key={price.fund}
                className="bg-white rounded-lg shadow p-4 border-l-4 border-blue-500"
              >
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h3 className="text-sm font-semibold text-gray-700">
                      {price.fund.replace(/_/g, " ").toUpperCase()}
                    </h3>
                    <p className="text-xs text-gray-500">{price.ticker}</p>
                  </div>
                  <span
                    className={`text-lg font-bold ${getChangeColor(
                      price.change
                    )}`}
                  >
                    {price.change > 0 ? "+" : ""}
                    {price.change.toFixed(2)}%
                  </span>
                </div>

                <p className="text-2xl font-bold text-gray-800 mb-2">
                  EGP {price.price.toFixed(2)}
                </p>

                <div className="flex justify-between text-xs text-gray-500">
                  <span>Vol: {(price.volume / 1000).toFixed(0)}K</span>
                  <span>
                    {new Date(price.timestamp).toLocaleTimeString()}
                  </span>
                </div>
              </div>
            ))}
          </div>

          {/* Opportunities */}
          {opportunities.length > 0 && (
            <div className="bg-white rounded-lg shadow p-4">
              <h2 className="text-lg font-semibold text-gray-800 mb-4">
                🎯 Price Opportunities
              </h2>

              <div className="space-y-2">
                {opportunities.map((opp, idx) => (
                  <div
                    key={idx}
                    className={`p-3 rounded flex justify-between items-center ${opp.action === "BUY"
                        ? "bg-green-50 border-l-4 border-green-500"
                        : "bg-red-50 border-l-4 border-red-500"
                      }`}
                  >
                    <div>
                      <p className="font-semibold text-gray-800">
                        {opp.fund.replace(/_/g, " ")}
                      </p>
                      <p className="text-sm text-gray-600">
                        {opp.action} - {opp.magnitude.toFixed(2)}% movement
                      </p>
                    </div>
                    <div className="text-right">
                      <span
                        className={`px-3 py-1 rounded text-sm font-semibold text-white ${opp.action === "BUY"
                            ? "bg-green-500"
                            : "bg-red-500"
                          }`}
                      >
                        {opp.action}
                      </span>
                      <p className="text-xs text-gray-600 mt-1">
                        {(opp.confidence * 100).toFixed(0)}% confidence
                      </p>
                    </div>
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

export default PriceMonitor;
