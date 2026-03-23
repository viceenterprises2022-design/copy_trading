from datetime import datetime, timezone
from typing import Iterable, List

from .base import TopTraderAdapter
from .http import JsonHttpClient
from ..models import TradeSignal, TraderSnapshot


class BinanceAdapter(TopTraderAdapter):
    """Adapter for Binance copy trading discovery endpoints.

    NOTE: Binance changes these endpoints frequently and may require auth cookies.
    Keep URLs configurable in production.
    """

    def __init__(self, http_client: JsonHttpClient | None = None):
        self.http = http_client or JsonHttpClient()
        self.leaderboard_url = "https://www.binance.com/bapi/futures/v1/friendly/future/copy-trade/lead-portfolio/rank"
        self.positions_url = "https://www.binance.com/bapi/futures/v1/friendly/future/copy-trade/lead-portfolio/trade-history"

    def fetch_top_traders(self, limit: int = 10) -> List[TraderSnapshot]:
        payload = {"pageNumber": 1, "pageSize": limit, "timeRange": "30D"}
        raw = self.http.request(self.leaderboard_url, method="POST", payload=payload)
        rows = raw.get("data", []) if isinstance(raw, dict) else []
        traders = []
        for row in rows[:limit]:
            traders.append(
                TraderSnapshot(
                    platform="binance",
                    trader_id=str(row.get("leadPortfolioId", "")),
                    pnl_30d=float(row.get("pnl", 0.0)),
                    win_rate=float(row.get("winRate", 0.0)),
                    roi_30d=float(row.get("roi", 0.0)),
                    max_drawdown=float(row.get("maxDrawdown", 0.0)),
                )
            )
        return traders

    def fetch_latest_signals(self, trader_ids: Iterable[str]) -> List[TradeSignal]:
        signals: List[TradeSignal] = []
        for trader_id in trader_ids:
            payload = {"leadPortfolioId": trader_id, "pageNumber": 1, "pageSize": 1}
            raw = self.http.request(self.positions_url, method="POST", payload=payload)
            rows = raw.get("data", []) if isinstance(raw, dict) else []
            if not rows:
                continue
            row = rows[0]
            signals.append(
                TradeSignal(
                    platform="binance",
                    trader_id=trader_id,
                    symbol=row.get("symbol", "UNKNOWN"),
                    side=row.get("side", "BUY").lower(),
                    entry_price=float(row.get("price", 0.0)),
                    timestamp=datetime.now(timezone.utc),
                )
            )
        return signals
