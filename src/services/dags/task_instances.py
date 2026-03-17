from src.services.base import BaseService
from src.services.dags.dags_models import TaskInstanceModel, TaskInstanceCollection

class TaskInstancesRequestBuilder(BaseService):
    def list_request(self, dag_id: str, dag_run_id: str, limit: int = 100, offset: int = 0):
        return self._construct_request("GET", f"dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances", params={"limit": limit, "offset": offset})

    def get_request(self, dag_id: str, dag_run_id: str, task_id: str):
        return self._construct_request("GET", f"dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}")


class TaskInstancesAPI(TaskInstancesRequestBuilder):
    def __init__(self, client):
        self.client = client

    def list(self, dag_id: str, dag_run_id: str, limit: int = 100, offset: int = 0) -> TaskInstanceCollection:
        raw_response = self.client.request(**self.list_request(dag_id, dag_run_id, limit, offset))
        return TaskInstanceCollection(**raw_response)

    def get(self, dag_id: str, dag_run_id: str, task_id: str) -> TaskInstanceModel:
        raw_response = self.client.request(**self.get_request(dag_id, dag_run_id, task_id))
        return TaskInstanceModel(**raw_response)


class AsyncTaskInstancesAPI(TaskInstancesRequestBuilder):
    def __init__(self, client):
        self.client = client

    async def list(self, dag_id: str, dag_run_id: str, limit: int = 100, offset: int = 0) -> TaskInstanceCollection:
        raw_response = await self.client.request(**self.list_request(dag_id, dag_run_id, limit, offset))
        return TaskInstanceCollection(**raw_response)

    async def get(self, dag_id: str, dag_run_id: str, task_id: str) -> TaskInstanceModel:
        raw_response = await self.client.request(**self.get_request(dag_id, dag_run_id, task_id))
        return TaskInstanceModel(**raw_response)
