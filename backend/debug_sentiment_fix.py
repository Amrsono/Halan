import asyncio
import os
import sys

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.services.sentiment_fetcher import RealSentimentFetcher

async def test_sentiment_logic():
    fetcher = RealSentimentFetcher()
    
    funds = ["az_gold", "az_opportunity", "halan_saving", "az_shariah"]
    
    print("Testing Sentiment Fetcher Logic (Real/Fallback)...\n")
    
    for fund in funds:
        print(f"--- Fetching for {fund} ---")
        try:
            result = await fetcher.fetch_sentiment(fund)
            if result:
                print(f"✅ Success for {fund}")
                print(f"   Score: {result.get('overall_score')}")
                print(f"   Sources: {len(result.get('sources', []))}")
                print(f"   Sample Source: {result.get('sources', [])[:1]}")
            else:
                print(f"❌ No data found for {fund} (should have triggered fallback)")
        except Exception as e:
            print(f"❌ Error: {e}")
        print("\n")

if __name__ == "__main__":
    asyncio.run(test_sentiment_logic())
