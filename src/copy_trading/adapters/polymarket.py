from datetime import datetime, timezone
from typing import Iterable, List

from .base import TopTraderAdapter
from .http import JsonHttpClient
from ..models import TradeSignal, TraderSnapshot


class PolymarketAdapter(TopTraderAdapter):
    """Adapter for Polymarket public data APIs."""

    def __init__(self, http_client: JsonHttpClient | None = None):
        self.http = http_client or JsonHttpClient()
        self.leaderboard_url = "https://data-api.polymarket.com/users"
        self.activity_url = "https://data-api.polymarket.com/activity"

    def fetch_top_traders(self, limit: int = 10) -> List[TraderSnapshot]:
        raw = self.http.request(f"{self.leaderboard_url}?limit={limit}&sort=volume")
        traders = []
        for row in raw[:limit]:
            traders.append(
                TraderSnapshot(
                    platform="polymarket",
                    trader_id=str(row.get("proxyWallet", "")),
                    pnl_30d=float(row.get("profit", 0.0)),
                    win_rate=float(row.get("winRate", 0.0)),
                    roi_30d=float(row.get("roi", 0.0)),
                    max_drawdown=float(row.get("maxDrawdown", 0.0)),
                )
            )
        return traders

    def fetch_latest_signals(self, trader_ids: Iterable[str]) -> List[TradeSignal]:
        signals: List[TradeSignal] = []
        for trader_id in trader_ids:
            raw = self.http.request(f"{self.activity_url}?user={trader_id}&limit=1")
            if not raw:
                continue
            row = raw[0]
            signals.append(
                TradeSignal(
                    platform="polymarket",
                    trader_id=trader_id,
                    symbol=row.get("market_slug", "UNKNOWN"),
                    side=row.get("side", "buy"),
                    entry_price=float(row.get("price", 0.0)),
                    timestamp=datetime.now(timezone.utc),
                )
            )
        return signals
