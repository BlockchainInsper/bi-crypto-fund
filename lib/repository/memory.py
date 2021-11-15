from typing import List

from lib.domain.transaction import Transaction
from lib.domain.asset import Asset
from lib.repository.repository import TransactionRepository, AssetRepository


class MemoryTransactionRepository(TransactionRepository):
    def __init__(self):
        self.history = []
    
    def get_history(self) -> List[Transaction]:
        return [Transaction.from_dict(i) for i in self.history]

    def create_transaction(self, transaction: Transaction) -> None:
        self.history.append(transaction.to_dict())

class MemoryAssetRepository(AssetRepository):
    def __init__(self):
        self.assets = []
    
    def create_asset(self, asset: Asset) -> None:
        self.assets.append(asset.to_dict())
    
    def get_asset_from_id(self, id: int) -> Asset:
        return self.assets[id]
