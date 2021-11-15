import yfinance as yf
import pandas as pd
from typing import List

def get_dataframe(tickers: List[str], start_date: str, interval: str = "1d") -> pd.DataFrame:
    ticker_string = " ".join(tickers)

    data = yf.download(
        tickers = ticker_string,
        start=start_date,
        interval = interval,
        threads = True,
    )

    return data["Adj Close"]

def check_if_ticker_exists(ticker: str):
    response = yf.Ticker(ticker)

    if response.info['regularMarketPrice'] == None: return False
    
    return True
