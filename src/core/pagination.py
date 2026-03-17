from typing import Dict, Any, List, Optional

class Pagination:
    """Helper class to handle Airflow API pagination."""
    
    @staticmethod
    def extract_metadata(response_data: Dict[str, Any]) -> Dict[str, int]:
        """Extracts total_entries from the response if available."""
        return {
            "total_entries": response_data.get("total_entries", 0)
        }

    @staticmethod
    def get_params(limit: int = 100, offset: int = 0) -> Dict[str, int]:
        """Returns standard pagination querystring parameters."""
        return {
            "limit": limit,
            "offset": offset
        }
