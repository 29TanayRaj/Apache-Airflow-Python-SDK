from typing import Dict, Any
from src.services.base import BaseService
from src.services.backfills.backfills_models import BackfillModel, BackfillCollection

class BackfillsRequestBuilder(BaseService):
    def list_request(self, limit: int = 100, offset: int = 0):
        return self._construct_request("GET", "backfills", params={"limit": limit, "offset": offset})

    def get_request(self, backfill_id: str):
        return self._construct_request("GET", f"backfills/{backfill_id}")

    def create_request(self, dag_id: str, from_date: str, to_date: str, **kwargs):
        payload = {"dag_id": dag_id, "from_date": from_date, "to_date": to_date}
        payload.update(kwargs)
        return self._construct_request("POST", "backfills", json=payload)

    def pause_request(self, backfill_id: str):
        return self._construct_request("PUT", f"backfills/{backfill_id}/pause")

    def unpause_request(self, backfill_id: str):
        return self._construct_request("PUT", f"backfills/{backfill_id}/unpause")

    def cancel_request(self, backfill_id: str):
        return self._construct_request("PUT", f"backfills/{backfill_id}/cancel")


class BackfillsAPI(BackfillsRequestBuilder):
    def __init__(self, client):
        self.client = client

    def list(self, limit: int = 100, offset: int = 0) -> BackfillCollection:
        raw_response = self.client.request(**self.list_request(limit, offset))
        return BackfillCollection(**raw_response)

    def get(self, backfill_id: str) -> BackfillModel:
        raw_response = self.client.request(**self.get_request(backfill_id))
        return BackfillModel(**raw_response)

    def create(self, dag_id: str, from_date: str, to_date: str, **kwargs) -> BackfillModel:
        raw_response = self.client.request(**self.create_request(dag_id, from_date, to_date, **kwargs))
        return BackfillModel(**raw_response)

    def pause(self, backfill_id: str) -> BackfillModel:
        raw_response = self.client.request(**self.pause_request(backfill_id))
        return BackfillModel(**raw_response)

    def unpause(self, backfill_id: str) -> BackfillModel:
        raw_response = self.client.request(**self.unpause_request(backfill_id))
        return BackfillModel(**raw_response)

    def cancel(self, backfill_id: str) -> BackfillModel:
        raw_response = self.client.request(**self.cancel_request(backfill_id))
        return BackfillModel(**raw_response)


class AsyncBackfillsAPI(BackfillsRequestBuilder):
    def __init__(self, client):
        self.client = client

    async def list(self, limit: int = 100, offset: int = 0) -> BackfillCollection:
        raw_response = await self.client.request(**self.list_request(limit, offset))
        return BackfillCollection(**raw_response)

    async def get(self, backfill_id: str) -> BackfillModel:
        raw_response = await self.client.request(**self.get_request(backfill_id))
        return BackfillModel(**raw_response)

    async def create(self, dag_id: str, from_date: str, to_date: str, **kwargs) -> BackfillModel:
        raw_response = await self.client.request(**self.create_request(dag_id, from_date, to_date, **kwargs))
        return BackfillModel(**raw_response)

    async def pause(self, backfill_id: str) -> BackfillModel:
        raw_response = await self.client.request(**self.pause_request(backfill_id))
        return BackfillModel(**raw_response)

    async def unpause(self, backfill_id: str) -> BackfillModel:
        raw_response = await self.client.request(**self.unpause_request(backfill_id))
        return BackfillModel(**raw_response)

    async def cancel(self, backfill_id: str) -> BackfillModel:
        raw_response = await self.client.request(**self.cancel_request(backfill_id))
        return BackfillModel(**raw_response)
