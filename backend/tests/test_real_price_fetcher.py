import asyncio
import sys
try:
    import pytest
except ImportError:
    pytest = None

from app.services.price_fetcher import RealPriceFetcher, get_price_fetcher

if pytest:
    @pytest.mark.asyncio
    async def test_real_price_fetcher_instantiation():
        """Test that factory returns RealPriceFetcher when forced"""
        fetcher = get_price_fetcher(use_real_data=True)
        assert isinstance(fetcher, RealPriceFetcher)

    @pytest.mark.asyncio
    async def test_fetch_gold_fund():
        """Test fetching Azimut Gold fund via proxy"""
        fetcher = RealPriceFetcher()
        if not fetcher.yf:
            pytest.skip("yfinance not installed")
            
        result = await fetcher.fetch_price("az_gold", {"ticker": "AZGOLD"})
        
        assert result is not None
        assert result["fund"] == "az_gold"
        assert result["price"] > 0
        assert "yfinance" in result["source"]
        print(f"Fetched GOLD: {result}")

    @pytest.mark.asyncio
    async def test_fetch_opportunity_fund():
        """Test fetching Azimut Opportunity fund via proxy"""
        fetcher = RealPriceFetcher()
        if not fetcher.yf:
            pytest.skip("yfinance not installed")
            
        result = await fetcher.fetch_price("az_opportunity", {"ticker": "AZOPPO"})
        
        assert result is not None
        assert result["fund"] == "az_opportunity"
        assert result["price"] > 0
        assert "yfinance" in result["source"]
        print(f"Fetched OPPORUNITY: {result}")

if __name__ == "__main__":
    # Manual run helper
    async def main():
        print("Testing RealPriceFetcher...")
        fetcher = RealPriceFetcher()
        if fetcher.yf:
            res_gold = await fetcher.fetch_price("az_gold", {"ticker": "AZGOLD"})
            print(f"Gold: {res_gold}")
            res_opp = await fetcher.fetch_price("az_opportunity", {"ticker": "AZOPPO"})
            print(f"Opp: {res_opp}")
        else:
            print("yfinance missing")
            
    asyncio.run(main())
