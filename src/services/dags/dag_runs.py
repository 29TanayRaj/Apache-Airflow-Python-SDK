from typing import Dict, Any, Optional
from src.services.base import BaseService
from src.services.dags.dags_models import DagRunModel, DagRunCollection

class DagRunsRequestBuilder(BaseService):
    def list_request(self, dag_id: str, limit: int = 100, offset: int = 0):
        return self._construct_request("GET", f"dags/{dag_id}/dagRuns", params={"limit": limit, "offset": offset})

    def get_request(self, dag_id: str, dag_run_id: str):
        return self._construct_request("GET", f"dags/{dag_id}/dagRuns/{dag_run_id}")

    def trigger_request(self, dag_id: str, conf: Optional[Dict[str, Any]] = None, logical_date: Optional[str] = None):
        payload = {}
        if conf is not None: payload["conf"] = conf
        if logical_date is not None: payload["logical_date"] = logical_date
        return self._construct_request("POST", f"dags/{dag_id}/dagRuns", json=payload if payload else None)

    def delete_request(self, dag_id: str, dag_run_id: str):
        return self._construct_request("DELETE", f"dags/{dag_id}/dagRuns/{dag_run_id}")

    def clear_request(self, dag_id: str, dag_run_id: str, dry_run: bool = False):
        return self._construct_request("POST", f"dags/{dag_id}/dagRuns/{dag_run_id}/clear", json={"dry_run": dry_run})


class DagRunsAPI(DagRunsRequestBuilder):
    def __init__(self, client):
        self.client = client

    def list(self, dag_id: str, limit: int = 100, offset: int = 0) -> DagRunCollection:
        raw_response = self.client.request(**self.list_request(dag_id, limit, offset))
        return DagRunCollection(**raw_response)

    def get(self, dag_id: str, dag_run_id: str) -> DagRunModel:
        raw_response = self.client.request(**self.get_request(dag_id, dag_run_id))
        return DagRunModel(**raw_response)

    def trigger(self, dag_id: str, conf: Optional[Dict[str, Any]] = None, logical_date: Optional[str] = None) -> DagRunModel:
        raw_response = self.client.request(**self.trigger_request(dag_id, conf, logical_date))
        return DagRunModel(**raw_response)

    def delete(self, dag_id: str, dag_run_id: str) -> None:
        self.client.request(**self.delete_request(dag_id, dag_run_id))

    def clear(self, dag_id: str, dag_run_id: str, dry_run: bool = False) -> Any:
        return self.client.request(**self.clear_request(dag_id, dag_run_id, dry_run))


class AsyncDagRunsAPI(DagRunsRequestBuilder):
    def __init__(self, client):
        self.client = client

    async def list(self, dag_id: str, limit: int = 100, offset: int = 0) -> DagRunCollection:
        raw_response = await self.client.request(**self.list_request(dag_id, limit, offset))
        return DagRunCollection(**raw_response)

    async def get(self, dag_id: str, dag_run_id: str) -> DagRunModel:
        raw_response = await self.client.request(**self.get_request(dag_id, dag_run_id))
        return DagRunModel(**raw_response)

    async def trigger(self, dag_id: str, conf: Optional[Dict[str, Any]] = None, logical_date: Optional[str] = None) -> DagRunModel:
        raw_response = await self.client.request(**self.trigger_request(dag_id, conf, logical_date))
        return DagRunModel(**raw_response)

    async def delete(self, dag_id: str, dag_run_id: str) -> None:
        await self.client.request(**self.delete_request(dag_id, dag_run_id))

    async def clear(self, dag_id: str, dag_run_id: str, dry_run: bool = False) -> Any:
        return await self.client.request(**self.clear_request(dag_id, dag_run_id, dry_run))
