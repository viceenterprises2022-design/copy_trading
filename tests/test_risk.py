from datetime import datetime, timezone

from copy_trading.models import TradeSignal
from copy_trading.risk import PositionSizer, StopLossManager


def test_position_sizer():
    qty = PositionSizer.size_position(
        capital_usd=10_000,
        risk_per_trade=0.01,
        entry_price=100,
        stop_loss_price=97,
    )
    assert round(qty, 2) == 33.33


def test_stop_loss_manager_buy():
    signal = TradeSignal(
        platform="hyperliquid",
        trader_id="abc",
        symbol="BTC",
        side="buy",
        entry_price=100,
        timestamp=datetime.now(timezone.utc),
    )
    position = StopLossManager.build_position(signal, quantity=1, stop_loss_pct=0.03, take_profit_pct=0.06)
    assert round(position.stop_loss_price, 2) == 97.0
    assert round(position.take_profit_price, 2) == 106.0
