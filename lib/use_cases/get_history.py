from lib.repository.repository import TransactionRepository
from lib.services.yahoo import get_dataframe
from datetime import datetime
import numpy as np
import pandas as pd

def get_history_use_case(transaction_repository: TransactionRepository) -> pd.Series:
    history = transaction_repository.get_history()
    ticker_list = list(set([transaction["ticker"] for transaction in history]))
    ticker_weight_list = []
    ticker_change_list = []
    ticker_impact_list = []

    df = get_dataframe(ticker_list, datetime.fromtimestamp(history[0]["timestamp"]))

    for ticker in ticker_list:
        ticker_weight = f"{ticker} Weight"
        ticker_change = f"{ticker} Pct Change"
        ticker_impact = f"{ticker} impact"
        
        ticker_weight_list.append(ticker_weight)
        ticker_change_list.append(ticker_change)
        ticker_impact_list.append(ticker_impact)

        df[ticker_weight] = np.nan
        df[ticker_change] = np.nan
        df[ticker_impact] = np.nan
        
    for transaction in history:
        ticker_name = transaction["ticker"]
        row_name = datetime.fromtimestamp(transaction["timestamp"]).strftime("%Y-%m-%d")
        column_name = f"{ticker_name} Weight"
        df.loc[row_name, column_name] = transaction["weight"]

    df = df.fillna(method="ffill")
    df = df.fillna(0)

    df["Linear Daily Return"] = 1

    for ticker, ticker_change, ticker_weight, ticker_impact in zip(ticker_list, ticker_change_list, ticker_weight_list, ticker_impact_list):
        df[ticker_change] = df[ticker].pct_change()
        df[ticker_weight] = df[ticker_weight].shift(1)
        df[ticker_impact] = (df[ticker_change])*df[ticker_weight]
        df["Linear Daily Return"] += df[ticker_impact]

    df["Cumulative Daily Return"] = df["Linear Daily Return"].cumprod() - 1

    return df["Cumulative Daily Return"]
