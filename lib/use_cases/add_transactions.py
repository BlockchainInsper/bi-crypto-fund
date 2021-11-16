from lib.domain.transaction import Transaction
from lib.repository.repository import TransactionRepository, AssetRepository
from lib.use_cases.utils import verify_weight_sum, verify_ids
from lib.use_cases.get_assets import get_assets_use_case
from typing import List
import time

def add_transactions_use_case(transactions: List[Transaction], transaction_repository: TransactionRepository, asset_repository: AssetRepository):
    assert verify_weight_sum(transactions), "Weight sum is larger than 1"
    assert verify_ids(transactions), "Same assets inside transactions"

    all_assets = get_assets_use_case(asset_repository)
    daily_assets = []

    for transaction in transactions:
        transaction_repository.create_transaction(transaction)
        daily_assets.append(transaction.asset_id)
    
    for asset in all_assets:
        if asset["_id"]["$oid"] not in daily_assets:
            transaction = Transaction(asset["_id"]["$oid"], 0, int(time.time()))
            transaction_repository.create_transaction(transaction)
