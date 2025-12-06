//@version=5
strategy("BTCUSDT Pro Strategy Clean", overlay=true, initial_capital=10000, commission_type=strategy.commission.percent, commission_value=0.04)

// Inputs
useLong  = input.bool(true,  title="Enable LONG Trades")
useShort = input.bool(true,  title="Enable SHORT Trades")
qty      = input.float(0.5, "Trade Quantity (BTC)", step=0.1)

tpPerc    = input.float(1.5, "Take Profit %", step=0.1)
slPerc    = input.float(0.8, "Stop Loss %", step=0.1)
trailPerc = input.float(0.6, "Trailing Stop %", step=0.1)

// Indicators
ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
rsi   = ta.rsi(close, 14)

plot(ema20, "EMA20", color=color.green)
plot(ema50, "EMA50", color=color.red)

// Conditions
longCondition  = ema20 > ema50 and rsi > 50 and ta.crossover(close, ema20)
shortCondition = ema20 < ema50 and rsi < 50 and ta.crossunder(close, ema20)

// LONG ENTRY
if (longCondition and useLong)
    strategy.entry("BUY", strategy.long, qty)

// LONG EXIT with TP, SL, Trailing
if (strategy.position_size > 0)
    long_sl  = strategy.position_avg_price * (1 - slPerc/100)
    long_tp  = strategy.position_avg_price * (1 + tpPerc/100)
    trail_offset = strategy.position_avg_price * (trailPerc/100)
    strategy.exit("LONG EXIT", "BUY", stop=long_sl, limit=long_tp, trail_offset=trail_offset)

// SHORT ENTRY
if (shortCondition and useShort)
    strategy.entry("SELL", strategy.short, qty)

// SHORT EXIT with TP, SL, Trailing
if (strategy.position_size < 0)
    short_sl = strategy.position_avg_price * (1 + slPerc/100)
    short_tp = strategy.position_avg_price * (1 - tpPerc/100)
    trail_offset = strategy.position_avg_price * (trailPerc/100)
    strategy.exit("SHORT EXIT", "SELL", stop=short_sl, limit=short_tp, trail_offset=trail_offset)

// Alerts
alertcondition(longCondition,  title="BUY Alert",  message="BTCUSDT BUY Signal!")
alertcondition(shortCondition, title="SELL Alert", message="BTCUSDT SELL Signal!")
