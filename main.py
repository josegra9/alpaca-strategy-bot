from flask import Flask, request, jsonify
from strategies import drawdown20, ma_crossover, time_dip_combo
from alpaca import place_order, get_stock_price
from utils import prepare_data
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/run_strategy", methods=["POST"])
def run_strategy():
    data = request.json
    ticker = data.get("ticker")
    strategy = data.get("strategy")
    quantity = int(data.get("quantity", 1))
    last_buy_date_str = data.get("last_buy_date")  # Optional

    # 🧪 Debug incoming request
    print("📥 Incoming request:")
    print(f"  Ticker: {ticker}")
    print(f"  Strategy: {strategy}")
    print(f"  Quantity: {quantity}")
    if last_buy_date_str:
        print(f"  Last Buy Date: {last_buy_date_str}")

    if not ticker or not strategy:
        return jsonify({"error": "Missing required fields: ticker and strategy"}), 400

    try:
        df = prepare_data(ticker)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch or prepare data: {str(e)}"}), 500

    # Pull live price from Alpaca
    try:
        live_price = get_stock_price(ticker)
    except Exception as e:
        return jsonify({"error": f"Failed to get price from Alpaca: {str(e)}"}), 500

    latest_row = df.iloc[-1]
    fallback_signal = {
        "date": str(latest_row["Date"].date()),
        "price": float(live_price)
    }

    trigger = False
    signal_info = {}

    try:
        if strategy == "Drawdown20":
            trigger, signal_info = drawdown20.should_buy(df)
        elif strategy == "MA_Crossover":
            trigger, signal_info = ma_crossover.should_buy(df)
        elif strategy == "TimeDipCombo":
            if not last_buy_date_str:
                return jsonify({"error": "last_buy_date is required for TimeDipCombo"}), 400
            last_buy_date = datetime.strptime(last_buy_date_str, "%Y-%m-%d")
            trigger, signal_info = time_dip_combo.should_buy(df, last_buy_date)
        else:
            return jsonify({"error": f"Unknown strategy: {strategy}"}), 400

        # Fallback to Alpaca price if strategy doesn't return price
        if not signal_info:
            signal_info = fallback_signal
        elif "price" not in signal_info:
            signal_info["price"] = float(live_price)

        print("📈 Strategy signal evaluation:")
        print(f"  Trigger: {trigger}")
        print(f"  Signal Info: {signal_info}")

        if trigger:
            order = place_order(ticker, quantity)
            print("✅ Order placed:", order)
            return jsonify({
                "status": "BUY PLACED",
                "strategy": strategy,
                "ticker": ticker,
                "signal": signal_info,
                "order": order
            })

        return jsonify({
            "status": "No signal",
            "strategy": strategy,
            "ticker": ticker,
            "signal": signal_info
        })

    except Exception as e:
        return jsonify({"error": f"Strategy evaluation failed: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "Strategy API live"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
