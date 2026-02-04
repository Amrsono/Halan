import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
from app.services.trading_service import TradingService
from app.models.database import Trade

# Mock Database Session
@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def trading_service(mock_db):
    return TradingService(db=mock_db)

def test_trade_size_limit(trading_service):
    """Test that individual trades exceeding the limit are rejected"""
    # 50,000 is default limit, try 51,000
    validation = trading_service.validate_trade(51000.0, is_live=True)
    assert not validation["valid"]
    assert "exceeds limit" in validation["reason"]

    # Try valid amount
    validation = trading_service.validate_trade(49000.0, is_live=True)
    assert validation["valid"]

def test_daily_spend_limit(trading_service):
    """Test that trades exceeding daily limit are rejected"""
    # Mock _get_daily_spend to return a high value
    with patch.object(trading_service, '_get_daily_spend', return_value=240000.0) as mock_spend:
        # Default daily limit is 250,000
        # 240,000 + 20,000 = 260,000 > 250,000
        validation = trading_service.validate_trade(20000.0, is_live=True)
        assert not validation["valid"]
        assert "Daily limit exceeded" in validation["reason"]
        
        # 240,000 + 5,000 = 245,000 < 250,000 (Valid)
        validation = trading_service.validate_trade(5000.0, is_live=True)
        assert validation["valid"]

def test_live_trading_disabled_by_default(trading_service):
    """Test that live trading requires the enabled flag"""
    # Ensure it's disabled by default (or as initialized in fixture)
    trading_service.enable_live_trading = False
    
    validation = trading_service.validate_trade(100.0, is_live=True)
    assert not validation["valid"]
    assert "Live trading is disabled" in validation["reason"]

    # Check that paper trade ignores this flag
    validation = trading_service.validate_trade(100.0, is_live=False)
    assert validation["valid"]

def test_get_daily_spend_query(mock_db):
    """Test the database query logic for daily spend"""
    service = TradingService(db=mock_db)
    
    # Mock query chain: db.query().filter().filter().scalar()
    mock_query = mock_db.query.return_value
    mock_filter1 = mock_query.filter.return_value
    mock_filter2 = mock_filter1.filter.return_value
    mock_filter2.scalar.return_value = 15000.0
    
    spend = service._get_daily_spend()
    assert spend == 15000.0
    
    # Verify query structure roughly
    assert mock_db.query.called
    assert mock_query.filter.call_count == 2 # timestamp and action
