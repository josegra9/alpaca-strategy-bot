import yfinance as yf
import pandas as pd
from datetime import date, timedelta

def prepare_data(ticker, years_back=5):
    end_date = date.today()
    start_date = end_date - timedelta(days=365 * years_back)

    # Fetch historical data
    df = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)
    
    if df.empty or 'Close' not in df.columns:
        raise ValueError("Downloaded data is empty or missing 'Close' column")

    df = df.reset_index()
    
    # Ensure numeric
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

    # Calculate indicators
    df['MA30'] = df['Close'].rolling(window=30, min_periods=1).mean()
    df['MA90'] = df['Close'].rolling(window=90, min_periods=1).mean()
    df['30DayHigh'] = df['Close'].rolling(window=30, min_periods=1).max()
    df['30DayLow'] = df['Close'].rolling(window=30, min_periods=1).min()

    # Compute drawdown safely
    highs = df['30DayHigh'].copy()
    drawdown_pct = ((df['Close'] - highs) / highs) * 100
    df['DrawdownPct'] = drawdown_pct

    # Drop any rows with critical NaNs
    df = df.dropna(subset=['Close', 'MA30', 'MA90', '30DayHigh', '30DayLow', 'DrawdownPct'])

    return df
