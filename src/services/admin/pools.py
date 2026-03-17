from typing import Dict, Any, Optional
from src.services.base import BaseService
from src.services.admin.admin_models import PoolModel, PoolCollection, PoolCreateRequest

class PoolsRequestBuilder(BaseService):
    def list_request(self, limit: int = 100, offset: int = 0):
        return self._construct_request("GET", "pools", params={"limit": limit, "offset": offset})

    def get_request(self, pool_name: str):
        return self._construct_request("GET", f"pools/{pool_name}")

    def create_request(self, name: str, slots: int, description: Optional[str] = None):
        payload = {"name": name, "slots": slots}
        if description: payload["description"] = description
        return self._construct_request("POST", "pools", json=payload)

    def patch_request(self, pool_name: str, update_mask: Optional[list] = None, **kwargs):
        params = {"update_mask": update_mask} if update_mask else {}
        return self._construct_request("PATCH", f"pools/{pool_name}", params=params, json=kwargs)

    def delete_request(self, pool_name: str):
        return self._construct_request("DELETE", f"pools/{pool_name}")


class PoolsAPI(PoolsRequestBuilder):
    def __init__(self, client):
        self.client = client

    def list(self, limit: int = 100, offset: int = 0) -> PoolCollection:
        raw_response = self.client.request(**self.list_request(limit, offset))
        return PoolCollection(**raw_response)

    def get(self, pool_name: str) -> PoolModel:
        raw_response = self.client.request(**self.get_request(pool_name))
        return PoolModel(**raw_response)

    def create(self, request: PoolCreateRequest) -> PoolModel:
        raw_response = self.client.request(**self.create_request(**request.model_dump(exclude_none=True)))
        return PoolModel(**raw_response)

    def patch(self, pool_name: str, update_mask: Optional[list] = None, **kwargs) -> PoolModel:
        raw_response = self.client.request(**self.patch_request(pool_name, update_mask, **kwargs))
        return PoolModel(**raw_response)

    def delete(self, pool_name: str) -> None:
        self.client.request(**self.delete_request(pool_name))


class AsyncPoolsAPI(PoolsRequestBuilder):
    def __init__(self, client):
        self.client = client

    async def list(self, limit: int = 100, offset: int = 0) -> PoolCollection:
        raw_response = await self.client.request(**self.list_request(limit, offset))
        return PoolCollection(**raw_response)

    async def get(self, pool_name: str) -> PoolModel:
        raw_response = await self.client.request(**self.get_request(pool_name))
        return PoolModel(**raw_response)

    async def create(self, request: PoolCreateRequest) -> PoolModel:
        raw_response = await self.client.request(**self.create_request(**request.model_dump(exclude_none=True)))
        return PoolModel(**raw_response)

    async def patch(self, pool_name: str, update_mask: Optional[list] = None, **kwargs) -> PoolModel:
        raw_response = await self.client.request(**self.patch_request(pool_name, update_mask, **kwargs))
        return PoolModel(**raw_response)

    async def delete(self, pool_name: str) -> None:
        await self.client.request(**self.delete_request(pool_name))
