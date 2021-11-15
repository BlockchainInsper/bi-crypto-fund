from lib.repository.repository import TransactionRepository, AssetRepository
from lib.services.yahoo import get_dataframe
from datetime import datetime

def get_history_use_case(transaction_repository: TransactionRepository):
    history = transaction_repository.get_history()
    ticker_list = []

    for transaction in history:
        transaction["timestamp"] = datetime.fromtimestamp(transaction["timestamp"]).strftime("%Y-%m-%d")
        ticker_list.append(transaction["ticker"])
    
    df = get_dataframe(set(ticker_list), history[0]["timestamp"])

    return history
