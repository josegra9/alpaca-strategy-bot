import os
import alpaca_trade_api as tradeapi

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL, api_version="v2")

def place_order(symbol: str, qty: int):
    order = api.submit_order(
        symbol=symbol,
        qty=qty,
        side="buy",
        type="market",
        time_in_force="gtc"
    )
    return order._raw

def get_stock_price(symbol: str) -> float:
    latest_trade = api.get_latest_trade(symbol)
    return float(latest_trade.price)
