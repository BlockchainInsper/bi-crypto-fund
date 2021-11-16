from lib.repository.repository import TransactionRepository, AssetRepository
from lib.use_cases.get_history import get_history_use_case
from lib.use_cases.get_assets import get_assets_use_case
from lib.services.yahoo import get_metrics
import numpy as np

def get_fund_info_use_case(transaction_repository: TransactionRepository, asset_repository: AssetRepository):
    history = get_history_use_case(transaction_repository)[1:]
    metrics = get_metrics()

    metrics["Bitcoin Daily Return"] = metrics["BTC-USD"].pct_change()
    metrics["Bitcoin Cum Return"] = (1 + metrics["Bitcoin Daily Return"]).cumprod() - 1

    metrics["SP500 Daily Return"] = metrics["^GSPC"].pct_change()
    metrics["SP500 Cum Return"] = (1 + metrics["SP500 Daily Return"]).cumprod() - 1

    response = { 
        "chart_data": [
            {
                "id": "Fundo BI",
                "data": []
            },
            {
                "id": "Bitcoin",
                "data": []
            },
            {
                "id": "S&P500",
                "data": []
            }
        ],
        "cumulative_return": 0,
        "annualized_return": 0,
        "six_month_return": 0,
        "number_of_assets": 0
    }

    for index, value in history.items():
        response["chart_data"][0]["data"].append({
            "x": index.strftime('%Y-%m-%d'),
            "y": value * 100
        })
    
    for index, value in metrics["Bitcoin Cum Return"][1:].items():
        response["chart_data"][1]["data"].append({
            "x": index.strftime('%Y-%m-%d'),
            "y": value * 100
        })
    
    for index, value in metrics["SP500 Cum Return"][1:].items():
        response["chart_data"][2]["data"].append({
            "x": index.strftime('%Y-%m-%d'),
            "y": value * 100
        })
    
    response["cumulative_return"] = f"{history[-1] * 100:.2f}%"
    response["annualized_return"] = f"{(history[-1] / len(history)) * 36500:.2f}%"
    response["number_of_assets"] = len(get_assets_use_case(asset_repository))   
    
    return response
