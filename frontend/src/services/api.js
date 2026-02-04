import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
});

// Retry logic with exponential backoff
let retryCount = 0;
const MAX_RETRIES = 3;
const BASE_DELAY = 1000;

api.interceptors.response.use(
  (response) => {
    retryCount = 0;
    return response;
  },
  async (error) => {
    const config = error.config;
    if (
      !config ||
      config.retry === false ||
      retryCount >= MAX_RETRIES ||
      !error.response ||
      error.response.status < 500
    ) {
      return Promise.reject(error);
    }
    retryCount++;
    config.retry = false;
    const delay = BASE_DELAY * Math.pow(2, retryCount - 1);
    await new Promise((resolve) => setTimeout(resolve, delay));
    return api(config);
  }
);

// Price endpoints
export const priceService = {
  getCurrentPrices: () => api.get("/prices/current"),
  getFundPrice: (fundName) => api.get(`/prices/fund/${fundName}`),
  getPriceOpportunities: () => api.get("/prices/opportunities"),
  getPriceHistory: (fundName, days = 7) =>
    api.get(`/prices/history/${fundName}`, { params: { days } }),
};

// Sentiment endpoints
export const sentimentService = {
  getAllSentiment: () => api.get("/sentiment/all"),
  getFundSentiment: (fundName) => api.get(`/sentiment/fund/${fundName}`),
  getTrendingKeywords: (fundName) =>
    api.get(`/sentiment/trending/${fundName}`),
  getSentimentAlerts: () => api.get("/sentiment/alerts"),
};

// Recommendation endpoints
export const recommendationService = {
  getAllRecommendations: () => api.get("/recommendations/all"),
  getTopOpportunities: () => api.get("/recommendations/opportunities"),
  getRiskAssessment: (fundName) =>
    api.get(`/recommendations/risk/${fundName}`),
};

export default api;
