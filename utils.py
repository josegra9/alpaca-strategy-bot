import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def prepare_data(ticker: str, years_back: int = 7) -> pd.DataFrame:
    try:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=years_back * 365)

        df = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)
        df.reset_index(inplace=True)

        if df.empty or "Close" not in df.columns:
            raise ValueError(f"Downloaded data is empty or missing 'Close' column for {ticker}")

        # Clean column names
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

        # Indicators
        df["MA30"] = df["Close"].rolling(30).mean()
        df["MA90"] = df["Close"].rolling(90).mean()
        df["30DayHigh"] = df["Close"].rolling(30).max()
        df["30DayLow"] = df["Close"].rolling(30).min()

        # ✅ Fix: Assign single column
        df["DrawdownPct"] = ((df["Close"] - df["30DayHigh"]) / df["30DayHigh"]) * 100

        df.dropna(inplace=True)

        return df

    except Exception as e:
        raise RuntimeError(f"Failed to fetch or prepare data: {e}")
