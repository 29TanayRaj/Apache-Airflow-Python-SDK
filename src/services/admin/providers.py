from src.services.base import BaseService
from src.services.admin.admin_models import ProviderCollection

class ProvidersRequestBuilder(BaseService):
    def list_request(self, limit: int = 100, offset: int = 0):
        return self._construct_request("GET", "providers", params={"limit": limit, "offset": offset})

class ProvidersAPI(ProvidersRequestBuilder):
    def __init__(self, client):
        self.client = client

    def list(self, limit: int = 100, offset: int = 0) -> ProviderCollection:
        raw_response = self.client.request(**self.list_request(limit, offset))
        return ProviderCollection(**raw_response)

class AsyncProvidersAPI(ProvidersRequestBuilder):
    def __init__(self, client):
        self.client = client

    async def list(self, limit: int = 100, offset: int = 0) -> ProviderCollection:
        raw_response = await self.client.request(**self.list_request(limit, offset))
        return ProviderCollection(**raw_response)
