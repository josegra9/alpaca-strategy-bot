from flask import Flask, request, jsonify
from strategies import drawdown20, ma_crossover, time_dip_combo
from alpaca import place_order
from utils import prepare_data
from datetime import datetime

app = Flask(__name__)

# === Health check route ===
@app.route("/", methods=["GET"])
def index():
    return "✅ Alpaca Strategy Bot is Live", 200

# === Strategy execution endpoint ===
@app.route("/run_strategy", methods=["POST"])
def run_strategy():
    data = request.json
    ticker = data.get("ticker")
    strategy = data.get("strategy")
    quantity = int(data.get("quantity", 1))
    last_buy_date_str = data.get("last_buy_date")  # Optional for TimeDipCombo

    if not ticker or not strategy:
        return jsonify({"error": "Missing required fields: ticker or strategy"}), 400

    try:
        df = prepare_data(ticker)
    except Exception as e:
        return jsonify({"error": f"Data fetch failed: {str(e)}"}), 500

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
            return jsonify({"error": "Unknown strategy"}), 400

    except Exception as e:
        return jsonify({"error": f"Strategy error: {str(e)}"}), 500

    if trigger:
        try:
            order = place_order(ticker, quantity)
            return jsonify({
                "status": "BUY PLACED",
                "signal": signal_info,
                "order": order
            }), 200
        except Exception as e:
            return jsonify({"error": f"Order placement failed: {str(e)}"}), 500

    return jsonify({
        "status": "No signal",
        "strategy": strategy,
        "ticker": ticker
    }), 200

# === Ensure server runs correctly on Render ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
