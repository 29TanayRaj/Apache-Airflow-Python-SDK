from typing import Dict, Any, Optional
from src.services.base import BaseService
from src.services.admin.admin_models import VariableModel, VariableCollection, VariableCreateRequest

class VariablesRequestBuilder(BaseService):
    def list_request(self, limit: int = 100, offset: int = 0):
        return self._construct_request("GET", "variables", params={"limit": limit, "offset": offset})

    def get_request(self, variable_key: str):
        return self._construct_request("GET", f"variables/{variable_key}")

    def create_request(self, key: str, value: str, description: Optional[str] = None):
        payload = {"key": key, "value": value}
        if description: payload["description"] = description
        return self._construct_request("POST", "variables", json=payload)

    def patch_request(self, variable_key: str, update_mask: Optional[list] = None, **kwargs):
        params = {"update_mask": update_mask} if update_mask else {}
        return self._construct_request("PATCH", f"variables/{variable_key}", params=params, json=kwargs)

    def delete_request(self, variable_key: str):
        return self._construct_request("DELETE", f"variables/{variable_key}")


class VariablesAPI(VariablesRequestBuilder):
    def __init__(self, client):
        self.client = client

    def list(self, limit: int = 100, offset: int = 0) -> VariableCollection:
        raw_response = self.client.request(**self.list_request(limit, offset))
        return VariableCollection(**raw_response)

    def get(self, variable_key: str) -> VariableModel:
        raw_response = self.client.request(**self.get_request(variable_key))
        return VariableModel(**raw_response)

    def create(self, request: VariableCreateRequest) -> VariableModel:
        raw_response = self.client.request(**self.create_request(**request.model_dump(exclude_none=True)))
        return VariableModel(**raw_response)

    def patch(self, variable_key: str, update_mask: Optional[list] = None, **kwargs) -> VariableModel:
        raw_response = self.client.request(**self.patch_request(variable_key, update_mask, **kwargs))
        return VariableModel(**raw_response)

    def delete(self, variable_key: str) -> None:
        self.client.request(**self.delete_request(variable_key))


class AsyncVariablesAPI(VariablesRequestBuilder):
    def __init__(self, client):
        self.client = client

    async def list(self, limit: int = 100, offset: int = 0) -> VariableCollection:
        raw_response = await self.client.request(**self.list_request(limit, offset))
        return VariableCollection(**raw_response)

    async def get(self, variable_key: str) -> VariableModel:
        raw_response = await self.client.request(**self.get_request(variable_key))
        return VariableModel(**raw_response)

    async def create(self, request: VariableCreateRequest) -> VariableModel:
        raw_response = await self.client.request(**self.create_request(**request.model_dump(exclude_none=True)))
        return VariableModel(**raw_response)

    async def patch(self, variable_key: str, update_mask: Optional[list] = None, **kwargs) -> VariableModel:
        raw_response = await self.client.request(**self.patch_request(variable_key, update_mask, **kwargs))
        return VariableModel(**raw_response)

    async def delete(self, variable_key: str) -> None:
        await self.client.request(**self.delete_request(variable_key))
