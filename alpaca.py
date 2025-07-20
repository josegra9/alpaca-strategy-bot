import os
import alpaca_trade_api as tradeapi

# 🔐 Alpaca API credentials from environment variables
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

# 📡 Initialize Alpaca client
api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL, api_version="v2")

def place_order(symbol: str, qty: int):
    """
    Places a market buy order for the given stock symbol and quantity.
    """
    order = api.submit_order(
        symbol=symbol,
        qty=qty,
        side="buy",
        type="market",
        time_in_force="gtc"
    )
    return order._raw  # Return raw dictionary for easier JSON response

def get_stock_price(symbol: str) -> float:
    """
    Retrieves the latest trade price for the given stock symbol.
    """
    latest_trade = api.get_latest_trade(symbol)
    return float(latest_trade.price)
