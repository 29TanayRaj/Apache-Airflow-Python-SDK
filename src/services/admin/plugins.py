from src.services.base import BaseService
from typing import Dict, Any
from src.services.admin.admin_models import PluginCollection

class PluginsRequestBuilder(BaseService):
    def list_request(self, limit: int = 100, offset: int = 0):
        return self._construct_request("GET", "plugins", params={"limit": limit, "offset": offset})

    def import_errors_request(self, limit: int = 100, offset: int = 0):
        return self._construct_request("GET", "plugins/importErrors", params={"limit": limit, "offset": offset})

class PluginsAPI(PluginsRequestBuilder):
    def __init__(self, client):
        self.client = client

    def list(self, limit: int = 100, offset: int = 0) -> PluginCollection:
        raw_response = self.client.request(**self.list_request(limit, offset))
        return PluginCollection(**raw_response)

    def import_errors(self, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        return self.client.request(**self.import_errors_request(limit, offset))

class AsyncPluginsAPI(PluginsRequestBuilder):
    def __init__(self, client):
        self.client = client

    async def list(self, limit: int = 100, offset: int = 0) -> PluginCollection:
        raw_response = await self.client.request(**self.list_request(limit, offset))
        return PluginCollection(**raw_response)

    async def import_errors(self, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        return await self.client.request(**self.import_errors_request(limit, offset))
