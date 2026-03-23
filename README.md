# copy_trading

Starter framework to copy top traders from:
- Hyperliquid
- Binance copy trading
- Polymarket

## What is implemented
- API adapter skeletons for top-trader discovery + latest trade signal fetch.
- Capital/risk configuration with default **$10,000 per bot**.
- Position sizing and stop-loss/take-profit position building.
- A `CopyTradingEngine` that runs one rebalance cycle per platform.

## Quick start
```bash
PYTHONPATH=src python -m copy_trading.main
```

## Layout
- `docs/api_analysis.md`: API findings + deployment/risk notes.
- `src/copy_trading/adapters/*`: Platform adapters.
- `src/copy_trading/risk.py`: Sizing + stop-loss management.
- `src/copy_trading/engine.py`: Orchestration.
- `tests/*`: basic unit tests.
