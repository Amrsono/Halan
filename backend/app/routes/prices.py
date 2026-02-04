"""Price monitoring API routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.agents.price_monitor import PriceMonitor
from app.models.database import PriceHistory, get_db
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/prices", tags=["prices"])
monitor = PriceMonitor()


@router.get("/current")
async def get_current_prices():
    """Get current prices for all funds"""
    prices = await monitor.monitor_all_funds()
    return {"data": prices, "timestamp": datetime.now().isoformat()}


@router.get("/fund/{fund_name}")
async def get_fund_price(fund_name: str):
    """Get price for a specific fund"""
    price = await monitor.fetch_price(fund_name)
    if not price:
        raise HTTPException(status_code=404, detail="Fund not found")
    return {"data": price}


@router.get("/opportunities")
async def get_price_opportunities():
    """Get detected price opportunities"""
    opportunities = await monitor.detect_arbitrage()
    return {"opportunities": opportunities, "count": len(opportunities)}


@router.get("/history/{fund_name}")
async def get_price_history(
    fund_name: str, days: int = 7, db: Session = Depends(get_db)
):
    """Get price history for a fund"""
    start_date = datetime.utcnow() - timedelta(days=days)

    history = (
        db.query(PriceHistory)
        .filter(
            PriceHistory.fund_name == fund_name,
            PriceHistory.timestamp >= start_date,
        )
        .order_by(PriceHistory.timestamp)
        .all()
    )

    return {
        "fund": fund_name,
        "days": days,
        "data": [
            {
                "price": h.price,
                "change": h.change_percent,
                "volume": h.volume,
                "timestamp": h.timestamp.isoformat(),
            }
            for h in history
        ],
    }
