import streamlit as st
from datetime import date

st.set_page_config(page_title="Angel One Options Paper Desk", page_icon="📈", layout="centered")
st.title("📈 NIFTY / BANK NIFTY Paper Trading Desk")
st.caption("Mobile-friendly prototype • Paper trading only • No Angel One login or live orders")

st.warning("This prototype does NOT connect to live Angel One data. Enter verified market/option values manually. Never treat sample inputs as live prices.")

if "trades" not in st.session_state:
    st.session_state.trades = []
if "active" not in st.session_state:
    st.session_state.active = None
if "trade_date" not in st.session_state:
    st.session_state.trade_date = str(date.today())

if st.session_state.trade_date != str(date.today()):
    st.session_state.trade_date = str(date.today())
    st.session_state.trades = []
    st.session_state.active = None

CAPITAL = 20000.0
RISK_LIMIT = 750.0
MAX_TRADES = 3

st.subheader("1. Risk settings")
c1, c2 = st.columns(2)
c1.metric("Trading capital", "₹20,000")
c2.metric("Risk limit / trade", "₹750")
st.caption("One active position at a time • Maximum 3 entries per day • Premium buying only")

st.subheader("2. Market confirmation")
market = st.selectbox("Index", ["NIFTY", "BANK NIFTY"])
spot = st.number_input("Current index spot (enter from your broker)", min_value=0.0, value=0.0, step=1.0)
vwap = st.number_input("VWAP", min_value=0.0, value=0.0, step=1.0)
ema9 = st.number_input("EMA 9", min_value=0.0, value=0.0, step=1.0)
ema21 = st.number_input("EMA 21", min_value=0.0, value=0.0, step=1.0)
rsi = st.number_input("RSI (5-minute)", min_value=0.0, max_value=100.0, value=50.0, step=0.5)
breakout = st.selectbox("5-minute candle confirmation", [
    "No confirmed breakout/breakdown",
    "Closed above a pre-marked resistance",
    "Closed below a pre-marked support"
])

bull = spot > 0 and vwap > 0 and ema9 > 0 and ema21 > 0 and spot > vwap and ema9 > ema21 and rsi >= 55 and breakout == "Closed above a pre-marked resistance"
bear = spot > 0 and vwap > 0 and ema9 > 0 and ema21 > 0 and spot < vwap and ema9 < ema21 and rsi <= 45 and breakout == "Closed below a pre-marked support"

if bull:
    st.success("Bullish confirmation: CE setup eligible (not a prediction).")
elif bear:
    st.error("Bearish confirmation: PE setup eligible (not a prediction).")
else:
    st.info("No complete confirmation. The disciplined action is NO TRADE.")

st.subheader("3. Paper order ticket")
side = st.selectbox("Option side", ["CE", "PE"])
premium = st.number_input("Option entry premium (₹)", min_value=0.0, value=0.0, step=0.05)
lot_size = st.number_input("Current exchange lot size (verify before entry)", min_value=1, value=1, step=1)
lots = st.number_input("Number of lots", min_value=1, value=1, step=1)

sl_premium = premium * 0.80
risk_per_unit = premium - sl_premium
quantity = int(lot_size * lots)
planned_loss = risk_per_unit * quantity
premium_cost = premium * quantity
trades_today = len(st.session_state.trades)

st.write(f"Indicative stop premium (20%): ₹{sl_premium:.2f}")
st.write(f"Planned loss to stop: ₹{planned_loss:,.2f}")
st.write(f"Premium outlay: ₹{premium_cost:,.2f}")
st.write("Targets: T1 ₹{:.2f} (+30%) • T2 ₹{:.2f} (+50%)".format(premium * 1.30, premium * 1.50))

eligible_signal = (side == "CE" and bull) or (side == "PE" and bear)
if side == "CE" and bear:
    st.warning("Selected CE conflicts with bearish confirmation.")
if side == "PE" and bull:
    st.warning("Selected PE conflicts with bullish confirmation.")

can_enter = (
    st.session_state.active is None
    and trades_today < MAX_TRADES
    and premium > 0
    and eligible_signal
    and planned_loss <= RISK_LIMIT
    and premium_cost <= CAPITAL
)
if st.button("Open PAPER position", disabled=not can_enter, use_container_width=True):
    st.session_state.active = {
        "date": str(date.today()), "index": market, "side": side,
        "premium": premium, "quantity": quantity, "lot_size": lot_size,
        "stop": sl_premium, "target1": premium * 1.30,
        "target2": premium * 1.50, "planned_loss": planned_loss,
        "premium_cost": premium_cost
    }
    st.rerun()

if not can_enter:
    reasons = []
    if st.session_state.active is not None: reasons.append("An active position already exists")
    if trades_today >= MAX_TRADES: reasons.append("Daily limit of 3 entries reached")
    if premium <= 0: reasons.append("Enter an option premium")
    if not eligible_signal: reasons.append("Matching CE/PE confirmation is absent")
    if planned_loss > RISK_LIMIT: reasons.append("Planned loss exceeds ₹750")
    if premium_cost > CAPITAL: reasons.append("Premium outlay exceeds ₹20,000")
    if reasons:
        st.caption("Entry disabled: " + " • ".join(reasons))

st.subheader("4. Active paper position")
if st.session_state.active:
    p = st.session_state.active
    st.write(f"**{p['index']} {p['side']}** | Entry ₹{p['premium']:.2f} | Qty {p['quantity']}")
    current = st.number_input("Current option premium for paper exit (₹)", min_value=0.0, value=float(p["premium"]), step=0.05)
    pnl = (current - p["premium"]) * p["quantity"]
    st.metric("Unrealised paper P&L", f"₹{pnl:,.2f}")
    st.write(f"Stop ₹{p['stop']:.2f} • T1 ₹{p['target1']:.2f} • T2 ₹{p['target2']:.2f}")
    if current <= p["stop"]:
        st.error("Paper stop level reached. Review and close; this app does not auto-exit.")
    if st.button("Close PAPER position at entered premium", use_container_width=True):
        result = dict(p)
        result.update({"exit_premium": current, "pnl": pnl})
        st.session_state.trades.append(result)
        st.session_state.active = None
        st.rerun()
else:
    st.caption("No active paper position.")

st.subheader("5. Today's paper trade log")
st.write(f"Entries used: {len(st.session_state.trades)} / {MAX_TRADES}")
if st.session_state.trades:
    total = sum(t["pnl"] for t in st.session_state.trades)
    st.metric("Closed paper P&L", f"₹{total:,.2f}")
    st.dataframe([{
        "Index": t["index"], "Side": t["side"], "Entry": t["premium"],
        "Exit": t["exit_premium"], "Qty": t["quantity"], "P&L": round(t["pnl"], 2)
    } for t in st.session_state.trades], use_container_width=True)
else:
    st.caption("No closed paper trades yet.")

st.divider()
st.caption("Risk note: Option buyers can lose the entire premium. A stop level is not a guaranteed fill; gaps, volatility, liquidity, slippage and charges can increase losses. This tool is an educational simulator, not investment advice. Confirm current exchange lot sizes, contract details and broker rules independently.")
