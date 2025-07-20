import yfinance as yf
import pandas as pd

def prepare_data(ticker):
    df = yf.download(ticker, period="6mo", auto_adjust=True, progress=False)
    df = df.reset_index()
    df["MA30"] = df["Close"].rolling(30).mean()
    df["MA90"] = df["Close"].rolling(90).mean()
    df["30DayHigh"] = df["Close"].rolling(30).max()
    df["DrawdownPct"] = (df["Close"] - df["30DayHigh"]) / df["30DayHigh"] * 100
    return df.dropna()
