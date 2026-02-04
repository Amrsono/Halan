# 🚀 Render Deployment Guide - Halan Invest

## Prerequisites
- GitHub account with the repo: https://github.com/Amrsono/Halan
- Render account: https://render.com

## Deployment Steps

### 1. Connect GitHub to Render
1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Select "Build and deploy from a Git repository"
4. Connect your GitHub account
5. Select `Amrsono/Halan` repository

### 2. Deploy Backend

**Create Web Service:**
- Name: `halan-invest-backend`
- Environment: Docker
- Build Command: (leave blank - uses Dockerfile)
- Start Command: (leave blank - uses Dockerfile)
- Instance Type: Free or Starter
- Branch: main

**Environment Variables:**
```
PYTHON_ENV=production
DEBUG=False
USE_REAL_DATA=True
DB_HOST=[PostgreSQL Host]
DB_PORT=5432
DB_USER=[PostgreSQL User]
DB_PASSWORD=[PostgreSQL Password]
DB_NAME=halan_invest
TWITTER_API_KEY=[your_key]
FARCASTER_API_KEY=[your_key]
ENABLE_LIVE_TRADING=False
```

### 3. Deploy PostgreSQL Database

1. Click "New +" → "PostgreSQL"
2. Name: `halan-postgres`
3. Database: `halan_invest`
4. Region: (same as backend)
5. Copy connection details to backend env vars

**Initialize Database:**
- Connect to PostgreSQL
- Run migrations (if any)
- Verify tables are created

### 4. Deploy Frontend

**Create Web Service:**
- Name: `halan-invest-frontend`
- Environment: Docker
- Build Command: (uses Dockerfile)
- Branch: main

**Environment Variables:**
```
REACT_APP_API_URL=https://halan-invest-backend.onrender.com/api
```

### 5. Configure Health Checks

Backend health check path: `/health`

### 6. DNS & SSL

Render provides automatic SSL certificates. Your URLs will be:
- Backend: `https://halan-invest-backend.onrender.com`
- Frontend: `https://halan-invest-frontend.onrender.com`

## Production Checklist

- ✅ Environment variables set
- ✅ Database initialized
- ✅ Backend running on `/health` endpoint
- ✅ Frontend built and serving
- ✅ CORS configured for frontend → backend
- ✅ Real data fetchers enabled (`USE_REAL_DATA=True`)
- ✅ SSL certificates active
- ✅ Database backups enabled
- ✅ Error logging configured

## Monitoring

### View Logs
- Backend: Dashboard → halan-invest-backend → Logs
- Frontend: Dashboard → halan-invest-frontend → Logs
- Database: Dashboard → halan-postgres → Logs

### Check Status
- Health: `https://halan-invest-backend.onrender.com/health`
- API Docs: `https://halan-invest-backend.onrender.com/docs`
- Frontend: `https://halan-invest-frontend.onrender.com`

## Troubleshooting

### Backend not connecting to database
- Verify DB_HOST, DB_USER, DB_PASSWORD are correct
- Check PostgreSQL is running
- Verify firewall allows connections

### Frontend can't reach backend
- Check REACT_APP_API_URL in frontend env vars
- Verify backend is running (`/health` endpoint)
- Check browser console for CORS errors

### Sentiment data not loading
- Verify `USE_REAL_DATA=True` in backend
- Check API keys (TWITTER_API_KEY, FARCASTER_API_KEY)
- Check backend logs for errors

## Updating Code

1. Push changes to GitHub `main` branch
2. Render automatically rebuilds and redeploys
3. Monitor deployment progress in dashboard
4. Check logs for any errors

## Cost Optimization

- **Backend**: Free tier suitable for development
- **Frontend**: Free tier suitable for development  
- **Database**: Free tier limited to 256MB - upgrade if needed
- Consider upgrading for production usage

## Support

- Render Docs: https://render.com/docs
- Project Repo: https://github.com/Amrsono/Halan
- API Docs: https://halan-invest-backend.onrender.com/docs
