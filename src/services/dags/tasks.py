from src.services.base import BaseService
from src.services.dags.dags_models import TaskModel, TaskCollection

class TasksRequestBuilder(BaseService):
    def list_request(self, dag_id: str):
        return self._construct_request("GET", f"dags/{dag_id}/tasks")

    def get_request(self, dag_id: str, task_id: str):
        return self._construct_request("GET", f"dags/{dag_id}/tasks/{task_id}")


class TasksAPI(TasksRequestBuilder):
    def __init__(self, client):
        self.client = client

    def list(self, dag_id: str) -> TaskCollection:
        raw_response = self.client.request(**self.list_request(dag_id))
        return TaskCollection(**raw_response)

    def get(self, dag_id: str, task_id: str) -> TaskModel:
        raw_response = self.client.request(**self.get_request(dag_id, task_id))
        return TaskModel(**raw_response)


class AsyncTasksAPI(TasksRequestBuilder):
    def __init__(self, client):
        self.client = client

    async def list(self, dag_id: str) -> TaskCollection:
        raw_response = await self.client.request(**self.list_request(dag_id))
        return TaskCollection(**raw_response)

    async def get(self, dag_id: str, task_id: str) -> TaskModel:
        raw_response = await self.client.request(**self.get_request(dag_id, task_id))
        return TaskModel(**raw_response)
