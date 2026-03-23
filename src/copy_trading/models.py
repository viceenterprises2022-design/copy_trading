from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class TraderSnapshot:
    platform: str
    trader_id: str
    pnl_30d: float
    win_rate: float
    roi_30d: float
    max_drawdown: float


@dataclass(frozen=True)
class TradeSignal:
    platform: str
    trader_id: str
    symbol: str
    side: str
    entry_price: float
    timestamp: datetime
    conviction: float = 1.0


@dataclass
class Position:
    platform: str
    trader_id: str
    symbol: str
    side: str
    quantity: float
    entry_price: float
    stop_loss_price: float
    take_profit_price: Optional[float] = None
    opened_at: Optional[datetime] = None
