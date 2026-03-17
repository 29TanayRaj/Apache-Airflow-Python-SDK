from typing import Optional
from src.services.base import BaseService
from src.services.dags.dags_models import DagWarningCollection

class DagWarningsRequestBuilder(BaseService):
    def list_request(self, dag_id: Optional[str] = None, warning_type: Optional[str] = None, limit: int = 100, offset: int = 0):
        params = {"limit": limit, "offset": offset}
        if dag_id: params["dag_id"] = dag_id
        if warning_type: params["warning_type"] = warning_type
        return self._construct_request("GET", "dagWarnings", params=params)

class DagWarningsAPI(DagWarningsRequestBuilder):
    def __init__(self, client):
        self.client = client

    def list(self, dag_id: Optional[str] = None, warning_type: Optional[str] = None, limit: int = 100, offset: int = 0) -> DagWarningCollection:
        raw_response = self.client.request(**self.list_request(dag_id, warning_type, limit, offset))
        return DagWarningCollection(**raw_response)

class AsyncDagWarningsAPI(DagWarningsRequestBuilder):
    def __init__(self, client):
        self.client = client

    async def list(self, dag_id: Optional[str] = None, warning_type: Optional[str] = None, limit: int = 100, offset: int = 0) -> DagWarningCollection:
        raw_response = await self.client.request(**self.list_request(dag_id, warning_type, limit, offset))
        return DagWarningCollection(**raw_response)
