from dataclasses import dataclass, field


@dataclass
class BotConfig:
    platform: str
    capital_usd: float = 10_000.0
    max_traders_to_copy: int = 5
    risk_per_trade: float = 0.01
    max_open_positions: int = 10
    stop_loss_pct: float = 0.03
    take_profit_pct: float = 0.06


@dataclass
class GlobalConfig:
    hyperliquid: BotConfig = field(default_factory=lambda: BotConfig(platform="hyperliquid"))
    binance: BotConfig = field(default_factory=lambda: BotConfig(platform="binance"))
    polymarket: BotConfig = field(default_factory=lambda: BotConfig(platform="polymarket"))
