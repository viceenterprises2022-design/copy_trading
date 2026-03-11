from .adapters.binance import BinanceAdapter
from .adapters.hyperliquid import HyperliquidAdapter
from .adapters.polymarket import PolymarketAdapter
from .config import GlobalConfig
from .engine import CopyTradingEngine


def build_engine() -> CopyTradingEngine:
    cfg = GlobalConfig()
    return CopyTradingEngine(
        adapters={
            "hyperliquid": HyperliquidAdapter(),
            "binance": BinanceAdapter(),
            "polymarket": PolymarketAdapter(),
        },
        configs={
            "hyperliquid": cfg.hyperliquid,
            "binance": cfg.binance,
            "polymarket": cfg.polymarket,
        },
    )


def run_once() -> None:
    engine = build_engine()
    for platform in ["hyperliquid", "binance", "polymarket"]:
        try:
            positions = engine.rebalance_once(platform)
            print(f"[{platform}] opened {len(positions)} new copied positions")
        except Exception as exc:  # noqa: BLE001 - top-level observability for dry-runs
            print(f"[{platform}] run failed: {exc}")


if __name__ == "__main__":
    run_once()
