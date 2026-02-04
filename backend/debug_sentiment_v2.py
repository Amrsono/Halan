
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
    # Try a broad query that definitely exists
    res = await g.fetch("Egypt") 
    print(f"Google (Egypt): {len(res)} items")
    if res: print(res[0]['text'])

    print("\nTesting Reddit...")
    r = RedditSource()
    res = await r.fetch("Egypt")
    print(f"Reddit (Egypt): {len(res)} items")
    if res: print(res[0]['text'][:50])

    print("\nTesting Investing.com...")
    i = InvestingComSource()
    res = await i.fetch("Market") # General query
    print(f"Investing: {len(res)} items")
    if res: print(res[0]['text'])

if __name__ == "__main__":
    asyncio.run(test())
