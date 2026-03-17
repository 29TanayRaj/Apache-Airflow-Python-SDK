from typing import Dict, Any, List, Optional
from src.services.base import BaseService
from src.services.dags.dags_models import DagModel, DagCollection


class DagsRequestBuilder(BaseService):
    def list_request(self, limit: int = 100, offset: int = 0, tags: Optional[List[str]] = None):
        params = {"limit": limit, "offset": offset}
        if tags: params["tags"] = tags
        return self._construct_request("GET", "dags", params=params)

    def get_request(self, dag_id: str):
        return self._construct_request("GET", f"dags/{dag_id}")

    def get_details_request(self, dag_id: str):
        return self._construct_request("GET", f"dags/{dag_id}/details")

    def patch_request(self, dag_id: str, update_mask: Optional[List[str]] = None, **kwargs):
        params = {"update_mask": update_mask} if update_mask else {}
        return self._construct_request("PATCH", f"dags/{dag_id}", params=params, json=kwargs)

    def delete_request(self, dag_id: str):
        return self._construct_request("DELETE", f"dags/{dag_id}")

    def pause_request(self, dag_id: str, is_paused: bool = True):
        return self.patch_request(dag_id, is_paused=is_paused, update_mask=["is_paused"])


class DagsAPI(DagsRequestBuilder):
    def __init__(self, client):
        self.client = client

    def list(self, limit: int = 100, offset: int = 0, tags: Optional[List[str]] = None) -> DagCollection:
        raw_response = self.client.request(**self.list_request(limit, offset, tags))
        return DagCollection(**raw_response)

    def get(self, dag_id: str) -> DagModel:
        raw_response = self.client.request(**self.get_request(dag_id))
        return DagModel(**raw_response)

    def get_details(self, dag_id: str) -> DagModel:
        raw_response = self.client.request(**self.get_details_request(dag_id))
        return DagModel(**raw_response)

    def patch(self, dag_id: str, update_mask: Optional[List[str]] = None, **kwargs) -> DagModel:
        raw_response = self.client.request(**self.patch_request(dag_id, update_mask, **kwargs))
        return DagModel(**raw_response)

    def delete(self, dag_id: str) -> None:
        self.client.request(**self.delete_request(dag_id))

    def pause(self, dag_id: str, is_paused: bool = True) -> DagModel:
        raw_response = self.client.request(**self.pause_request(dag_id, is_paused))
        return DagModel(**raw_response)


class AsyncDagsAPI(DagsRequestBuilder):
    def __init__(self, client):
        self.client = client

    async def list(self, limit: int = 100, offset: int = 0, tags: Optional[List[str]] = None) -> DagCollection:
        raw_response = await self.client.request(**self.list_request(limit, offset, tags))
        return DagCollection(**raw_response)

    async def get(self, dag_id: str) -> DagModel:
        raw_response = await self.client.request(**self.get_request(dag_id))
        return DagModel(**raw_response)

    async def get_details(self, dag_id: str) -> DagModel:
        raw_response = await self.client.request(**self.get_details_request(dag_id))
        return DagModel(**raw_response)

    async def patch(self, dag_id: str, update_mask: Optional[List[str]] = None, **kwargs) -> DagModel:
        raw_response = await self.client.request(**self.patch_request(dag_id, update_mask, **kwargs))
        return DagModel(**raw_response)

    async def delete(self, dag_id: str) -> None:
        await self.client.request(**self.delete_request(dag_id))

    async def pause(self, dag_id: str, is_paused: bool = True) -> DagModel:
        raw_response = await self.client.request(**self.pause_request(dag_id, is_paused))
        return DagModel(**raw_response)
