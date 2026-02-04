
import asyncio
import logging
import sys
from app.services.sentiment_sources import GoogleNewsSource, RedditSource, InvestingComSource

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test():
    print("Testing Google News...")
    g = GoogleNewsSource()
    res = await g.fetch("Egypt Inflation")
    print(f"Google: {len(res)} items")
    for r in res: print(r['text'])

    print("\nTesting Reddit...")
    r = RedditSource()
    res = await r.fetch("Egypt Economy")
    print(f"Reddit: {len(res)} items")
    for item in res: print(item['text'][:50])

    print("\nTesting Investing.com...")
    i = InvestingComSource()
    res = await i.fetch("Market") # General query
    print(f"Investing: {len(res)} items")
    for item in res: print(item['text'])

if __name__ == "__main__":
    asyncio.run(test())
