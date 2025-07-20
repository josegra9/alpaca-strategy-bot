def should_buy(df):
    if len(df) < 2:
        return False, {}
    today = df.iloc[-1]
    yesterday = df.iloc[-2]
    if (
        today["MA30"] > today["MA90"] and
        yesterday["MA30"] <= yesterday["MA90"]
    ):
        return True, {
            "reason": "MA30 crossed above MA90",
            "price": today["Close"]
        }
    return False, {}
