# API analysis for copy-trading targets

## 1) Hyperliquid
- **Primary API host**: `https://api.hyperliquid.xyz/info` (POST).
- Useful read-only payloads for this framework:
  - `{"type": "leaderboard"}` for top-ranked accounts.
  - `{"type": "userFills", "user": "<wallet>"}` for latest fills from a trader.
- Notes:
  - Returned field names can vary by endpoint version.
  - This bot treats leaderboard rank + recent fills as the source of copy signals.

## 2) Binance copy trading
- **Observed web API pattern** under `https://www.binance.com/bapi/futures/.../copy-trade/...`.
- Candidate endpoints used in this framework:
  - `/lead-portfolio/rank` for ranked lead traders.
  - `/lead-portfolio/trade-history` for latest lead trades.
- Notes:
  - Binance often changes these routes and may require browser auth/cookies.
  - The adapter is intentionally isolated so auth headers/cookies can be injected later.

## 3) Polymarket
- **Data API host**: `https://data-api.polymarket.com`.
- Candidate endpoints used in this framework:
  - `/users?limit=<n>&sort=volume` to surface active traders.
  - `/activity?user=<wallet>&limit=1` for latest activity to convert into copy signals.
- Notes:
  - For production, add secondary validation from CLOB/market APIs before execution.

## Trader selection policy in this repo
Top traders are selected per platform adapter with these criteria fields:
1. 30-day pnl
2. Win rate
3. ROI
4. Max drawdown (for filtering and later risk scoring)

## Risk and capital framework
- Capital split: **$10,000 per bot** (`hyperliquid`, `binance`, `polymarket`).
- Baseline risk config:
  - Risk per trade: 1%
  - Max open positions per platform: 10
  - Stop loss: 3%
  - Take profit: 6%
- Position sizing:
  - `size = (capital * risk_per_trade) / |entry - stop|`

## Fine-tuning and scale plan
1. Run each bot in paper mode for 2-4 weeks.
2. Track realized slippage vs leader fill price.
3. Remove traders that exceed drawdown or degrade consistency.
4. Tighten/loosen stop-loss by volatility bucket.
5. Scale capital gradually (e.g., +25% every stable review window).
