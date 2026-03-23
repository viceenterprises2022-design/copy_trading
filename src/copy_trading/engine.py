from dataclasses import dataclass, field
from typing import Dict, List

from .adapters.base import TopTraderAdapter
from .config import BotConfig
from .models import Position
from .risk import PositionSizer, StopLossManager


@dataclass
class BotState:
    config: BotConfig
    positions: List[Position] = field(default_factory=list)


class CopyTradingEngine:
    def __init__(self, adapters: Dict[str, TopTraderAdapter], configs: Dict[str, BotConfig]):
        self.adapters = adapters
        self.states = {name: BotState(config=cfg) for name, cfg in configs.items()}

    def rebalance_once(self, platform: str) -> List[Position]:
        state = self.states[platform]
        adapter = self.adapters[platform]

        top_traders = adapter.fetch_top_traders(limit=state.config.max_traders_to_copy)
        trader_ids = [t.trader_id for t in top_traders]
        signals = adapter.fetch_latest_signals(trader_ids)

        new_positions: List[Position] = []
        for signal in signals:
            if len(state.positions) + len(new_positions) >= state.config.max_open_positions:
                break

            dummy_stop = signal.entry_price * (1 - state.config.stop_loss_pct)
            qty = PositionSizer.size_position(
                capital_usd=state.config.capital_usd,
                risk_per_trade=state.config.risk_per_trade,
                entry_price=signal.entry_price,
                stop_loss_price=dummy_stop,
            )
            new_positions.append(
                StopLossManager.build_position(
                    signal,
                    quantity=qty,
                    stop_loss_pct=state.config.stop_loss_pct,
                    take_profit_pct=state.config.take_profit_pct,
                )
            )

        state.positions.extend(new_positions)
        return new_positions
