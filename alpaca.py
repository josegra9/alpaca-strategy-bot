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

def get_stock_price(symbol: str) -> float:
    req = StockLatestQuoteRequest(symbol_or_symbols=[symbol])
    latest = data_client.get_stock_latest_quote(req)
    quote = latest.get(symbol)
    if quote is None or quote.ask_price is None:
        raise RuntimeError(f"No latest quote for {symbol}")
    return float(quote.ask_price)

def place_order(symbol: str, qty: float):
    req = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY
    )
    order = trading_client.submit_order(order_data=req)
    return order.__dict__
