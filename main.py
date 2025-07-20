from flask import Flask, request, jsonify
from strategies import drawdown20, ma_crossover, time_dip_combo
from alpaca import place_order
import yfinance as yf
from utils import prepare_data
from datetime import datetime

app = Flask(__name__)

@app.route("/run_strategy", methods=["POST"])
def run_strategy():
    data = request.json
    ticker = data.get("ticker")
    strategy = data.get("strategy")
    quantity = int(data.get("quantity", 1))
    last_buy_date_str = data.get("last_buy_date")  # Optional

    if not ticker or not strategy:
        return jsonify({"error": "Missing required fields"}), 400

    df = prepare_data(ticker)

    trigger = False
    signal_info = {}

    if strategy == "Drawdown20":
        trigger, signal_info = drawdown20.should_buy(df)

    elif strategy == "MA_Crossover":
        trigger, signal_info = ma_crossover.should_buy(df)

    elif strategy == "TimeDipCombo":
        if not last_buy_date_str:
            return jsonify({"error": "last_buy_date required for TimeDipCombo"}), 400
        last_buy_date = datetime.strptime(last_buy_date_str, "%Y-%m-%d")
        trigger, signal_info = time_dip_combo.should_buy(df, last_buy_date)

    else:
        return jsonify({"error": "Unknown strategy"}), 400

    if trigger:
        order = place_order(ticker, quantity)
        return jsonify({
            "status": "BUY PLACED",
            "signal": signal_info,
            "order": order
        })

    return jsonify({
        "status": "No signal",
        "strategy": strategy,
        "ticker": ticker
    })

if __name__ == "__main__":
    app.run()
