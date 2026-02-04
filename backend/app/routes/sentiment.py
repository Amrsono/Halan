"""Sentiment analysis API routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.agents.sentiment_analyzer import SentimentAnalyzer
from app.models.database import SentimentRecord, get_db
from datetime import datetime

router = APIRouter(prefix="/api/sentiment", tags=["sentiment"])
analyzer = SentimentAnalyzer()


@router.get("/all")
async def get_all_sentiment():
    """Get sentiment analysis for all funds"""
    sentiments = await analyzer.analyze_all_funds()
    return {
        "data": sentiments,
        "timestamp": datetime.now().isoformat(),
    }


@router.get("/fund/{fund_name}")
async def get_fund_sentiment(fund_name: str):
    """Get sentiment for a specific fund"""
    sentiment = await analyzer.fetch_sentiment_for_fund(fund_name)
    if not sentiment:
        raise HTTPException(status_code=404, detail="Fund not found")
    return {"data": sentiment}


@router.get("/trending/{fund_name}")
async def get_trending_keywords(fund_name: str):
    """Get trending keywords for a fund"""
    keywords = await analyzer.get_trending_keywords(fund_name)
    return {
        "fund": fund_name,
        "trending_keywords": keywords,
        "timestamp": datetime.now().isoformat(),
    }


@router.get("/alerts")
async def get_sentiment_alerts():
    """Get sentiment-based trading alerts"""
    funds = [
        "halan_saving",
        "az_gold",
        "az_opportunity",
        "az_shariah",
    ]
    alerts = []
    for fund in funds:
        alert = analyzer.get_sentiment_alert(fund)
        if alert:
            alerts.append({"fund": fund, "alert": alert})

    return {"alerts": alerts}


@router.post("/analyze")
async def analyze_text(text: str, fund_name: str):
    """Analyze sentiment of custom text"""
    result = await analyzer.analyze_tweet(text, fund_name)
    return {"data": result}
