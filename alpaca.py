import yfinance as yf

def place_order(symbol: str, qty: int):
    # Fake order simulation for now — Alpaca dependency removed
    return {
        "symbol": symbol,
        "qty": qty,
        "side": "buy",
        "type": "market",
        "status": "simulated"
    }

def get_stock_price(symbol: str) -> float:
    try:
        ticker = yf.Ticker(symbol)
        price = ticker.info.get("regularMarketPrice")
        if price is None:
            raise ValueError(f"No price found for {symbol}")
        return float(price)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch price for {symbol} from Yahoo Finance: {str(e)}")
