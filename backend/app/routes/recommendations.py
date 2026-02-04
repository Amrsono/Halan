"""Recommendation API routes"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.agents.recommendation_engine import RecommendationEngine
from app.agents.price_monitor import PriceMonitor
from app.agents.sentiment_analyzer import SentimentAnalyzer
from app.models.database import TradeRecommendation, get_db
from datetime import datetime

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])
rec_engine = RecommendationEngine()
price_monitor = PriceMonitor()
sentiment_analyzer = SentimentAnalyzer()


@router.get("/all")
async def get_all_recommendations():
    """Get recommendations for all funds"""
    # Fetch current prices and sentiment
    prices = await price_monitor.monitor_all_funds()
    sentiments = await sentiment_analyzer.analyze_all_funds()

    # Convert to dicts for recommendation engine
    price_dict = {p["fund"]: p for p in prices}
    sentiment_dict = {s["fund"]: s for s in sentiments}

    # Generate recommendations
    recommendations = await rec_engine.generate_all_recommendations(
        price_dict, sentiment_dict
    )

    return {
        "recommendations": recommendations,
        "timestamp": datetime.now().isoformat(),
    }


@router.get("/opportunities")
async def get_top_opportunities():
    """Get top trading opportunities"""
    # Fetch current data
    prices = await price_monitor.monitor_all_funds()
    sentiments = await sentiment_analyzer.analyze_all_funds()

    price_dict = {p["fund"]: p for p in prices}
    sentiment_dict = {s["fund"]: s for s in sentiments}

    recommendations = await rec_engine.generate_all_recommendations(
        price_dict, sentiment_dict
    )

    top_3 = rec_engine.get_top_opportunities(recommendations, limit=3)

    return {
        "top_opportunities": top_3,
        "count": len(top_3),
        "timestamp": datetime.now().isoformat(),
    }


@router.get("/risk/{fund_name}")
async def get_risk_assessment(fund_name: str):
    """Get risk score for a fund"""
    prices = await price_monitor.monitor_all_funds()
    price_data = next((p for p in prices if p["fund"] == fund_name), None)

    if not price_data:
        return {"error": "Fund not found"}

    volatility = abs(price_data["change"]) / 100
    risk_score = rec_engine.get_risk_score(fund_name, volatility)

    return {
        "fund": fund_name,
        "risk_score": risk_score,
        "risk_level": "HIGH" if risk_score > 60 else "MEDIUM" if risk_score > 40 else "LOW",
        "volatility": volatility,
    }
