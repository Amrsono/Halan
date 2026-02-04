
import logging
import feedparser
import aiohttp
import asyncio
from typing import List, Dict
from datetime import datetime
from urllib.parse import quote

logger = logging.getLogger(__name__)

class BaseSource:
    async def fetch(self, query: str) -> List[Dict]:
        raise NotImplementedError


class GoogleNewsSource(BaseSource):
    """
    Fetches news from Google News RSS feed.
    """
    BASE_URL = "https://news.google.com/rss/search?q={query}&hl=en-EG&gl=EG&ceid=EG:en"

    async def fetch(self, query: str) -> List[Dict]:
        try:
            # URL encode the query to handle spaces
            encoded_query = quote(query)
            url = self.BASE_URL.format(query=encoded_query)
            # feedparser can hang, so we wrap in wait_for
            feed = await asyncio.wait_for(
                asyncio.to_thread(feedparser.parse, url),
                timeout=5.0
            )
            
            results = []
            for entry in feed.entries[:5]: # Top 5 news
                results.append({
                    "text": entry.title,
                    "url": entry.link,
                    "source": "Google News",
                    "timestamp": datetime.now().isoformat()
                })
            return results
        except asyncio.TimeoutError:
            logger.error(f"Google News fetch timed out for {query}")
            return []
        except Exception as e:
            logger.error(f"Google News fetch error for {query}: {e}")
            return []

class RedditSource(BaseSource):
    """
    Fetches recent posts from relevant subreddits (json).
    Targeting r/PersonalFinanceEgypt and general search.
    """
    # Using public JSON endpoints
    SUBREDDITS = ["PersonalFinanceEgypt", "Egypt"]

    async def fetch(self, query: str) -> List[Dict]:
        results = []
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            for sub in self.SUBREDDITS:
                try:
                    # Search within subreddit - URL encode the query
                    encoded_query = quote(query)
                    url = f"https://www.reddit.com/r/{sub}/search.json?q={encoded_query}&restrict_sr=1&sort=new&limit=3"
                    async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            posts = data.get("data", {}).get("children", [])
                            for post in posts:
                                p_data = post.get("data", {})
                                title = p_data.get("title", "")
                                selftext = p_data.get("selftext", "")[:100] # truncated body
                                
                                results.append({
                                    "text": f"{title} - {selftext}",
                                    "url": f"https://reddit.com{p_data.get('permalink')}",
                                    "source": f"Reddit (r/{sub})",
                                    "timestamp": datetime.now().isoformat()
                                })
                except Exception as e:
                    logger.error(f"Reddit fetch error for {sub}: {e}")
        return results

class InvestingComSource(BaseSource):
    """
    Fetches news from Investing.com RSS (General Market News).
    """
    # Investing.com RSS feeds (General Market)
    RSS_URL = "https://www.investing.com/rss/news_25.rss" # Commodities/Futures often relevant

    async def fetch(self, query: str) -> List[Dict]:
        try:
             # This is a general feed, so we filter by query locally
            feed = await asyncio.wait_for(
                asyncio.to_thread(feedparser.parse, self.RSS_URL),
                timeout=5.0
            )
            results = []
            
            query_lower = query.lower()
            
            for entry in feed.entries:
                title = entry.get("title", "")
                summary = entry.get("summary", entry.get("description", ""))
                text_content = f"{title} {summary}".lower()
                
                # Relaxed matching: match query OR general market terms
                # If query is very specific (e.g. "Azimut"), it might not match general news.
                # So we always return some general market news if specific fail?
                # For now, just broaden "market", "economy", "stock", "rates"
                general_terms = ["market", "economy", "stock", "rate", "price", "invest", "dow", "nasdaq", "egx"]
                
                is_match = query_lower in text_content
                if not is_match:
                     is_match = any(term in text_content for term in general_terms)

                if is_match: 
                     results.append({
                        "text": entry.get("title", "No Title"),
                        "url": entry.get("link", ""),
                        "source": "Investing.com",
                        "timestamp": datetime.now().isoformat()
                    })
            
            return results
        except asyncio.TimeoutError:
            logger.warning("Investing.com fetch timed out")
            return []
        except Exception as e:
            logger.error(f"Investing.com fetch error: {e}")
            return []


class TradingViewSource(BaseSource):
    """
    Fetches market data and insights from TradingView.
    """
    BASE_URL = "https://www.tradingview.com/search/?q={query}"

    async def fetch(self, query: str) -> List[Dict]:
        try:
            encoded_query = quote(query)
            # TradingView doesn't have direct RSS, we fetch HTML and parse
            # For now, return general trading insights
            results = [
                {
                    "text": f"TradingView: {query} - Technical analysis and market trends",
                    "url": f"https://www.tradingview.com/search/?q={encoded_query}",
                    "source": "TradingView",
                    "timestamp": datetime.now().isoformat()
                }
            ]
            return results
        except Exception as e:
            logger.error(f"TradingView fetch error: {e}")
            return []


class YahooFinanceSource(BaseSource):
    """
    Fetches financial news from Yahoo Finance RSS.
    """
    BASE_URL = "https://feeds.finance.yahoo.com/rss/2.0/headline?s={query}"

    async def fetch(self, query: str) -> List[Dict]:
        try:
            encoded_query = quote(query)
            url = self.BASE_URL.format(query=encoded_query)
            
            feed = await asyncio.wait_for(
                asyncio.to_thread(feedparser.parse, url),
                timeout=5.0
            )
            
            results = []
            for entry in feed.entries[:5]:  # Top 5 articles
                results.append({
                    "text": entry.get("title", "No Title"),
                    "url": entry.get("link", ""),
                    "source": "Yahoo Finance",
                    "timestamp": datetime.now().isoformat()
                })
            
            return results
        except asyncio.TimeoutError:
            logger.warning("Yahoo Finance fetch timed out")
            return []
        except Exception as e:
            logger.error(f"Yahoo Finance fetch error: {e}")
            return []
