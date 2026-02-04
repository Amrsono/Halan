"""Recommendation Engine - Generates buy/sell recommendations"""
import logging
from datetime import datetime
from typing import Dict, List

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """Generate trading recommendations based on price and sentiment"""

    # Recommendation Thresholds
    THRESHOLDS = {
        "STRONG_BUY": {"price_drop": -2.0, "sentiment": 0.5},
        "BUY": {"price_drop": 0.0, "sentiment": 0.3},
        "STRONG_SELL": {"price_rise": 2.0, "sentiment": -0.5},
        "SELL": {"price_rise": 1.0, "sentiment": -0.2},
    }

    # Weights
    WEIGHTS = {"price": 0.3, "sentiment": 0.7}

    def __init__(self):
        self.recommendations = {}

    async def generate_recommendation(
        self, fund_name: str, price_data: Dict, sentiment_data: Dict, price_history: List[Dict] = None
    ) -> Dict:
        """Generate recommendation based on price and sentiment"""
        price_change = price_data.get("change", 0)
        sentiment_score = sentiment_data.get("overall_score", 0)
        
        # Calculate RSI
        rsi = self.calculate_rsi(price_history) if price_history else 50.0

        # Simple recommendation logic
        # RSI < 30 is oversold (Buy signal), RSI > 70 is overbought (Sell signal)
        
        score = (abs(price_change) * self.WEIGHTS["price"]) + (
            sentiment_score * self.WEIGHTS["sentiment"]
        )

        t = self.THRESHOLDS
        
        recommendation = "HOLD"
        confidence = 0.7

        if (
            price_change < t["STRONG_BUY"]["price_drop"]
            and sentiment_score > t["STRONG_BUY"]["sentiment"]
        ):
            recommendation = "STRONG_BUY"
            confidence = min(0.95, 0.6 + abs(price_change) / 10 + sentiment_score)
        elif (
            price_change < t["BUY"]["price_drop"]
            and sentiment_score > t["BUY"]["sentiment"]
        ) or rsi < 30: # Added RSI buy signal
            recommendation = "BUY"
            confidence = min(0.9, 0.5 + sentiment_score + (0.1 if rsi < 30 else 0))
        elif (
            price_change > t["STRONG_SELL"]["price_rise"]
            and sentiment_score < t["STRONG_SELL"]["sentiment"]
        ):
            recommendation = "STRONG_SELL"
            confidence = min(0.95, 0.6 + price_change / 10 - sentiment_score)
        elif (
            price_change > t["SELL"]["price_rise"]
            and sentiment_score < t["SELL"]["sentiment"]
        ) or rsi > 70: # Added RSI sell signal
            recommendation = "SELL"
            confidence = min(0.9, 0.5 - sentiment_score + (0.1 if rsi > 70 else 0))

        return {
            "fund": fund_name,
            "recommendation": recommendation,
            "confidence": confidence,
            "price_change": price_change,
            "sentiment_score": sentiment_score,
            "rsi": rsi,
            "reason": self._generate_reason(
                recommendation, price_change, sentiment_score, rsi
            ),
            "target_price": price_data.get("price", 0)
            * (1 + (0.02 if "BUY" in recommendation else -0.02)),
            "timestamp": datetime.now().isoformat(),
        }

    def calculate_rsi(self, price_history: List[Dict], period: int = 14) -> float:
        """Calculate Relative Strength Index (RSI)"""
        if not price_history or len(price_history) < period + 1:
            return 50.0
            
        prices = [p["price"] for p in price_history]
        changes = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        
        # We need at least 'period' changes
        if len(changes) < period:
            return 50.0
            
        # Use only the last 'period' changes
        recent_changes = changes[-period:]
        
        gains = [c for c in recent_changes if c > 0]
        losses = [abs(c) for c in recent_changes if c < 0]
        
        avg_gain = sum(gains) / period if gains else 0
        avg_loss = sum(losses) / period if losses else 0
        
        if avg_loss == 0:
            return 100.0
            
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return round(rsi, 2)

    def _generate_reason(
        self, recommendation: str, price_change: float, sentiment_score: float, rsi: float = 50.0
    ) -> str:
        """Generate human-readable reason for recommendation"""
        reasons = []
        t = self.THRESHOLDS

        if abs(price_change) > 2:
            reasons.append(f"Price moved {price_change:.1f}%")

        if sentiment_score > t["STRONG_BUY"]["sentiment"]:
            reasons.append("Strong positive sentiment")
        elif sentiment_score < t["STRONG_SELL"]["sentiment"]:
            reasons.append("Strong negative sentiment")
            
        if rsi < 30:
            reasons.append(f"RSI Oversold ({rsi})")
        elif rsi > 70:
            reasons.append(f"RSI Overbought ({rsi})")

        return " | ".join(reasons) if reasons else "Neutral indicators"

    async def generate_all_recommendations(
        self,
        price_data: Dict[str, Dict],
        sentiment_data: Dict[str, Dict],
        price_history: Dict[str, List[Dict]] = None
    ) -> List[Dict]:
        """Generate recommendations for all funds"""
        recommendations = []

        for fund_name, prices in price_data.items():
            sentiment = sentiment_data.get(fund_name, {})
            history = price_history.get(fund_name, []) if price_history else []
            
            rec = await self.generate_recommendation(fund_name, prices, sentiment, history)
            recommendations.append(rec)

        return recommendations

    def get_top_opportunities(
        self, recommendations: List[Dict], limit: int = 3
    ) -> List[Dict]:
        """Get top trading opportunities"""
        buy_recs = [r for r in recommendations if "BUY" in r["recommendation"]]
        sorted_recs = sorted(buy_recs, key=lambda x: x["confidence"], reverse=True)
        return sorted_recs[:limit]

    def get_risk_score(self, fund_name: str, price_volatility: float) -> float:
        """Calculate risk score for a fund"""
        # Simple risk calculation (0-100)
        base_risk = 30
        volatility_risk = min(40, price_volatility * 10)
        return base_risk + volatility_risk
