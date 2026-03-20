import httpx
from typing import Dict, Any, Optional

from src.core.auth import AuthManager
from src.core.retry import RetryStrategy
from src.core.mixins import HTTPClientMixin
from src.exceptions import AirflowAuthError

class AsyncAPIClient(HTTPClientMixin):
    """Asynchronous HTTP client for Airflow API."""

    def __init__(self, base_url: str,
        username: str = None,
        password: str = None,
        retries: int = 3):
        self.base_url = base_url.rstrip("/") + "/api/v2" if not base_url.endswith("/api/v2") else base_url.rstrip("/")
        # Store the raw base (without /api/v2) for the token endpoint
        self._auth_base_url = base_url.rstrip("/")
        self.auth_manager = AuthManager(username, password)
        self.retry_strategy = RetryStrategy(max_retries=retries)
        self.client = httpx.AsyncClient()   # No basic auth; token headers injected per-request

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self.client.aclose()

    async def _do_request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """Internal helper: runs the request through the retry strategy and error handler."""
        response = await self.retry_strategy.execute_async(
            self.client.request,
            method=method,
            url=url,
            **kwargs
        )
        self.handle_error(response)
        return response

    async def request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Executes an asynchronous HTTP request against the Airflow API.

        If a 401 is returned (expired token), the token is refreshed and the
        request is retried exactly once before re-raising.
        """
        url = self.build_url(endpoint)
        existing_headers = kwargs.pop("headers", {})

        # First attempt with the cached (or freshly fetched) token
        kwargs["headers"] = {**(await self.auth_manager.get_headers_async(self._auth_base_url)), **existing_headers}
        try:
            response = await self._do_request(method, url, **kwargs)
        except AirflowAuthError:
            # Token likely expired — refresh and retry once
            kwargs["headers"] = {**(await self.auth_manager.get_headers_async(self._auth_base_url, force_refresh=True)), **existing_headers}
            response = await self._do_request(method, url, **kwargs)

        if response.status_code == 204:
            return {}
        try:
            return response.json()
        except ValueError:
            return {"content": response.text}