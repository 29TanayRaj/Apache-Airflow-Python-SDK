class AirflowAPIError(Exception):
    """Base exception for Airflow SDK errors."""
    pass

class AirflowAuthError(AirflowAPIError):
    """Raised when authentication fails."""
    pass

class AirflowRequestError(AirflowAPIError):
    """Raised when an HTTP request fails or returns an error status code."""
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data

class AirflowRateLimitError(AirflowRequestError):
    """Raised when the API rate limit is exceeded (e.g., HTTP 429)."""
    pass

class AirflowNotFoundError(AirflowRequestError):
    """Raised when a requested resource is not found (HTTP 404)."""
    pass
