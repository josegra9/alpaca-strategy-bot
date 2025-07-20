def should_buy(df):
    latest = df.iloc[-1]
    if latest["DrawdownPct"] <= -20:
        return True, {
            "reason": "Drawdown <= -20%",
            "price": latest["Close"]
        }
    return False, {}
