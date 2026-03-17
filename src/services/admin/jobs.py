from src.services.base import BaseService

class JobsRequestBuilder(BaseService):
    def list_request(self, limit: int = 100, offset: int = 0):
        return self._construct_request("GET", "jobs", params={"limit": limit, "offset": offset})

class JobsAPI(JobsRequestBuilder):
    def __init__(self, client):
        self.client = client

    def list(self, limit: int = 100, offset: int = 0):
        return self.client.request(**self.list_request(limit, offset))

class AsyncJobsAPI(JobsRequestBuilder):
    def __init__(self, client):
        self.client = client

    async def list(self, limit: int = 100, offset: int = 0):
        return await self.client.request(**self.list_request(limit, offset))
