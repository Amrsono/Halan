"""Sentiment Analysis Agent - Analyzes social sentiment for funds"""
import logging
import os
from datetime import datetime
from typing import Dict, List
import re
from app.services.sentiment_fetcher import get_sentiment_fetcher, MockSentimentFetcher

logger = logging.getLogger(__name__)

# Mock sentiment keywords for demo (kept for local text analysis if needed)
BULLISH_KEYWORDS = [
    "bullish", "gains", "moon", "rally", "surge", "beat", "outperform", "strong", "surge"
]
BEARISH_KEYWORDS = [
    "bearish", "crash", "dump", "recession", "weak", "loss", "underperform", "dip", "panic"
]


class SentimentAnalyzer:
    """Analyze sentiment from X (Twitter) and Farcaster for funds"""

    def __init__(self):
        self.sentiment_cache = {}
        
        # Check environment variable to decide which fetcher to use
        # Default to False (Mock) if not set
        use_real_data = os.getenv("USE_REAL_DATA", "False").lower() == "true"
        self.fetcher = get_sentiment_fetcher(use_real_data)
        self.mock_fetcher = MockSentimentFetcher()

    async def analyze_tweet(self, text: str, fund_name: str) -> Dict:
        """Analyze sentiment of a single tweet (helper method)"""
        # This might still be useful if the fetcher returns raw tweets
        text_lower = text.lower()

        bullish_count = sum(1 for word in BULLISH_KEYWORDS if word in text_lower)
        bearish_count = sum(1 for word in BEARISH_KEYWORDS if word in text_lower)

        if bullish_count > bearish_count:
            sentiment = "positive"
            score = min(1.0, bullish_count / 5)
        elif bearish_count > bullish_count:
            sentiment = "negative"
            score = min(1.0, bearish_count / 5)
        else:
            sentiment = "neutral"
            score = 0.5

        return {
            "text": text[:100],
            "fund": fund_name,
            "sentiment": sentiment,
            "score": score,
            "timestamp": datetime.now().isoformat(),
        }

    async def fetch_sentiment_for_fund(self, fund_name: str) -> Dict:
        """Fetch aggregated sentiment for a fund from X and Farcaster"""
        try:
            result = await self.fetcher.fetch_sentiment(fund_name)
            
            if result is None:
                 result = await self.mock_fetcher.fetch_sentiment(fund_name)
                 
            if result:
                self.sentiment_cache[fund_name] = result
                
            return result
            
        except Exception as e:
            logger.error(f"Error fetching sentiment for {fund_name}: {e}")
            return None

    async def get_trending_keywords(self, fund_name: str) -> List[str]:
        """Get trending keywords for a fund on X/Farcaster"""
        try:
            keywords = await self.fetcher.get_trending_keywords(fund_name)
            if not keywords:
                keywords = await self.mock_fetcher.get_trending_keywords(fund_name)
            return keywords
        except Exception as e:
            logger.error(f"Error fetching keywords for {fund_name}: {e}")
            return []

    async def analyze_all_funds(self) -> List[Dict]:
        """Analyze sentiment for all funds"""
        # TODO: Refactor to get funds list dynamically or from config
        funds = [
            "halan_saving",
            "az_gold",
            "az_opportunity",
            "az_shariah",
        ]
        tasks = [self.fetch_sentiment_for_fund(fund) for fund in funds]
        results = []
        for task in tasks:
            result = await task
            if result:
                results.append(result)
        return results

    def get_sentiment_alert(self, fund_name: str, threshold: float = 0.7) -> str:
        """Generate sentiment-based alert"""
        if fund_name in self.sentiment_cache:
            score = self.sentiment_cache[fund_name].get("overall_score", 0)
            if score > threshold:
                return f"🚀 Strong positive sentiment for {fund_name}"
            elif score < -threshold:
                return f"⚠️ Strong negative sentiment for {fund_name}"
        return None
