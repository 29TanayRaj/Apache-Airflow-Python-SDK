from src.services.base import BaseService

class ImportErrorsRequestBuilder(BaseService):
    def list_request(self, limit: int = 100, offset: int = 0):
        return self._construct_request("GET", "importErrors", params={"limit": limit, "offset": offset})

    def get_request(self, import_error_id: int):
        return self._construct_request("GET", f"importErrors/{import_error_id}")

class ImportErrorsAPI(ImportErrorsRequestBuilder):
    def __init__(self, client):
        self.client = client

    def list(self, limit: int = 100, offset: int = 0):
        return self.client.request(**self.list_request(limit, offset))

    def get(self, import_error_id: int):
        return self.client.request(**self.get_request(import_error_id))

class AsyncImportErrorsAPI(ImportErrorsRequestBuilder):
    def __init__(self, client):
        self.client = client

    async def list(self, limit: int = 100, offset: int = 0):
        return await self.client.request(**self.list_request(limit, offset))

    async def get(self, import_error_id: int):
        return await self.client.request(**self.get_request(import_error_id))
