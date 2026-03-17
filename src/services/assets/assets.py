from src.services.base import BaseService
from src.services.assets.assets_models import AssetModel, AssetCollection, AssetEventCollection

class AssetsRequestBuilder(BaseService):
    def list_request(self, limit: int = 100, offset: int = 0):
        return self._construct_request("GET", "assets", params={"limit": limit, "offset": offset})

    def get_request(self, asset_id: int):
        return self._construct_request("GET", f"assets/{asset_id}")

    def events_request(self, limit: int = 100, offset: int = 0):
        return self._construct_request("GET", "assets/events", params={"limit": limit, "offset": offset})

class AssetsAPI(AssetsRequestBuilder):
    def __init__(self, client):
        self.client = client

    def list(self, limit: int = 100, offset: int = 0) -> AssetCollection:
        raw_response = self.client.request(**self.list_request(limit, offset))
        return AssetCollection(**raw_response)

    def get(self, asset_id: int) -> AssetModel:
        raw_response = self.client.request(**self.get_request(asset_id))
        return AssetModel(**raw_response)

    def events(self, limit: int = 100, offset: int = 0) -> AssetEventCollection:
        raw_response = self.client.request(**self.events_request(limit, offset))
        return AssetEventCollection(**raw_response)


class AsyncAssetsAPI(AssetsRequestBuilder):
    def __init__(self, client):
        self.client = client

    async def list(self, limit: int = 100, offset: int = 0) -> AssetCollection:
        raw_response = await self.client.request(**self.list_request(limit, offset))
        return AssetCollection(**raw_response)

    async def get(self, asset_id: int) -> AssetModel:
        raw_response = await self.client.request(**self.get_request(asset_id))
        return AssetModel(**raw_response)

    async def events(self, limit: int = 100, offset: int = 0) -> AssetEventCollection:
        raw_response = await self.client.request(**self.events_request(limit, offset))
        return AssetEventCollection(**raw_response)
