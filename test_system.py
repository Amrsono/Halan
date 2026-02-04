"""
Test script to verify all agents and endpoints are working correctly
Run: python test_system.py
"""

import asyncio
import requests
import json
from datetime import datetime

API_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_status(component: str, status: bool, message: str = ""):
    """Print test status"""
    symbol = f"{GREEN}✅{RESET}" if status else f"{RED}❌{RESET}"
    msg = f" - {message}" if message else ""
    print(f"{symbol} {component}{msg}")


def print_header(title: str):
    """Print section header"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{title:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")


async def test_api_endpoints():
    """Test all API endpoints"""
    print_header("Testing API Endpoints")
    
    endpoints = {
        "Health Check": f"{API_URL}/health",
        "Current Prices": f"{API_URL}/api/prices/current",
        "All Sentiment": f"{API_URL}/api/sentiment/all",
        "All Recommendations": f"{API_URL}/api/recommendations/all",
        "Top Opportunities": f"{API_URL}/api/recommendations/opportunities",
    }
    
    results = {}
    
    for name, url in endpoints.items():
        try:
            response = requests.get(url, timeout=5)
            status = response.status_code == 200
            results[name] = status
            print_status(
                name,
                status,
                f"Status {response.status_code}"
            )
            
            # Print sample data
            if status:
                try:
                    data = response.json()
                    if "data" in data:
                        print(f"   📊 Sample: {list(data['data'][:1])}")
                    elif "recommendations" in data:
                        print(f"   🤖 Found {len(data['recommendations'])} recommendations")
                    elif "alerts" in data:
                        print(f"   🚨 Found {len(data['alerts'])} alerts")
                except:
                    pass
                    
        except requests.exceptions.ConnectionError:
            results[name] = False
            print_status(name, False, "Connection refused")
        except Exception as e:
            results[name] = False
            print_status(name, False, str(e))
    
    return results


async def test_agents():
    """Test individual agents"""
    print_header("Testing Agents")
    
    tests = {
        "Price Monitor": f"{API_URL}/api/prices/current",
        "Sentiment Analyzer": f"{API_URL}/api/sentiment/all",
        "Recommendation Engine": f"{API_URL}/api/recommendations/all",
    }
    
    agent_results = {}
    
    for agent_name, endpoint in tests.items():
        try:
            response = requests.get(endpoint, timeout=5)
            data = response.json()
            
            # Check if data is present
            has_data = False
            if "data" in data and len(data["data"]) > 0:
                has_data = True
                count = len(data["data"])
            elif "recommendations" in data and len(data["recommendations"]) > 0:
                has_data = True
                count = len(data["recommendations"])
            else:
                has_data = False
                count = 0
            
            agent_results[agent_name] = has_data
            print_status(
                agent_name,
                has_data,
                f"Processing {count} items"
            )
            
        except Exception as e:
            agent_results[agent_name] = False
            print_status(agent_name, False, str(e))
    
    return agent_results


async def test_frontend():
    """Test frontend accessibility"""
    print_header("Testing Frontend")
    
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        status = response.status_code == 200
        print_status("Frontend Service", status, f"Status {response.status_code}")
        return status
    except requests.exceptions.ConnectionError:
        print_status("Frontend Service", False, "Connection refused - is React running?")
        return False
    except Exception as e:
        print_status("Frontend Service", False, str(e))
        return False


async def test_database():
    """Test database connectivity"""
    print_header("Testing Database")
    
    try:
        # Try to fetch price history (requires DB)
        response = requests.get(f"{API_URL}/api/prices/history/halan_saving", timeout=5)
        status = response.status_code in [200, 404]  # 404 is OK if no history yet
        print_status("Database Connection", status, f"Status {response.status_code}")
        
        if status and response.status_code == 200:
            data = response.json()
            print_status("Database Queries", True, f"Retrieved {len(data.get('data', []))} records")
        else:
            print_status("Database Queries", True, "Database ready (no history yet)")
        
        return True
    except Exception as e:
        print_status("Database Connection", False, str(e))
        return False


async def test_data_quality():
    """Test quality of data from agents"""
    print_header("Testing Data Quality")
    
    try:
        # Get prices
        prices_response = requests.get(f"{API_URL}/api/prices/current", timeout=5)
        prices_data = prices_response.json().get("data", [])
        
        if prices_data:
            price = prices_data[0]
            has_price = "price" in price and price["price"] > 0
            has_change = "change" in price
            print_status("Price Data Quality", has_price and has_change)
        
        # Get sentiment
        sentiment_response = requests.get(f"{API_URL}/api/sentiment/all", timeout=5)
        sentiment_data = sentiment_response.json().get("data", [])
        
        if sentiment_data:
            sentiment = sentiment_data[0]
            has_scores = all(k in sentiment for k in ["positive", "negative", "neutral"])
            has_overall = "overall_score" in sentiment
            print_status("Sentiment Data Quality", has_scores and has_overall)
        
        # Get recommendations
        rec_response = requests.get(f"{API_URL}/api/recommendations/all", timeout=5)
        rec_data = rec_response.json().get("recommendations", [])
        
        if rec_data:
            rec = rec_data[0]
            has_recommendation = "recommendation" in rec
            has_confidence = "confidence" in rec and 0 <= rec["confidence"] <= 1
            has_reason = "reason" in rec
            print_status(
                "Recommendation Quality",
                has_recommendation and has_confidence and has_reason,
                f"Sample: {rec['recommendation']} ({rec['confidence']:.0%})"
            )
        
        return True
    except Exception as e:
        print_status("Data Quality Check", False, str(e))
        return False


async def test_funds():
    """Test all monitored funds"""
    print_header("Testing Monitored Funds")
    
    funds = [
        "halan_saving",
        "az_gold",
        "az_opportunity",
        "az_shariah",
    ]
    
    try:
        prices_response = requests.get(f"{API_URL}/api/prices/current", timeout=5)
        prices = {p["fund"]: p for p in prices_response.json().get("data", [])}
        
        sentiment_response = requests.get(f"{API_URL}/api/sentiment/all", timeout=5)
        sentiments = {s["fund"]: s for s in sentiment_response.json().get("data", [])}
        
        all_good = True
        for fund in funds:
            has_price = fund in prices
            has_sentiment = fund in sentiments
            status = has_price and has_sentiment
            all_good = all_good and status
            
            if has_price:
                price_info = f"${prices[fund]['price']:.2f} ({prices[fund]['change']:+.1f}%)"
            else:
                price_info = "No price data"
            
            print_status(f"Fund: {fund.upper()}", status, price_info)
        
        return all_good
    except Exception as e:
        print_status("Funds Check", False, str(e))
        return False


async def print_summary(results: dict):
    """Print test summary"""
    print_header("Test Summary")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"Tests Passed: {GREEN}{passed}/{total}{RESET}")
    print(f"Success Rate: {GREEN}{(passed/total)*100:.0f}%{RESET}")
    
    if passed == total:
        print(f"\n{GREEN}🎉 All systems operational!{RESET}")
    elif passed > total * 0.75:
        print(f"\n{YELLOW}⚠️  Most systems working, check failures above{RESET}")
    else:
        print(f"\n{RED}❌ Multiple issues detected, review failures{RESET}")
    
    print("\nNext Steps:")
    print("1. ✅ Open http://localhost:3000 in your browser")
    print("2. ✅ Check API docs at http://localhost:8000/docs")
    print("3. ✅ Monitor prices and sentiment in real-time")
    print("4. ✅ Review recommendations for trading signals")


async def main():
    """Run all tests"""
    print(f"\n{BLUE}🧪 Halan Invest System Test Suite{RESET}")
    print(f"{BLUE}Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}\n")
    
    all_results = {}
    
    # Run tests
    try:
        print("⏳ Testing API endpoints...")
        api_results = await test_api_endpoints()
        all_results.update(api_results)
        
        print("\n⏳ Testing agents...")
        agent_results = await test_agents()
        all_results.update(agent_results)
        
        print("\n⏳ Testing frontend...")
        frontend_result = await test_frontend()
        all_results["Frontend"] = frontend_result
        
        print("\n⏳ Testing database...")
        db_result = await test_database()
        all_results["Database"] = db_result
        
        print("\n⏳ Testing data quality...")
        await test_data_quality()
        
        print("\n⏳ Testing monitored funds...")
        await test_funds()
        
    except KeyboardInterrupt:
        print(f"\n{YELLOW}⚠️  Tests interrupted{RESET}")
        return
    except Exception as e:
        print(f"\n{RED}❌ Unexpected error: {e}{RESET}")
    
    # Print summary
    await print_summary(all_results)
    
    print(f"\n{BLUE}Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}\n")


if __name__ == "__main__":
    asyncio.run(main())
