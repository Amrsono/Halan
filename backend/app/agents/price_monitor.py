"""Price Monitoring Agent - Tracks fund prices in real-time"""
import asyncio
import logging
import os
from datetime import datetime
from typing import Dict, List
import aiohttp
from bs4 import BeautifulSoup
from app.services.price_fetcher import get_price_fetcher, MockPriceFetcher

logger = logging.getLogger(__name__)

FUNDS = {
    "halan_saving": {"ticker": "HALAN", "url": "https://www.egx.com.eg/"},
    "az_gold": {"ticker": "AZGOLD", "url": "https://www.egx.com.eg/"},
    "az_opportunity": {"ticker": "AZOPPO", "url": "https://www.egx.com.eg/"},
    "az_shariah": {"ticker": "ASO", "url": "https://thndr.app/"},
}


class PriceMonitor:
    """Monitor real-time prices for investment funds"""

    def __init__(self):
        self.prices = {}
        self.price_history = {}
        # Check environment variable to decide which fetcher to use
        # Default to True (Real) now that we have proxies
        use_real_data = os.getenv("USE_REAL_DATA", "True").lower() == "true"
        self.fetcher = get_price_fetcher(use_real_data)
        
        # Fallback to mock if real fetcher fails or returns None is handled in fetch logic
        self.mock_fetcher = MockPriceFetcher()

    async def fetch_price(self, fund_name: str) -> Dict:
        """Fetch current price for a fund"""
        try:
            fund_data = FUNDS.get(fund_name)
            if not fund_data:
                logger.error(f"Fund {fund_name} not found")
                return None

            price_info = await self.fetcher.fetch_price(fund_name, fund_data)
            
            # Fallback to mock if real fetcher returns nothing (e.g. not implemented yet)
            if price_info is None:
                price_info = await self.mock_fetcher.fetch_price(fund_name, fund_data)

            if price_info:
                self.prices[fund_name] = price_info
                
                # Update history
                if fund_name not in self.price_history:
                    self.price_history[fund_name] = []
                self.price_history[fund_name].append(price_info)
                
                # Keep last 100 records
                if len(self.price_history[fund_name]) > 100:
                    self.price_history[fund_name].pop(0)
                
            return price_info

        except Exception as e:
            logger.error(f"Error fetching price for {fund_name}: {e}")
            return None

    async def monitor_all_funds(self) -> List[Dict]:
        """Monitor all funds simultaneously"""
        tasks = [self.fetch_price(fund_name) for fund_name in FUNDS.keys()]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r]

    def get_price_change_24h(self, fund_name: str) -> float:
        """Get 24h price change percentage"""
        if fund_name in self.prices:
            return self.prices[fund_name]["change"]
        return 0.0

    def get_all_prices(self) -> Dict:
        """Get all current prices"""
        return self.prices

    async def detect_arbitrage(self) -> List[Dict]:
        """Detect price discrepancies between markets"""
        # This will compare prices across different brokers/platforms
        # For now, returns mock opportunities
        opportunities = []
        prices = await self.monitor_all_funds()

        for price in prices:
            if abs(price["change"]) > 2:  # Threshold for opportunity
                opportunities.append(
                    {
                        "fund": price["fund"],
                        "opportunity": "price_swing",
                        "magnitude": price["change"],
                        "action": "BUY" if price["change"] < -2 else "SELL",
                        "confidence": 0.75,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

        return opportunities
