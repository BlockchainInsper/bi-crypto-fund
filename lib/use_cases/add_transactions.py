from lib.domain.transaction import Transaction
from lib.repository.repository import TransactionRepository
from lib.use_cases.utils import verify_weight_sum, verify_ids
from typing import List

def add_transactions_use_case(transactions: List[Transaction], repository: TransactionRepository):
    assert verify_weight_sum(transactions), "Weight sum is larger than 1"
    assert verify_ids(transactions), "Same assets inside transactions"

    for transaction in transactions:
        repository.create_transaction(transaction)