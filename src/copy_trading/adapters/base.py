from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, List

from ..models import TraderSnapshot, TradeSignal


class TopTraderAdapter(ABC):
    @abstractmethod
    def fetch_top_traders(self, limit: int = 10) -> List[TraderSnapshot]:
        raise NotImplementedError

    @abstractmethod
    def fetch_latest_signals(self, trader_ids: Iterable[str]) -> List[TradeSignal]:
        raise NotImplementedError
