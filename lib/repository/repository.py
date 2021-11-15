from abc import ABC, abstractmethod
from typing import List

from lib.domain.transaction import Transaction
from lib.domain.asset import Asset


class TransactionRepository(ABC):
    
    @abstractmethod
    def get_history(self) -> List[Transaction]:
        pass

    @abstractmethod
    def create_transaction(self, transaction: Transaction) -> None:
        pass


class AssetRepository(ABC):

    @abstractmethod
    def get_assets(self) -> List[Asset]:
        pass

    @abstractmethod
    def create_asset(self, asset: Asset) -> None:
        pass
