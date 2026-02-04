# 🚀 Halan Invest - Fund Orchestrator

Real-time monitoring and sentiment analysis platform for Egyptian investment funds with AI-powered trading recommendations.

## 📋 Features

### 🎯 Core Agents
- **Price Monitor Agent**: Real-time fund price tracking with arbitrage detection
- **Sentiment Analyzer Agent**: Social sentiment analysis from X (Twitter) & Farcaster
- **Recommendation Engine**: AI-driven buy/sell recommendations based on technical & sentiment signals

### 📊 Supported Funds
1. **Halan Saving** - Long-term savings fund
2. **AZ Gold** - Gold hedge fund
3. **AZ Opportunity** - Growth opportunities fund
4. **AZ Shariah** - Islamic-compliant Sharia fund

### 🎨 Split-Screen Dashboard
- **Left Side**: Real-time price monitor with opportunities
- **Right Side**: Sentiment analysis & trending keywords
- **Tabs**: Switch between split view, prices-only, or sentiment-only

## 🏗️ Architecture

```
Halan Invest/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── agents/         # Specialized agents
│   │   │   ├── price_monitor.py
│   │   │   ├── sentiment_analyzer.py
│   │   │   └── recommendation_engine.py
│   │   ├── models/         # Database models
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page containers
│   │   ├── services/       # API client
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml       # Docker orchestration
├── .env.example            # Environment template
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Option 1: Docker (Recommended)

1. **Clone and setup**
```bash
cd "d:/New projects/Project halan invest"
cp .env.example .env
```

2. **Start all services**
```bash
docker-compose up -d
```

3. **Access the app**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Local Development

**Backend Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend Setup:**
```bash
cd frontend
npm install
npm start
```

**Database:**
```bash
# Start PostgreSQL (ensure it's running on localhost:5432)
# Then initialize:
python -c "from app.models.database import init_db; init_db()"
```

## 📡 API Endpoints

### Prices
- `GET /api/prices/current` - Get current prices for all funds
- `GET /api/prices/fund/{fund_name}` - Get price for specific fund
- `GET /api/prices/opportunities` - Get arbitrage opportunities
- `GET /api/prices/history/{fund_name}` - Get price history

### Sentiment
- `GET /api/sentiment/all` - Get sentiment for all funds
- `GET /api/sentiment/fund/{fund_name}` - Get sentiment for specific fund
- `GET /api/sentiment/trending/{fund_name}` - Get trending keywords
- `GET /api/sentiment/alerts` - Get sentiment-based alerts

### Recommendations
- `GET /api/recommendations/all` - Get recommendations for all funds
- `GET /api/recommendations/opportunities` - Get top 3 trading opportunities
- `GET /api/recommendations/risk/{fund_name}` - Get risk assessment

### Health
- `GET /health` - Service health check

## 🔧 Configuration

Edit `.env` file to configure:

```env
# Database
DB_USER=user
DB_PASSWORD=password
DB_NAME=halan_invest

# API Keys (add your real keys)
TWITTER_API_KEY=your_key
FARCASTER_API_KEY=your_key
THNDR_API_KEY=your_key

# Trading (use with caution!)
ENABLE_LIVE_TRADING=False
TRADE_SIZE_LIMIT=1000
SLIPPAGE_TOLERANCE=0.5
```

## 🤖 How It Works

### Price Monitoring Flow
1. Monitor Agent fetches prices from EGX & brokers every 5 seconds
2. Detects price discrepancies between markets
3. Calculates 24h change and volume
4. Publishes opportunities to recommendation engine

### Sentiment Analysis Flow
1. Analyzer fetches tweets/posts about each fund
2. Processes text through sentiment model
3. Calculates positive/negative/neutral distribution
4. Generates trending keywords and alerts
5. Combines with price data for final recommendations

### Recommendation Generation
1. Combines price signals (change %, volume, technical indicators)
2. Weights sentiment score (positive = bullish, negative = bearish)
3. Generates BUY, SELL, HOLD, STRONG_BUY, STRONG_SELL signals
4. Assigns confidence score (0-1)
5. Calculates target price and risk assessment

## 🛡️ Safety Features

- **Dry-Run Mode**: All trades simulated by default
- **Trade Size Limits**: Configurable maximum trade size
- **Slippage Protection**: Configurable slippage tolerance
- **Circuit Breakers**: Auto-halt on abnormal market conditions
- **Audit Logging**: All actions logged to PostgreSQL
- **API Rate Limiting**: Built-in to prevent excessive calls

## 📊 Data Storage

### PostgreSQL Tables
- `price_history` - Historical price data
- `sentiment_records` - Sentiment analysis results
- `trade_recommendations` - Generated recommendations
- `trades` - Executed trades (when enabled)

## 🔌 Integration Guides

### Adding X (Twitter) API
1. Get credentials from https://developer.twitter.com
2. Add to `.env`:
```env
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
```
3. Update `sentiment_analyzer.py` to use real API

### Adding Farcaster API
1. Get API key from Farcaster
2. Add to `.env`:
```env
FARCASTER_API_KEY=your_key
```
3. Update sentiment analyzer to fetch Farcaster data

### Adding EGX Web Scraping
1. Install Selenium/Playwright
2. Update `price_monitor.py` with EGX listing page scraper
3. Parse HTML to extract real-time prices

## 📈 Performance

- **Response Time**: < 500ms for all API calls
- **Update Frequency**: Prices every 5s, sentiment every 10s
- **Database**: Optimized with indexes on `fund_name` and `timestamp`
- **Frontend**: React with lazy loading and caching

## ⚠️ Important Notes

### Legal & Compliance
- This is a monitoring tool, not financial advice
- Ensure you comply with local regulations (KYC/AML)
- Do NOT use live trading without proper risk management
- Test extensively on paper trading first
- Keep API keys secure - never commit to git

### Operational
- Monitor database disk usage (price history grows quickly)
- Set up backup cron jobs for PostgreSQL
- Configure alerts for API failures
- Use VPN/firewall to protect backend
- Consider rate limits on public APIs

## 🚨 Troubleshooting

### Port already in use
```bash
# Change ports in docker-compose.yml or
docker ps  # Find container
docker stop <container_id>
```

### Database connection error
```bash
# Ensure DB is running
docker-compose ps
docker-compose logs db
```

### Frontend can't reach backend
```bash
# Check API URL in .env
REACT_APP_API_URL=http://localhost:8000/api
```

### Out of memory
```bash
# Increase Docker memory limits
# Clean up old images/containers
docker system prune
```

## 📚 Documentation

- API Docs: http://localhost:8000/docs (Swagger UI)
- ReDoc: http://localhost:8000/redoc

## 🤝 Contributing

To add new features:
1. Create a new agent in `backend/app/agents/`
2. Add routes in `backend/app/routes/`
3. Update frontend components as needed
4. Add tests
5. Update documentation

## 📝 License

This project is provided as-is for educational and research purposes.

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Review logs: `docker-compose logs backend`
3. Check API health: http://localhost:8000/health

---

**Built with ❤️ for Egyptian fund investors**

**⚠️ DISCLAIMER**: This tool is for monitoring and analysis only. It does NOT provide financial advice. Use at your own risk and always consult with a professional advisor before making investment decisions.
