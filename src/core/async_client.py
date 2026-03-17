import httpx
from typing import Dict, Any, Optional

from src.core.auth import AuthManager
from src.core.retry import RetryStrategy
from src.core.mixins import HTTPClientMixin

class AsyncAPIClient(HTTPClientMixin):
    """Asynchronous HTTP client for Airflow API."""

    def __init__(self, base_url: str, 
        username: str = None, 
        password: str = None, 
        retries: int = 3):
        self.base_url = base_url.rstrip("/") + "/api/v2" if not base_url.endswith("/api/v2") else base_url.rstrip("/")
        self.auth_manager = AuthManager(username, password)
        self.retry_strategy = RetryStrategy(max_retries=retries)
        self.client = httpx.AsyncClient(auth=self.auth_manager.get_auth())

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self.client.aclose()

    async def request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Executes an asynchronous HTTP request against the Airflow API."""
        url = self.build_url(endpoint)
        response = await self.retry_strategy.execute_async(
            self.client.request,
            method=method,
            url=url,
            **kwargs
        )
        self.handle_error(response)
        
        if response.status_code == 204:
            return {}
        try:
            return response.json()
        except ValueError:
            return {"content": response.text}
