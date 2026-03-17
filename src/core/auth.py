import httpx
from typing import Optional, Union, Tuple

class AuthManager:
    """Manages authentication for the Airflow API."""
    
    def __init__(self, username: str = None, password: str = None):
        self.username = username
        self.password = password

    def get_auth(self) -> Optional[Union[tuple, httpx.Auth]]:
        """Returns the authentication credentials or httpx.Auth object."""
        if self.username and self.password:
            return (self.username, self.password)
        return None
