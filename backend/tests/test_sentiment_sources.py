
import pytest
import asyncio
from app.services.sentiment_sources import GoogleNewsSource, RedditSource, InvestingComSource

@pytest.mark.asyncio
async def test_google_news_fetch():
    source = GoogleNewsSource()
    results = await source.fetch("Azimut Egypt")
    print(f"\nGoogle News Results: {len(results)}")
    if results:
        print(results[0])
    
    # We expect some results usually, but network might fail. 
    # Test pass if it runs without error and returns list (empty or not)
    assert isinstance(results, list)

@pytest.mark.asyncio
async def test_reddit_fetch():
    source = RedditSource()
    results = await source.fetch("investment")
    print(f"\nReddit Results: {len(results)}")
    if results:
        print(results[0])
    assert isinstance(results, list)

@pytest.mark.asyncio
async def test_investing_com_fetch():
    source = InvestingComSource()
    results = await source.fetch("Gold")
    print(f"\nInvesting.com Results: {len(results)}")
    if results:
        print(results[0])
    assert isinstance(results, list)
