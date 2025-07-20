def should_buy(df, last_buy_date):
    latest = df.iloc[-1]
    if latest["DrawdownPct"] <= -25:
        if (latest["Date"] - last_buy_date).days >= 180:
            return True, {
                "reason": "Drawdown <= -25% and 180 days since last buy",
                "price": latest["Close"]
            }
    return False, {}
