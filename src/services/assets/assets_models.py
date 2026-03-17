from typing import List, Optional, Any, Dict
from pydantic import BaseModel

# --- Asset Models ---

class AssetModel(BaseModel):
    id: int
    uri: str
    extra: Any = None
    created_at: str
    updated_at: str

class AssetCollection(BaseModel):
    assets: List[AssetModel]
    total_entries: int

# --- AssetEvent Models ---

class AssetEventModel(BaseModel):
    id: int
    asset_id: int
    asset_uri: str
    extra: Any = None
    source_task_id: Optional[str] = None
    source_dag_id: Optional[str] = None
    source_run_id: Optional[str] = None
    source_map_index: int = -1
    created_dagruns: List[Dict[str, str]] = []
    timestamp: str

class AssetEventCollection(BaseModel):
    asset_events: List[AssetEventModel]
    total_entries: int
