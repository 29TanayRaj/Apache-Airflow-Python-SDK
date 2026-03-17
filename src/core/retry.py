import asyncio
import time
from typing import Callable, Any
from httpx import Response
from src.exceptions import AirflowRequestError, AirflowRateLimitError

class RetryStrategy:
    """Implements exponential backoff strategy for API requests."""
    
    def __init__(self, max_retries: int = 3, backoff_factor: float = 1.0, allowed_methods: set = None):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.allowed_methods = allowed_methods or {"HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST", "PATCH"}

    def should_retry(self, response: Response) -> bool:
        """Determines if a request should be retried based on the status code."""
        return response.status_code in (429, 500, 502, 503, 504)

    def execute(self, request_func: Callable[..., Response], *args, **kwargs) -> Response:
        """Executes a synchronous request with retries."""
        retries = 0
        method = kwargs.get("method", "GET").upper()
        
        while True:
            try:
                response = request_func(*args, **kwargs)
                if response.is_success or not self.should_retry(response) or retries >= self.max_retries or method not in self.allowed_methods:
                    return response
            except Exception as e:
                if retries >= self.max_retries:
                    raise AirflowRequestError(f"Request failed after {retries} retries: {str(e)}") from e
            
            # Delay and backoff
            sleep_time = self.backoff_factor * (2 ** retries)
            time.sleep(sleep_time)
            retries += 1

    async def execute_async(self, request_func: Callable[..., Any], *args, **kwargs) -> Response:
        """Executes an asynchronous request with retries."""
        retries = 0
        method = kwargs.get("method", "GET").upper()
        
        while True:
            try:
                response = await request_func(*args, **kwargs)
                if response.is_success or not self.should_retry(response) or retries >= self.max_retries or method not in self.allowed_methods:
                    return response
            except Exception as e:
                if retries >= self.max_retries:
                    raise AirflowRequestError(f"Request failed after {retries} retries: {str(e)}") from e
            
            # Delay and backoff
            sleep_time = self.backoff_factor * (2 ** retries)
            await asyncio.sleep(sleep_time)
            retries += 1
