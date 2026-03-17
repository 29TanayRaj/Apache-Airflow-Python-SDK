from typing import List, Optional, Any, Dict
from pydantic import BaseModel

# --- Backfill Models ---

class BackfillModel(BaseModel):
    id: int
    dag_id: str
    from_date: str
    to_date: str
    dag_run_conf: Optional[Dict[str, Any]] = None
    is_paused: bool
    created_at: str
    completed_at: Optional[str] = None
    updated_at: str

class BackfillCollection(BaseModel):
    backfills: List[BackfillModel]
    total_entries: int
