from datetime import datetime, timezone
from typing import Iterable, List

from .base import TopTraderAdapter
from .http import JsonHttpClient
from ..models import TradeSignal, TraderSnapshot


class HyperliquidAdapter(TopTraderAdapter):
    """Adapter for Hyperliquid public API."""

    def __init__(self, http_client: JsonHttpClient | None = None):
        self.http = http_client or JsonHttpClient()
        self.info_url = "https://api.hyperliquid.xyz/info"

    def fetch_top_traders(self, limit: int = 10) -> List[TraderSnapshot]:
        payload = {"type": "leaderboard"}
        raw = self.http.request(self.info_url, method="POST", payload=payload)
        traders = []
        for row in raw[:limit]:
            traders.append(
                TraderSnapshot(
                    platform="hyperliquid",
                    trader_id=str(row.get("user")),
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
            payload = {"type": "userFills", "user": trader_id}
            raw = self.http.request(self.info_url, method="POST", payload=payload)
            if not raw:
                continue
            fill = raw[0]
            signals.append(
                TradeSignal(
                    platform="hyperliquid",
                    trader_id=trader_id,
                    symbol=fill.get("coin", "UNKNOWN"),
                    side=fill.get("side", "buy"),
                    entry_price=float(fill.get("px", 0.0)),
                    timestamp=datetime.now(timezone.utc),
                    conviction=1.0,
                )
            )
        return signals
