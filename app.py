import json
import flask
import os
import time
import threading
import pymongo
from flask import Flask, jsonify

from lib.domain.asset import Asset
from lib.domain.transaction import Transaction
from lib.repository.memory import MemoryAssetRepository, MemoryTransactionRepository
from lib.repository.mongo import MongoAssetRepository, MongoTransactionRepository
from lib.use_cases.get_history import get_history_use_case
from lib.use_cases.get_assets import get_assets_use_case
from lib.use_cases.add_asset import add_asset_use_case
from lib.use_cases.add_transactions import add_transactions_use_case

app = Flask(__name__)

client = pymongo.MongoClient("").FundoBI
asset_repository = MongoAssetRepository(client)
transactions_repository = MongoTransactionRepository(client)

@app.route('/', methods=['GET'])
def display_history():
    history = get_history_use_case(transactions_repository)
    response = {"history": history, "length": len(history)}
    
    return jsonify(response), 200

@app.route('/assets/list', methods=['GET'])
def display_assets():
    assets = get_assets_use_case(asset_repository)
    response = {"assets": assets, "length": len(assets)}
    
    return jsonify(response), 200

@app.route('/assets', methods=['POST'])
def add_asset():
    asset = flask.request.get_json()

    new_asset = Asset(
        asset["name"],
        asset["ticker"]
    )

    try:
        add_asset_use_case(new_asset, asset_repository)
    except AssertionError as error:
        return f"Something went wrong\n{error}", 500

    return "Asset added", 200

@app.route('/transactions', methods=['POST'])
def add_transactions():
    transactions = flask.request.get_json()["transactions"]

    new_transactions = [Transaction(transaction["asset_id"], transaction["weight"], int(time.time())) for transaction in transactions]

    try:
        add_transactions_use_case(new_transactions, transactions_repository, asset_repository)
    except AssertionError as error:
        return f"Something went wrong\n{error}", 500

    return "Transactions added", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    # Local
    app.run(host='127.0.0.1', port=port, debug=True)
