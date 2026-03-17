from typing import List, Optional
from src.services.base import BaseService
from src.services.dags.dags_models import DagStatsCollection

class DagStatsRequestBuilder(BaseService):
    def get_request(self, dag_ids: Optional[List[str]] = None):
        params = {"dag_ids": dag_ids} if dag_ids else {}
        return self._construct_request("GET", "dagStats", params=params)

class DagStatsAPI(DagStatsRequestBuilder):
    def __init__(self, client):
        self.client = client

    def get(self, dag_ids: Optional[List[str]] = None) -> DagStatsCollection:
        raw_response = self.client.request(**self.get_request(dag_ids))
        return DagStatsCollection(**raw_response)

class AsyncDagStatsAPI(DagStatsRequestBuilder):
    def __init__(self, client):
        self.client = client

    async def get(self, dag_ids: Optional[List[str]] = None) -> DagStatsCollection:
        raw_response = await self.client.request(**self.get_request(dag_ids))
        return DagStatsCollection(**raw_response)
