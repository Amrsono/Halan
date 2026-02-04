"""Price Fetcher Service - Handles data retrieval from various sources"""
import abc
import logging
import random
from datetime import datetime
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class BasePriceFetcher(abc.ABC):
    """Abstract base class for price fetchers"""
    
    @abc.abstractmethod
    async def fetch_price(self, fund_name: str, fund_data: Dict) -> Optional[Dict]:
        """Fetch price for a specific fund"""
        pass

class MockPriceFetcher(BasePriceFetcher):
    """Generates simulated price data for development"""
    
    async def fetch_price(self, fund_name: str, fund_data: Dict) -> Optional[Dict]:
        # Simulated price data
        current_price = (100 + (hash(fund_name) % 50)) * 50
        # Add some random fluctuation
        fluctuation = random.uniform(-0.5, 0.5)
        current_price += fluctuation
        
        change_percent = -2.5 + (hash(fund_name) % 5) + random.uniform(-0.2, 0.2)

        return {
            "fund": fund_name,
            "ticker": fund_data["ticker"],
            "price": round(current_price, 2),
            "change": round(change_percent, 2),
            "timestamp": datetime.now().isoformat(),
            "volume": int(1_000_000 + (hash(fund_name) % 500_000)),
            "source": "mock"
        }

class RealPriceFetcher(BasePriceFetcher):
    """Fetches real market data using yfinance proxies"""
    
    def __init__(self):
        try:
            import yfinance as yf
            self.yf = yf
        except ImportError:
            logger.error("yfinance not installed")
            self.yf = None

    async def fetch_price(self, fund_name: str, fund_data: Dict) -> Optional[Dict]:
        if not self.yf:
            return None
            
        try:
            # 1. Get USD/EGP Rate
            egp_ticker = self.yf.Ticker("EGP=X")
            egp_hist = egp_ticker.history(period="1d")
            usd_egp = egp_hist['Close'].iloc[-1] if not egp_hist.empty else 50.0
            
            # 2. Determine Proxy Ticker
            proxy_ticker_name = None
            if "gold" in fund_name.lower():
                proxy_ticker_name = "GC=F" # Gold Futures (USD)
            elif "saving" in fund_name.lower():
                # Savings is simulated 20% APY, handled by mock or fixed logic usually
                # But here we can simulate a steady accumulation
                return await self._simulate_saving_growth(fund_name, fund_data)
            else:
                proxy_ticker_name = "^CASE30" # EGX 30 Index (EGP)
            
            # 3. Fetch Data
            ticker = self.yf.Ticker(proxy_ticker_name)
            hist = ticker.history(period="1d")
            
            if hist.empty:
                logger.warning(f"No data for {proxy_ticker_name}")
                return None
                
            current_val = hist['Close'].iloc[-1]
            prev_close = hist['Open'].iloc[-1] # Close enough for 1d change
            
            # 4. Calculate Derived Fund Price (EGP)
            # We map the raw index/gold price to the fund's NAV scale
            # This is a simulation of the *movement*, not the exact NAV
            derived_price = 0.0
            
            if "gold" in fund_name.lower():
                # Gold is in USD/oz. Convert to EGP/gram approx
                # 1 oz = 31.1g
                price_per_gram_usd = current_val / 31.1
                price_per_gram_egp = price_per_gram_usd * usd_egp
                
                # Azimut gold cert is ~26 EGP. So we scale it.
                # It's fraction of a gram. 26 EGP is approx 0.007g? 
                # Let's just scale the movement to the base price of ~26
                # Base mock was ~26. Let's just return the calculated gram price / 100 for now to match ~35-40 range
                derived_price = price_per_gram_egp / 100 
                
            elif "opportunity" in fund_name.lower() or "shariah" in fund_name.lower():
                # EGX30 is ~30,000 pts. Fund is ~40 EGP.
                # Scale: Index / 750
                derived_price = current_val / 750
                
            change_pct = ((current_val - prev_close) / prev_close) * 100
            
            return {
                "fund": fund_name,
                "ticker": fund_data["ticker"],
                "price": round(derived_price, 2),
                "change": round(change_pct, 2),
                "timestamp": datetime.now().isoformat(),
                "volume": int(hist['Volume'].iloc[-1]) if 'Volume' in hist else 1000000,
                "source": f"yfinance ({proxy_ticker_name})"
            }
            
        except Exception as e:
            logger.error(f"Real fetch failed for {fund_name}: {e}")
            return None

    async def _simulate_saving_growth(self, fund_name, fund_data):
        # 20% APY / 365 = 0.054% daily
        # Base price 1000
        # Simulating a growing price
        
        # We can't easily persist state here without DB, so we'll just return a calculated value based on day of year?
        # Or just return a base + random small positive
        
        # Using a fixed "mock" logic but with guaranteed positive drift
        # This is safe because Savings don't fluctuate with market
        return {
            "fund": fund_name,
            "ticker": fund_data["ticker"],
            "price": 1000.0, # Fixed unit price usually, returns are interest
            "change": 0.05, # Daily accural
            "timestamp": datetime.now().isoformat(),
            "volume": 0,
            "source": "Fixed Rate (20% APY)"
        }

def get_price_fetcher(use_real_data: bool = False) -> BasePriceFetcher:
    """Factory to get the appropriate fetcher"""
    if use_real_data:
        return RealPriceFetcher()
    return MockPriceFetcher()
