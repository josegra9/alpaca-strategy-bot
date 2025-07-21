import os
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

# 🛠️ Replace with your keys
API_KEY = os.getenv("ALPACA_API_KEY")
SECRET = os.getenv("ALPACA_SECRET")

# Market Data
data_client = StockHistoricalDataClient(API_KEY, SECRET)

# Trading
trading_client = TradingClient(API_KEY, SECRET, paper=True)

import os
import requests

def get_stock_price(symbol: str) -> float:
    try:
        base_url = "https://data.alpaca.markets/v2/stocks"
        endpoint = f"{base_url}/{symbol}/quotes/latest"
        headers = {
            "APCA-API-KEY-ID": os.getenv("ALPACA_API_KEY"),
            "APCA-API-SECRET-KEY": os.getenv("ALPACA_SECRET")
        }

        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()

        data = response.json()
        price = data["quote"]["ap"]
        return float(price)

    except Exception as e:
        raise RuntimeError(f"Failed to fetch price from Alpaca: {e}")


def place_order(symbol: str, qty: float):
    req = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY
    )
    order = trading_client.submit_order(order_data=req)
    return order.__dict__
