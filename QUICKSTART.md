# 🎯 Halan Invest - Quick Reference Guide

## What You Got 📦

A complete **full-stack investment monitoring platform** with:
- ✅ **3 Specialized Agents** (Price Monitor, Sentiment Analyzer, Recommendations)
- ✅ **Split-Screen Dashboard** (React frontend)
- ✅ **REST API** with comprehensive endpoints
- ✅ **PostgreSQL Database** for persistent storage
- ✅ **Docker Setup** for easy deployment
- ✅ **Complete Documentation** and setup guides

## Project Structure 📁

```
d:/New projects/Project halan invest/
├── backend/                    # Python FastAPI service
│   ├── app/
│   │   ├── agents/            # Three specialized agents
│   │   ├── models/            # Database schemas
│   │   ├── routes/            # API endpoints
│   │   ├── main.py            # FastAPI app
│   │   └── orchestrator.py     # Agent coordination
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                   # React dashboard
│   ├── src/
│   │   ├── components/        # UI components
│   │   ├── services/          # API client
│   │   └── App.js             # Main app
│   └── package.json
├── docker-compose.yml         # Docker orchestration
├── .env.example              # Environment template
├── README.md                 # Full documentation
├── SETUP.md                  # Setup instructions
├── start.sh / start.bat      # Quick start scripts
└── stocks.txt                # Your original file
```

## Quick Start (Choose One) ⚡

### Option A: Docker (Easiest - Recommended)
```bash
cd "d:/New projects/Project halan invest"
./start.bat          # On Windows
# or
bash start.sh        # On Mac/Linux
```
Then open: **http://localhost:3000**

### Option B: Manual Docker
```bash
cd "d:/New projects/Project halan invest"
cp .env.example .env
docker-compose up -d
```

### Option C: Local Development
```bash
# Terminal 1: Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm install
npm start
```

## Access Points 🌐

| Component | URL | Purpose |
|-----------|-----|---------|
| Dashboard | http://localhost:3000 | Main UI |
| API | http://localhost:8000 | REST endpoints |
| API Docs | http://localhost:8000/docs | Swagger UI |
| ReDoc | http://localhost:8000/redoc | Alternative docs |
| Health | http://localhost:8000/health | Service status |

## Main Features 🎨

### Left Side: Price Monitor 📊
- Real-time prices for 4 funds
- % change indicators (red/green)
- Trading volume
- Buy/Sell opportunities
- Refreshes every 5 seconds

### Right Side: Sentiment Analysis 💬
- Social sentiment distribution
- Positive/Negative/Neutral breakdown
- Trending keywords
- Sentiment alerts
- Source mention count

### Top Navigation 🧭
- **Split View**: Both price & sentiment side-by-side
- **Prices Tab**: Full-screen price monitoring
- **Sentiment Tab**: Full-screen sentiment dashboard

## The Three Agents 🤖

### 1. Price Monitor Agent
**What it does**: Tracks fund prices and detects arbitrage opportunities
- Fetches prices every 5 seconds
- Calculates 24h % change
- Tracks trading volume
- Detects price discrepancies
- Flags unusual movement (>2%)

**Files**:
- [backend/app/agents/price_monitor.py](../backend/app/agents/price_monitor.py)

**Endpoints**:
- `GET /api/prices/current` - All fund prices
- `GET /api/prices/opportunities` - Trading opportunities
- `GET /api/prices/history/{fund}` - Historical data

### 2. Sentiment Analyzer Agent
**What it does**: Analyzes social sentiment from X (Twitter) & Farcaster
- Processes social media mentions
- Calculates sentiment distribution
- Identifies trending keywords
- Generates alerts for sentiment shifts

**Files**:
- [backend/app/agents/sentiment_analyzer.py](../backend/app/agents/sentiment_analyzer.py)

**Endpoints**:
- `GET /api/sentiment/all` - All fund sentiment
- `GET /api/sentiment/fund/{fund}` - Specific fund sentiment
- `GET /api/sentiment/trending/{fund}` - Trending keywords
- `GET /api/sentiment/alerts` - Sentiment alerts

### 3. Recommendation Engine Agent
**What it does**: Combines price + sentiment into actionable recommendations
- Generates BUY/SELL/HOLD signals
- Calculates confidence scores (0-100%)
- Suggests target prices
- Assesses risk levels
- Provides reasoning for each recommendation

**Files**:
- [backend/app/agents/recommendation_engine.py](../backend/app/agents/recommendation_engine.py)

**Endpoints**:
- `GET /api/recommendations/all` - All recommendations
- `GET /api/recommendations/opportunities` - Top 3 opportunities
- `GET /api/recommendations/risk/{fund}` - Risk assessment

## Monitored Funds 💰

1. **Halan Saving** - Conservative savings fund
2. **AZ Gold** - Gold hedge fund
3. **AZ Opportunity** - Growth fund
4. **AZ Shariah** - Islamic-compliant fund

## How It Works (Flow Diagram) 🔄

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                             │
└────────┬──────────────────────────────────────┬─────────────┘
         │                                      │
    ┌────▼────────┐              ┌─────────────▼────────┐
    │ Price       │              │ Sentiment           │
    │ Monitor     │              │ Analyzer            │
    │ Agent       │              │ Agent               │
    └────┬────────┘              └─────────────┬────────┘
         │ (prices)                   │ (sentiment)
         │                           │
         └───────────┬───────────────┘
                     │
            ┌────────▼────────────┐
            │ Recommendation      │
            │ Engine              │
            │ Agent               │
            └────────┬────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
    ┌────▼────┐ ┌───▼────┐ ┌──▼──────┐
    │ BUY/    │ │Target  │ │Risk    │
    │SELL/    │ │Prices  │ │Score   │
    │HOLD     │ │        │ │        │
    └─────────┘ └────────┘ └────────┘
         │
    ┌────▼──────────────┐
    │ Frontend Display  │
    │ (Split-Screen)    │
    └───────────────────┘
```

## Configuration 🔧

### Environment Variables (.env)

```env
# Database
DB_USER=user                    # Default user
DB_PASSWORD=password            # Change this!
DB_NAME=halan_invest           # Database name

# APIs (get your own keys)
TWITTER_API_KEY=your_key       # X (Twitter)
FARCASTER_API_KEY=your_key     # Farcaster
THNDR_API_KEY=your_key         # Thndr broker

# Trading (DANGEROUS - leave False!)
ENABLE_LIVE_TRADING=False       # DO NOT SET TO TRUE
TRADE_SIZE_LIMIT=1000
SLIPPAGE_TOLERANCE=0.5
```

## API Examples 📡

### Get Current Prices
```bash
curl http://localhost:8000/api/prices/current
```
Response:
```json
{
  "data": [
    {
      "fund": "halan_saving",
      "ticker": "HALAN",
      "price": 102.5,
      "change": 1.25,
      "volume": 1500000
    }
  ]
}
```

### Get Recommendations
```bash
curl http://localhost:8000/api/recommendations/all
```
Response:
```json
{
  "recommendations": [
    {
      "fund": "az_opportunity",
      "recommendation": "STRONG_BUY",
      "confidence": 0.88,
      "target_price": 105.2,
      "reason": "Price moved -2.5% | Strong positive sentiment"
    }
  ]
}
```

### Get Top Opportunities
```bash
curl http://localhost:8000/api/recommendations/opportunities
```

## Data Storage 💾

### PostgreSQL Tables

**price_history**
- Stores all price data points
- Indexed by fund_name and timestamp
- Enables historical analysis

**sentiment_records**
- Sentiment analysis results
- Positive/negative/neutral scores
- Source mention counts

**trade_recommendations**
- Generated recommendations
- Confidence scores
- Target prices and reasoning

**trades**
- Executed trades (when enabled)
- Action, quantity, price
- Status tracking

## Real-Time Updates ⏰

| Component | Update Frequency |
|-----------|-----------------|
| Prices | Every 5 seconds |
| Sentiment | Every 10 seconds |
| Recommendations | Every 15 seconds |
| Database | On each update |
| Frontend | Real-time via API polling |

## Development Roadmap 🗺️

### Phase 1: Current (Monitor & Analyze)
- ✅ Price monitoring
- ✅ Sentiment analysis
- ✅ Recommendations
- ✅ Dashboard display

### Phase 2: Integration (Next)
- ⏳ Real EGX price scraping
- ⏳ Real X (Twitter) API integration
- ⏳ Real Farcaster integration
- ⏳ Database historical analysis

### Phase 3: Advanced (Future)
- ⏳ Paper trading simulation
- ⏳ ML-powered sentiment models
- ⏳ Technical indicators library
- ⏳ Multi-user support
- ⏳ Portfolio tracking

### Phase 4: Production (Advanced)
- ⏳ Live trading (with extreme caution!)
- ⏳ Hardware wallet integration
- ⏳ SMS/Email alerts
- ⏳ Mobile app

## Troubleshooting 🔧

| Problem | Solution |
|---------|----------|
| Port 3000 in use | Change in docker-compose.yml or kill process |
| DB connection error | Wait 15s for DB to start, check POSTGRES_PASSWORD |
| API returns 404 | Verify backend is running: `curl http://localhost:8000/health` |
| Frontend blank | Clear cache (Ctrl+Shift+Delete), check console (F12) |
| Slow performance | Increase Docker memory, check database logs |

## Security Notes ⚠️

🚨 **IMPORTANT**:
- Never commit `.env` file
- Change database password immediately
- Never enable live trading without testing
- Use environment variables for all secrets
- Keep private keys in hardware wallet
- Monitor for unusual API activity
- Backup database regularly

## Support & Help 💡

1. **Setup Issues**: Read [SETUP.md](./SETUP.md)
2. **API Questions**: Visit http://localhost:8000/docs
3. **Code Issues**: Check logs with `docker-compose logs`
4. **Configuration**: Review `.env` file
5. **Database**: Use `docker exec halan_invest_db psql ...`

## Next Steps 🚀

### Immediate (Today)
- [ ] Run `./start.bat` or `bash start.sh`
- [ ] Access http://localhost:3000
- [ ] Verify all three components visible
- [ ] Check API endpoints at http://localhost:8000/docs

### Short Term (This Week)
- [ ] Add your API keys to `.env`
- [ ] Customize fund list
- [ ] Implement real price scraper
- [ ] Test sentiment analysis

### Medium Term (This Month)
- [ ] Full integration with EGX APIs
- [ ] Real-time social media feeds
- [ ] Enhanced technical indicators
- [ ] Paper trading module

### Long Term (Advanced)
- [ ] Live trading with safeguards
- [ ] Mobile app
- [ ] Multi-user support
- [ ] Backtesting engine

## License & Disclaimer ⚖️

**This is provided AS-IS for educational purposes only.**

⚠️ **NOT FINANCIAL ADVICE**
- Consult a professional advisor before investing
- Test extensively before live trading
- Use at your own risk
- We provide no guarantees or warranties

---

## Quick Links 🔗

- [Full README](./README.md) - Complete documentation
- [Setup Guide](./SETUP.md) - Detailed setup instructions
- [API Documentation](http://localhost:8000/docs) - Interactive API docs
- [Architecture](./backend/app/orchestrator.py) - Agent orchestration

---

**Built with ❤️ for Egyptian investors**

**Status**: ✅ Ready for testing | ⚠️ Not production-ready without live trading safeguards

**Questions?** Review logs, check API health, or consult documentation.

Happy monitoring! 📊
