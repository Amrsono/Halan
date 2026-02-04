import pytest
import asyncio
from app.agents.price_monitor import PriceMonitor
from app.services.price_fetcher import MockPriceFetcher, RealPriceFetcher

@pytest.mark.asyncio
async def test_price_monitor_initialization():
    monitor = PriceMonitor()
    assert isinstance(monitor.fetcher, MockPriceFetcher)  # Default should be mock
    assert isinstance(monitor.mock_fetcher, MockPriceFetcher)

@pytest.mark.asyncio
async def test_fetch_price_mock():
    monitor = PriceMonitor()
    price_info = await monitor.fetch_price("halan_saving")
    
    assert price_info is not None
    assert price_info["fund"] == "halan_saving"
    assert "price" in price_info
    assert "change" in price_info
    assert price_info["source"] == "mock"

@pytest.mark.asyncio
async def test_monitor_all_funds():
    monitor = PriceMonitor()
    results = await monitor.monitor_all_funds()
    
    assert len(results) == 4  # We have 4 configured funds
    funds = [r["fund"] for r in results]
    assert "halan_saving" in funds
    assert "az_gold" in funds
    assert "az_opportunity" in funds
    assert "az_shariah" in funds
