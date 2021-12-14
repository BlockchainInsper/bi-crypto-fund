from typing import List
import pymongo
import os
import json
from bson.objectid import ObjectId
from bson.json_util import dumps

from lib.domain.transaction import Transaction
from lib.domain.asset import Asset
from lib.domain.user import User
from lib.repository.repository import TransactionRepository, AssetRepository, UserRepository


class MongoTransactionRepository(TransactionRepository):
    def __init__(self, client):
        self.client = client.transactions
    
    def get_history(self) -> List[Transaction]:
        pipeline = [
            {"$lookup": { "from": "assets", "localField": "asset_id", "foreignField": "_id", "as": "asset_info" }},
            {"$unwind": "$asset_info" },
            {"$project": { "name": "$asset_info.name", "ticker": "$asset_info.ticker", "weight": 1, "timestamp": 1, "_id": 0 }},
            {"$sort": { "date": 1 } },
        ]

        history = list(self.client.aggregate(pipeline))

        return json.loads(dumps(history))

    def create_transaction(self, transaction: Transaction) -> None:
        transaction_serialized = transaction.to_dict()
        transaction_serialized["asset_id"] = ObjectId(transaction_serialized["asset_id"])
        transaction_serialized["added_by"] = ObjectId(transaction_serialized["added_by"])

        self.client.insert_one(transaction_serialized)

class MongoAssetRepository(AssetRepository):
    def __init__(self, client):
        self.client = client.assets

    def get_assets(self) -> List[Asset]:
        assets = self.client.find({})
        return json.loads(dumps(assets))
    
    def create_asset(self, asset: Asset) -> None:
        asset_serialized = asset.to_dict()
        asset_serialized["added_by"] = ObjectId(asset_serialized["added_by"])

        self.client.insert_one(asset_serialized)
    
class MongoUserRepository(UserRepository):
    def __init__(self, client):
        self.client = client.users
    
    def get_user_by_username(self, username: str) -> User:
        query = { "username": username }

        return json.loads(dumps(self.client.find_one(query)))
