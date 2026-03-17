from src.services.base import BaseService
from src.services.dags.dags_models import DagVersionModel, DagVersionCollection

class DagVersionsRequestBuilder(BaseService):
    def list_request(self, dag_id: str, limit: int = 100, offset: int = 0):
        return self._construct_request("GET", f"dags/{dag_id}/dagVersions", params={"limit": limit, "offset": offset})

    def get_request(self, dag_id: str, version_number: int):
        return self._construct_request("GET", f"dags/{dag_id}/dagVersions/{version_number}")

class DagVersionsAPI(DagVersionsRequestBuilder):
    def __init__(self, client):
        self.client = client

    def list(self, dag_id: str, limit: int = 100, offset: int = 0) -> DagVersionCollection:
        raw_response = self.client.request(**self.list_request(dag_id, limit, offset))
        return DagVersionCollection(**raw_response)

    def get(self, dag_id: str, version_number: int) -> DagVersionModel:
        raw_response = self.client.request(**self.get_request(dag_id, version_number))
        return DagVersionModel(**raw_response)

class AsyncDagVersionsAPI(DagVersionsRequestBuilder):
    def __init__(self, client):
        self.client = client

    async def list(self, dag_id: str, limit: int = 100, offset: int = 0) -> DagVersionCollection:
        raw_response = await self.client.request(**self.list_request(dag_id, limit, offset))
        return DagVersionCollection(**raw_response)

    async def get(self, dag_id: str, version_number: int) -> DagVersionModel:
        raw_response = await self.client.request(**self.get_request(dag_id, version_number))
        return DagVersionModel(**raw_response)
