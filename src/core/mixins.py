import httpx
from typing import Dict, Any, Optional
from src.exceptions import AirflowRequestError, AirflowRateLimitError, AirflowAuthError, AirflowNotFoundError

class HTTPClientMixin:
    """Shared HTTP logic for both Sync and Async clients."""
    
    base_url: str

    def build_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"
        
    def handle_error(self, response: httpx.Response) -> None:
        if response.is_success:
            return

        status = response.status_code
        try:
            data = response.json()
            message = data.get("detail", response.text)
        except ValueError:
            message = response.text
            data = None

        if status == 401:
            raise AirflowAuthError(f"Authentication failed: {message}")
        elif status == 403:
            raise AirflowAuthError(f"Permission denied: {message}")
        elif status == 404:
            raise AirflowNotFoundError(f"Resource not found: {message}")
        elif status == 429:
            raise AirflowRateLimitError(f"Rate limit exceeded: {message}")
        else:
            raise AirflowRequestError(f"API request failed with status {status}: {message}", status_code=status, response_data=data)
