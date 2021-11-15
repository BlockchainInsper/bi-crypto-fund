from typing import List
from lib.domain.transaction import Transaction

def verify_weight_sum(transactions: List[Transaction]):
    weight_sum = sum([transaction.weight for transaction in transactions])

    return weight_sum <= 1

def verify_ids(transactions: List[Transaction]):
    list_of_ids = [transaction.asset_id for transaction in transactions]

    return len(list_of_ids) == len(set(list_of_ids))
