# 📋 Halan Invest - Complete Project Index

## 🚀 START HERE

### 1. **First Time?** → Read [QUICKSTART.md](./QUICKSTART.md)
- 5-minute overview
- Choose your startup method
- Quick access to all components

### 2. **Ready to Go?** → Run Start Script
**Windows:**
```bash
.\start.bat
```

**Mac/Linux:**
```bash
bash start.sh
```

Then open: **http://localhost:3000**

---

## 📁 Project Structure

```
d:/New projects/Project halan invest/
│
├── 📚 DOCUMENTATION
│   ├── README.md              → Full documentation & features
│   ├── QUICKSTART.md          → 5-minute quick reference
│   ├── SETUP.md               → Detailed setup guide
│   └── THIS FILE              → Project index
│
├── 🐳 DOCKER & CONFIG
│   ├── docker-compose.yml     → Docker orchestration
│   ├── .env.example           → Environment template
│   ├── start.bat              → Windows quick start
│   └── start.sh               → Mac/Linux quick start
│
├── 🔧 BACKEND (Python/FastAPI)
│   └── backend/
│       ├── app/
│       │   ├── main.py              → FastAPI application
│       │   ├── orchestrator.py       → Agent coordination logic
│       │   ├── agents/              → Specialized agents
│       │   │   ├── price_monitor.py         → Tracks fund prices
│       │   │   ├── sentiment_analyzer.py    → Analyzes social sentiment
│       │   │   └── recommendation_engine.py → Generates buy/sell signals
│       │   ├── models/              → Database models
│       │   │   └── database.py      → PostgreSQL schemas
│       │   ├── routes/              → API endpoints
│       │   │   ├── prices.py        → Price endpoints
│       │   │   ├── sentiment.py     → Sentiment endpoints
│       │   │   └── recommendations.py → Recommendation endpoints
│       │   └── services/            → Business logic
│       ├── requirements.txt   → Python dependencies
│       ├── Dockerfile        → Backend container
│       └── .gitignore
│
├── 🎨 FRONTEND (React)
│   └── frontend/
│       ├── src/
│       │   ├── App.js                    → Main app (split-screen)
│       │   ├── index.js                  → React entry point
│       │   ├── index.css                 → Tailwind CSS
│       │   ├── components/
│       │   │   ├── PriceMonitor.js       → Left panel (prices)
│       │   │   └── SentimentDashboard.js → Right panel (sentiment)
│       │   ├── pages/                    → Page containers
│       │   └── services/
│       │       └── api.js                → API client
│       ├── public/
│       │   └── index.html          → HTML entry
│       ├── package.json            → Dependencies
│       ├── tailwind.config.js       → Tailwind config
│       ├── postcss.config.js        → PostCSS config
│       ├── Dockerfile              → Frontend container
│       ├── .gitignore
│       └── .env.example
│
├── 🧪 TESTING
│   └── test_system.py          → System verification script
│
└── 📄 OTHER
    └── stocks.txt              → Your original file
```

---

## 🎯 Key Files Explained

### Backend Agents (The Brain)

#### `backend/app/agents/price_monitor.py`
- **Purpose**: Monitors fund prices in real-time
- **Monitors**: 4 Egyptian investment funds
- **Detects**: Price discrepancies, arbitrage opportunities
- **Update Frequency**: Every 5 seconds
- **Key Methods**:
  - `fetch_price()` - Get current price
  - `monitor_all_funds()` - Track all funds
  - `detect_arbitrage()` - Find opportunities

#### `backend/app/agents/sentiment_analyzer.py`
- **Purpose**: Analyzes social sentiment
- **Sources**: X (Twitter), Farcaster
- **Calculates**: Sentiment distribution, trending keywords
- **Update Frequency**: Every 10 seconds
- **Key Methods**:
  - `fetch_sentiment_for_fund()` - Get sentiment data
  - `analyze_tweet()` - Process text
  - `get_trending_keywords()` - Extract trends

#### `backend/app/agents/recommendation_engine.py`
- **Purpose**: Generates trading recommendations
- **Combines**: Price signals + Sentiment data
- **Outputs**: BUY/SELL/HOLD signals with confidence
- **Update Frequency**: Every 15 seconds
- **Key Methods**:
  - `generate_recommendation()` - Create signal
  - `get_top_opportunities()` - Best trades
  - `get_risk_score()` - Risk assessment

### Frontend Components (The UI)

#### `frontend/src/components/PriceMonitor.js`
- **Shows**: Current prices, % change, volume
- **Features**: Real-time updates, opportunity alerts
- **Updates**: Every 5 seconds
- **Left side of dashboard**

#### `frontend/src/components/SentimentDashboard.js`
- **Shows**: Sentiment distribution, trending keywords
- **Features**: Color-coded sentiment, alert notifications
- **Updates**: Every 10 seconds
- **Right side of dashboard**

#### `frontend/src/App.js`
- **Main layout**: Split-screen design
- **Navigation**: Switch between views
- **Controls**: Tab selection (Split/Prices/Sentiment)
- **Header**: App title and branding

### Configuration Files

#### `.env` (Environment Variables)
```env
# Database credentials
DB_USER=user
DB_PASSWORD=password

# API Keys (add your real keys)
TWITTER_API_KEY=your_key
FARCASTER_API_KEY=your_key

# Trading settings
ENABLE_LIVE_TRADING=False
TRADE_SIZE_LIMIT=1000
```

#### `docker-compose.yml`
- **Services**: Database, Backend, Frontend
- **Networking**: Internal communication
- **Volumes**: Persistent data storage
- **Health Checks**: Service monitoring

---

## 🌐 API Endpoints Reference

### Health & Status
```
GET /health                              → Service status
GET /docs                                → Swagger UI
```

### Price Endpoints
```
GET /api/prices/current                  → All fund prices
GET /api/prices/fund/{fund_name}         → Specific fund price
GET /api/prices/opportunities            → Trading opportunities
GET /api/prices/history/{fund_name}      → Historical prices (7+ days)
```

### Sentiment Endpoints
```
GET /api/sentiment/all                   → All fund sentiment
GET /api/sentiment/fund/{fund_name}      → Specific fund sentiment
GET /api/sentiment/trending/{fund_name}  → Trending keywords
GET /api/sentiment/alerts                → Sentiment alerts
```

### Recommendation Endpoints
```
GET /api/recommendations/all             → All recommendations
GET /api/recommendations/opportunities   → Top 3 opportunities
GET /api/recommendations/risk/{fund}     → Risk assessment
```

---

## 🔄 Data Flow

```
1. MONITOR PHASE
   └─→ Price Monitor fetches prices every 5 seconds
   └─→ Stored in price_history table

2. ANALYZE PHASE
   └─→ Sentiment Analyzer processes social data every 10 seconds
   └─→ Stored in sentiment_records table

3. RECOMMEND PHASE
   └─→ Recommendation Engine combines signals every 15 seconds
   └─→ Generates BUY/SELL/HOLD with confidence
   └─→ Stored in trade_recommendations table

4. DISPLAY PHASE
   └─→ Frontend polls API every 5-10 seconds
   └─→ Updates split-screen dashboard
   └─→ Real-time visualization

5. ALERT PHASE
   └─→ Orchestrator detects significant changes
   └─→ Generates alerts for users
   └─→ Triggers notifications
```

---

## 📊 Database Schema

### price_history
- `id` - Primary key
- `fund_name` - Fund identifier
- `ticker` - Ticker symbol
- `price` - Current price (EGP)
- `change_percent` - 24h change
- `volume` - Trading volume
- `timestamp` - When recorded

### sentiment_records
- `id` - Primary key
- `fund_name` - Fund identifier
- `positive` - Positive percentage
- `neutral` - Neutral percentage
- `negative` - Negative percentage
- `overall_score` - Combined score (-1 to 1)
- `source_count` - Number of mentions
- `timestamp` - When recorded

### trade_recommendations
- `id` - Primary key
- `fund_name` - Fund identifier
- `recommendation` - BUY/SELL/HOLD
- `confidence` - Confidence (0-1)
- `price_change` - Price movement %
- `sentiment_score` - Sentiment value
- `target_price` - Suggested price
- `reason` - Explanation text
- `timestamp` - When generated

### trades
- `id` - Primary key
- `fund_name` - Fund identifier
- `action` - BUY or SELL
- `quantity` - Amount
- `price` - Execution price
- `total` - Total value
- `status` - pending/executed/failed
- `timestamp` - When executed

---

## 🚀 Getting Started Checklist

### First Time Setup
- [ ] Read [QUICKSTART.md](./QUICKSTART.md)
- [ ] Have Docker installed
- [ ] Copy `.env.example` to `.env`
- [ ] Run `./start.bat` or `bash start.sh`
- [ ] Wait 15 seconds for services
- [ ] Open http://localhost:3000

### Verify Installation
- [ ] Frontend loads (http://localhost:3000)
- [ ] See price cards on left side
- [ ] See sentiment dashboard on right side
- [ ] Real-time data updating
- [ ] No error messages in browser console

### Test APIs
- [ ] http://localhost:8000/health → OK
- [ ] http://localhost:8000/docs → Swagger UI loads
- [ ] http://localhost:8000/api/prices/current → JSON response
- [ ] http://localhost:8000/api/sentiment/all → JSON response
- [ ] http://localhost:8000/api/recommendations/all → JSON response

### Configure
- [ ] Review `.env` file
- [ ] Update database password (optional but recommended)
- [ ] Add your API keys (for production use)

---

## 🔍 Troubleshooting Quick Links

| Issue | Solution |
|-------|----------|
| **Port 3000 in use** | Stop other process or change port in docker-compose.yml |
| **DB connection error** | Wait 30s for DB to start, check DB_PASSWORD in .env |
| **API returns 404** | Verify backend running: `docker-compose logs backend` |
| **Frontend blank page** | Press F12, check console errors, clear cache |
| **Slow performance** | Increase Docker memory, check DB logs |

See [SETUP.md](./SETUP.md#troubleshooting) for detailed troubleshooting.

---

## 📖 Documentation Navigation

```
QUICKSTART.md
├── What You Got (5 min)
├── Quick Start (5 min)
├── Features Overview (5 min)
└── Links to detailed docs

README.md
├── Full Feature List
├── Architecture Diagram
├── Setup Instructions
├── API Documentation
└── Safety & Legal Notes

SETUP.md
├── Step-by-Step Setup
├── Docker Usage
├── Local Development
├── Configuration Guide
├── Troubleshooting
└── Performance Tips

THIS FILE (PROJECT_INDEX.md)
├── Project Structure
├── File Descriptions
├── API Reference
├── Data Flows
└── Checklist
```

---

## 🎯 Recommended Learning Path

### Day 1: Understand
1. Read [QUICKSTART.md](./QUICKSTART.md)
2. Understand the 3 agents
3. Learn the split-screen dashboard
4. Explore API endpoints at http://localhost:8000/docs

### Day 2: Setup & Test
1. Run Docker with `./start.bat`
2. Access http://localhost:3000
3. Monitor prices and sentiment
4. Run `python test_system.py` to verify

### Day 3: Customize
1. Modify fund list in price_monitor.py
2. Add your API keys to .env
3. Test with real data sources
4. Fine-tune recommendation thresholds

### Day 4+: Integrate & Extend
1. Add real EGX price scraper
2. Integrate real social media APIs
3. Implement more indicators
4. Build paper trading module

---

## 🔒 Security Checklist

- [ ] Never commit `.env` file
- [ ] Change database password
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS in production
- [ ] Set up API rate limiting
- [ ] Rotate API keys regularly
- [ ] Monitor for suspicious activity
- [ ] Keep dependencies updated
- [ ] Use strong passwords
- [ ] Backup database regularly

---

## 📞 Need Help?

1. **Setup Issues**: Check [SETUP.md](./SETUP.md)
2. **API Questions**: Visit http://localhost:8000/docs
3. **Code Issues**: Review logs with `docker-compose logs`
4. **Config Help**: Review `.env` template
5. **Database Help**: Use `docker exec halan_invest_db psql`

---

## 🎉 You're All Set!

Everything is ready to go. Follow these steps:

1. **Run**: `./start.bat` (Windows) or `bash start.sh` (Mac/Linux)
2. **Wait**: 15 seconds for services to start
3. **Open**: http://localhost:3000
4. **Explore**: Monitor prices and sentiment in real-time
5. **Analyze**: Check recommendations for trading signals

**Happy investing! 📈**

---

**Project Status**: ✅ Ready for Testing | ⚠️ Not Production-Ready (Live Trading)

**Last Updated**: February 2, 2026

**Support**: Consult documentation or review system logs for issues
