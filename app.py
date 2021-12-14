import json
import flask
import os
import time
import threading
import pymongo
import jwt
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from functools import wraps

from lib.domain.asset import Asset
from lib.domain.transaction import Transaction
from lib.repository.memory import MemoryAssetRepository, MemoryTransactionRepository
from lib.repository.mongo import MongoAssetRepository, MongoTransactionRepository, MongoUserRepository
from lib.use_cases.get_history import get_history_use_case
from lib.use_cases.get_assets import get_assets_use_case
from lib.use_cases.add_asset import add_asset_use_case
from lib.use_cases.get_fund_info import get_fund_info_use_case
from lib.use_cases.add_transactions import add_transactions_use_case
from lib.use_cases.authenticate_user import authenticate_user_use_case

app = Flask(__name__)
CORS(app)

client = pymongo.MongoClient(os.environ.get("MONGO_URL")).FundoBI
asset_repository = MongoAssetRepository(client)
transactions_repository = MongoTransactionRepository(client)
user_repository = MongoUserRepository(client)


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if not 'Authorization' in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = str.replace(str(data), 'Bearer ','')
        try:
            user_id = jwt.decode(token, os.environ.get("SECRET_KEY", "myprecious"))["sub"]
        except:
            abort(401)

        return f(user_id, *args, **kws)            
    return decorated_function

# Authenticate User
@app.route('/auth', methods=['POST'])
def authenticate_user():
    data = flask.request.get_json()

    response_data, response_status = authenticate_user_use_case(data["username"], data["password"], user_repository)
    
    return jsonify(response_data), response_status

# Retrieve information used in website
@app.route('/', methods=['GET'])
def display_fund_info():
    fund_info = get_fund_info_use_case(transactions_repository, asset_repository)
    response = {"fund_info": fund_info}
    
    return jsonify(response), 200

# Retrieve raw information from fund 
@app.route('/raw', methods=['GET'])
def display_history():
    history = get_history_use_case(transactions_repository)
    response = {"history": history.to_json(), "length": len(history)}
    
    return jsonify(response), 200

# Retrieve list of registered assets 
@app.route('/assets/list', methods=['GET'])
@authorize
def display_assets(user_id):
    assets = get_assets_use_case(asset_repository)
    response = {"assets": assets, "length": len(assets)}
    
    return jsonify(response), 200

# Add a new asset
@app.route('/assets', methods=['POST'])
@authorize
def add_asset(user_id):
    asset = flask.request.get_json()

    new_asset = Asset(
        asset["name"],
        asset["ticker"],
        user_id
    )

    try:
        add_asset_use_case(new_asset, asset_repository)
    except AssertionError as error:
        return f"Something went wrong\n{error}", 500

    return jsonify(new_asset.to_dict()), 200

# Add a new transaction
@app.route('/transactions', methods=['POST'])
@authorize
def add_transactions(user_id):
    transactions = flask.request.get_json()["transactions"]

    new_transactions = [Transaction(transaction["asset_id"], transaction["weight"], int(time.time()), user_id) for transaction in transactions]

    try:
        add_transactions_use_case(new_transactions, transactions_repository, asset_repository)
    except AssertionError as error:
        return f"Something went wrong\n{error}", 500

    return jsonify([transaction.to_dict() for transaction in new_transactions]), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # Local
    # app.run(host='127.0.0.1', port=port, debug=True)
