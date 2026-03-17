from src.services.base import BaseService

class EventLogsRequestBuilder(BaseService):
    def list_request(self, limit: int = 100, offset: int = 0):
        return self._construct_request("GET", "eventLogs", params={"limit": limit, "offset": offset})

    def get_request(self, event_log_id: int):
        return self._construct_request("GET", f"eventLogs/{event_log_id}")

class EventLogsAPI(EventLogsRequestBuilder):
    def __init__(self, client):
        self.client = client

    def list(self, limit: int = 100, offset: int = 0):
        return self.client.request(**self.list_request(limit, offset))

    def get(self, event_log_id: int):
        return self.client.request(**self.get_request(event_log_id))

class AsyncEventLogsAPI(EventLogsRequestBuilder):
    def __init__(self, client):
        self.client = client

    async def list(self, limit: int = 100, offset: int = 0):
        return await self.client.request(**self.list_request(limit, offset))

    async def get(self, event_log_id: int):
        return await self.client.request(**self.get_request(event_log_id))
