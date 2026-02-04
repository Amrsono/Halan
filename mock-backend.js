/**
 * Mock Backend Server for Development
 * Simulates all API endpoints without Python/FastAPI
 * Run: node mock-backend.js
 */

const express = require('express');
const cors = require('cors');

const app = express();
const PORT = 8000;

// Middleware
app.use(cors());
app.use(express.json());

// Mock data
const FUNDS = ['halan_saving', 'az_gold', 'az_opportunity', 'az_shariah'];

function getMockPriceData() {
  return FUNDS.map((fund) => {
    const basePrice = { halan_saving: 105, az_gold: 98, az_opportunity: 102, az_shariah: 101 };
    return {
      fund,
      ticker: fund.split('_')[0].toUpperCase(),
      price: (basePrice[fund] || 100) + (Math.random() - 0.5) * 5,
      change: -2.5 + Math.random() * 5,
      volume: 1000000 + Math.floor(Math.random() * 500000),
      timestamp: new Date().toISOString(),
    };
  });
}

function getMockSentimentData() {
  return FUNDS.map((fund) => {
    const positive = 40 + Math.random() * 50;
    const negative = 10 + Math.random() * 20;
    const neutral = 100 - positive - negative;
    return {
      fund,
      sentiment_distribution: {
        positive,
        neutral: Math.max(5, neutral),
        negative: Math.max(5, negative),
      },
      overall_score: (positive - negative) / 100,
      trending: Math.random() > 0.5,
      source_count: Math.floor(100 + Math.random() * 200),
      timestamp: new Date().toISOString(),
    };
  });
}

// Routes: Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'halan-invest-mock-api' });
});

// Routes: Prices
app.get('/api/prices/current', (req, res) => {
  res.json({ data: getMockPriceData(), timestamp: new Date().toISOString() });
});

app.get('/api/prices/fund/:fundName', (req, res) => {
  const prices = getMockPriceData();
  const price = prices.find((p) => p.fund === req.params.fundName);
  if (price) {
    res.json({ data: price });
  } else {
    res.status(404).json({ error: 'Fund not found' });
  }
});

app.get('/api/prices/opportunities', (req, res) => {
  const prices = getMockPriceData();
  const opportunities = prices
    .filter((p) => Math.abs(p.change) > 2)
    .map((p) => ({
      fund: p.fund,
      opportunity: 'price_swing',
      magnitude: p.change,
      action: p.change < 0 ? 'BUY' : 'SELL',
      confidence: 0.75,
      timestamp: p.timestamp,
    }));
  res.json({ opportunities, count: opportunities.length });
});

app.get('/api/prices/history/:fundName', (req, res) => {
  res.json({
    fund: req.params.fundName,
    days: parseInt(req.query.days) || 7,
    data: [],
  });
});

// Routes: Sentiment
app.get('/api/sentiment/all', (req, res) => {
  res.json({ data: getMockSentimentData(), timestamp: new Date().toISOString() });
});

app.get('/api/sentiment/fund/:fundName', (req, res) => {
  const sentiments = getMockSentimentData();
  const sentiment = sentiments.find((s) => s.fund === req.params.fundName);
  if (sentiment) {
    res.json({ data: sentiment });
  } else {
    res.status(404).json({ error: 'Fund not found' });
  }
});

app.get('/api/sentiment/trending/:fundName', (req, res) => {
  const keywords = {
    halan_saving: ['growth', 'savings', 'compound'],
    az_gold: ['gold', 'hedge', 'inflation'],
    az_opportunity: ['opportunity', 'rally', 'bullish'],
    az_shariah: ['sharia', 'compliant', 'ethical'],
  };
  res.json({
    fund: req.params.fundName,
    trending_keywords: keywords[req.params.fundName] || [],
    timestamp: new Date().toISOString(),
  });
});

app.get('/api/sentiment/alerts', (req, res) => {
  res.json({ alerts: [] });
});

// Routes: Recommendations
app.get('/api/recommendations/all', (req, res) => {
  const recommendations = ['STRONG_BUY', 'BUY', 'HOLD', 'SELL', 'STRONG_SELL'];
  const recs = FUNDS.map((fund) => ({
    fund,
    recommendation: recommendations[Math.floor(Math.random() * recommendations.length)],
    confidence: 0.5 + Math.random() * 0.5,
    price_change: -2.5 + Math.random() * 5,
    sentiment_score: -1 + Math.random() * 2,
    target_price: 100 + Math.random() * 10,
    reason: 'Based on price and sentiment analysis',
    timestamp: new Date().toISOString(),
  }));
  res.json({ recommendations: recs, timestamp: new Date().toISOString() });
});

app.get('/api/recommendations/opportunities', (req, res) => {
  const recs = FUNDS.slice(0, 3).map((fund) => ({
    fund,
    recommendation: 'STRONG_BUY',
    confidence: 0.85 + Math.random() * 0.15,
    price_change: -3 + Math.random() * 2,
    sentiment_score: 0.5 + Math.random() * 0.5,
    target_price: 105 + Math.random() * 10,
    reason: 'Strong buy signal detected',
    timestamp: new Date().toISOString(),
  }));
  res.json({ top_opportunities: recs, count: recs.length, timestamp: new Date().toISOString() });
});

app.get('/api/recommendations/risk/:fundName', (req, res) => {
  res.json({
    fund: req.params.fundName,
    risk_score: 30 + Math.random() * 40,
    risk_level: 'MEDIUM',
    volatility: 0.02 + Math.random() * 0.04,
  });
});

// Root
app.get('/', (req, res) => {
  res.json({
    message: 'Halan Invest - Mock Backend API',
    version: '1.0.0',
    endpoints: {
      prices: '/api/prices',
      sentiment: '/api/sentiment',
      recommendations: '/api/recommendations',
      health: '/health',
    },
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`\n🚀 Mock Backend Server running on http://localhost:${PORT}\n`);
  console.log('📡 Available endpoints:');
  console.log('   /health - Service health');
  console.log('   /api/prices/current - All fund prices');
  console.log('   /api/sentiment/all - All sentiment data');
  console.log('   /api/recommendations/all - All recommendations');
  console.log('\n✨ Frontend: http://localhost:3000');
  console.log('💬 Type CTRL+C to stop\n');
});
