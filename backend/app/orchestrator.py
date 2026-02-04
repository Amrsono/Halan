"""
Orchestrator - Coordinates all agents and handles cross-agent communication
This is the main orchestration logic that ties everything together
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List
from app.agents.price_monitor import PriceMonitor
from app.agents.sentiment_analyzer import SentimentAnalyzer
from app.agents.recommendation_engine import RecommendationEngine
from app.services.trading_service import trading_service

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Master orchestrator that coordinates all specialized agents
    
    Flow:
    1. Price Monitor → Detects price changes
    2. Sentiment Analyzer → Analyzes social signals
    3. Recommendation Engine → Combines signals into actionable recommendations
    4. Alert System → Notifies users of opportunities
    """

    def __init__(self):
        self.price_monitor = PriceMonitor()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.recommendation_engine = RecommendationEngine()
        
        self.last_prices = {}
        self.last_sentiment = {}
        self.last_recommendations = {}

    async def run_full_cycle(self) -> Dict:
        """
        Execute a complete monitoring cycle:
        1. Fetch prices
        2. Analyze sentiment
        3. Generate recommendations
        4. Detect alerts
        """
        logger.info("🔄 Starting agent orchestration cycle...")
        
        cycle_start = datetime.now()
        
        try:
            # Phase 1: Price Monitoring
            logger.info("📊 Phase 1: Price Monitoring")
            prices = await self.price_monitor.monitor_all_funds()
            self.last_prices = {p["fund"]: p for p in prices}
            
            # Phase 2: Sentiment Analysis
            logger.info("💬 Phase 2: Sentiment Analysis")
            sentiments = await self.sentiment_analyzer.analyze_all_funds()
            self.last_sentiment = {s["fund"]: s for s in sentiments}
            
            # Phase 3: Generate Recommendations
            logger.info("🤖 Phase 3: Recommendation Generation")
            recommendations = await self.recommendation_engine.generate_all_recommendations(
                self.last_prices, self.last_sentiment, self.price_monitor.price_history
            )
            self.last_recommendations = {r["fund"]: r for r in recommendations}
            
            # Phase 4: Detect Alerts & Execute Paper Trades
            logger.info("🚨 Phase 4: Alert Detection & Paper Trading")
            alerts = self._generate_alerts(prices, sentiments, recommendations)
            
            # Auto-Trade on Strong Signals (Paper Trading)
            await self._process_auto_trading(recommendations)
            
            # Phase 5: Compile Results
            cycle_time = (datetime.now() - cycle_start).total_seconds()
            
            result = {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "cycle_time_seconds": cycle_time,
                "prices": prices,
                "sentiments": sentiments,
                "recommendations": recommendations,
                "alerts": alerts,
                "summary": {
                    "funds_monitored": len(prices),
                    "strong_buy_signals": len([r for r in recommendations if r["recommendation"] == "STRONG_BUY"]),
                    "strong_sell_signals": len([r for r in recommendations if r["recommendation"] == "STRONG_SELL"]),
                    "alerts_generated": len(alerts),
                }
            }
            
            logger.info(f"✅ Cycle completed in {cycle_time:.2f}s - {result['summary']}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error in orchestration cycle: {e}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    async def _process_auto_trading(self, recommendations: List[Dict]):
        """Execute paper trades based on strong recommendations"""
        for rec in recommendations:
            if rec["confidence"] > 0.85: # High confidence threshold for auto-trade
                fund_name = rec["fund"]
                price_data = self.last_prices.get(fund_name, {})
                current_price = price_data.get("price", 0)
                
                if current_price > 0:
                    if rec["recommendation"] == "STRONG_BUY":
                         trading_service.execute_paper_trade(fund_name, "BUY", current_price, rec["confidence"])
                    elif rec["recommendation"] == "STRONG_SELL":
                         trading_service.execute_paper_trade(fund_name, "SELL", current_price, rec["confidence"])


    def _generate_alerts(self, prices: List, sentiments: List, recommendations: List) -> List[Dict]:
        """
        Generate actionable alerts based on combined signals
        """
        alerts = []
        
        for rec in recommendations:
            fund = rec["fund"]
            
            # Alert 1: Strong Buy Signal
            if rec["recommendation"] == "STRONG_BUY" and rec["confidence"] > 0.8:
                alerts.append({
                    "type": "STRONG_BUY",
                    "fund": fund,
                    "title": f"🟢 Strong Buy Signal: {fund}",
                    "message": rec["reason"],
                    "confidence": rec["confidence"],
                    "action": "CONSIDER_BUY",
                })
            
            # Alert 2: Strong Sell Signal
            elif rec["recommendation"] == "STRONG_SELL" and rec["confidence"] > 0.8:
                alerts.append({
                    "type": "STRONG_SELL",
                    "fund": fund,
                    "title": f"🔴 Strong Sell Signal: {fund}",
                    "message": rec["reason"],
                    "confidence": rec["confidence"],
                    "action": "CONSIDER_SELL",
                })
            
            # Alert 3: Sentiment Shift
            sentiment = next((s for s in sentiments if s["fund"] == fund), None)
            if sentiment:
                if sentiment["overall_score"] > 0.7 and sentiment.get("trending"):
                    alerts.append({
                        "type": "SENTIMENT_SURGE",
                        "fund": fund,
                        "title": f"📈 Sentiment Surge: {fund}",
                        "message": f"Strong positive sentiment ({sentiment['overall_score']:.0%})",
                        "confidence": sentiment["overall_score"],
                        "action": "WATCH_FUND",
                    })
                elif sentiment["overall_score"] < -0.7:
                    alerts.append({
                        "type": "SENTIMENT_DROP",
                        "fund": fund,
                        "title": f"📉 Negative Sentiment: {fund}",
                        "message": f"Strong negative sentiment ({abs(sentiment['overall_score']):.0%})",
                        "confidence": abs(sentiment["overall_score"]),
                        "action": "CAUTION_FUND",
                    })
            
            # Alert 4: Price Volatility
            price_data = next((p for p in prices if p["fund"] == fund), None)
            if price_data and abs(price_data["change"]) > 5:
                alerts.append({
                    "type": "HIGH_VOLATILITY",
                    "fund": fund,
                    "title": f"⚡ High Volatility: {fund}",
                    "message": f"{price_data['change']:.1f}% price movement",
                    "confidence": 0.9,
                    "action": "MONITOR_CLOSELY",
                })
        
        return alerts

    async def get_trading_opportunities(self, min_confidence: float = 0.75) -> List[Dict]:
        """
        Get current trading opportunities above confidence threshold
        """
        recs = self.last_recommendations.values()
        
        buy_opportunities = [
            r for r in recs
            if "BUY" in r["recommendation"] and r["confidence"] > min_confidence
        ]
        
        return sorted(buy_opportunities, key=lambda x: x["confidence"], reverse=True)

    async def get_risk_exposure(self) -> Dict:
        """
        Calculate overall portfolio risk exposure
        """
        if not self.last_recommendations:
            return {"error": "No data available"}
        
        total_risk = 0
        high_risk_funds = []
        
        for rec in self.last_recommendations.values():
            fund = rec["fund"]
            volatility = abs(rec["price_change"]) / 100
            risk_score = self.recommendation_engine.get_risk_score(fund, volatility)
            
            total_risk += risk_score
            
            if risk_score > 60:
                high_risk_funds.append({
                    "fund": fund,
                    "risk_score": risk_score,
                    "reason": "High volatility detected",
                })
        
        avg_risk = total_risk / len(self.last_recommendations) if self.last_recommendations else 0
        
        return {
            "average_risk": avg_risk,
            "portfolio_risk_level": "HIGH" if avg_risk > 60 else "MEDIUM" if avg_risk > 40 else "LOW",
            "high_risk_funds": high_risk_funds,
            "total_funds_monitored": len(self.last_recommendations),
        }

    async def health_check(self) -> Dict:
        """
        Check health of all agents
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "price_monitor": "healthy" if self.last_prices else "not_run",
            "sentiment_analyzer": "healthy" if self.last_sentiment else "not_run",
            "recommendation_engine": "healthy" if self.last_recommendations else "not_run",
            "last_cycle": self.last_recommendations.get("timestamp", "never") if self.last_recommendations else None,
        }


# Global orchestrator instance
orchestrator = AgentOrchestrator()


async def start_continuous_monitoring(interval_seconds: int = 30):
    """
    Start continuous monitoring in background
    Runs orchestrator cycle every N seconds
    """
    logger.info(f"🚀 Starting continuous monitoring (every {interval_seconds}s)")
    
    while True:
        try:
            await orchestrator.run_full_cycle()
            await asyncio.sleep(interval_seconds)
        except Exception as e:
            logger.error(f"❌ Monitoring error: {e}")
            await asyncio.sleep(interval_seconds)
