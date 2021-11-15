from lib.domain.asset import Asset
from lib.services.yahoo import check_if_ticker_exists
from lib.repository.repository import AssetRepository

def add_asset_use_case(asset: Asset, repository: AssetRepository):
    assert check_if_ticker_exists(asset.ticker), "Ticker is invalid"
    
    repository.create_asset(asset)
