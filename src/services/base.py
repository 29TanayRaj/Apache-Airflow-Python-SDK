from typing import Dict, Any, Optional

class BaseService:
    """Constructs the request arguments without executing them."""
    def _construct_request(self, 
                            method: str, 
                            endpoint: str, 
                            params: Optional[Dict[str, Any]] = None, 
                            json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Constructs the request arguments without executing them.
        
        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint (e.g., "dags", "dags/{dag_id}")
            params: Query parameters
            json: JSON body
            
        Returns:
            Dictionary containing request arguments
        """
        
        req = {"method": method, "endpoint": endpoint}
        if params is not None:
            req["params"] = params
        if json is not None:
            req["json"] = json
        return req
