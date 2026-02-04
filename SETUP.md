# 📖 Halan Invest - Setup Guide

## Step 1: Initial Setup

### Clone/Setup the Project
```bash
cd "d:/New projects/Project halan invest"
```

### Create Environment File
```bash
cp .env.example .env
```

## Step 2: Using Docker (Recommended)

### Start Services
```bash
docker-compose up -d
```

### Verify Services
```bash
docker-compose ps
```

Expected output:
```
NAME                    COMMAND                  SERVICE      STATUS
halan_invest_db         "docker-entrypoint..."   db           Up (healthy)
halan_invest_backend    "uvicorn app.main..."    backend      Up
halan_invest_frontend   "docker-entrypoint..."   frontend     Up
```

### Access Application
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Stop Services
```bash
docker-compose down
```

### Reset Database
```bash
docker-compose down -v  # Remove volumes
docker-compose up -d
```

## Step 3: Using Local Development

### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# or (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (if needed)
# python app/models/database.py

# Start server
uvicorn app.main:app --reload
```

### Frontend Setup (in new terminal)
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Database Setup
Ensure PostgreSQL is running locally on port 5432

## Step 4: Accessing the Dashboard

### Split-Screen View (Default)
- **Left**: Price Monitor
- **Right**: Sentiment Dashboard
- Real-time updates every 5-10 seconds

### Available Views
1. **Split View**: See both prices and sentiment side-by-side
2. **Prices Only**: Full-screen price monitoring
3. **Sentiment Only**: Full-screen sentiment analysis

### Using the Dashboard

#### Price Monitor (Left Side)
- Shows current price, change %, volume for each fund
- Click on fund cards to see history
- Red/Green colors indicate down/up movement
- 🎯 Opportunities section shows buy/sell signals

#### Sentiment Dashboard (Right Side)
- Shows sentiment distribution (positive/negative/neutral)
- Color-coded: 🟢 Positive, 🔴 Negative, 🟡 Neutral
- Displays number of analyzed mentions
- Shows trending keywords
- ⚠️ Alerts for significant sentiment shifts

## Step 5: API Testing

### Using Swagger UI
Visit: http://localhost:8000/docs

### Using curl

**Get Current Prices**
```bash
curl http://localhost:8000/api/prices/current
```

**Get Fund Price**
```bash
curl http://localhost:8000/api/prices/fund/halan_saving
```

**Get Sentiment**
```bash
curl http://localhost:8000/api/sentiment/all
```

**Get Recommendations**
```bash
curl http://localhost:8000/api/recommendations/all
```

**Get Top Opportunities**
```bash
curl http://localhost:8000/api/recommendations/opportunities
```

## Step 6: Configuration

### Adding API Keys

Edit `.env` file with your real credentials:

```env
# Twitter API
TWITTER_API_KEY=your_actual_key
TWITTER_API_SECRET=your_actual_secret

# Farcaster
FARCASTER_API_KEY=your_actual_key

# Thndr (optional)
THNDR_API_KEY=your_actual_key

# Trading Settings
ENABLE_LIVE_TRADING=False    # Keep False for testing!
TRADE_SIZE_LIMIT=1000
SLIPPAGE_TOLERANCE=0.5
```

### Database Configuration
```env
DB_USER=user
DB_PASSWORD=password
DB_NAME=halan_invest
```

## Step 7: Next Steps

### For Development
1. Customize fund list in `backend/app/agents/price_monitor.py`
2. Add real API integrations in sentiment_analyzer.py
3. Implement EGX web scraper
4. Add more recommendation signals

### For Production
1. Use strong database password
2. Enable HTTPS
3. Set up monitoring/alerting
4. Implement authentication
5. Use environment-specific configs
6. Set up backup strategy

### For Live Trading (⚠️ ADVANCED)
1. Thoroughly test on paper trading
2. Start with small trade sizes
3. Enable circuit breakers
4. Monitor 24/7
5. Keep emergency kill-switch ready
6. Use hardware wallet for key storage

## Troubleshooting

### Port 3000/8000 already in use
```bash
# Find process using port
netstat -ano | findstr :3000

# Kill process
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
```

### Database won't connect
```bash
# Check if PostgreSQL is running
docker-compose logs db

# Restart database
docker-compose restart db
```

### Frontend shows blank page
```bash
# Check browser console for errors (F12)
# Verify backend is running: http://localhost:8000/health
# Clear browser cache (Ctrl+Shift+Delete)
```

### API returns 404
```bash
# Verify backend service is running
docker-compose logs backend

# Check API endpoint
curl http://localhost:8000/health
```

## Performance Tips

1. **Reduce Update Frequency**: Adjust intervals in components
2. **Enable Caching**: Use Redis for frequent queries
3. **Database Indexes**: Already optimized, but monitor query logs
4. **Frontend Optimization**: React DevTools to profile

## Security Checklist

- [ ] Never commit `.env` file
- [ ] Use strong database passwords
- [ ] Rotate API keys regularly
- [ ] Use environment variables for secrets
- [ ] Enable database backups
- [ ] Monitor API usage
- [ ] Use rate limiting
- [ ] Validate all user inputs
- [ ] Keep dependencies updated

## Support

For issues:
1. Check logs: `docker-compose logs`
2. Review API docs: http://localhost:8000/docs
3. Verify .env configuration
4. Check database connection
5. Review browser console errors

---

**Happy monitoring! 📊**
