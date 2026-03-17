from typing import Dict, Any, Optional
from src.services.base import BaseService
from src.services.admin.admin_models import ConnectionModel, ConnectionCollection, ConnectionCreateRequest

class ConnectionsRequestBuilder(BaseService):
    def list_request(self, limit: int = 100, offset: int = 0):
        return self._construct_request("GET", "connections", params={"limit": limit, "offset": offset})

    def get_request(self, connection_id: str):
        return self._construct_request("GET", f"connections/{connection_id}")

    def create_request(self, connection_id: str, conn_type: str, host: Optional[str] = None, login: Optional[str] = None, **kwargs):
        payload = {"connection_id": connection_id, "conn_type": conn_type}
        if host: payload["host"] = host
        if login: payload["login"] = login
        payload.update(kwargs)
        return self._construct_request("POST", "connections", json=payload)

    def patch_request(self, connection_id: str, update_mask: Optional[list] = None, **kwargs):
        params = {"update_mask": update_mask} if update_mask else {}
        return self._construct_request("PATCH", f"connections/{connection_id}", params=params, json=kwargs)

    def delete_request(self, connection_id: str):
        return self._construct_request("DELETE", f"connections/{connection_id}")


class ConnectionsAPI(ConnectionsRequestBuilder):
    def __init__(self, client):
        self.client = client

    def list(self, limit: int = 100, offset: int = 0) -> ConnectionCollection:
        raw_response = self.client.request(**self.list_request(limit, offset))
        return ConnectionCollection(**raw_response)

    def get(self, connection_id: str) -> ConnectionModel:
        raw_response = self.client.request(**self.get_request(connection_id))
        return ConnectionModel(**raw_response)

    def create(self, request: ConnectionCreateRequest) -> ConnectionModel:
        raw_response = self.client.request(**self.create_request(**request.model_dump(exclude_none=True)))
        return ConnectionModel(**raw_response)

    def patch(self, connection_id: str, update_mask: Optional[list] = None, **kwargs) -> ConnectionModel:
        raw_response = self.client.request(**self.patch_request(connection_id, update_mask, **kwargs))
        return ConnectionModel(**raw_response)

    def delete(self, connection_id: str) -> None:
        self.client.request(**self.delete_request(connection_id))


class AsyncConnectionsAPI(ConnectionsRequestBuilder):
    def __init__(self, client):
        self.client = client

    async def list(self, limit: int = 100, offset: int = 0) -> ConnectionCollection:
        raw_response = await self.client.request(**self.list_request(limit, offset))
        return ConnectionCollection(**raw_response)

    async def get(self, connection_id: str) -> ConnectionModel:
        raw_response = await self.client.request(**self.get_request(connection_id))
        return ConnectionModel(**raw_response)

    async def create(self, request: ConnectionCreateRequest) -> ConnectionModel:
        raw_response = await self.client.request(**self.create_request(**request.model_dump(exclude_none=True)))
        return ConnectionModel(**raw_response)

    async def patch(self, connection_id: str, update_mask: Optional[list] = None, **kwargs) -> ConnectionModel:
        raw_response = await self.client.request(**self.patch_request(connection_id, update_mask, **kwargs))
        return ConnectionModel(**raw_response)

    async def delete(self, connection_id: str) -> None:
        await self.client.request(**self.delete_request(connection_id))
