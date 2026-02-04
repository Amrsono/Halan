import logging
import os
from datetime import datetime
from typing import Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.database import Trade, SessionLocal

logger = logging.getLogger(__name__)

class TradingService:
    """
    Manages trade execution, supports both Paper Trading and Live Trading (future).
    """
    
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()
        # Default starting paper balance
        self.paper_balance = 500000.00 
        
        # Load Configuration
        self.enable_live_trading = os.getenv("ENABLE_LIVE_TRADING", "False").lower() == "true"
        self.trade_size_limit = float(os.getenv("TRADE_SIZE_LIMIT", "50000.0"))
        self.daily_spend_limit = float(os.getenv("DAILY_SPEND_LIMIT", "250000.0"))

    def validate_trade(self, amount: float, is_live: bool = False) -> Dict:
        """Validate if a trade is safe to execute"""
        # 1. Check Master Switch for Live Trading
        if is_live and not self.enable_live_trading:
            return {"valid": False, "reason": "Live trading is disabled via ENABLE_LIVE_TRADING"}
            
        # 2. Check Trade Size Limit
        if amount > self.trade_size_limit:
            return {"valid": False, "reason": f"Trade amount EGP {amount:.2f} exceeds limit EGP {self.trade_size_limit:.2f}"}
            
        # 3. Check Daily Limit (Simplified)
        today_spend = self._get_daily_spend()
        if (today_spend + amount) > self.daily_spend_limit:
             return {"valid": False, "reason": f"Daily limit exceeded. Spent: EGP {today_spend:.2f}, Limit: EGP {self.daily_spend_limit:.2f}"}

        return {"valid": True, "reason": "Trade checks passed"}

    def _get_daily_spend(self) -> float:
        """Calculate total amount spent today"""
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        try:
            # Query sum of all BUY trades since start of today
            result = self.db.query(func.sum(Trade.total))\
                .filter(Trade.timestamp >= today_start)\
                .filter(Trade.action == "BUY")\
                .scalar()
                
            return float(result) if result else 0.0
        except Exception as e:
            logger.error(f"Error calculating daily spend: {e}")
            # If DB fails, assume 0 to avoid blocking, or safer to assume max?
            # Safer to return 0 but log error, as blocking all trades due to DB glitch might be too aggressive
            # But for safety critical system, maybe fail open or closed?
            # Let's return 0 but log strictly.
            return 0.0

    def execute_paper_trade(self, fund_name: str, action: str, price: float, confidence: float) -> Optional[Dict]:
        """
        Execute a simulated paper trade.
        """
        try:
            # Simple logic: Fixed position size for now
            position_size = 1000.0  # $1000 per trade
            quantity = position_size / price
            
            # Validation (Apply same rules to paper trading to test them)
            validation = self.validate_trade(position_size, is_live=False)
            if not validation["valid"]:
                logger.warning(f"⚠️ Paper trade rejected: {validation['reason']}")
                return None

            trade = Trade(
                fund_name=fund_name,
                action=action,
                quantity=round(quantity, 4),
                price=price,
                total=round(position_size, 2),
                status="executed", # Immediate execution for paper trading
                timestamp=datetime.now()
            )
            
            self.db.add(trade)
            self.db.commit()
            self.db.refresh(trade)
            
            logger.info(f"📝 PAPER TRADE EXECUTED: {action} {fund_name} @ EGP {price:.2f} (Qty: {quantity:.4f})")
            
            return {
                "id": trade.id,
                "fund": trade.fund_name,
                "action": trade.action,
                "price": trade.price,
                "quantity": trade.quantity,
                "total": trade.total,
                "status": trade.status,
                "timestamp": trade.timestamp.isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to execute paper trade: {e}")
            self.db.rollback()
            return None

    def execute_live_trade(self, fund_name: str, action: str, price: float, quantity: float) -> Optional[Dict]:
        """
        Execute a REAL-DATA SIMULATION trade.
        Uses real-time prices but executes internally (Paper Trading with Real Data).
        """
        total_amount = price * quantity
        
        # 1. Critical Validation
        # Check against 'live' limits even though it's simulation, to mimic production constraints
        validation = self.validate_trade(total_amount, is_live=True)
        if not validation["valid"]:
            logger.error(f"⛔ LIVE SIMULATION BLOCKED: {validation['reason']}")
            return None
            
        # 2. Execution Logic (Simulation)
        logger.info(f"🚀 EXECUTING LIVE SIMULATION: {action} {quantity} of {fund_name} @ {price}")
        
        try:
            # Create trade record - Status 'executed' so it shows up in history as done
            trade = Trade(
                fund_name=fund_name,
                action=action,
                quantity=round(quantity, 4),
                price=price,
                total=round(total_amount, 2),
                status="executed", 
                timestamp=datetime.now()
            )
            
            self.db.add(trade)
            self.db.commit()
            self.db.refresh(trade)
            
            logger.info("✅ Live simulation trade confirmed and recorded in DB")
            
            return {
                "id": trade.id,
                "fund": trade.fund_name,
                "action": trade.action,
                "price": trade.price,
                "quantity": trade.quantity,
                "total": trade.total,
                "status": trade.status,
                "timestamp": trade.timestamp.isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Live simulation failed to record: {e}")
            self.db.rollback()
            return None
    
    def get_recent_trades(self, limit: int = 10):
        """Get recent trades from database"""
        return self.db.query(Trade).order_by(Trade.timestamp.desc()).limit(limit).all()

# Global instance
trading_service = TradingService()
