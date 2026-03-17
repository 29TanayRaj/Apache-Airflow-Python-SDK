from src.services.base import BaseService
from src.services.dags.dags_models import DagSourceModel

class DagSourcesRequestBuilder(BaseService):
    def get_request(self, dag_id: str):
        return self._construct_request("GET", f"dagSources/{dag_id}")

class DagSourcesAPI(DagSourcesRequestBuilder):
    def __init__(self, client):
        self.client = client

    def get(self, dag_id: str) -> DagSourceModel:
        raw_response = self.client.request(**self.get_request(dag_id))
        return DagSourceModel(**raw_response)

class AsyncDagSourcesAPI(DagSourcesRequestBuilder):
    def __init__(self, client):
        self.client = client

    async def get(self, dag_id: str) -> DagSourceModel:
        raw_response = await self.client.request(**self.get_request(dag_id))
        return DagSourceModel(**raw_response)
