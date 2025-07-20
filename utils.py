import yfinance as yf
import pandas as pd
from datetime import date, timedelta

def prepare_data(ticker: str, years_back: int = 5) -> pd.DataFrame:
    end_date = date.today()
    start_date = end_date - timedelta(days=365 * years_back)

    df = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)

    if df.empty or 'Close' not in df.columns:
        raise ValueError(f"Downloaded data is empty or missing 'Close' column for {ticker}")

    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])

    # Drop any rows with NaNs in critical columns
    df = df[['Date', 'Close']].copy()
    df['MA30'] = df['Close'].rolling(30).mean()
    df['MA90'] = df['Close'].rolling(90).mean()
    df['30DayHigh'] = df['Close'].rolling(30).max()
    df['30DayLow'] = df['Close'].rolling(30).min()
    df['DrawdownPct'] = (df['Close'] - df['30DayHigh']) / df['30DayHigh'] * 100

    df = df.dropna(subset=['Close', 'MA30', 'MA90', '30DayHigh', '30DayLow', 'DrawdownPct'])

    return df
