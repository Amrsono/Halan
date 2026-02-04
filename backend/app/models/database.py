"""Database models and configuration"""
from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@db:5432/halan_invest"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class PriceHistory(Base):
    """Store historical price data"""
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    fund_name = Column(String, index=True)
    ticker = Column(String)
    price = Column(Float)
    change_percent = Column(Float)
    volume = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class SentimentRecord(Base):
    """Store sentiment analysis results"""
    __tablename__ = "sentiment_records"

    id = Column(Integer, primary_key=True, index=True)
    fund_name = Column(String, index=True)
    positive = Column(Float)
    neutral = Column(Float)
    negative = Column(Float)
    overall_score = Column(Float)
    source_count = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class TradeRecommendation(Base):
    """Store trade recommendations"""
    __tablename__ = "trade_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    fund_name = Column(String, index=True)
    recommendation = Column(String)  # BUY, SELL, HOLD, STRONG_BUY, STRONG_SELL
    confidence = Column(Float)
    price_change = Column(Float)
    sentiment_score = Column(Float)
    target_price = Column(Float)
    reason = Column(String)
    executed = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class Trade(Base):
    """Store executed trades"""
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    fund_name = Column(String, index=True)
    action = Column(String)  # BUY or SELL
    quantity = Column(Float)
    price = Column(Float)
    total = Column(Float)
    status = Column(String, default="pending")  # pending, executed, failed
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
