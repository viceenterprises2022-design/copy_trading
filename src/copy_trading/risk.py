from .models import Position, TradeSignal


class PositionSizer:
    """Risk-based position sizing using stop distance."""

    @staticmethod
    def size_position(capital_usd: float, risk_per_trade: float, entry_price: float, stop_loss_price: float) -> float:
        risk_budget = capital_usd * risk_per_trade
        risk_per_unit = abs(entry_price - stop_loss_price)
        if risk_per_unit <= 0:
            raise ValueError("Stop loss must differ from entry price")
        return risk_budget / risk_per_unit


class StopLossManager:
    """Basic stop-loss and take-profit management for copied trades."""

    @staticmethod
    def build_position(signal: TradeSignal, quantity: float, stop_loss_pct: float, take_profit_pct: float) -> Position:
        if signal.side.lower() == "buy":
            stop_loss = signal.entry_price * (1 - stop_loss_pct)
            take_profit = signal.entry_price * (1 + take_profit_pct)
        else:
            stop_loss = signal.entry_price * (1 + stop_loss_pct)
            take_profit = signal.entry_price * (1 - take_profit_pct)

        return Position(
            platform=signal.platform,
            trader_id=signal.trader_id,
            symbol=signal.symbol,
            side=signal.side,
            quantity=quantity,
            entry_price=signal.entry_price,
            stop_loss_price=stop_loss,
            take_profit_price=take_profit,
            opened_at=signal.timestamp,
        )
