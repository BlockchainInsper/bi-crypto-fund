from lib.repository.repository import TransactionRepository, AssetRepository

def get_assets_use_case(asset_repository: AssetRepository):
    return asset_repository.get_assets()
