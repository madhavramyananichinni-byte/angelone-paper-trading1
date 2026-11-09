# Angel One Mobile Paper Trading Prototype

## Run on Replit from Android
1. Open https://replit.com/ in Chrome and sign in.
2. Create a new **Python** Repl.
3. In the file panel, replace `main.py` with the contents of `app.py` (or upload `app.py` and set the run command).
4. Add `requirements.txt` with the supplied contents.
5. In the Shell, run: `pip install -r requirements.txt`
6. Run: `streamlit run app.py --server.port 3000 --server.address 0.0.0.0`
7. Open the web preview. If Replit asks for a port, use 3000.

## What this prototype does
- Mobile-friendly manual paper-trading ticket for NIFTY and BANK NIFTY CE/PE.
- Requires a matching manually entered confirmation: spot vs VWAP, EMA 9/21, RSI, and 5-minute breakout/breakdown.
- Uses a 20% premium stop reference, 30% and 50% target references.
- Enforces ₹750 planned risk, ₹20,000 premium outlay, one open paper position, and at most 3 closed/entered trades per day.

## Important limitations
- No Angel One credentials or API key are used.
- No live prices, option chain, live signals, or broker orders are connected.
- Enter verified current values manually. This is not a backtest and does not guarantee stop execution.
- The current exchange lot size must be checked and entered manually; do not assume it is unchanged.
- Keep this in paper mode until the logic is tested. Do not paste PIN, TOTP, password, API secret, or access tokens into chat or source code.

## Next phase
After SmartAPI registration and review of current Angel One API permissions, add server-side authentication and market-data integration. Never expose credentials in browser-side code. Use Replit Secrets for server-side credentials.
