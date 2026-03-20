import httpx
from typing import Optional

class AuthManager:
    """Manages Bearer-token authentication for the Airflow API."""

    def __init__(self, username: str = None, password: str = None):
        self.username = username
        self.password = password
        self._token: Optional[str] = None

    # ------------------------------------------------------------------
    # Synchronous token fetch
    # ------------------------------------------------------------------
    def fetch_token(self, base_url: str) -> str:
        """POSTs credentials to /auth/token and caches the access token."""
        response = httpx.post(
            f"{base_url}/auth/token",
            json={"username": self.username, "password": self.password},
        )
        response.raise_for_status()
        self._token = response.json()["access_token"]
        return self._token

    def get_headers(self, base_url: str, force_refresh: bool = False) -> dict:
        """Returns Authorization headers, fetching a token if needed.
        
        Pass force_refresh=True to discard the cached token and fetch a new one
        (e.g. after receiving a 401 indicating the token has expired).
        """
        if not self._token or force_refresh:
            self.fetch_token(base_url)
        return {"Authorization": f"Bearer {self._token}"}

    # ------------------------------------------------------------------
    # Asynchronous token fetch
    # ------------------------------------------------------------------
    async def fetch_token_async(self, base_url: str) -> str:
        """Async version of fetch_token."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/auth/token",
                json={"username": self.username, "password": self.password},
            )
        response.raise_for_status()
        self._token = response.json()["access_token"]
        return self._token

    async def get_headers_async(self, base_url: str, force_refresh: bool = False) -> dict:
        """Async version of get_headers.

        Pass force_refresh=True to discard the cached token and fetch a new one
        (e.g. after receiving a 401 indicating the token has expired).
        """
        if not self._token or force_refresh:
            await self.fetch_token_async(base_url)
        return {"Authorization": f"Bearer {self._token}"}