"""Sentiment Fetcher Service - Aggregates social sentiment data"""
import abc
import logging
import random
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class BaseSentimentFetcher(abc.ABC):
    """Abstract base class for sentiment fetchers"""
    
    @abc.abstractmethod
    async def fetch_sentiment(self, fund_name: str) -> Dict:
        """Fetch sentiment data for a specific fund"""
        pass
    
    @abc.abstractmethod
    async def get_trending_keywords(self, fund_name: str) -> List[str]:
        """Fetch trending keywords for a fund"""
        pass

class MockSentimentFetcher(BaseSentimentFetcher):
    """Generates simulated sentiment data"""
    
    async def fetch_sentiment(self, fund_name: str) -> Dict:
        # Simulated sentiment distribution
        # Add salt based on time to make it slightly dynamic
        salt = datetime.now().minute
        
        positive = 65 + (hash(fund_name) % 20) + (salt % 5)
        neutral = 20 + (salt % 3)
        negative = 15 - (hash(fund_name) % 10) + (salt % 2)
        
        # Normalize to 100%
        total = positive + neutral + negative
        
        normalized = {
            "positive": round((positive / total) * 100, 1),
            "neutral": round((neutral / total) * 100, 1),
            "negative": round((negative / total) * 100, 1),
        }
        
        sentiment_score = (normalized["positive"] - normalized["negative"]) / 100
        
        return {
            "fund": fund_name,
            "sentiment_distribution": normalized,
            "overall_score": round(sentiment_score, 2),
            "trending": normalized["positive"] > 60,
            "source_count": 150 + (hash(fund_name) % 200),
            "timestamp": datetime.now().isoformat(),
            "sources": ["mock_twitter", "mock_farcaster"]
        }

    async def get_trending_keywords(self, fund_name: str) -> List[str]:
        """Mock trending keywords"""
        trending_keywords = {
            "halan_saving": ["growth", "savings", "compound", "yield"],
            "az_gold": ["gold", "hedge", "inflation", "safe haven"],
            "az_opportunity": ["opportunity", "rally", "bullish", "stocks"],
            "az_shariah": ["sharia", "compliant", "ethical", "halal"],
        }
        return trending_keywords.get(fund_name, ["investing", "finance"])

class RealSentimentFetcher(BaseSentimentFetcher):
    """Fetches real data from Twitter/Farcaster APIs"""
    
    def __init__(self, twitter_api_key: str = None, farcaster_api_key: str = None):
        self.twitter_key = twitter_api_key
        self.farcaster_key = farcaster_api_key
    
    async def fetch_sentiment(self, fund_name: str) -> Dict:
        # TODO: Implement real API calls here
        # 1. Search Twitter API for fund_name
        # 2. Search Farcaster API for fund_name
        # 3. Analyze text (using NLP or simple keyword counting)
        # 4. Aggregate results
        
        logger.warning(f"Real sentiment fetching not implemented for {fund_name}")
        return None

    async def get_trending_keywords(self, fund_name: str) -> List[str]:
        # TODO: Implement real keyword extraction
        return []

def get_sentiment_fetcher(use_real_data: bool = False) -> BaseSentimentFetcher:
    """Factory to get the appropriate fetcher"""
    if use_real_data:
        # In a real app, you'd fetch keys from env vars here
        return RealSentimentFetcher()
    return MockSentimentFetcher()
